# 🌾 AgroAI: Multilingual AI-Powered Portal for Farmers

**AgroAI** is an intuitive, high-contrast, sunlight-readable web application designed to empower farmers, including non-literate communities, with real-time agricultural intelligence, localized AI advisory, crop rotation plans, and financial tracking.

Built with **Python (Flask)**, **Groq AI (Llama/Qwen models)**, and **SQLite**, the portal integrates core **Data Structures and Algorithms (DSA)** to power every major recommendation, calculation, and data handling module.

---

## 🚀 Key Features

* **🎙️ Voice & Multilingual AI Assistant:** Supports Hindi, Chhattisgarhi, and English text/voice inputs. Includes Text-to-Speech (TTS) audio playback (`🔊 Listen / Awaaz`) tailored for non-literate farmers.
* **📍 Location-Aware Advisory:** Integrated GPS auto-detection and regional dropdown (e.g., Bhilai, CG) automatically inject geographical context into AI prompt buffers.
* **🔄 Graph-Based Crop Rotation Engine:** Recommends optimal successor crops (e.g., *Rice* → *Chickpea*) based on soil nitrogen restoration levels using graph structures.
* **🧪 Soil N-P-K & Fertilizer Calculator:** Computes exact Urea and DAP requirements (in kg) based on crop selection and land acreage.
* **🛠️ Equipment & Tool Budget Calculator:** Filters and displays affordable farming machinery and tools using budget-constrained sorting logic.
* **⏳ Urgency Task Scheduler:** Keeps track of urgent field operations (irrigation, spraying, weather alerts) ranked by due date.
* **📊 Ledger Tracker & Mandi Market Rates:** Tracks daily farming expenses/income using linked structures and displays real-time sorted market rates.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python (Flask)
* **AI Engine:** Groq API (`qwen/qwen3.8-27b`, `openai/gpt-oss-120b`)
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3 (High-Contrast, Sunlight-Readable Theme), Vanilla JavaScript
* **Voice Capabilities:** Web Speech API (Speech Recognition STT & Speech Synthesis TTS)

---

## 🧩 Data Structures & Algorithms (DSA) Architecture

AgroAI emphasizes efficient computer science fundamentals across all features:

| Feature / Module | Core DSA Concept | Time Complexity |
| :--- | :--- | :--- |
| **AI Request Buffering** | FIFO Queue / Processing Buffer | O(1) |
| **Crop List Stack** | Dynamic Array Push & Pop | O(1) Push / O(N) Pop |
| **Crop Rotation Advisory** | Directed Acyclic Graph (DAG) & BFS | O(V + E) |
| **Task Urgency Planner** | Min-Heap / Priority Queue | O(log N) Insert / O(1) Top |
| **Soil N-P-K Calculator** | Multi-Dimensional Lookup Array | O(1) |
| **Mandi Price Ranking** | Merge Sort Algorithm | O(N log N) |
| **Crop Recommendation Lookup** | Binary Search Algorithm (Sorted Array) | O(log N) |
| **Soil & Season Category Index** | Hash Map Indexing | O(1) Average |
| **Financial Ledger Tracker** | Singly Linked List Traversal | O(N) |

---

## 📁 Repository Structure

```text
AgroAI/
├── .env.example            # Example configuration for API keys
├── .gitignore              # Git ignore rules for virtual env & database
├── README.md               # Project documentation
├── requirements.txt        # Python package dependencies
└── src/                    # Primary application source files
    ├── app/
    │   ├── database/       # SQLite database configuration & scripts
    │   ├── dsa_core/       # Core Data Structures & Algorithms modules
    │   │   ├── arrays_stacks.py
    │   │   ├── graph_rotation.py
    │   │   ├── hash_map.py
    │   │   ├── linked_list.py
    │   │   ├── npk_calculator.py
    │   │   ├── priority_heap.py
    │   │   └── sorting_searching.py
    │   ├── static/         # High-contrast CSS & Vanilla JS
    │   │   ├── css/
    │   │   └── js/
    │   ├── templates/      # Jinja2 HTML templates
    │   ├── __init__.py
    │   └── routes.py       # Flask backend routes
    └── run.py              # Application entry point script
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites

* **Python 3.10+**
* **Git**
* A valid **Groq API Key** (get one from [console.groq.com](https://console.groq.com/))

### 2. Clone the Repository

```bash
git clone https://github.com/ansarisaad810-lgtm/AgroAI.git
cd AgroAI
```

### 3. Create and Activate Virtual Environment

* **Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

* **Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
FLASK_ENV=development
```

### 6. Run the Application

Execute the entry script inside `src/`:

```bash
python src/run.py
```

Open your web browser and navigate to `http://127.0.0.1:5000/`.

---

## 🎨 UI Design Guidelines

* **Primary Theme:** Forest Green (`#1E5631`) & Marigold Gold (`#EAA81B`)
* **Background:** Off-White / Sunlight-Readable Light Gray (`#F7FAFC`)
* **Indicators:** Standard Green (Success), Yellow (Warning), Red (Urgent)
* **Corner Radius:** Subtle rounded edges (`6px`) with crisp border outlines for outdoor sunlight visibility.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
