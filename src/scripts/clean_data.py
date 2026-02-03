import pandas as pd
import numpy as np

# CONFIG: Make sure this matches your downloaded file name exactly
INPUT_FILE = "data/nba_2008-2025.csv"
OUTPUT_FILE = "data/nba_clean.csv"

def clean_data():
    try:
        print(f"Loading {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE)
        
        # 1. Standardize Column Names
        # only keep what need for the MVP
        required_cols = {
            'date': 'date',
            'home': 'home_team',
            'away': 'away_team',
            'score_home': 'home_score',
            'score_away': 'away_score',
            'moneyline_home': 'home_odds',
            'moneyline_away': 'away_odds'
        }
        
        # Check if columns exist before renaming
        missing_cols = [col for col in required_cols.keys() if col not in df.columns]
        if missing_cols:
            print(f"❌ CRITICAL ERROR: The dataset is missing these columns: {missing_cols}")
            return

        # Rename and select only the columns we need
        df = df[required_cols.keys()].rename(columns=required_cols)
        
        # 2. Fix Dates
        df['date'] = pd.to_datetime(df['date'])
        
        # 3. INVESTIGATE THE WARNING (The "Missing Odds" Check)
        print("\n--- DIAGNOSTICS ---")
        recent_games = df[df['date'].dt.year >= 2024]
        total_recent = len(recent_games)
        missing_odds = recent_games['home_odds'].isna().sum()
        
        print(f"Total games from 2024-2025: {total_recent}")
        print(f"Games with MISSING odds: {missing_odds}")
        
        if missing_odds > (total_recent * 0.9):
            print("⚠️ WARNING: It looks like the note was right. Most recent games have NO odds.")
            print("   For the MVP, we might have to test on older data (2015-2022).")
        else:
            print("✅ GOOD NEWS: We found odds for recent games! The note might be outdated.")

        # 4. Drop rows where we can't calculate a winner (missing scores or odds)
        # For the MVP, if there are no odds, we can't bet.
        original_count = len(df)
        df = df.dropna(subset=['home_odds', 'away_odds', 'home_score'])
        dropped_count = original_count - len(df)
        
        print(f"\n--- CLEANING SUMMARY ---")
        print(f"Original Rows: {original_count}")
        print(f"Dropped Rows (Missing Data): {dropped_count}")
        print(f"Final Clean Rows: {len(df)}")
        
        # 5. Save the Clean File
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Success! Saved clean data to {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file at {INPUT_FILE}")
        print("Did you move the downloaded CSV into the 'data' folder?")

if __name__ == "__main__":
    clean_data()