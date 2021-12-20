import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"http://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  resul = requests.get(URL)
  soup = BeautifulSoup(resul.text, "html.parser")
  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []
  for link in links[0:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(result):
  title = result.select_one('.jobTitle>span').string
  company = result.find("span", {"class": "companyName"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company = str(company_anchor.string)
  else:
    company = str((company.string))
  company = company.strip()
  location = result.find("div", {"class": "companyLocation"}).string
  job_id = result.parent["data-jk"]
  return {'title': title, 'company': company, 'location': location, 'link': f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_pages):
  jobs = []
  for page in range(last_pages):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "slider_container"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs