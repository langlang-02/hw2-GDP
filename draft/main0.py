import matplotlib.pyplot as plt
from gdp_data import GDPData
import tkinter as tk
from tkinter import ttk

class GDPGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP 时间段选择")
        
        self.country = 'USA'  # 默认国家
        self.gdp_data = GDPData(self.country)
        self.data = self.gdp_data.get_gdp_data()
        
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
        
        # 创建一个绘制图表的按钮
        self.plot_button = tk.Button(self.root, text="更新图表", command=self.update_plot)
        self.plot_button.pack(pady=20)

    
    def update_plot(self, event=None):
        self.start_year = self.start_year_slider.get()
        self.end_year = self.end_year_slider.get()

        # 过滤数据，确保年份是整数类型并且在选择的范围内
        filtered_data = [(int(year), gdp) for year, gdp in self.data if self.start_year <= int(year) <= self.end_year]

        if filtered_data:
            years = [year for year, gdp in filtered_data]
            gdp_values = [gdp for year, gdp in filtered_data]
            
            # 清除当前图表
            plt.clf()
            
            # 绘制新的图表
            plt.plot(years, gdp_values, marker='o', color='b', label=f'{self.country} GDP')
            plt.title(f'{self.country} GDP from {self.start_year} to {self.end_year}')
            plt.xlabel('Year')
            plt.ylabel('GDP (in USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.legend()
            plt.show()
        else:
            print("没有符合选择年份范围的数据。")

if __name__ == "__main__":
    root = tk.Tk()
    app = GDPGraphApp(root)
    root.mainloop()
