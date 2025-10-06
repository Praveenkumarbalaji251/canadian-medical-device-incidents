import requests
import pandas as pd
from typing import List, Dict
import zipfile
import os


class MedicalDeviceIncidentsExtractor:
    """
    A class to extract data from the Health Canada Medical Device Incidents (MDI) database.
    """
    
    def __init__(self):
        self.base_url = "https://hpr-rps.hres.ca"
        self.search_url = f"{self.base_url}/mdi_landing.php"
        self.extract_url = f"{self.base_url}/files/extract.zip"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def download_full_extract(self, save_path: str = "mdi_full_extract.zip") -> str:
        """
        Download the full extract file from the MDI database.
        
        Args:
            save_path: Path to save the downloaded zip file
            
        Returns:
            Path to the downloaded file
        """
        print("Downloading full Medical Device Incidents extract...")
        
        try:
            response = self.session.get(self.extract_url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Downloaded extract to: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"Error downloading extract: {e}")
            raise
    
    def extract_zip_contents(self, zip_path: str, extract_dir: str = "mdi_data") -> List[str]:
        """
        Extract contents from the downloaded zip file.
        
        Args:
            zip_path: Path to the zip file
            extract_dir: Directory to extract files to
            
        Returns:
            List of extracted file paths
        """
        print(f"Extracting contents from {zip_path}...")
        
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
        
        extracted_files = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"Found {len(file_list)} files in archive:")
                
                for file_name in file_list:
                    print(f"  - {file_name}")
                    zip_ref.extract(file_name, extract_dir)
                    extracted_files.append(os.path.join(extract_dir, file_name))
                
        except Exception as e:
            print(f"Error extracting zip: {e}")
            raise
        
        return extracted_files
    
    def load_incident_data(self, file_path: str) -> pd.DataFrame:
        """
        Load incident data from extracted file (CSV/Excel).
        
        Args:
            file_path: Path to the data file
            
        Returns:
            DataFrame containing the incident data
        """
        print(f"Loading data from: {file_path}")
        
        try:
            # Try different file formats
            if file_path.lower().endswith('.dsv'):
                # DSV files are typically pipe-delimited (|)
                df = pd.read_csv(file_path, sep='|', encoding='utf-8')
            elif file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.lower().endswith('.txt'):
                # Try tab-separated or comma-separated
                try:
                    df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                except Exception:
                    df = pd.read_csv(file_path, encoding='utf-8')
            else:
                # Try as CSV by default
                df = pd.read_csv(file_path, encoding='utf-8')
            
            print(f"Loaded {len(df)} records")
            print(f"Columns: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            # Try with different encoding
            try:
                df = pd.read_csv(file_path, encoding='latin-1')
                print(f"Successfully loaded with latin-1 encoding: {len(df)} records")
                return df
            except Exception as e2:
                print(f"Failed with latin-1 encoding: {e2}")
                raise
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                           start_date: str = "2024-09-01", 
                           end_date: str = "2025-09-30",
                           date_column: str = None) -> pd.DataFrame:
        """
        Filter incident data by date range.
        
        Args:
            df: DataFrame containing incident data
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            date_column: Name of the date column (auto-detected if None)
            
        Returns:
            Filtered DataFrame
        """
        print(f"Filtering data from {start_date} to {end_date}")
        
        # Auto-detect date column if not specified
        if date_column is None:
            date_columns = []
            for col in df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['date', 'received', 'report', 'incident', 'time']):
                    date_columns.append(col)
            
            if date_columns:
                date_column = date_columns[0]
                print(f"Using date column: {date_column}")
            else:
                print("No date column found. Available columns:")
                for col in df.columns:
                    print(f"  - {col}")
                return df
        
        try:
            # Convert start and end dates
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Convert the date column to datetime
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            
            # Filter the data
            mask = (df[date_column] >= start_dt) & (df[date_column] <= end_dt)
            filtered_df = df[mask].copy()
            
            print(f"Filtered from {len(df)} to {len(filtered_df)} records")
            
            # Remove rows where date conversion failed
            filtered_df = filtered_df.dropna(subset=[date_column])
            print(f"After removing invalid dates: {len(filtered_df)} records")
            
            return filtered_df
            
        except Exception as e:
            print(f"Error filtering by date: {e}")
            print(f"Sample values in {date_column}:")
            print(df[date_column].head(10).tolist())
            return df
    
    def analyze_incidents(self, df: pd.DataFrame) -> Dict:
        """
        Perform basic analysis on incident data.
        
        Args:
            df: DataFrame containing incident data
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'total_incidents': len(df),
            'date_range': {},
            'top_devices': {},
            'top_manufacturers': {},
            'incident_types': {},
            'severity_levels': {}
        }
        
        # Date range analysis
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if date_columns:
            date_col = date_columns[0]
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            valid_dates = df[date_col].dropna()
            if len(valid_dates) > 0:
                analysis['date_range'] = {
                    'earliest': valid_dates.min().strftime('%Y-%m-%d'),
                    'latest': valid_dates.max().strftime('%Y-%m-%d')
                }
        
        # Top devices/products
        device_columns = [col for col in df.columns if any(keyword in col.lower() 
                         for keyword in ['device', 'product', 'name', 'brand'])]
        if device_columns:
            device_col = device_columns[0]
            top_devices = df[device_col].value_counts().head(10)
            analysis['top_devices'] = top_devices.to_dict()
        
        # Top manufacturers
        mfr_columns = [col for col in df.columns if any(keyword in col.lower() 
                      for keyword in ['manufacturer', 'company', 'mfr'])]
        if mfr_columns:
            mfr_col = mfr_columns[0]
            top_mfrs = df[mfr_col].value_counts().head(10)
            analysis['top_manufacturers'] = top_mfrs.to_dict()
        
        # Incident types
        type_columns = [col for col in df.columns if any(keyword in col.lower() 
                       for keyword in ['type', 'category', 'incident', 'problem'])]
        if type_columns:
            type_col = type_columns[0]
            incident_types = df[type_col].value_counts().head(10)
            analysis['incident_types'] = incident_types.to_dict()
        
        return analysis
    
    def export_filtered_data(self, df: pd.DataFrame, filename: str = "mdi_sept2024_sept2025"):
        """
        Export filtered data to multiple formats.
        
        Args:
            df: DataFrame to export
            filename: Base filename (without extension)
        """
        if df.empty:
            print("No data to export")
            return
        
        # Export to CSV
        csv_file = f"{filename}.csv"
        df.to_csv(csv_file, index=False)
        print(f"Exported to CSV: {csv_file}")
        
        # Export to Excel
        excel_file = f"{filename}.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"Exported to Excel: {excel_file}")
        
        # Export summary statistics
        summary_file = f"{filename}_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("Medical Device Incidents Data Summary\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total Records: {len(df)}\n")
            f.write(f"Date Range: September 2024 - September 2025\n\n")
            
            f.write("Columns:\n")
            for i, col in enumerate(df.columns, 1):
                f.write(f"{i:2d}. {col}\n")
            
            f.write(f"\nData Types:\n")
            f.write(str(df.dtypes))
            
            f.write(f"\n\nSample Data (first 5 rows):\n")
            f.write(str(df.head()))
        
        print(f"Exported summary: {summary_file}")
    
    def extract_september_2024_to_2025(self) -> pd.DataFrame:
        """
        Main method to extract Medical Device Incidents data from September 2024 to September 2025.
        
        Returns:
            DataFrame containing the filtered incident data
        """
        print("🏥 Extracting Medical Device Incidents Data")
        print("📅 Date Range: September 2024 - September 2025")
        print("=" * 60)
        
        try:
            # Step 1: Download the full extract
            zip_path = self.download_full_extract()
            
            # Step 2: Extract the zip contents
            extracted_files = self.extract_zip_contents(zip_path)
            
            # Step 3: Load the main data file
            data_file = None
            for file_path in extracted_files:
                if any(ext in file_path.lower() for ext in ['.dsv', '.csv', '.xlsx', '.txt']):
                    # Prioritize INCIDENT.dsv as main data file
                    if 'INCIDENT.dsv' in file_path:
                        data_file = file_path
                        break
                    elif data_file is None:  # Use as fallback
                        data_file = file_path
            
            if not data_file:
                raise Exception("No data file found in extract")
            
            # Step 4: Load the data
            df = self.load_incident_data(data_file)
            
            # Step 5: Filter by date range (use RECEIPT_DT as the primary date column)
            filtered_df = self.filter_by_date_range(
                df, 
                start_date="2024-09-01", 
                end_date="2025-09-30",
                date_column="RECEIPT_DT"
            )
            
            # Step 6: Perform analysis
            analysis = self.analyze_incidents(filtered_df)
            
            # Step 7: Print summary
            print("\n📊 Analysis Summary:")
            print("-" * 30)
            print(f"Total incidents in period: {analysis['total_incidents']}")
            
            if analysis['date_range']:
                print(f"Actual date range: {analysis['date_range']['earliest']} to {analysis['date_range']['latest']}")
            
            if analysis['top_devices']:
                print(f"\nTop 5 devices with incidents:")
                for i, (device, count) in enumerate(list(analysis['top_devices'].items())[:5], 1):
                    print(f"  {i}. {device}: {count} incidents")
            
            if analysis['top_manufacturers']:
                print(f"\nTop 5 manufacturers with incidents:")
                for i, (mfr, count) in enumerate(list(analysis['top_manufacturers'].items())[:5], 1):
                    print(f"  {i}. {mfr}: {count} incidents")
            
            # Step 8: Export the filtered data
            self.export_filtered_data(filtered_df, "medical_device_incidents_sept2024_sept2025")
            
            return filtered_df
            
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            raise


def main():
    """
    Main function to run the Medical Device Incidents extraction
    """
    extractor = MedicalDeviceIncidentsExtractor()
    
    try:
        # Extract data for the specified period
        incident_data = extractor.extract_september_2024_to_2025()
        
        print(f"\n✅ Extraction completed successfully!")
        print(f"📁 Check the output files for detailed data")
        
        # Additional analysis options
        print(f"\n🔍 Additional Analysis Options:")
        print(f"1. View column details")
        print(f"2. Filter by specific device type")
        print(f"3. Filter by manufacturer")
        print(f"4. Export custom date range")
        
        return incident_data
        
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        return None


if __name__ == "__main__":
    main()