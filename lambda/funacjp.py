# coding: UTF-8

from urllib import request

from bs4 import BeautifulSoup

from models.scrap import Scrap

URL = "https://www.fun.ac.jp"


def lambda_handler(_event, _context):
    """
    スクレイピングをして、
    新しい記事をスラックに投稿する
    """
    print('start funacjp#execute.')
    latest = Scrap.get_latest(URL)
    articles = __scraping()
    # 最新データからチェックしていく
    articles.reverse()
    regist_list = []
    for article in articles:
        # 登録済みデータに来るまで登録対象とする
        if latest is not None and article['title'] == latest.text:
            break
        regist_list.append(article)

    # 古いデータから入れていく
    regist_list.reverse()
    for data in regist_list:
        __insert(data)
        __tweet(data)
    print('finish funacjp#execute.')
    return regist_list


def __scraping():
    """
    スクレイピングをする

    :return [
        {
            text: 記事タイトル
            date: 投稿日付
            href: リダイレクト先URL
        }, ...
    ]
    """
    html = request.urlopen(URL)
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find("ul", attrs={"class", "uodateListUl"}).find_all("li")

    res = []
    for headline in headlines:
        res.append({
            'date': headline.find("span", attrs={"class", "date"}).string,
            'title': headline.find("a", attrs={"class", "title"}).string,
            'href': headline.find("a", attrs={"class", "title"})["href"]
            })
    return res


def __insert(data):
    # 登録処理
    print("title:{}\nhref:{}\ndate:{}".format(
        data['title'],
        data['href'],
        data['date']
        ))
    record = Scrap(
        URL,
        text=data['title'],
        redirect_url=data['href'],
        released_at=data['date']
    )
    record.save()
    print("insert done.")
    return record


def __tweet(_data):
    """ 投稿する """
    print('comming soon...')


if __name__ == "__main__":
    lambda_handler(None, None)


# TODO: lambdaで動く形に整形
# TODO: slackに渡すフォーマットに整形
# TODO: slackに渡す
