# 🌱 Project: Touch Grass
> *Quantifying the "Misery Loop" of Mainstream Gaming through Data Engineering.*

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Dependency Manager](https://img.shields.io/badge/uv-lightning%20fast-purple)
![Status](https://img.shields.io/badge/Status-Based-green)

![Project: Touch Grass Banner](./banner.png)

## The Premise
**Imagine a product.**

It costs $70 a year. You don't just use it; you obsess over it.
You spend nearly 15 hours—two full workdays—grinding away at it.
It demands more of your time than any other form of entertainment you own.

**And you hate almost every minute of it.**

Engineered this repo to prove that **Sports Gamers** are trapped in a statistical anomaly I call the **"Misery Index"**.

Ingested over **24,000 games** from the `RAWG API` to settle the "Jock vs. Nerd" debate once and for all.
Are shooters and sports games just "dumb fun" for casuals? Or is something darker happening?

## Read the Full Analysis

I discovered that Mainstream gamers aren't casuals,they are "Grinders". We also found that Sports gamers have the highest retention but the lowest satisfaction in the industry.

👉 **[Read the full blog post and see the visualizations here](https://fezcode.com/blog/gun-and-ball/?theme=editorial)**

## The Stack (Engineered for Speed)
Avoided the bloat of standard Data Science setups. This project uses **`uv`**, a Rust-based Python package manager that is significantly faster than `pip` or `poetry`.

* **Ingestion:** Python scripts hitting RAWG.io API (with rate-limit handling).
* **Storage:** Local CSV Data Lake (Idempotent updates).
* **Analysis:** Pandas & Seaborn (Jupyter Notebooks).
* **Environment:** Managed by `uv`.

## The "Misery Index"
To quantify the relationship between addiction and satisfaction, engineered a custom feature:

$$
Misery\ Index = 
\begin{cases} 
   \frac{Average\ Hours\ Played}{User\ Rating} & \text{if } Rating > 0 \\
   \text{Excluded} & \text{if } Rating = 0 
\end{cases}
$$

* **Low Score:** Healthy engagement (High Fun / Moderate Time).
* **High Score:** Toxic engagement (Low Fun / Massive Time).

## Project Structure

```bash
project-touch-grass/
├── data/
│   └── raw/
│       └── gun_vs_ball.csv    # The raw dataset (24k+ games)
├── notebooks/
│   ├── gun_and_ball.ipynb     # Part 1: Mainstream vs. The World
│   └── gun_vs_ball.ipynb      # Part 2: The Civil War (Shooters vs. Sports)
├── src/
│   ├── ingest_games.py        # The ETL script
│   ├── check_data.py          # RAWG API Data Checker
│   └── analyze_gun_ball.py    # Non-notebook version of the analysis
├── pyproject.toml             # uv configuration
└── README.md                  # You are here

```

## How to Run

### 1. Prerequisite: Install `uv`

If you don't have it, get it. It changes lives.

**Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Sync Dependencies

This will create the virtual environment and install `pandas`, `seaborn`, `ipykernel`, etc.

```bash
uv sync
```

### 3. Run the Analysis

Open VS Code, select the `gun_vs_ball.ipynb` notebook, and select the Kernel named `.venv`.

```bash
code notebooks/gun_vs_ball.ipynb
```
## Contributing

I am an engineer, not a statistician. If you find a flaw in the `Misery Index` or want to add a new dimension to the analysis (e.g., "Price per Hour of Fun"), feel free to open a PR!

1. Fork it.
2. Branch it (`git checkout -b feature/new-metric`).
3. Commit it (`git commit -m 'Added the Microtransaction-Pain-Ratio'`).
4. Push it.
