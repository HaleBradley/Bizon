from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def find_data():
    find_programs()

def find_programs():
    link = 'https://catalog.ndsu.edu/course-catalog/descriptions/'
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    programs = soup.find_all('a', class_='sitemaplink')
    num_of_programs = len(programs)

    current_date = datetime.now().date()
    with open(f'data/programs/data_{current_date}.txt', 'w') as f:
        for index, program in enumerate(programs):
            program_name = program.text.split('(', 1)[0].strip()
            program_abbr = program.text.split('(', 1)[1].strip()[:-1]
            program_link = link[:-1] + '/' + program.get('href').split('/', 3)[3]
            find_courses(program_name, program_abbr, program_link)

            f.write(f'{program_name}\n')
            f.write(f'{program_abbr}\n')
            f.write(f'{program_link}\n')
            if index != (num_of_programs - 1):
                f.write('\n')

def find_courses(name, abbr, link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    courses = soup.find_all('div', class_='courseblock')
    num_of_courses = len(courses)

    current_date = datetime.now().date()
    with open(f'data/courses/{abbr}_{current_date}.txt', 'w') as f:
        for index, course in enumerate(courses):
            course_title_html = course.find('p', class_='courseblocktitle').text
            course_num = course_title_html.split('.', 1)[0][-3:].strip()
            course_title = course_title_html.split('.', 2)[1].strip()
            course_credits = course_title_html.split('.', 2)[2][:-1].split('C', 1)[0].strip()
            course_description = course.find('p', class_='courseblockdesc').text.strip()
            if course_description == '':
                course_description = 'undefinded'

            f.write(f'{course_num}\n')
            f.write(f'{course_title}\n')
            f.write(f'{course_credits}\n')
            f.write(f'{course_description}\n')
            if index != (num_of_courses - 1):
                f.write('\n') 
#TODO
def find_available_courses(abbr, num):
    link = os.environ.get('CAMPUS_CONNECTION_SEARCH_LINK')
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
            

if __name__ == '__main__':
    find_data()
        