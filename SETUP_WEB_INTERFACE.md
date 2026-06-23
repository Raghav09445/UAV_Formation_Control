# Running the Web Interface

## Backend Setup (Flask + Python)

1. Install Flask dependencies:
```powershell
cd "C:\Users\r3642\UAV formation"
.\venv\Scripts\pip install -r requirements-flask.txt
```

2. Start the Flask server:
```powershell
cd "C:\Users\r3642\UAV formation"
.\venv\Scripts\python.exe app.py
```

The backend will run on `http://localhost:5000`

## Frontend Setup (React)

1. Install Node.js dependencies:
```powershell
cd "C:\Users\r3642\UAV formation\frontend"
npm install
```

2. Start the React development server:
```powershell
cd "C:\Users\r3642\UAV formation\frontend"
npm start
```

The frontend will open at `http://localhost:3000`

## Full Workflow

1. Open two terminals
2. **Terminal 1**: Run Flask backend
   ```powershell
   cd "C:\Users\r3642\UAV formation"
   .\venv\Scripts\python.exe app.py
   ```
3. **Terminal 2**: Run React frontend
   ```powershell
   cd "C:\Users\r3642\UAV formation\frontend"
   npm start
   ```
4. Browser opens to `http://localhost:3000`
5. Adjust parameters and click "Run Simulation"
6. View results with interactive plots

## What the Web Interface Shows

- **Simulation Controls**: Adjust `T_sim`, `σ(0)`, `ρ`
- **Summary Stats**: Bandwidth reduction %, total broadcasts
- **Trajectory Plot**: XY positions of all 5 UAVs + center path
- **Broadcast Chart**: Total broadcasts per UAV
- **Bandwidth Chart**: Periodic vs DECM comparison

## API Endpoints

- `POST /api/simulate` — Run simulation with custom parameters
- `GET /api/parameters` — Get current system configuration
- `GET /api/health` — Health check
