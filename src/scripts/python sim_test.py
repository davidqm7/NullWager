import pandas as pd

def run_simulation():
    # 1. Load the clean data
    print("Loading data...")
    df = pd.read_csv("data/nba_clean.csv")
    
    # 2. Define the Player's Portfolio
    STARTING_CASH = 1000
    BET_SIZE = 50
    
    current_cash = STARTING_CASH
    
    print(f"\n--- SIMULATION START ---")
    print(f"Bankroll: ${STARTING_CASH}")
    print(f"Strategy: Bet ${BET_SIZE} on the HOME TEAM every time they are the FAVORITE.")
    print("------------------------\n")
    
    wins = 0
    losses = 0
    
    # 3. The Time Machine Loop
    # We iterate through every game in history
    for index, row in df.iterrows():
        
        # KEY LOGIC: Check the Odds
        # In American Odds, negative (-150) means they are the Favorite.
        # Positive (+130) means they are the Underdog.
        odds = row['home_odds']
        
        # STRATEGY: Only bet if Home Team is Favorite (odds < 0)
        if odds < 0: 
            
            # Check the Result
            if row['home_score'] > row['away_score']:
                # --- WIN ---
                wins += 1
                
                # Calculate Profit for Negative Odds
                # Formula: Profit = (100 / Odds) * Bet
                profit = (100 / abs(odds)) * BET_SIZE
                current_cash += profit
                
            else:
                # --- LOSS ---
                losses += 1
                current_cash -= BET_SIZE
            
            # Bankruptcy Check (The "Reality" Feature)
            if current_cash <= 0:
                print(f"💀 WENT BROKE on row #{index} ({row['date']})")
                current_cash = 0
                break

    # 4. Final Report
    print(f"--- FINAL RESULTS ---")
    print(f"Total Bets Placed: {wins + losses}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {round((wins / (wins+losses)) * 100, 2)}%")
    print(f"Final Bankroll: ${round(current_cash, 2)}")
    
    profit_loss = current_cash - STARTING_CASH
    if profit_loss > 0:
        print(f"Total Profit: +${round(profit_loss, 2)} 📈")
    else:
        print(f"Total Loss: -${abs(round(profit_loss, 2))} 📉")

if __name__ == "__main__":
    run_simulation()