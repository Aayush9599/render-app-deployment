import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_irdai_notices(url):
    """Modified version of your script as a callable function"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        
        notices_data = []
        for row in rows:
            short_desc_tag = row.find('td', class_='table-cell table-col-shortDesc')
            date_tag = row.find('td', class_='table-cell table-cell-minw-100 table-col-lastUpdated')
            link_tag = row.find('td', class_='table-cell table-cell-expand-smaller table-cell-minw-150 table-col-subTitle')
            
            notices_data.append({
                "Short Description": short_desc_tag.text.strip() if short_desc_tag else None,
                "Date Updated": date_tag.text.strip() if date_tag else None,
                "Title": link_tag.find('a').text.strip() if link_tag and link_tag.find('a') else None,
                "Link": link_tag.find('a')['href'] if link_tag and link_tag.find('a') else None
            })
            
        return pd.DataFrame(notices_data)
    
    except requests.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Scraping error: {str(e)}")
