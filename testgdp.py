import requests
import matplotlib.pyplot as plt

class EconomicData:
    def __init__(self, country, start_year=1990, end_year=2022):
        self.country = country
        self.start_year = start_year
        self.end_year = end_year
        self.api_url = f'https://api.imf.org/v1/data/economic/indicator/{country}?start={start_year}&end={end_year}'

    def get_data(self, indicator):
        # 根据经济指标的名称从IMF获取数据
        url = f'{self.api_url}&indicator={indicator}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'data' not in data:
                print(f"No data found for {indicator}")
                return None
            # 提取年份和指标值
            return [(entry['year'], entry['value']) for entry in data['data'] if entry['value'] is not None]
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def plot_data(self):
        # 获取GDP数据、通货膨胀率和失业率数据
        gdp_data = self.get_data('NY.GDP.MKTP.CD')  # GDP
        inflation_data = self.get_data('FP.CPI.TOTL.ZG')  # 通货膨胀率
        unemployment_data = self.get_data('SL.UEM.TOTL.ZS')  # 失业率

        if gdp_data is None or inflation_data is None or unemployment_data is None:
            print("无法获取数据，无法绘制图表")
            return

        # 生成年份列表
        years = [year for year, _ in gdp_data]

        # 提取GDP值
        gdp_values = [gdp for _, gdp in gdp_data]
        inflation_values = [inflation for _, inflation in inflation_data]
        unemployment_values = [unemployment for _, unemployment in unemployment_data]

        # 创建图表
        plt.figure(figsize=(10, 6))

        # 绘制各个数据的折线
        plt.plot(years, gdp_values, label="GDP (USD)", color='b')
        plt.plot(years, inflation_values, label="Inflation (%)", color='g')
        plt.plot(years, unemployment_values, label="Unemployment Rate (%)", color='r')

        # 设置图表标题和标签
        plt.title(f'{self.country} Economic Indicators (1990-2022)', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value', fontsize=12)

        # 显示图例
        plt.legend()

        # 展示图表
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# 示例用法
economic_data = EconomicData("USA")
economic_data.plot_data()