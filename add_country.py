import requests
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

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
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GDP Visualization")
        self.geometry("400x200")

        # Initialize list to store economic data for countries
        self.economic_data_list = []

        # Create input field for country name
        self.label = tk.Label(self, text="Enter country name:")
        self.label.pack(pady=10)
        
        self.country_entry = tk.Entry(self)
        self.country_entry.pack(pady=10)
        
        # Create button to add country data
        self.add_button = tk.Button(self, text="Add Country GDP", command=self.add_country)
        self.add_button.pack(pady=10)

        # Create a button to show the chart
        self.show_button = tk.Button(self, text="Show GDP Chart", command=self.plot_data)
        self.show_button.pack(pady=10)

    def add_country(self):
        country_name = self.country_entry.get()
        if country_name:
            try:
                # Fetch GDP data for the entered country
                economic_data = GDPData(country_name)
                gdp_data = economic_data.get_gdp_data()

                if gdp_data is not None:
                    self.economic_data_list.append((country_name, gdp_data))
                    print(f"Added GDP data for {country_name}")
                else:
                    print(f"No GDP data found for {country_name}")
            except Exception as e:
                print(f"Error fetching data for {country_name}: {e}")
        else:
            print("Please enter a country name.")

    def plot_data(self):
        if not self.economic_data_list:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        
        for country_name, gdp_data in self.economic_data_list:
            years = [year for year, _ in gdp_data]
            gdp_values = [gdp for _, gdp in gdp_data]
            plt.plot(years, gdp_values, label=country_name)

        plt.title('GDP Over Time for Selected Countries', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('GDP (USD)', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
