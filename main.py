import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
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

class GDPGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP 和 CPI 时间段选择")
        self.root.geometry("600x400+100+100")
        
        # 默认国家列表，初始时只有一个国家
        self.countries = ['USA']
        self.gdp_data = {country: GDPData(country) for country in self.countries}
        self.data = {country: self.gdp_data[country].get_gdp_data() for country in self.countries}
        self.cpi_values = {country: self.gdp_data[country].get_cpi_data() for country in self.countries}  # 新增CPI数据获取
        
        # 设置初始时间段
        self.start_year = 1990
        self.end_year = 2022

        # 国家代码下拉菜单选项
        self.country_codes = ['USA', 'CHN', 'DEU', 'IND', 'JPN', 'GBR', 'CAN', 'AUS', 'BRA', 'RUS']

        # 创建 GUI 元素
        self.create_widgets()

    def create_widgets(self):
        # 显示选择年份的标签
        self.label = tk.Label(self.root, text="请选择显示的年份范围")
        self.label.pack(pady=10)

        # 创建滑块来选择开始年份
        self.start_year_slider = tk.Scale(self.root, from_=1990, to=2022, orient=tk.HORIZONTAL, label="开始年份", command=self.update_plot)
        self.start_year_slider.set(self.start_year)
        self.start_year_slider.pack(pady=5)

        # 创建滑块来选择结束年份
        self.end_year_slider = tk.Scale(self.root, from_=1990, to=2022, orient=tk.HORIZONTAL, label="结束年份", command=self.update_plot)
        self.end_year_slider.set(self.end_year)
        self.end_year_slider.pack(pady=5)

        # 创建一个添加国家的按钮
        self.add_country_button = tk.Button(self.root, text="添加国家", command=self.add_country)
        self.add_country_button.pack(pady=10)

        # Create input field for country name
        self.label = tk.Label(self.root, text="Enter country name:")
        self.label.pack(pady=10)
        
        self.country_entry = tk.Entry(self.root)
        self.country_entry.pack(pady=10)

    def add_country(self):
        country_name = self.country_entry.get().strip()

        if country_name and country_name not in self.countries:
            try:
                # Fetch GDP and CPI data for the entered country
                economic_data = GDPData(country_name)
                gdp_data = economic_data.get_gdp_data()
                cpi_values = economic_data.get_cpi_data()

                if gdp_data is not None and cpi_values is not None:
                    self.countries.append(country_name)
                    self.gdp_data[country_name] = economic_data
                    self.data[country_name] = gdp_data
                    self.cpi_values[country_name] = cpi_values

                    self.update_plot()
                    self.country_entry.delete(0, tk.END)
                    print(f"Added GDP and CPI data for {country_name}")
                else:
                    if gdp_data is None:
                        print(f"No GDP data found for {country_name}")
                    else:
                        print(f"No CPI data found for {country_name}")
            except Exception as e:
                print(f"Error fetching data for {country_name}: {e}")            
        else:
            print("Please enter a valid country name.")

    def update_plot(self, event=None):
        self.start_year = self.start_year_slider.get()
        self.end_year = self.end_year_slider.get()

        plt.clf()

        for country in self.countries:
            # 过滤GDP数据
            filtered_gdp_data = [(int(year), gdp) for year, gdp in self.data[country] if self.start_year <= int(year) <= self.end_year]
            filtered_cpi_data = [(int(year), cpi) for year, cpi in self.cpi_values[country] if self.start_year <= int(year) <= self.end_year]

            if filtered_gdp_data:
                years = [year for year, gdp in filtered_gdp_data]
                gdp_values = [gdp for year, gdp in filtered_gdp_data]
                
                # 绘制GDP图表
                plt.subplot(2,1,1)
                plt.plot(years, gdp_values, marker='o', label=f'{country} GDP')
                plt.legend()

            if filtered_cpi_data:
                cpi_values = [cpi for year, cpi in filtered_cpi_data]

                # 绘制CPI图表
                plt.subplot(2,1,2)
                plt.plot(years, cpi_values, marker='x', label=f'{country} CPI', linestyle='--')
                plt.legend()

        # 设置图表标题与标签
        plt.title(f'GDP and CPI from {self.start_year} to {self.end_year}')
        plt.xlabel('Year')
        plt.ylabel('Value (in USD / CPI)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()

        # 调整图表位置，避免与GUI窗口重叠
        fig = plt.gcf()
        fig.canvas.manager.window.wm_geometry("+800+100")

        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = GDPGraphApp(root)
    root.mainloop()
