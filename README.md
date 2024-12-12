# Stock Prices and Sentiment Analysis Dashboard

## Overview
This application visualizes the relationship between stock prices and sentiment analysis from news and social media data. It provides an interactive dashboard with the following features:

1. **Line Chart:** Displays stock prices over time with sentiment thresholds.
2. **Bar Chart:** Summarizes sentiment composition for a selected stock and date range.
3. **Compound Sentiment Chart:** Shows overall sentiment trends over time, with interactive features.

## Prerequisites
To run the application, ensure you have the following installed:

- Python 3.7+
- Required Python libraries:
  - `dash`
  - `pandas`
  - `plotly`

## Installation Steps

1. Clone or download the project files.
2. Navigate to the project directory:
   ```bash
   cd path/to/project
   ```
3. Install the required dependencies:
   ```bash
   pip install dash pandas plotly
   ```

## Dataset
The application requires a CSV file named `sentiment.csv` in the same directory. The CSV should contain the following columns:

- `Date` (YYYY-MM-DD format)
- `Stock` (Stock name or symbol)
- `Open Price` (Stock price at market open)
- `Articles` (Number of articles analyzed)
- `Positive` (Positive sentiment score)
- `Neutral` (Neutral sentiment score)
- `Negative` (Negative sentiment score)

The application preprocesses the data by:
- Converting `Date` to datetime format.
- Calculating a `Compound` sentiment score as `Positive - Negative`.
- Renaming columns for consistency.
- Dropping rows with missing values.

## Running the Application

1. Start the Dash server by executing:
   ```bash
   python app.py
   ```
   Replace `app.py` with the filename containing your code.

2. Open a web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

## Using the Dashboard

### Filters
- **Select Stock:** Choose a stock from the dropdown to analyze.
- **Select Sentiment Type:** View positive, neutral, negative, or all sentiments.
- **Select Sentiment Threshold:** Adjust the sentiment score threshold using the slider.
- **Select Date Range:** Choose a specific range of dates to filter the data.

### Visualizations
- **Line Chart:** Displays stock prices with sentiment thresholds.
- **Compound Sentiment Chart:** Tracks overall sentiment trends. Clicking on the chart provides detailed metrics for the selected stock.
- **Bar Chart:** Summarizes the sentiment composition for the selected filters.

## Notes
- Ensure the CSV file format matches the expected structure.
- The application includes robust preprocessing to handle missing or incorrect data formats, but providing clean data is recommended for optimal performance.

## Customization
Feel free to modify the layout and style settings in the `app.layout` section to match your requirements.

## Troubleshooting
- **Error: File not found**: Ensure `sentiment.csv` is in the correct directory.
- **Missing library**: Run `pip install <library-name>` for any missing dependencies.
- **Server not starting**: Check for conflicting processes on port `8050` or specify another port using `app.run_server(port=XXXX)`.

