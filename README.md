<div align="center">

# 🛒📉 E‑Commerce Price Tracker  
### *Scrape • Store • Analyze • Visualize • Automate*

A full‑stack engineering project featuring OOP architecture, threading, cloud DB, analytics, dashboards, and PDF reporting.

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-green?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-success?style=for-the-badge&logo=mongodb)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge&logo=plotly)
![Threading](https://img.shields.io/badge/Threading-Concurrency-red?style=for-the-badge)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Generation-lightgrey?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Optional-blue?style=for-the-badge&logo=docker)

</div>

## 📌 Overview

A full‑stack engineering project that:

- Scrapes product data from e‑commerce sites  
- Tracks price history in MongoDB Atlas  
- Analyzes trends using Pandas  
- Visualizes insights using Matplotlib/Seaborn/Plotly  
- Generates PDF reports using ReportLab  
- Runs automatically using a threaded scheduler  

Built using clean OOP architecture and real‑world engineering practices.

---

## 🧩 Architecture Diagram

```mermaid
flowchart TD

A[Scraper] --> B[Parser]
B --> C[ThreadManager]
C --> D[DatabaseClient]
D --> E[Analyzer]
E --> F[Visualizer]
F --> G[ReportBuilder]

A -->|Fetch HTML| B
B -->|Extract Data| D
D -->|Store Price History| E
E -->|Compute Trends| F
F -->|Generate Charts| G
```

## 🏗 Class Diagram

```mermaid
classDiagram

    class Product {
        +id
        +name
        +url
        +metadata
    }

    class Scraper {
        +fetch_page(url)
    }

    class Parser {
        +parse_name(html)
        +parse_price(html)
    }

    class BestBuyParser {
        +parse_name(html)
        +parse_price(html)
    }

    class ThreadManager {
        +run_in_threads(func, inputs)
        +run_periodic(interval)
    }

    class DatabaseClient {
        +insert_price_record()
        +get_price_history()
        +update_product_info()
    }

    class Analyzer {
        +get_price_trend(id)
        +detect_price_drop(id)
        +compute_statistics(id)
    }

    class Visualizer {
        +plot_price_history(id)
        +plot_comparison(ids)
        +plot_discount_heatmap(id)
    }

    class ReportBuilder {
        +generate_product_report(id)
    }

    Scraper --> Parser
    Parser <|-- BestBuyParser
    ThreadManager --> Scraper
    ThreadManager --> DatabaseClient
    DatabaseClient --> Analyzer
    Analyzer --> Visualizer
    Visualizer --> ReportBuilder

```

## 🔄 System Flow

```mermaid
flowchart LR

    classDef core fill:#1e90ff,stroke:#fff,color:#fff
    classDef parse fill:#6a5acd,stroke:#fff,color:#fff
    classDef db fill:#2e8b57,stroke:#fff,color:#fff
    classDef analysis fill:#ff8c00,stroke:#fff,color:#fff
    classDef viz fill:#dc143c,stroke:#fff,color:#fff
    classDef pdf fill:#696969,stroke:#fff,color:#fff
    classDef cloud fill:#20b2aa,stroke:#fff,color:#fff
    classDef user fill:#444,stroke:#fff,color:#fff

    U[User / Scheduler]:::user --> TM[ThreadManager]:::core
    TM --> SC[Scraper]:::core
    SC --> HTML[HTML Content]:::parse
    HTML --> PR[Parser]:::parse
    PR --> DB[DatabaseClient]:::db
    DB --> AN[Analyzer]:::analysis
    AN --> VS[Visualizer]:::viz
    VS --> RP[ReportBuilder]:::pdf

    DB -->|Store Price History| MDB[(MongoDB Atlas)]:::cloud
```







