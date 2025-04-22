import matplotlib.pyplot as plt
from gdp_data import GDPData
import tkinter as tk
from tkinter import simpledialog

class GDPGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP 时间段选择")

        # 默认国家列表，初始时只有一个国家
        self.countries = ['USA']
        self.gdp_data = {country: GDPData(country) for country in self.countries}
        self.data = {country: self.gdp_data[country].get_gdp_data() for country in self.countries}

        # 设置初始时间段
        self.start_year = 1990
        self.end_year = 2022

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

        #创建标签 （提示作用）
        self.label = tk.Label(self.root, text="Enter country name:")
        self.label.pack(pady=10)
        
        #创建输入框
        self.country_entry = tk.Entry(self.root)
        self.country_entry.pack(pady=10)

    def add_country(self):
        # 弹出输入框，获取用户输入的国家名称
        # country_name = simpledialog.askstring("输入国家", "请输入国家名称：")
        
        #不使用弹出输入框，直接从Entry获取国家名称
        country_name = self.country_entry.get().strip()
        # if country_name:
        #     try:
        #         # Fetch GDP data for the entered country
        #         economic_data = GDPData(country_name)
        #         gdp_data = economic_data.get_gdp_data()

        #         if gdp_data is not None:
        #             self.economic_data_list.append((country_name, gdp_data))
        #             print(f"Added GDP data for {country_name}")
        #             self.plot_data()
        #         else:
        #             print(f"No GDP data found for {country_name}")
        #     except Exception as e:
        #         print(f"Error fetching data for {country_name}: {e}")
        # else:
        #     print("Please enter a country name.")



        if country_name and country_name not in self.countries:
            # 如果输入的国家有效并且不在已有国家列表中
            self.countries.append(country_name)
            self.gdp_data[country_name] = GDPData(country_name)
            self.data[country_name] = self.gdp_data[country_name].get_gdp_data()

            # 更新图表
            self.update_plot()

    def update_plot(self, event=None):
        # 获取当前滑动条选择的年份
        self.start_year = self.start_year_slider.get()
        self.end_year = self.end_year_slider.get()

        # 清除当前图表
        plt.clf()

        # 对所有国家的数据进行过滤并绘图
        for country in self.countries:
            filtered_data = [(int(year), gdp) for year, gdp in self.data[country] if self.start_year <= int(year) <= self.end_year]
            
            if filtered_data:
                years = [year for year, gdp in filtered_data]
                gdp_values = [gdp for year, gdp in filtered_data]
                
                # 绘制国家的GDP图表
                plt.plot(years, gdp_values, marker='o', label=f'{country} GDP')

        # 设置图表标题与标签
        plt.title(f'GDP from {self.start_year} to {self.end_year}')
        plt.xlabel('Year')
        plt.ylabel('GDP (in USD)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()

        # 显示图表
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = GDPGraphApp(root)
    root.mainloop()
