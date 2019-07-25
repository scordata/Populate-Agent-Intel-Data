import bs4 as bs
import urllib.request
import re


def get_bugs():
    bugs_url = "https://bz.apache.org/bugzilla/buglist.cgi?quicksearch=error"
    source = urllib.request.urlopen(bugs_url).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    bugs = soup.find_all('td', class_='bz_short_desc_column')
    bug_descriptions = []
    for bug in bugs:
        # Gross regex because I don't know how beautifulsoup works
        match_object = re.match(r"\[<a href=\"show_bug.cgi\?id=.*\">(.*).*</a>\]", str(bug.find_all('a')))
        bug_descriptions.append(match_object.group(1).strip())

    return bug_descriptions
