import urllib3
from bs4 import BeautifulSoup


class resume:
    def __init__(self, title, specialization, salary, age, employment, work_schedule, experience_years,
                 experience_month, citizenship, sex):
        self.title = title
        self.specialization = specialization
        self.salary = salary
        self.age = age
        self.employment = employment
        self.work_schedule = work_schedule
        self.experience_years = experience_years
        self.experience_month = experience_month
        self.citizenship = citizenship
        self.sex = sex

    def __repr__(self):
        return f"Title: {self.title}\n\
               Specialization: {self.specialization}\n\
               Age: {self.age}\n\
               Gender: {self.sex}\n\
               Citizenship: {self.citizenship}\n\
               Salary: {self.salary}\n\
               Employment: {self.employment}\n\
               Work Schedule: {self.work_schedule}\n\
               Experience Years: {self.experience_years} \n\
               Experience Months: {self.experience_month} \n"


def get_max_page(http, search_text):
    url = f"https://hh.kz/search/resume?text={search_text}&area=40&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&currency_code=KZT&ored_clusters=true&order_by=relevance"
    res = http.request('GET', url)
    soup = BeautifulSoup(res.data, "html.parser")
    pages = soup.find_all('a', attrs={'class': 'bloko-button'})[2:-1]
    max_page = 0
    for page in pages:
        max_page = max(int(page.text), max_page)
    return min(1, max_page)


def parse_resume(http, url):
    res = http.request('GET', url)
    soup = BeautifulSoup(res.data, "html.parser")


    resume_experience = soup.find('span',
                                  attrs={'class': 'resume-block__title-text resume-block__title-text_sub'}).find_all(
        'span')
    try:
        resume_title = soup.find('span', attrs={'class': 'resume-block__title-text'}).text
    except:
        resume_title = None

    try:
        resume_gender = soup.find('span', attrs={'data-qa': 'resume-personal-gender'}).text
    except:
        resume_gender = None

    try:
        resume_citizenship = soup.find('div', attrs={'data-qa': 'resume-block-additional'}).find('p').text
    except:
        resume_citizenship = None
    try:
        resume_experience_year = resume_experience[0].text
    except:
        resume_experience_year = None

    try:
        resume_experience_month = resume_experience[1].text
    except:
        resume_experience_month = None

    try:
        resume_work_schedule = soup.find('div', attrs={'class': 'resume-block-item-gap'}).find_all('p')[1].text
    except:
        resume_work_schedule = None

    try:
        resume_experiences = [i.text for i in
                              soup.find_all('div', attrs={'data-qa': 'resume-block-experience-position'})]
    except:
        resume_experiences = None

    try:
        resume_age = soup.find('span', attrs={'data-qa': 'resume-personal-age'}).text
    except:
        resume_age = None

    try:
        resume_salary = soup.find('span', attrs={'class': 'resume-block__salary'}).text
    except:
        resume_salary = None

    try:
        resume_specialization = [i.text for i in soup.find_all('li', attrs={'class': 'resume-block__specialization'})]
    except:
        resume_specialization = None

    # print(f"{resume_title} - {resume_specialization} - {resume_salary} - {resume_gender} - {resume_age} - {resume_work_schedule} - {resume_experience_year} - {resume_experience_month} - {resume_citizenship}")
    return resume(resume_title, resume_specialization, resume_salary, resume_age, resume_experiences,
                  resume_work_schedule, resume_experience_year, resume_experience_month, resume_citizenship,
                  resume_gender)


def parse_resumes(search_text):
    http = urllib3.PoolManager()
    resumes = []
    for i in range(0, get_max_page(http, search_text)):
        url = f"https://hh.kz/search/resume?text={search_text}&area=40&isDefaultArea=true&pos=full_text&logic=normal" \
              f"&exp_period=all_time&currency_code=KZT&ored_clusters=true&order_by=relevance&page={i}"
        res = http.request('GET', url)
        soup = BeautifulSoup(res.data, "html.parser")
        resume_links = soup.find_all('a', attrs={'class', 'serp-item__title'})
        for resume_link in resume_links:
            href = "https://hh.kz" + resume_link.get("href")
            # print(href)
            resumes.append(parse_resume(http, href))
    return resumes


if __name__ == "__main__":
    search_text = "java"
    http = urllib3.PoolManager()
    print("Loading...")
    resumes = parse_resumes(search_text)
    print("Done!")
    print(resumes)