# How to Run the Project

Follow these simple steps to run the Sales Forecasting project on your machine. You will need to open **two separate terminal windows**.

---

### Step 1: Generate the AI Model
*You only need to do this once so the backend has a model to load.*
1. Open a terminal in the root folder (`depi final`).
2. Run this command:
   ```bash
   python generate_dummy_model.py
   ```
   *This creates `forecast_model.pkl` inside the `models/` folder.*

---

### Step 2: Start the Backend (FastAPI)
1. In your terminal, go into the `backend` folder:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
   *(If you are on Mac/Linux, use `source venv/bin/activate` instead)*
3. Run the server:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
   *Leave this terminal open and running!*

---

### Step 3: Start the Frontend (React Dashboard)
1. Open a **new, second terminal window**.
2. Go into the `frontend` folder:
   ```bash
   cd frontend
   ```
3. Start the website:
   ```bash
   npm run dev
   ```
4. Open your browser and go to the link shown in the terminal (usually `http://localhost:5173`).

---

### You're Done! 🎉
You can now upload the `sample_sales.csv` file on the website and see the dashboard working.
