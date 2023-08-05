from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime


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

            f.write(f'{program_name}\n')
            f.write(f'{program_abbr}\n')
            f.write(f'{program_link}\n')
            if index != (num_of_programs - 1):
                f.write('\n')

if __name__ == '__main__':
    find_programs()
        