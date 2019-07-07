# coding: UTF-8
from urllib import request

from bs4 import BeautifulSoup

from scrap_app import ScrapApp


def scrapingAndSearchNew():
    res = []
    articles = __scraping()
    for article in articles:
        if True:  # 未登録データか？
            create(article)
            res << article


def __scraping():
    url = "https://www.fun.ac.jp/"

    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find("ul", attrs={"class", "uodateListUl"}).find_all("li")
    # import pdb; pdb.set_trace()

    # print headlines
    for headline in headlines:
        print(
                headline.find("span", attrs={"class", "date"}).string,
                headline.find("a", attrs={"class", "title"}).string,
                headline.find("a", attrs={"class", "title"})["href"],
        )


def create(article):
    # 登録処理
    print('comming soon...')


def formatToSlack(data):
    # todo
    print('comming soon...')


def tweet(msg):
    print('comming soon...')


if __name__ == "__main__":
    articles = scrapingAndSearchNew()


# TODO: lambdaで動く形に整形
# TODO: DynamoDBのデータを取得
# TODO: DynamoDBデータと比較して、差分があれば登録
# TODO: slackに渡すフォーマットに整形
# TODO: slackに渡す
