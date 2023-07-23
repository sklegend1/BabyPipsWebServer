from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime
import pandas as pd

class BabyPipsCollector():
    MONTH_DICT = {
        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'MAY': 5,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12
    }

    def __init__(self, start_date=datetime.date.today(), end_date=datetime.date.today(), web_driver=webdriver):
        self.driver = web_driver
        self.raw_data = []
        self.start_date = start_date
        self.end_date = end_date
        self.start_week = start_date.isocalendar().week
        self.end_week = end_date.isocalendar().week
        self.is_today = (self.start_date == self.end_date == datetime.date.today)
        self.data_frame = None
        self.records_count = 0

    def get_week_page(self, driver, page_url):
        print(page_url)
        driver.get(page_url)
        driver.implicitly_wait(1)

        while True:
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button.WeekDayPicker-module__button___Qx5PG')
            for button in buttons:
                if button.text == "Week":
                    week_button = button
            active_button = driver.find_element(By.CSS_SELECTOR, 'button.WeekDayPicker-module__active___ciocu')
            print(active_button.text)
            if active_button.text == "Week":
                break
            elif active_button.text == "Day":
                try:
                    week_button.click()
                    print('Clicked')
                    break
                except:
                    print('Not clickable')
                    try:
                        ad = driver.find_element(By.CSS_SELECTOR, 'button.css-47sehv')
                        print(ad.text)
                        ad.click()
                        driver.implicitly_wait(1)
                        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.WeekDayPicker-module__button___Qx5PG')
                        for button in buttons:
                            if button.text == "Week":
                                week_button = button
                        print(week_button.text)
                        week_button.click()
                        print('Clicked')
                        break
                    except:
                        print('Not clickable again')
                        driver.close()
                        driver = self.driver.Chrome()
                        driver.get(page_url)
                        driver.implicitly_wait(1)

        return driver

    def data_to_dataframe(self, data_list):
        table = [data_list[i:i + 8] for i in range(0, len(data_list), 9)]
        self.records_count = len(table)
        table_df = pd.DataFrame(table, columns=['news_date', 'news_time',
                                               'currency', 'description',
                                               'impact', 'actual', 'forecast',
                                               'previous'])

        return table_df

    def collecting_babypips_data(self):
        print(self.start_date, self.end_date, self.start_week, self.end_week)
        year1 = self.start_date.year
        year2 = self.end_date.year
        for year in range(year1, year2 + 1):
            try:
                if year == year1:
                    first_week = self.start_week
                else:
                    first_week = 1

                if year == year2:
                    last_week = self.end_week
                else:
                    last_week = 52

                driver = self.driver.Chrome()

                if last_week < 53:
                    last_week += 1
                elif last_week > 53:
                    last_week = 53
                if self.is_today:
                    first_week = 0
                    last_week = 1

                for week in range(first_week, last_week):
                    if self.is_today:
                        url = 'https://www.babypips.com/economic-calendar'
                        driver = self.get_week_page(driver, url)
                    else:
                        week_number = f'0{week}' if week < 10 else str(week)
                        url = f'https://www.babypips.com/economic-calendar?week={year}-W{week_number}'
                        driver = self.get_week_page(driver, url)

                    text = driver.find_elements(By.CSS_SELECTOR, 'table')
                    for tab in text:
                        dates = []
                        htext = tab.find_elements(By.CSS_SELECTOR, 'thead')
                        for t in htext:
                            for d in t.find_elements(By.CSS_SELECTOR, 'div'):
                                dates.append(d.text)
                        for t in tab.find_elements(By.CSS_SELECTOR, 'tr'):
                            row_cells = []
                            for d in t.find_elements(By.CSS_SELECTOR, 'td'):
                                if len(row_cells) == 0:
                                    if d.text == '':
                                        break
                                    row_cells.append(datetime.date(year, self.MONTH_DICT[dates[0]], int(dates[1])))
                                row_cells.append(d.text)
                            if row_cells:
                                self.raw_data.extend(row_cells)
                driver.close()
            except:
                break
        self.data_frame = self.data_to_dataframe(self.raw_data)

        return self.data_frame.to_dict(orient="split", index=False)

    def save_data(self, file_address):
        if self.data_frame is not None:
            self.data_frame.to_json(f"{file_address}.json")
            self.data_frame.to_excel(f"{file_address}.xlsx")
            self.data_frame.to_csv(f"{file_address}.csv")


BPCollector = BabyPipsCollector()
