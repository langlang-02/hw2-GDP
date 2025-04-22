import requests

class GDPData:
    def __init__(self, country):
        self.country = country
        self.api_url = f'https://api.worldbank.org/v2/country/{country}/indicator/NY.GDP.MKTP.CD?date=1990:2022&format=json'
    
    def get_gdp_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            gdp_values = []
            for item in data[1]:
                year = item['date']
                gdp = item['value']
                if gdp is not None:
                    gdp_values.append((year, gdp))
            return gdp_values
        else:
            return None
