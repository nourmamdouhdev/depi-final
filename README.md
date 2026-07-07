<div align="center">
  
# 📈 Forecast AI

**Enterprise-Grade Stateless Sales Forecasting Platform**

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

<br />

Forecast AI is a completely **stateless**, high-performance sales forecasting dashboard. It transforms historical sales data into actionable future insights using pre-trained machine learning models. Built with a premium, minimalist "Linear/Stripe" aesthetic, it is designed for enterprise presentations, MVP demonstrations, and Graduation Projects.

---

## ✨ Features

- **Stateless Architecture**: No databases (PostgreSQL/SQLite), no Redis, no Celery. The backend is blazing fast, loading the model into memory upon startup.
- **AI Analytics Insights**: Automatically generates business-readable summaries (Revenue Outlook, Growth Analysis, Daily Averages) based on predictions.
- **Premium UI/UX**: 
  - Glassmorphism & Framer Motion animations.
  - Interactive Drag & Drop file uploads (`react-dropzone`).
  - Seamless responsive Dashboard layout.
- **Advanced Visualizations**: Beautiful, combined historical and forecast charts powered by Recharts.
- **Export Capabilities**: Instantly download forecast data to CSV.

---

## 🛠️ Technology Stack

### Frontend
- **React.js** (Vite)
- **Tailwind CSS** (v3.4) - *Minimalist Dark Theme*
- **Framer Motion** - *Micro-animations and layout transitions*
- **Recharts** - *Data visualization*
- **Axios** - *API communication*
- **Lucide React** - *Premium iconography*

### Backend
- **FastAPI** - *High-performance asynchronous API*
- **Python 3.12+**
- **Pandas & NumPy** - *Data preprocessing & imputation*
- **Scikit-Learn & Joblib** - *Model serving*
- **Uvicorn** - *ASGI Server*

---

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

Ensure you have the following installed:
- [Node.js](https://nodejs.org/en/) (v18+)
- [Python](https://www.python.org/downloads/) (3.10+)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/forecast-ai.git
cd forecast-ai
```

### 2. Generate the Pre-trained Model

Since this is a stateless inference platform, the API expects a trained model to exist in the `models/` directory.

```bash
# Ensure you are in the root directory
python generate_dummy_model.py
```
*This will create a `forecast_model.pkl` file inside the `models/` directory.*

### 3. Setup the Backend

Open a terminal and navigate to the backend directory:

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*The API will now be running at `http://127.0.0.1:8000`*

### 4. Setup the Frontend

Open a **new** terminal window and navigate to the frontend directory:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*The React application will open locally at `http://localhost:5173`*

---

## 📁 Project Structure

```text
forecast-ai/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point & model loader
│   │   ├── routes/            # API endpoints (POST /forecast)
│   │   └── services/          # Data cleaning & KPI generation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/        # Dashboard, Charts, Upload components
│   │   ├── hooks/             # Custom React hooks (useForecast)
│   │   ├── layouts/           # Sidebar & TopNav Layouts
│   │   ├── App.jsx            # Main view assembler
│   │   └── index.css          # Tailwind & custom CSS
│   ├── package.json
│   └── tailwind.config.js
├── models/                    # Stores the .pkl models
└── generate_dummy_model.py    # Utility to create a test model
```

---

## 📊 How to Use

1. Open the web interface.
2. Go to the **Upload Dataset** section.
3. Upload a CSV file. The CSV **must** contain two columns: `Date` and `Sales`.
   *(You can find a `sample_sales.csv` in the project root for testing).*
4. Select your **Forecast Horizon** (e.g., 7 Days, 30 Days).
5. Click **Generate Forecast**. The dashboard will automatically scroll down to reveal the animated KPI metrics, charts, and AI-generated insights!
