# 🌾 AgriScan APAC

> Zero-cost multimodal crop disease diagnosis and advisory for smallholder farmers across Asia Pacific using Google AI Studio and Gemini Flash.

Built for the **Google Cloud Gen AI Academy APAC (Cohort 3) — #Meetthebuilders Campaign**.

---

## 📌 Problem Statement
Smallholder farmers across rural Asia Pacific frequently experience 20% to 40% harvest losses due to delayed identification of plant pathology and pest infestations. Traditional advisory systems present clear barriers:
* Limited access to on-site agronomy experts in remote villages.
* Advice often locked behind language barriers and complex technical terminology.
* High reliance on expensive commercial chemicals instead of affordable, locally accessible interventions.

---

## 💡 The Solution
**AgriScan APAC** is a lightweight web tool that enables smallholder farmers to upload a leaf photograph and receive actionable diagnostics in seconds:
* **Multimodal Visual Analysis:** Inspects crop images using Gemini Flash vision capabilities.
* **Vernacular Language Support:** Delivers advice directly translated into regional languages including Telugu, Hindi, Tamil, Gujarati, and Bengali.
* **Accessible Remedies:** Prioritizes low-cost, organic, and homemade treatments (such as neem oil solutions, wood ash, composting, and moisture management).

---

## 🛠️ Tech Stack
* **AI Model:** Google AI Studio (Gemini Flash REST API)
* **Backend:** Python 3, Flask
* **Networking:** Requests (direct HTTP calls without heavy SDK overhead)
* **Frontend:** Responsive HTML5/CSS3 interface

---

## 📂 Project Structure
```text
agriscan-apac/
├── app.py              # Flask server and UI
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes environment caches
└── README.md           # Project documentation
