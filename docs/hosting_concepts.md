# Architecture Decision Record (ADR): Hosting & Security Strategy

## 1. Executive Summary
**Decision:** The Procurement Intelligence Dashboard will be deployed as a **Static Artifact** within a version-controlled repository, rather than a live public web application.
**Status:** Accepted
**Driver:** Compliance with Government of Alberta (GoA) Information Security Management Directives for "Protected B" financial data.

## 2. The Trade-Off Analysis

### Option A: Public Cloud Hosting ("Publish to Web")
* **Mechanism:** Generates an anonymous embed token (`<iframe>`) accessible via public URL.
* **Pros:** Immediate interactivity for external stakeholders.
* **Cons (Critical Risk):** * **Data Exfiltration:** Underlying JSON datasets are cached on public CDNs and susceptible to scraping.
    * **Identity Bypass:** Completely circumvents Azure Active Directory (AAD) and Row-Level Security (RLS).
    * **Sovereignty Violation:** Potential for data replication across non-Canadian geo-regions.

### Option B: Static Artifact Deployment (Selected)
* **Mechanism:** The `.pbix` binary is confined to the local development environment (Local State). Deliverables are rendered as high-fidelity audits (Screenshots/Video) and stored in `docs/assets`.
* **Pros:**
    * **Zero Trust Alignment:** Simulates an air-gapped environment where data never leaves the secure zone.
    * **Audit Trail:** Static artifacts provide immutable proof of reporting state at a specific point in time.
* **Cons:** Reduced interactivity for public viewers (mitigated via GIF walkthroughs).

## 3. Security Posture & Access Control
* **Identity Management:** In a production GoA environment, access would be federated via **Azure Active Directory (AAD)** using OIDC protocols. Personal namespaces (e.g., `@gmail.com`) are explicitly blocked to enforce RBAC (Role-Based Access Control).
* **Data Integrity:** The mock dataset (`data/processed/procurement_data_audited.csv`) serves as a functional twin. This separation of concerns allows developers to build against the schema without accessing the Production Data Lake.

## 4. Practical Implication
This repository demonstrates the **"Code-First, Data-Secure"** development lifecycle required for sensitive public sector IT projects.