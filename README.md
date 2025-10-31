# 🛰️ NIRA — Neighborhood Incident Response & Allocation

> **A Multi-Agent AI System for Community Incident Triage, Verification, and Dispatch**

NIRA is a multi-agent orchestration system designed to help communities respond to local incidents (e.g., waste, flooding, safety, medical emergencies) more efficiently.  
It automates **report collection, verification, prioritization, and dispatch coordination** among volunteers or municipal services — ensuring faster, data-driven community response.

---

## 🚀 Overview

Many communities lack a structured way to handle public incident reports. NIRA bridges this gap using **AI agents** that work together to process incoming incident reports, verify them, and dispatch available responders based on location, severity, and resource availability.

Each agent performs a unique, well-defined role within a LangGraph-based orchestration.

---

## 🤖 Multi-Agent Architecture

| Agent | Role | Key Tools / Capabilities |
|:------|:-----|:--------------------------|
| 📨 **Reporter Agent** | Collects incident reports from users via web form, SMS, or messaging apps and normalizes data | Geocoding Tool (OpenStreetMap Nominatim) |
| 🧠 **Triage & Verification Agent** | Classifies the report (category, severity), verifies validity via web search or image analysis, and computes urgency score | Web Search Tool, Image Analysis API, Math/Scoring Tool |
| 🚚 **Dispatcher Agent** | Matches verified incidents to available volunteers or municipal crews and sends route + task info | Routing API (OSRM / GraphHopper), Messaging API (Twilio) |
| 🔄 **Monitor & Feedback Agent** | Tracks task progress, requests feedback, closes the loop with confirmation and report generation | Database / File Generator Tool |

All agents communicate through a LangGraph (or CrewAI / AutoGen) orchestration layer following a simple message protocol (sender, recipient, intent, payload, confidence).

---

## 🧩 Tool Integrations

NIRA integrates multiple tools to extend beyond simple LLM text reasoning:

1. **Web Search Tool** — cross-check or validate community incident claims.  
2. **Geocoding & Routing Tool** — convert addresses to coordinates and calculate optimal volunteer dispatch routes.  
3. **Messaging Tool** — send task details and updates to responders via SMS or WhatsApp.  
4. *(Optional)* **Image Processing Tool** — analyze attached photos to verify incident type and severity.  
5. *(Optional)* **Database & Report Tool** — store logs and generate PDF/CSV summaries.

---

## ⚙️ Tech Stack

- **Orchestration:** LangGraph (recommended), or AutoGen / CrewAI  
- **LLM Framework:** LangChain or OpenAI API wrappers  
- **Backend:** Python 3.11+, FastAPI / Flask for webhooks  
- **Database:** PostgreSQL / Supabase  
- **Mapping APIs:** OpenStreetMap Nominatim + OSRM  
- **Messaging:** Twilio (SMS / WhatsApp)  
- **Containerization:** Docker + docker-compose  
- **Testing & Simulation:** pytest, scenario runner scripts  

---

## 🧠 How It Works

1. **Report submission:** A user submits an incident via web, SMS, or chat.  
2. **Normalization:** Reporter Agent converts input to structured JSON (adds geolocation).  
3. **Triage & Verification:** Second agent validates and scores urgency.  
4. **Dispatch:** Dispatcher Agent assigns tasks to the nearest available responder.  
5. **Monitoring:** Feedback Agent collects completion confirmations and closes reports.  
6. **Evaluation:** Metrics are logged for system benchmarking.

---

## 📊 Evaluation Metrics

| Metric | Description |
|:-------|:-------------|
| **Resolution Rate** | % of reports resolved within a defined timeframe |
| **Time-to-Dispatch** | Avg. time between report receipt and responder assignment |
| **Verification Accuracy** | Precision / recall of AI verification vs. human review |
| **False Dispatch Rate** | % of dispatched tasks later deemed unnecessary |

These metrics are automatically computed during replayed simulations using synthetic incident data.

---
                Citizen / App / SMS
                         |
                 [Reporter Agent]
                         |
                 + normalize + geocode
                         |
                [Dedup / Similarity Node]
                         |
                 [Triage Agent]
                         |
                [Verification Supervisor]
     ┌──────────┬─────────┬─────────┬─────────┐
     |          |         |         |         |
[Web Search] [Social] [Image] [Metadata] [Crowd/Local]
     |          |         |         |         |
        --> Evidence DB (S3 + Postgres + Vector)
                         |
                [Credibility Aggregator]
          Bayesian truth score 0 → 1
               /              \
     below threshold      above threshold
         |                     |
 [Human Review]         [Dispatch Agent]
                              |
                        Send responders
                              |
                      [Monitoring + Feedback]
                              |
                         [Learning Agent]
                 update source reliabilities

---
## 🧪 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/<your-username>/NIRA.git
cd NIRA
cp .env_example .env
# Add API keys (Twilio, OSM endpoints, DB_URL, etc.)
