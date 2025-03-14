import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def fetch_xml_to_df():
    # Get previous day's date in YYYY-MM-DD format
    previous_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Construct the URL with the previous date
    url = f"https://ems02.emsbk.com/WebTrak/lis2/data/operation/hourly/{previous_date}"
    
    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    # Request the XML data
    response = requests.get(url, headers=headers)
    
    # Check if response is successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    # Parse the XML data
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        print("Error parsing XML. The response may not be valid XML.")
        return None
    
    # Extract day attribute
    day = root.attrib.get("day", "Unknown")
    
    # Extract data into a list of dictionaries
    data = []
    for elem in root.findall(".//hour"):
        hour = elem.attrib.get("hour")
        operations = elem.attrib.get("operations")
        data.append({"day": day, "hour": int(hour), "operations": int(operations)})
    
    # Convert list of dictionaries into a DataFrame and sort by hour
    df = pd.DataFrame(data).sort_values(by="hour", ascending=True)
    return df

# Fetch and display the DataFrame
df = fetch_xml_to_df()


# Exportar
from datetime import datetime
df.to_csv(datetime.now().strftime('data_sources/data_transformed/voos_aeroporto-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
