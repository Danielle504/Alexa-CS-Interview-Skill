from bs4 import BeautifulSoup
import requests
import os

top_domain = r'https://www.codeforces.com'
problems_link = r'http://codeforces.com/problemset?order=BY_SOLVED_DESC'
link = r'http://codeforces.com/problemset/problem/4/A'

def scrape_problem(url: str):
    with requests.get(url) as page:
        soup = BeautifulSoup(page.content, 'html.parser')
        problem_div = soup.find('div', class_='problem-statement')
        sub_div = problem_div.find_all('div', recursive=False)
        problem_info_div = sub_div[1]

        return problem_info_div.text


def scrape_problems(url: str, top_domain: str):
    problem_links=[]
    with requests.get(url) as page:
        soup = BeautifulSoup(page.content, 'html.parser')
        for a in soup.find_all("a"):
            href = a.get('href')
            if href and href.startswith("/problemset/problem") and href not in problem_links:
                problem_links.append(href)

        for href in problem_links:
            with open(f'{href.replace("/", "-")}.txt', "w") as ofp:
                print(f"{href.replace('/', '-')}")
                print(scrape_problem(top_domain+href), file=ofp)

def main():
    if not os.path.isdir("problems"):
        os.makedirs("problems")
    os.chdir("problems")
    print(scrape_problems(problems_link, top_domain))


if __name__ == '__main__':
    main()
