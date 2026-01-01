# Architecture Decision Record (ADR): Hosting & Security Strategy

## 1. Executive Summary

**Decision:** The Procurement Intelligence Dashboard will be deployed as a **Static Artifact** within a version-controlled repository, rather than as a live public web application.

**Status:** Accepted

**Compliance Driver:** Adherence to Government of Alberta (GoA) Information Security Management Directives regarding the handling of "Protected B" financial data.

---

## 2. Trade-Off Analysis

### Option A: Public Cloud Hosting ("Publish to Web")

* **Mechanism:** Leveraging Power BI's "Publish to Web" feature to generate an anonymous embed token (`<iframe>`) accessible via a public URL.
* **Pros:** Provides immediate interactivity for external stakeholders without licensing costs.
* **Cons (Critical Risks):**
* **Data Exfiltration:** The underlying JSON datasets are cached on public Content Delivery Networks (CDNs) and are susceptible to scraping by external actors.
* **Identity Bypass:** This method circumvents Azure Active Directory (AAD) authentication and Row-Level Security (RLS), effectively making all data public.
* **Sovereignty Violation:** There is a potential risk of data replication across non-Canadian geo-regions, violating data residency requirements.



### Option B: Static Artifact Deployment (Selected)

* **Mechanism:** The `.pbix` binary remains confined to the local development environment (Local State). Deliverables are rendered as high-fidelity audits (Screenshots/Video) and stored in `docs/assets` for documentation.
* **Pros:**
* **Zero Trust Alignment:** Simulates an "air-gapped" environment where sensitive data never leaves the secure development zone.
* **Audit Trail:** Static artifacts provide an immutable proof of the reporting state at a specific point in time, which is critical for financial auditing.


* **Cons:** Reduced interactivity for public viewers.
* *Mitigation:* Use of high-frame-rate GIF walkthroughs to demonstrate UI responsiveness and filtering logic.



---

## 3. Security Posture & Access Control

### Identity Management

In a production GoA environment, access would be federated via **Azure Active Directory (AAD)** using OIDC protocols.

* **Constraint:** Personal namespaces (e.g., `@gmail.com`) are explicitly blocked to enforce **Role-Based Access Control (RBAC)**.
* **Implementation:** This project mirrors that restriction by refusing to publish to a non-enterprise tenant, thereby adhering to the principle of least privilege.

### Data Integrity & Separation of Concerns

The mock dataset (`data/processed/procurement_data_audited.csv`) serves as a **Functional Twin** of the production data.

* **Benefit:** This allows developers to build and test the schema/ETL pipelines without requiring direct access to the Production Data Lake, reducing the attack surface.

---

## 4. Practical Implication

This repository demonstrates the **"Code-First, Data-Secure"** development lifecycle required for sensitive public sector IT projects. It prioritizes data sovereignty and compliance over convenience, reflecting the operational reality of government IT infrastructure.