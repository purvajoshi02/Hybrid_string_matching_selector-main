# Hybrid String Matching Algorithm Selector

## About the Project

The Hybrid String Matching Algorithm Selector is a Python-based application that automatically selects a suitable string-matching algorithm based on the characteristics of the input text and search pattern.

The application uses Streamlit to provide a simple, interactive web interface for searching text and comparing algorithm performance.

## Algorithms Implemented

* **Naive String Matching:** Searches the text by checking possible pattern positions.
* **Knuth–Morris–Pratt (KMP):** Uses an LPS (Longest Proper Prefix which is also a Suffix) table to avoid unnecessary comparisons.
* **Boyer–Moore:** Uses the bad-character rule to skip positions during searching.

## Features

* Automatic algorithm selection using rule-based heuristics.
* Analysis of text length, pattern length, character diversity, and repetition.
* Search results showing all matching positions.
* Performance comparison between the three algorithms.
* Interactive web interface built with Streamlit.
* Execution-time measurement.

## Technologies Used

* Python
* Streamlit
* Time module
* Collections module

## Installation and Setup

1. Clone this repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project folder:

   ```bash
   cd hybrid-string-matching-selector
   ```

3. Install the required dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

## How It Works

1. The user enters text and a search pattern.
2. The application analyzes the input characteristics.
3. The selector recommends one of the three implemented algorithms.
4. The selected algorithm searches for every occurrence of the pattern.
5. The application displays the match positions and execution time.
6. Users can optionally compare all three algorithms.

## Important Note

The selector uses predefined rules and thresholds. Its recommendations are heuristic-based and are not guaranteed to select the fastest algorithm for every input.

Execution times depend on input size, system conditions, and implementation details.

## Future Improvements

* Improve the selector using benchmark results.
* Add repeated benchmark trials and median execution times.
* Include additional test cases and automated correctness checks.
* Add visual performance comparison charts.
* Deploy the application online.

## Author

Prem Massand
