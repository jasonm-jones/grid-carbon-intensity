import pandas as pd
import glob
import os

def calculate_daily_variability(df):
    """
    Calculate average daily variability of carbon intensity: (max - min)/min
    """
    # Resample to daily and calculate max, min for each day
    daily_stats = df.resample('D')['Carbon Intensity gCO₂eq/kWh (direct)'].agg(['max', 'min'])
    # Calculate daily variability
    daily_variability = (daily_stats['max'] - daily_stats['min']) / daily_stats['min']
    # Return mean of daily variability
    return daily_variability.mean()

def load_hourly_data(data_dir='data/hourly'):
    """
    Load all hourly carbon intensity data files from the specified directory.
    Returns a dictionary of DataFrames, keyed by zone ID.
    """
    all_data = {}
    
    # Get list of all CSV files in the hourly directory
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    for file_path in csv_files:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert datetime column to pandas datetime
        df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
        
        # Set datetime as index
        df.set_index('Datetime (UTC)', inplace=True)
        
        # Get zone ID from the first row
        zone_id = df['Zone Id'].iloc[0]
        
        # Store in dictionary
        all_data[zone_id] = df
    
    return all_data

def analyze_data(data_dict):
    """
    Perform basic analysis on the loaded data.
    """
    results = []
    
    for zone_id, df in data_dict.items():
        zone_results = {
            'zone_id': zone_id,
            'zone_name': df['Zone Name'].iloc[0],
            'total_hours': len(df),
            'avg_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (direct)'].mean(),
            'max_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (direct)'].max(),
            'min_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (direct)'].min(),
            'avg_renewable_percentage': df['Renewable Percentage'].mean(),
            'max_renewable_percentage': df['Renewable Percentage'].max(),
            'daily_variability': calculate_daily_variability(df)
        }
        results.append(zone_results)
    
    # Sort results by average carbon intensity in descending order
    results.sort(key=lambda x: x['avg_carbon_intensity'], reverse=True)
    return results

if __name__ == "__main__":
    # Load all data
    print("Loading data...")
    data = load_hourly_data()
    
    # Analyze data
    print("\nAnalyzing data...")
    results = analyze_data(data)
    
    # Print results
    print("\nZones ranked by average carbon intensity (highest to lowest):")
    print("-" * 130)
    
    # Print header
    print(f"{'Rank':<6}{'Zone Name':<40}{'Zone ID':<15}{'Avg Carbon Intensity':>20}{'Daily Variability':>20}")
    print("-" * 130)
    
    # Print sorted results
    for i, stats in enumerate(results, 1):
        zone_name = stats['zone_name'][:40]  # Truncate to 40 chars
        print(f"{i:<6}{zone_name:<40}{stats['zone_id']:<15}{stats['avg_carbon_intensity']:>20.2f}{stats['daily_variability']:>20.2%}")
    
    # Print detailed stats for top 5 highest carbon intensity zones
    print("\nDetailed statistics for top 5 highest carbon intensity zones:")
    print("-" * 100)
    for stats in results[:5]:
        print(f"\nZone: {stats['zone_name']} ({stats['zone_id']})")
        print(f"Total hours: {stats['total_hours']}")
        print(f"Average carbon intensity: {stats['avg_carbon_intensity']:.2f} gCO₂eq/kWh")
        print(f"Max carbon intensity: {stats['max_carbon_intensity']:.2f} gCO₂eq/kWh")
        print(f"Min carbon intensity: {stats['min_carbon_intensity']:.2f} gCO₂eq/kWh")
        print(f"Daily variability: {stats['daily_variability']:.2%}")
        print(f"Average renewable percentage: {stats['avg_renewable_percentage']:.2f}%")
        print(f"Max renewable percentage: {stats['max_renewable_percentage']:.2f}%") 