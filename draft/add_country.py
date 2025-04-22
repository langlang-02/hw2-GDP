import requests
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from gdp_data import GDPData


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
        # self.show_button = tk.Button(self, text="Show GDP Chart", command=self.plot_data)
        # self.show_button.pack(pady=10)

        self.root = tk.Tk()
    #     self.create_widgets()   #创建滑块和标签

    # def create_widgets(self):
    #     
        # 设置初始时间段
        self.start_year = 1990
        self.end_year = 2022

        # 显示选择年份的标签
        self.label = tk.Label(self.root, text="请选择显示的年份范围")
        self.label.pack(pady=10)
        
        # 创建滑块来选择开始年份
        self.start_year_slider = tk.Scale(self.root, from_=1990, to=2022, orient=tk.HORIZONTAL, label="开始年份", command=self.plot_data)
        self.start_year_slider.set(self.start_year)
        self.start_year_slider.pack(pady=5)
        
        # 创建滑块来选择结束年份
        self.end_year_slider = tk.Scale(self.root, from_=1990, to=2022, orient=tk.HORIZONTAL, label="结束年份", command=self.plot_data)
        self.end_year_slider.set(self.end_year)
        self.end_year_slider.pack(pady=5)

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
                    self.plot_data()
                else:
                    print(f"No GDP data found for {country_name}")
            except Exception as e:
                print(f"Error fetching data for {country_name}: {e}")
        else:
            print("Please enter a country name.")

    def plot_data(self):
        self.start_year = self.start_year_slider.get()
        self.end_year = self.end_year_slider.get()

        if not self.economic_data_list:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        
        for country_name, gdp_data in self.economic_data_list:
            years = [year for year, _ in gdp_data]
            gdp_values = [gdp for _, gdp in gdp_data]
            # plt.cla()
            plt.plot(years, gdp_values, label=country_name)

        plt.title('GDP Over Time for Selected Countries', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('GDP (USD)', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 过滤数据，确保年份是整数类型并且在选择的范围内
        # filtered_data = [(int(year), gdp) for year, gdp in self.data if self.start_year <= int(year) <= self.end_year]

        # if filtered_data:
        #     years = [year for year, gdp in filtered_data]
        #     gdp_values = [gdp for year, gdp in filtered_data]
            
        #     # 清除当前图表
        #     plt.clf()
            
        #     # 绘制新的图表
        #     plt.plot(years, gdp_values, marker='o', color='b', label=f'{self.country} GDP')
        #     plt.title(f'{self.country} GDP from {self.start_year} to {self.end_year}')
        #     plt.xlabel('Year')
        #     plt.ylabel('GDP (in USD)')
        #     plt.xticks(rotation=45)
        #     plt.grid(True)
        #     plt.tight_layout()
        #     plt.legend()
        #     plt.show()
        # else:
        #     print("没有符合选择年份范围的数据。")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
