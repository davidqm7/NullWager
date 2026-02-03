from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS (Allows your React site to talk to this Python backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data once when server starts
print("Loading data...")
df = pd.read_csv("../data/nba_clean.csv")
print("Data loaded!")

@app.get("/")
def read_root():
    return {"status": "NullWager API is running"}

@app.get("/simulate")
def run_simulation(start_cash: int = 1000, bet_size: int = 50, strategy: str = "flat"):
    """
    Strategies:
    - 'flat': Always bet the same amount (e.g., $50).
    - 'martingale': Double the bet after every loss. Reset after a win.
    """
    bankroll = start_cash
    history = []
    
    # NEW: Track the "Current Bet" separately from the "Base Bet"
    current_bet = bet_size
    
    history.append({"game": 0, "bankroll": start_cash})
    
    for index, row in df.iterrows():
        # LOGIC: Still betting on Home Favorites
        odds = row['home_odds']
        
        if odds < 0: 
            # Cap the bet: You can't bet more than you have!
            actual_bet = min(current_bet, bankroll)
            
            if row['home_score'] > row['away_score']:
                # --- WIN ---
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
            
            # Record data
            if index % 10 == 0:
                history.append({"game": index, "bankroll": round(bankroll, 2)})
            
            if bankroll <= 0:
                history.append({"game": index, "bankroll": 0})
                break
                
    return {"history": history, "final_balance": round(bankroll, 2)}