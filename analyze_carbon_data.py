import pandas as pd
import glob
import os

def calculate_daily_variability(df):
    """
    Calculate average daily variability of carbon intensity: (max - min)/min
    """
    # Resample to daily and calculate max, min for each day
    daily_stats = df.resample('D')['Carbon Intensity gCO₂eq/kWh (LCA)'].agg(['max', 'min'])
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
            'avg_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (LCA)'].mean(),
            'max_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (LCA)'].max(),
            'min_carbon_intensity': df['Carbon Intensity gCO₂eq/kWh (LCA)'].min(),
            'avg_renewable_percentage': df['Renewable Percentage'].mean(),
            'min_renewable_percentage': df['Renewable Percentage'].min(),
            'max_renewable_percentage': df['Renewable Percentage'].max(),
            'daily_variability': calculate_daily_variability(df)
        }
        results.append(zone_results)
    
    # Sort results by average carbon intensity in descending order
    results.sort(key=lambda x: x['avg_carbon_intensity'], reverse=True)
    return results

# Add debugging information
def analyze_zone_data(df, zone_id):
    """Analyze a single zone with detailed output"""
    carbon_mean = df['Carbon Intensity gCO₂eq/kWh (LCA)'].mean()
    data_points = len(df)
    missing_points = df['Carbon Intensity gCO₂eq/kWh (LCA)'].isna().sum()
    
    print(f"\nAnalyzing {zone_id}:")
    print(f"Total data points: {data_points}")
    print(f"Missing values: {missing_points}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Average carbon intensity: {carbon_mean:.1f}")
    return carbon_mean

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
        print(f"Min renewable percentage: {stats['min_renewable_percentage']:.2f}%")
        print(f"Max renewable percentage: {stats['max_renewable_percentage']:.2f}%") 

    # Calculate stats for top 15 zones
    top_15 = results[:15]

    # Calculate group averages
    avg_carbon = sum(z['avg_carbon_intensity'] for z in top_15) / len(top_15)
    avg_variability = sum(z['daily_variability'] for z in top_15) / len(top_15)

    # Print table with totals
    print("\nCarbon Intensity Analysis - 15 Highest-Emission Zones (2023)")
    print("===========================================================================")
    print(f"{'Zone':<35} {'Carbon Intensity':>20} {'Daily Variation':>15}")
    print("---------------------------------------------------------------------------")

    for zone in top_15:
        name = zone['zone_name'][:34]  # Truncate long names
        carbon = f"{zone['avg_carbon_intensity']:.1f}"
        var = f"{zone['daily_variability']:.1%}"
        print(f"{name:<35} {carbon:>15} gCO₂eq/kWh {var:>12}")

    print("---------------------------------------------------------------------------")
    print(f"{'Group Average':<35} {avg_carbon:>15.1f} gCO₂eq/kWh {avg_variability:>12.1%}")
    
    # Calculate stats for top 15 zones with verification
    print("Verifying calculations for top 15 zones...")
    for zone in top_15:
        zone_df = data[zone['zone_id']]
        verified_avg = analyze_zone_data(zone_df, zone['zone_id'])
        if abs(verified_avg - zone['avg_carbon_intensity']) > 0.1:
            print(f"WARNING: Mismatch found for {zone['zone_id']}")
            print(f"Stored value: {zone['avg_carbon_intensity']:.1f}")
            print(f"Calculated value: {verified_avg:.1f}")
    
    