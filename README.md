# The Mirsky Ratio: An Empirical Analysis

This repository contains the Python code and data to reproduce the results from the paper "The Mirsky Ratio: An Empirical Study on the Predictive Power of R&D to SG&A Allocation" by Gilbert Mirsky.

**Preprint:** [Link to your paper on the repository where you uploaded it]

## Description

This script calculates the "Mirsky Ratio" (R&D / SG&A) for a sample of companies from the S&P 100 and computes the Pearson correlation between this ratio and the one-year stock market performance.

## How to Run the Analysis

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gmirsky2/mirsky-ratio-analysis.git
    cd mirsky-ratio-analysis
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the analysis script:**
    ```bash
    python analysis.py
    ```

The script will then print the correlation coefficient and p-value to the console.

## Citation

If you use this code or the concepts presented in the paper, please cite the original work:

> Mirsky, G. (2025). *The Mirsky Ratio: An Empirical Study on the Predictive Power of R&D to SG&A Allocation*. Zenodo, https://github.com/gmirsky2/mirsky-ratio-analysis.

## License

The code in this repository is licensed under the MIT License. See the `LICENSE` file for more details.
