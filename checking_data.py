import pandas as pd
import numpy as np

def check_data_quality(file_path, dataset_name):
    """
    Check data quality metrics for a given CSV file
    """
    print(f"\n=== Checking {dataset_name} ===")
    try:
        df = pd.read_csv(file_path)
        
        # Basic information
        print(f"\nShape: {df.shape}")
        print(f"Number of columns: {len(df.columns)}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print("\nMissing values:")
            print(missing_values[missing_values > 0])
        else:
            print("\nNo missing values found")
            
        # Check for duplicates
        duplicates = df.duplicated().sum()
        print(f"\nNumber of duplicate rows: {duplicates}")
        
        # Data types
        print("\nData types:")
        print(df.dtypes)
        
        # Basic statistics
        print("\nNumerical columns statistics:")
        print(df.describe().round(2))
        
        return df
        
    except Exception as e:
        print(f"Error reading {dataset_name}: {str(e)}")
        return None

def main():
    # Define file paths
    files = {
        'Songs Normalize': 'các dataset/songs_normalize.csv',
        'Spotify': 'các dataset/spotify.csv',
        'Top Songs': 'các dataset/top_songs_through_year.csv',
        'Billboard Clean': 'các dataset/đã làm sạch/billboard_clean.csv',
        'Spotify Clean': 'các dataset/đã làm sạch/spotify_clean.csv',
        'Merged Music': 'các dataset/đã làm sạch/top song (có audio features)/merged_music_data.csv'
    }
    
    # Check each dataset
    for name, path in files.items():
        df = check_data_quality(path, name)
        
        if df is not None:
            # Additional checks specific to music data
            if 'year' in df.columns:
                print(f"\nYear range: {df['year'].min()} - {df['year'].max()}")
            
            if 'duration_ms' in df.columns:
                print("\nChecking for suspicious duration values:")
                print(f"Min duration: {df['duration_ms'].min()} ms")
                print(f"Max duration: {df['duration_ms'].max()} ms")
            
            print("\n" + "="*50)

if __name__ == "__main__":
    main()