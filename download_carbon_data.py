import requests
import os

# Complete list of all 55 USA zones from https://www.electricitymaps.com/data-portal/united-states-of-america
ZONES = [
    'US',                    # United States (Country average)
    'US-CAR-YAD',           # Alcoa Power Generating Inc Yadkin Division
    'US-CENT-SWPP',         # Southwest Power Pool
    'US-FLA-FMPP',          # Florida Municipal Power Pool
    'US-FLA-FPC',           # Duke Energy Florida
    'US-FLA-FPL',           # Florida Power & Light
    'US-FLA-GVL',           # Gainesville Regional Utilities
    'US-FLA-HST',           # City of Homestead
    'US-FLA-JEA',           # Jacksonville Electric Authority
    'US-FLA-NSB',           # New Smyrna Beach Utilities
    'US-FLA-SEC',           # Seminole Electric Cooperative
    'US-FLA-TAL',           # City of Tallahassee
    'US-FLA-TEC',           # Tampa Electric Company
    'US-MIDA-PJM',          # PJM Interconnection
    'US-MIDW-AECI',         # Associated Electric Cooperative
    'US-MIDW-GLHB',         # GridLiance High Plains
    'US-MIDW-LGEE',         # Louisville Gas & Electric/Kentucky Utilities
    'US-MIDW-MISO',         # Midcontinent Independent System Operator
    'US-NE-ISNE',           # ISO New England
    'US-NW-AVA',            # Avista Corporation
    'US-NW-BPAT',           # Bonneville Power Administration
    'US-NW-CHPD',           # Public Utility District No. 1 of Chelan County
    'US-NW-DOPD',           # Public Utility District No. 1 of Douglas County
    'US-NW-GCPD',           # Public Utility District No. 2 of Grant County
    'US-NW-GRID',           # Gridforce Energy Management
    'US-NW-IPCO',           # Idaho Power Company
    'US-NW-NEVP',           # Nevada Power Company
    'US-NW-NWMT',           # NorthWestern Energy
    'US-NW-PACE',           # PacifiCorp East
    'US-NW-PACW',           # PacifiCorp West
    'US-NW-PGE',            # Portland General Electric
    'US-NW-PSCO',           # Public Service Company of Colorado
    'US-NW-PSEI',           # Puget Sound Energy
    'US-NW-SCL',            # Seattle City Light
    'US-NW-TPWR',           # City of Tacoma
    'US-NW-WACM',           # Western Area Power Administration - Rocky Mountain Region
    'US-NW-WAUW',           # Western Area Power Administration - Upper Great Plains West
    'US-NY-NYIS',           # New York Independent System Operator
    'US-SE-AEC',            # PowerSouth Energy Cooperative
    'US-SE-SEPA',           # Southeastern Power Administration
    'US-SE-SOCO',           # Southern Company Services
    'US-SW-AZPS',           # Arizona Public Service Company
    'US-SW-DEAA',           # Arlington Valley
    'US-SW-EPE',            # El Paso Electric Company
    'US-SW-GRIF',           # Griffith Energy
    'US-SW-GRMA',           # Gila River Power
    'US-SW-HGMA',           # New Harquahala Generating Company
    'US-SW-PNM',            # Public Service Company of New Mexico
    'US-SW-SRP',            # Salt River Project
    'US-SW-TEPC',           # Tucson Electric Power
    'US-SW-WALC',           # Western Area Power Administration - Desert Southwest Region
    'US-TEN-TVA',           # Tennessee Valley Authority
    'US-TEX-ERCO',          # Electric Reliability Council of Texas
    'US-SW-IID',            # Imperial Irrigation District
    'US-CAL-BANC'           # Balancing Authority of Northern California
]

def download_carbon_data():
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Base URL pattern
    base_url = 'https://data.electricitymaps.com/2024-01-17'
    
    for zone in ZONES:
        filename = f'{zone}_2023_hourly.csv'
        url = f'{base_url}/{filename}'
        output_path = os.path.join('data/hourly', filename)
        
        print(f'Downloading data for {zone}...')
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f'Successfully downloaded {filename}')
            
        except requests.exceptions.RequestException as e:
            print(f'Error downloading {filename}: {e}')
            print(f'Failed URL: {url}')

if __name__ == '__main__':
    print(f'Starting download for {len(ZONES)} zones...')
    download_carbon_data()
    print('Download process completed.') 