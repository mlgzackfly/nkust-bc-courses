import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 請根據您的系統安裝的中文字體進行修改

class CourseScraper:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.session = requests.session()

    def fetch_course_data(self, payload):
        response = self.session.post(url=self.url, headers=self.headers, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find_all('table')[1]
        rows = table.find_all('tr')

        data = []
        for row in rows[2:]:  # 從第三行開始抓取，以跳過標題和表頭
            cols = [ele.text.strip() for ele in row.find_all('td')]
            data.append([col if col else " " for col in cols])

        return data

    def calculate_selection_rate(self, course):
        selected_students = int(course[14])
        max_capacity = int(course[15])
        if max_capacity == 0:
            return 0
        else:
            selection_rate = (selected_students / max_capacity) * 100
            return round(selection_rate, 2)

    def generate_payload(self, year, semester):
        payload = {
            'yms_yms': f'{year}#{semester}',
            'cmp_area_id': 4,
            'dgr_id': 14,
            'unt_id': 'UV01',
            'clyear': 2,
            'reading': 'reading'
        }
        return payload

    def scrape_courses(self, start_year, end_year):
        all_course_data = []
        for year in range(start_year, end_year + 1):
            for semester in range(1, 3):
                payload = self.generate_payload(year, semester)
                course_data = self.fetch_course_data(payload)
                all_course_data.extend(course_data[2:])
        return all_course_data

    def close_session(self):
        self.session.close()

def plot_course_selection(course_data, course_type):
    course_names = [course[7] for course in course_data if course[11][0] == course_type]
    selected_students = [int(course[14]) for course in course_data if course[11][0] == course_type]
    max_capacity = [int(course[15]) for course in course_data if course[11][0] == course_type]

    plt.figure(figsize=(12, 6))
    sns.barplot(x=course_names, y=selected_students, color='b', alpha=0.5, label='選課人數')
    sns.barplot(x=course_names, y=max_capacity, color='r', alpha=0.5, label='人數上限')
    plt.xlabel('課程名稱')
    plt.ylabel('學生人數')
    plt.title(f'{course_type}修 課程選課情況')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    URL = 'http://webap.nkust.edu.tw/nkust/ag_pro/ag202.jsp'
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    course_scraper = CourseScraper(URL, HEADERS)
    course_data = course_scraper.scrape_courses(108, 113)
    course_scraper.close_session()

    plot_course_selection(course_data, '必')
    plot_course_selection(course_data, '選')

if __name__ == "__main__":
    main()
