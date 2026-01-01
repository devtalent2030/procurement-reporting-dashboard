# 🏗️ System Architecture & Data Pipeline

## 1. High-Level Design

This solution implements a modern **ELT (Extract, Load, Transform)** pattern enhanced with an AI-driven auditing layer. It is designed to simulate a secure government reporting environment where data privacy, auditability, and automation are paramount.

### Data Flow Diagram

```mermaid
graph TD
    subgraph Data_Generation_Zone [Secure Local Environment]
        A[Data Generator<br/>(Python/Faker)] -->|JSON/CSV| B(Raw Data Lake<br/>'data/raw')
    end

    subgraph Intelligence_Layer [Auditing Engine]
        B -->|Pandas Ingestion| C{Anomaly Detector<br/>(Scikit-Learn)}
        C -->|Isolation Forest Logic| D(Audited Dataset<br/>'data/processed')
    end

    subgraph Presentation_Layer [Business Intelligence]
        D -->|Import| E[Power BI Data Model<br/>(Star Schema)]
        E -->|DAX Measures| F[Executive Dashboard]
    end

    subgraph Orchestration
        G[run_pipeline.sh] --> A
        G --> C
    end

```

---

## 2. Component Breakdown

### A. Data Engineering Layer (The "Bronze" Layer)

* **Component:** `scripts/data_generator.py`
* **Function:** Simulates the extraction of vendor spend logs from an ERP system (like SAP Ariba).
* **Design Choice:** utilized **Synthetic Data Generation** via the `Faker` library (`en_CA` locale) rather than sanitizing real data.
* **Deep Dive (Privacy-by-Design):**
* *Concept:* **Synthetic Data** involves creating artificial datasets that mimic the statistical properties of real data without containing any Personally Identifiable Information (PII).
* *Why?* This eliminates the risk of data leakage, allowing for safe development and testing in lower environments.



### B. Data Science Layer (The "Silver" Layer)

* **Component:** `scripts/anomaly_detector.py`
* **Function:** Acts as an automated auditor, tagging transactions that deviate from established patterns.
* **Algorithm:** **Isolation Forest** (Unsupervised Learning).
* **Deep Dive (The Logic):**
* *Concept:* **Unsupervised Learning** means the model finds patterns on its own without being told what a "fraud" looks like.
* *Why Isolation Forest?* Unlike standard statistical methods (like Z-Score) which assume data follows a "Bell Curve" (Normal Distribution), Isolation Forest works on irregular datasets. It isolates anomalies by randomly "slicing" the data; rare points require fewer slices to isolate.
* *Configuration:* `contamination=0.05` ensures we only flag the top 5% most suspicious records, reducing "Alert Fatigue" for human auditors.



### C. Reporting Layer (The "Gold" Layer)

* **Component:** `powerbi/Procurement_Dashboard.pbix`
* **Function:** Visualizes the audited data for decision support.
* **Data Model:** **Star Schema**.
* *Fact Table:* `Procurement_Data` (Transactions).
* *Dimension Tables:* `Dim_Category` (Lookups).


* **Deep Dive (Performance):**
* *Concept:* **VertiPaq Engine** is Power BI's internal database. It uses **Columnar Storage**, meaning it reads data vertically (column by column) rather than horizontally (row by row).
* *Why Star Schema?* Separating "Facts" (Numbers) from "Dimensions" (Text) maximizes compression. It allows the dashboard to filter millions of rows in milliseconds.



---

## 3. Automation & Orchestration

* **Component:** `run_pipeline.sh`
* **Function:** Provides a single entry point for the entire workflow.
* **Design:** Idempotent Execution.
* *Concept:* **Idempotency** means you can run the script 1 time or 100 times, and the result will always be the consistent state (it won't duplicate data or crash if files already exist).
* *Error Handling:* The script uses "Exit Codes" (`$?`). If the Data Generator fails, the Anomaly Detector will not run, preventing the corruption of the downstream report.



---

## 4. Security Constraints & Trade-offs

| Decision | Option Selected | Alternative Considered | Rationale |
| --- | --- | --- | --- |
| **Hosting** | Static Artifacts (GitHub) | Publish to Web | **Compliance.** Public hosting violates "Protected B" data sovereignty. Static artifacts simulate an air-gapped delivery. |
| **ML Model** | Isolation Forest | Rules Engine (If/Else) | **Scalability.** Rules require constant maintenance. ML adapts to new vendor behaviors automatically. |
| **Data Type** | Mock/Synthetic | Anonymized Real Data | **Privacy.** Re-identification attacks are possible with anonymized data. Synthetic data is mathematically safe. |

---

## 5. Future Scalability Roadmap

* **Phase 2:** Integrate **Azure Data Factory** to replace the Python scripts for cloud-native orchestration.
* **Phase 3:** Implement **Row-Level Security (RLS)** in Power BI to restrict Ministry views based on user login.
* **Phase 4:** Deploy model as a **REST API** (using FastAPI) to score contracts in real-time as they are submitted.