import pandas as pd

def validate_download_data(df):
    # 1. Check for missing dates (gaps in the data)
    missing_dates = df.index.isnull().sum()
    print(f"Missing dates: {missing_dates}")

    # 2. Check for any gaps between consecutive dates
    date_diff = df.index.diff().dropna()  # Compute the difference between consecutive dates
    gap_days = date_diff[date_diff > pd.Timedelta(days=1)]  # Find gaps larger than 1 day
    if not gap_days.empty:
        print(f"Gaps found on dates: {gap_days.index}")
    else:
        print("No gaps found.")

    # 3. Check for zero downloads
    zero_downloads = df[df['downloads'] == 0]
    print(f"Zero download days: {len(zero_downloads)}")

    # 4. Check for outliers (e.g., downloads > 2 standard deviations from the mean)
    mean = df['downloads'].mean()
    std = df['downloads'].std()
    outliers = df[df['downloads'] > mean + 2 * std]
    print(f"Outliers (downloads > 2 std dev): {len(outliers)}")

    # 5. Check for overall trends (check if there are sudden spikes)
    # This could be done by checking for large changes in the data
    large_changes = df['downloads'].pct_change().abs() > 0.5  # 50% change is significant
    print(f"Large changes detected on days: {df.index[large_changes]}")

    return missing_dates, gap_days, zero_downloads, outliers, large_changes

# Load your data (Python and JS examples)
python_df = pd.read_csv('python_download_data.csv', index_col=0, parse_dates=True)
javascript_df = pd.read_csv('javascript_download_data.csv', index_col=0, parse_dates=True)

# Validate the data
print("Validating Python download data...")
validate_download_data(python_df)

print("Validating JavaScript download data...")
validate_download_data(javascript_df)