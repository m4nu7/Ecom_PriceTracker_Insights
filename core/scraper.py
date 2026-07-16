import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects
)

import time
from typing import Optional

from config import settings
from config.logger import get_logger


logger = get_logger(__name__)




class Scraper:
    """
    Fetches pages over HTTP with retry and backoff behavior.
 
    This class does not know about HTML structure or product
    data — it only returns raw page content (or None on failure).
    """

    def __init__(
        self, 
        user_agent: str = settings.USER_AGENT,
        timeout: int = settings.REQUEST_TIMEOUT_SECONDS, 
        max_retries: int = settings.MAX_RETRIES, 
        delay_seconds: int = settings.REQUEST_DELAY_SECONDS,
        retry_backoff_seconds: int = settings.RETRY_BACKOFF_SECONDS
    ):
        
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.retry_backoff_seconds = retry_backoff_seconds
        # Reusing one session gives us connection pooling/keep-alive,
        # which is both faster and slightly more polite than opening
        # a brand new TCP connection on every single request.
        self._session = requests.Session()


    def fetch_page(self, url: str) -> Optional[str]:

        """
        Fetch a single URL and return its raw HTML as a string.
 
        Retries on transient failures (timeouts, connection errors,
        5xx server errors) with exponential backoff. Does NOT retry
        on 4xx client errors (bad URL, blocked, not found) since
        retrying those just wastes time and hammers the server for
        no benefit.
 
        Always waits `self.delay_seconds` before each attempt as a
        politeness delay, regardless of success/failure.
 
        Returns None if the page could not be fetched after all
        retries are exhausted — callers (Parser, ThreadManager) are
        expected to handle that gracefully rather than assume a
        string is always returned.
        """

        for attempt in range(1, self.max_retries + 1):
            # Politeness delay before every attempt, including the first.
            time.sleep(self.delay_seconds)

            try: 
                response = self._session.get(
                    url,
                    headers=self._build_headers(),
                    timeout=self.timeout,
                )


                # Raises HTTPError for 4xx/5xx responses.
                response.raise_for_status()

                logger.info(f"Successfully fetched {url} (status {response.status_code})")
                return response.text
            
            except HTTPError as e:
                status = e.response.status_code if e.response is not None else None


                # Client errors (404, 403, etc.) won't be fixed by
                # retrying — fail immediately instead of wasting
                # attempts and hitting the server again for nothing.
                if status is not None and 400 <= status < 500:
                    logger.error(f"Client error {status} fetching {url} - not retrying")
                    return None
                


                # Server errors (5xx) are often transient — worth a retry.
                logger.warning(f"Server error {status} fetching {url} (attempt {attempt/self.max_retries})")

            
            except Timeout as e:
                logger.warning(
                    f"Timeout fetching {url} (attempt {attempt/self.max_retries})"
                )

            except ConnectionError as e:
                logger.warning(
                    f"Connection error fetching {url} (attempt {attempt/self.max_retries})"
                )

            except TooManyRedirects as e:
                # Redirect loops won't resolve on retry — fail immediately.
                logger.error(
                    f"Too many redirects fetching {url} - not retrying"
                )
                return None
            
            except RequestException as e :
                # Catch-all for any other requests-library failure we
                # didn't anticipate. Log it with detail rather than
                # crashing the whole batch/thread.
                logger.warning(
                    f"Unexpected request error fetching {url} (attempt {attempt/self.max_retries})"
                )

            # Only reached after a retryable failure above.
            if attempt < self.max_retries:
                backoff = self.retry_backoff_seconds * attempt  # linear backoff growth
                logger.info(f"Retrying {url} in {backoff:.1f}s...")
                time.sleep(backoff)
        
        
        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None 

            
    

    def _build_headers(self) -> dict:
        """Build the request headers, including the configured User-Agent."""
        return {
            "User-Agent" : self.user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
    

    def close(self) -> None:
        """Close the underlying session's connections cleanly."""
        self._session.close()




