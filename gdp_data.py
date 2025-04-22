import requests

class GDPData:
    def __init__(self, country):
        self.country = country
        self.gdp_api_url = f'https://api.worldbank.org/v2/country/{country}/indicator/NY.GDP.MKTP.CD?date=1990:2022&format=json'
        self.cpi_api_url = f'https://api.worldbank.org/v2/country/{country}/indicator/FP.CPI.TOTL.ZG?date=1990:2022&format=json'
    
    def get_gdp_data(self):
        response = requests.get(self.gdp_api_url)
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

    def get_cpi_data(self):
        response = requests.get(self.cpi_api_url)
        if response.status_code == 200:
            data = response.json()
            cpi_values = []
            for item in data[1]:
                year = item['date']
                cpi = item['value']
                if cpi is not None:
                    cpi_values.append((year, cpi))
            return cpi_values
        else:
            return None