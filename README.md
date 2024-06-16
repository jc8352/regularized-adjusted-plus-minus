# Calculating Regularized Adjusted Plus-Minus (RAPM) for NBA Players

## Introduction
This repository provides a framework for calculating Regularized Adjusted Plus-Minus (RAPM) for NBA players using play-by-play data. RAPM is a statistic that offers a more nuanced understanding of player impact compared to traditional plus-minus.

## Overview
This repository processes NBA play-by-play data to:
- Identify players on the court for each play.
- Convert the play-by-play data into a matrix of possessions.
- One-hot encode the matrix of possessions.
- Perform ridge regression to calculate RAPM, estimating the impact of each player on a per-possession basis.

## Background
Regularized Adjusted Plus-Minus (RAPM) improves upon traditional plus-minus by:
- Considering the specific players on the court for each possession.
- Accounting for home-court advantage.

### Example
For a single possession:
- Players on the court are represented as a vector: `[O_P1, O_P2, O_P3, O_P4, O_P5, D_P1, D_P2, D_P3, D_P4, D_P5]`
- The outcome of the possession (e.g., 2 points for a made field goal) is predicted by multiplying this vector by the regression coefficients.

Extended across many possessions, the regression coefficients become estimates of each individual player's impact on the possessions they were on the court for.

## Procedure
To generate the data and perform the regression:

1. **Run the Main Script**:
   ```bash
   python3 main.py
  
This script processes play-by-play data for the 2021-22 season, generates the required matrices, and performs ridge regression. Intermediate data is stored in the `created_possession_data` folder, and final regression results are saved in `regression_results`.

2. **View Results**: 
    
    Precomputed results are available for:
    - 2021-22 season: `2021-22_rapm.html`
    - 2022-23 season: `2022-23_rapm.html`
    - Combined (2021-22 and 2022-23): `2021-23_rapm.html`

3. **Run for Different Seasons**:
    - Modify the `YEAR` variable in `main.py` to 2022 to analyze the 2022-23 season.
    - For combined analysis of both seasons, run:
        ```bash
        python3 2021-23regression.py
        ```
        after processing both seasons with `main.py`.
    
## Repository Structure
- `main.py`: Main script for data processing and regression.
- `2021-23regression.py`: Script to combine data and perform regression across multiple seasons.
- `created_possession_data/`: Folder containing intermediate data.
- `regression_results/`: Folder with final regression results for easy viewing.

## Notes
- Running the complete process may take several minutes due to the volume of data.
- Results are stored in CSV files (`regression_results`) and HTML format for quick access and analysis.

