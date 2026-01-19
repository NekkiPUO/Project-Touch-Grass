import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# CONSTANTS
INPUT_FILE = "data/raw/gun_vs_ball.csv"
IMG_DIR = "reports/images_gun_ball"

def load_data():
    if not os.path.exists(INPUT_FILE):
        print("Error: Data file not found.")
        return None
    df = pd.read_csv(INPUT_FILE)
    
    # 1. DEFINE THE COHORTS
    # Leg 1: The "Jock" Cohort (Gun & Ball) vs "The World"
    target_genres = ['Gun', 'Ball']
    df['Cohort'] = df['category'].apply(lambda x: 'Gun & Ball' if x in target_genres else 'The Rest')
    
    return df

def leg_1_gun_ball_vs_world(df):
    print("\n==================================================")
    print("LEG 1: GUN & BALL vs. THE WORLD")
    print("==================================================")
    
    # Q1: Do they perform better? (Critical Score)
    print("\n--- Q1: CRITICAL PERFORMANCE (Metascore) ---")
    print(df.groupby('Cohort')['metacritic'].describe()[['mean', '50%', 'max']].round(1))
    
    # Q2: Are players casuals? (Median Playtime is the best 'Casual' indicator)
    print("\n--- Q2: CASUAL FACTOR (Median Playtime in Hours) ---")
    print(df.groupby('Cohort')['playtime'].median().round(1))
    
    # Q3: Are they soulless? (User Rating vs Metacritic gap)
    print("\n--- Q3: THE 'SOUL' TEST (User Ratings out of 5) ---")
    print(df.groupby('Cohort')['rating'].mean().round(2))
    
    # Q4: Do they make more money? (Proxy: Ratings Count = Popularity)
    print("\n--- Q4: POPULARITY / SALES PROXY (Avg Ratings Count) ---")
    print(df.groupby('Cohort')['ratings_count'].mean().round(0))
    
    # Q6: Are they played more? (Average Playtime - Dedication)
    print("\n--- Q6: DEDICATION (Average Playtime in Hours) ---")
    print(df.groupby('Cohort')['playtime'].mean().round(1))

    # Visualization for Leg 1
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Cohort', y='metacritic', data=df, palette="Set2")
    plt.title("Q1: Do Critics Like 'Gun & Ball' Games?")
    save_plot("L1_Critical_Score.png")

def leg_2_gun_vs_ball(df):
    print("\n==================================================")
    print("LEG 2: CIVIL WAR (GUN vs. BALL)")
    print("==================================================")
    
    # Filter only for Gun and Ball
    df_gb = df[df['category'].isin(['Gun', 'Ball'])].copy()
    
    # Direct Head-to-Head Table
    summary = df_gb.groupby('category').agg({
        'metacritic': 'mean',       # Quality
        'rating': 'mean',           # Soul
        'playtime': 'median',       # Casualness (Lower = More Casual)
        'ratings_count': 'mean'     # Popularity
    }).round(2)
    
    print(summary)

    # Visualization for Leg 2 (The Quadrant)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        data=df_gb[df_gb['playtime'] < 100], # Filter outliers
        x='playtime', 
        y='metacritic', 
        hue='category',
        alpha=0.6
    )
    plt.title("Gun vs. Ball: Quality vs. Addiction")
    plt.axvline(x=df_gb['playtime'].median(), color='red', linestyle='--', alpha=0.3, label='Median Playtime')
    save_plot("L2_Gun_vs_Ball_Scatter.png")

def save_plot(filename):
    os.makedirs(IMG_DIR, exist_ok=True)
    plt.savefig(os.path.join(IMG_DIR, filename))
    plt.close()

def main():
    df = load_data()
    if df is not None:
        leg_1_gun_ball_vs_world(df)
        leg_2_gun_vs_ball(df)

if __name__ == "__main__":
    main()