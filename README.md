# Frappe Ocean Freight Bill Audit & Container Detention Demurrage Ledger

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![Logistics Billing](https://img.shields.io/badge/Logistics-Freight%20Audit-teal.svg)]()
[![Exim](https://img.shields.io/badge/EXIM-Ocean%20Shipping-navy.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

International shippers, freight forwarders, and importers experience significant profit leakages in **ocean freight invoices**:
1. **Rampant Carrier Surcharge Overbilling:** Shipping lines bill fluctuating Bunker Adjustment Factors (BAF), Currency Adjustment Factors (CAF), and Terminal Handling Charges (THC) that deviate from agreed contract rate sheets.
2. **Container Demurrage & Detention Traps:** Ports and container terminals levy steep detention fees (often \$100–\$250/day per TEU) when empty containers are returned even 1 day past contractual free-time allowances.
3. **Lack of Automated Dispute Evidence:** Logistics teams lack timestamped gate-in/gate-out logs to challenge incorrect demurrage invoices, losing thousands of dollars per voyage.

This Frappe application delivers an automated freight invoice audit engine and real-time container demurrage tracking ledger.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["Shipping Line Ocean Freight Invoice"] -->|Carrier Invoicing Feed| B["Automated Freight Audit Engine"]
    C["Contract Rate Master (Agreed Tariffs)"] --> B
    B -->|Compare Base Ocean Freight & Surcharges (BAF, CAF, THC)| D{"Billing Matches Contract?"}
    D -->|Variance Detected (>0 USD)| E["Auto-Generate Overcharge Dispute Notice"]
    D -->|Audit Cleared| F["Approve Freight Payment Voucher"]
    G["Container Discharge at Port (JNPT / Mundra)"] -->|Track Free-Time Clock (e.g. 14 Days)| H["Container Dwell Tracker"]
    H -->|Empty Gate-In Return at CFS| I{"Dwell Days vs Free Days"}
    I -->|Within Free Time| J["Zero Detention: Clearance Approved"]
    I -->|Exceeded Free Time| K["Calculate Daily Detention Liability (USD)"]
```

---

## 🚀 Key Engineering Capabilities

- **3-Way Freight Audit:** Cross-verifies carrier invoices against Purchase Orders, ocean contracts, and Bills of Lading.
- **Surcharge Discrepancy Detector:** Catches unauthorized bunker, congestion, and war risk rate spikes.
- **Container Free-Time Countdown:** Tracks container numbers, discharge timestamps, and alerts logistics dispatchers before detention incurs.
- **Dispute Settlement Journal:** Generates credit note debit claims against shipping carriers.

---

## 📂 Frappe DocType Schema & Data Structure

```text
freight_audit_demurrage/
├── freight_audit_demurrage_core/
│   ├── doctype/
│   │   ├── ocean_freight_audit/
│   │   │   ├── ocean_freight_audit.json
│   │   │   ├── ocean_freight_audit.py
│   │   │   └── ocean_freight_audit.js
│   │   └── container_dwell_tracker/
│   │       └── container_dwell_tracker.json
│   └── workspace/
│       └── freight_audit_demurrage_workspace/
│           └── freight_audit_demurrage_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/freight_audit_demurrage.api.audit_ocean_freight_invoice`
- **Whitelisted Method:** `@frappe.whitelist() def compute_container_detention(container_number, discharge_date, gate_out_date, free_days, daily_rate)`
- **Hooks Event:** `on_submit` of `Purchase Invoice` (Freight) initiates automated tariff checks.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/frappe-freight-audit-container-demurrage
bench --site erp.yourdomain.com install-app freight_audit_demurrage
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Built for International Importers, Exporters, and 3PL Freight Forwarders.
