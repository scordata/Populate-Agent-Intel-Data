from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


def get_news(search_query):
    # Add + to make a valid google query
    google_query = search_query.replace(' ', '+')
    news_url = "https://news.google.com/rss/search?q=" + google_query + "&as_qdr=y2&hl=en-US&gl=US&ceid=US:en"
    client = urlopen(news_url)
    xml_page = client.read()
    client.close()
    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    headlines = []
    for news in news_list:
        headlines.append(news.title.text)

    return headlines

