import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json
from typing import List, Dict, Optional
import urllib.parse


class CanadianMedicalDevicesExtractor:
    """
    A class to extract data from the Canadian Medical Devices Active Licence Listing (MDALL) database.
    """
    
    def __init__(self):
        self.base_url = "https://health-products.canada.ca/mdall-limh"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_active_licenses(self, 
                             device_name: Optional[str] = None,
                             license_number: Optional[str] = None,
                             company_name: Optional[str] = None,
                             device_identifier: Optional[str] = None,
                             max_results: int = 100) -> List[Dict]:
        """
        Search for active medical device licenses.
        
        Args:
            device_name: Name of the medical device
            license_number: License number
            company_name: Company/manufacturer name
            device_identifier: Device identifier
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing device information
        """
        
        # Prepare search URL
        search_url = f"{self.base_url}/prepareSearch"
        
        # Get the search page first to establish session
        response = self.session.get(f"{search_url}?type=active")
        if response.status_code != 200:
            raise Exception(f"Failed to access search page: {response.status_code}")
        
        # Parse the search form to get required parameters
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Prepare search parameters
        search_params = {
            'type': 'active',
            'search': 'Search'
        }
        
        if device_name:
            search_params['devicename'] = device_name
        if license_number:
            search_params['licencenumber'] = license_number
        if company_name:
            search_params['companyname'] = company_name
        if device_identifier:
            search_params['deviceidentifier'] = device_identifier
            
        # Perform the search
        search_result_url = f"{self.base_url}/searchResults"
        response = self.session.post(search_result_url, data=search_params)
        
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.status_code}")
        
        return self._parse_search_results(response.content, max_results)
    
    def _parse_search_results(self, html_content: str, max_results: int) -> List[Dict]:
        """
        Parse the search results HTML and extract device information.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        devices = []
        
        # Find the results table
        results_table = soup.find('table', {'class': 'table'}) or soup.find('table')
        
        if not results_table:
            print("No results table found")
            return devices
        
        # Extract table rows (skip header)
        rows = results_table.find_all('tr')[1:]  # Skip header row
        
        for i, row in enumerate(rows[:max_results]):
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 4:  # Ensure we have enough columns
                device_info = {
                    'license_number': cells[0].get_text(strip=True) if len(cells) > 0 else '',
                    'device_name': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                    'company_name': cells[2].get_text(strip=True) if len(cells) > 2 else '',
                    'license_date': cells[3].get_text(strip=True) if len(cells) > 3 else '',
                    'device_identifier': cells[4].get_text(strip=True) if len(cells) > 4 else '',
                    'device_class': cells[5].get_text(strip=True) if len(cells) > 5 else '',
                }
                
                # Clean up the data
                for key, value in device_info.items():
                    device_info[key] = value.replace('\n', ' ').replace('\t', ' ').strip()
                
                devices.append(device_info)
        
        return devices
    
    def get_device_details(self, license_number: str) -> Dict:
        """
        Get detailed information for a specific device license.
        """
        # This would require navigating to the detailed view
        # Implementation depends on the specific URL structure
        pass
    
    def export_to_csv(self, devices: List[Dict], filename: str = "medical_devices.csv"):
        """
        Export device data to CSV file.
        """
        if not devices:
            print("No data to export")
            return
            
        df = pd.DataFrame(devices)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        
    def export_to_excel(self, devices: List[Dict], filename: str = "medical_devices.xlsx"):
        """
        Export device data to Excel file.
        """
        if not devices:
            print("No data to export")
            return
            
        df = pd.DataFrame(devices)
        df.to_excel(filename, index=False)
        print(f"Data exported to {filename}")


def main():
    """
    Example usage of the CanadianMedicalDevicesExtractor
    """
    extractor = CanadianMedicalDevicesExtractor()
    
    print("Canadian Medical Devices Data Extractor")
    print("=" * 40)
    
    # Example searches
    search_examples = [
        {"device_name": "pacemaker", "description": "Searching for pacemakers"},
        {"device_name": "stent", "description": "Searching for stents"},
        {"company_name": "Abbott", "description": "Searching for Abbott devices"},
        {"device_name": "insulin pump", "description": "Searching for insulin pumps"},
    ]
    
    all_devices = []
    
    for example in search_examples:
        print(f"\n{example['description']}...")
        try:
            devices = extractor.search_active_licenses(
                device_name=example.get('device_name'),
                company_name=example.get('company_name'),
                max_results=50
            )
            
            print(f"Found {len(devices)} devices")
            all_devices.extend(devices)
            
            # Display first few results
            for i, device in enumerate(devices[:3]):
                print(f"  {i+1}. {device['device_name']} - {device['company_name']}")
            
            # Be respectful with requests
            time.sleep(2)
            
        except Exception as e:
            print(f"Error during search: {e}")
    
    # Export results
    if all_devices:
        print(f"\nTotal devices found: {len(all_devices)}")
        extractor.export_to_csv(all_devices, "canadian_medical_devices.csv")
        extractor.export_to_excel(all_devices, "canadian_medical_devices.xlsx")
    else:
        print("No devices found")


if __name__ == "__main__":
    main()