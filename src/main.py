from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Enable CORS (Allows your React site to talk to this Python backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA LOADING SECTION (Render Fix) ---
print("Loading data...")

# 1. Get the directory where THIS file (main.py) lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Build the path to the CSV file relative to this script
# Go up one level ("..") from 'src' to get to root, then into 'data'
file_path = os.path.join(script_dir, "..", "data", "nba_clean.csv")

print(f"Looking for data at: {file_path}")

try:
    df = pd.read_csv(file_path)
    print("✅ Data loaded successfully!")
except FileNotFoundError:
    print(f"❌ ERROR: File not found at {file_path}")
    print("Current working directory is:", os.getcwd())
    # Create an empty dataframe so the server doesn't crash immediately
    df = pd.DataFrame()

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "NullWager API is running", "data_rows": len(df)}

@app.get("/simulate")
def run_simulation(start_cash: int = 1000, bet_size: int = 50, strategy: str = "flat"):
    """
    Run the simulation based on user inputs.
    Strategies:
    - 'flat': Always bet the same amount.
    - 'martingale': Double the bet after every loss. Reset after a win.
    """
    # Safety check if data didn't load
    if df.empty:
        return {"error": "Data not loaded on server.", "history": [], "final_balance": 0}

    bankroll = start_cash
    history = []
    
    # Track the "Current Bet" separately (it changes in Martingale)
    current_bet = bet_size
    
    # Add initial starting point
    history.append({"game": 0, "bankroll": start_cash})
    
    for index, row in df.iterrows():
        # LOGIC: Still betting on Home Favorites (Odds < 0)
        odds = row['home_odds']
        
        if odds < 0: 
            # Cap the bet: You can't bet more than you have!
            # (In real life, this is where Martingale fails—you run out of cash)
            actual_bet = min(current_bet, bankroll)
            
            if actual_bet <= 0:
                # You are broke, stop betting
                break

            if row['home_score'] > row['away_score']:
                # --- WIN ---
                # Profit Formula for Negative Odds: (100 / Odds) * Bet
                profit = (100 / abs(odds)) * actual_bet
                bankroll += profit
                
                # MARTINGALE LOGIC: Reset bet to base size after a win
                if strategy == "martingale":
                    current_bet = bet_size
                    
            else:
                # --- LOSS ---
                bankroll -= actual_bet
                
                # MARTINGALE LOGIC: Double the bet after a loss
                if strategy == "martingale":
                    current_bet = current_bet * 2
            
            # Optimization: Only record data every 10 bets to keep the graph fast
            if index % 10 == 0:
                history.append({"game": index, "bankroll": round(bankroll, 2)})
            
            # Bankruptcy Check
            if bankroll <= 1: # effectively zero
                history.append({"game": index, "bankroll": 0})
                bankroll = 0
                break
                
    return {"history": history, "final_balance": round(bankroll, 2)}