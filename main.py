import requests
from bs4 import BeautifulSoup

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
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('td')]
            data.append([col if col else " " for col in cols])

        return data

    def print_course_details(self, course_data):
        for course in course_data[2:]:
            selection_rate = self.calculate_selection_rate(course)
            print(f"{course[11][0]} {course[6]} {course[7]} {course[14]}/{course[15]} 選課率: {selection_rate}%")


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
        for year in range(start_year, end_year):
            for semester in range(1,3):
                payload = self.generate_payload(year, semester)
                course_data = self.fetch_course_data(payload)
                print(f"{year} 學年度 第 {semester} 學期：")
                self.print_course_details(course_data)
                print()

    def close_session(self):
        self.session.close()

def main():
    URL = 'http://webap.nkust.edu.tw/nkust/ag_pro/ag202.jsp'
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    course_scraper = CourseScraper(URL, HEADERS)
    course_scraper.scrape_courses(108, 112)
    course_scraper.close_session()

if __name__ == "__main__":
    main()
