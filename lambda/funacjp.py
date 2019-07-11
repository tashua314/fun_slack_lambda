# coding: UTF-8

import datetime
import sys
from time import sleep
from urllib import request

from bs4 import BeautifulSoup

from lib.slack_custom import SlackCustom

from models.scrap import Scrap

URL = "https://www.fun.ac.jp/category/information/"
MAX_COUNT = 2  # 一回あたりに投稿できる最大数


def init(target_year, method=None):
    """
    DBの初期化
    params:
        method: 処理対象となるデータの範囲を決める
            None: target_yearの年のみ
            upper: target_year年度分までの過去分全て
        target_year: 指定の年
    """
    articles = __scraping()
    # 古い順に入れる
    articles.reverse()
    for data in articles:
        start_date = datetime.datetime(target_year, 1, 1)
        end_date = datetime.datetime(target_year + 1, 1, 1)
        target_date = datetime.datetime.strptime(data['date'], '%Y.%m.%d')
        if method == 'upper' and target_date < end_date:
            # 対象年度分までの過去分全てを登録
            __insert(data)
        elif start_date <= target_date and target_date < end_date:
            # 対象年度分のみ登録
            __insert(data)

    print('{}件登録しました。'.format(len(articles)))
    print('<<<<< finish funacjp#init.')


def lambda_handler(_event, _context):
    """
    スクレイピングをして、
    新しい記事をスラックに投稿する
    """
    print('>>>>> start funacjp#execute. URL: {}'.format(URL))
    articles = __scraping()
    regist_list = __make_regist_list(articles)
    count = 1  # 投稿数カウンタ

    for data in regist_list:
        __insert(data)
        __tweet(data)
        count += 1
        if count > MAX_COUNT:
            break  # 一回あたり、MAX_COUNT分のみ投稿

    print('<<<<< finish funacjp#execute.')
    return regist_list


def __make_regist_list(articles):
    """ 登録用データを生成 """
    latest = Scrap.get_latest(URL)
    # 最新データからチェックしていく
    regist_list = []
    for article in articles:
        # 登録済みデータに来るまで登録対象とする
        if latest is not None and article['title'] == latest.text:
            break
        regist_list.append(article)

    print(
        "articles count is {}, regist list count is {}, max regist count is {}".format(
            len(articles), len(regist_list), MAX_COUNT
        )
    )
    # 古い順に入れる
    regist_list.reverse()
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
    """ 登録処理 """
    print(
        "title: {}\nhref : {}\ndate : {}".format(
            data['title'], data['href'], data['date']
        )
    )
    record = Scrap(
        URL,
        text=data['title'],
        redirect_url=data['href'],
        released_at=data['date']
    )
    record.save()
    print("id: {}, unit_id: {}".format(record.id, record.unit_id))
    print("----- insert done.")
    sleep(0.2)  # lambdaには単位時間あたりの最大処理件数があるため、sleep
    return record


def __tweet(data):
    """ 投稿する """
    msg = "<:fun: {}|[{}] {}>".format(
        data['href'], data['date'], data['title']
    )
    response = SlackCustom().post(msg, '<!here>')
    print(response)
    print('----- SlackCustom#post done.')


if __name__ == "__main__":
    """
    実行例)
    'python funacjp init 2018': 2018年度分のみ登録
    'python funacjp init_set_upper 2018': 2018年度分まで登録
    'python funacjp': 最新の未登録分を所定の数(MAX_COUT)だけ登録
    """
    ARGS = sys.argv
    if len(ARGS) > 1 and ARGS[1] == 'init':
        if len(ARGS) > 2:
            try:
                TARGET_YEAR = int(ARGS[2])
                init(TARGET_YEAR)
            except ValueError:
                print('対象年度を入力してください。')
        else:
            print('対象年度を入力してください。')
        sys.exit()
    elif len(ARGS) > 1 and ARGS[1] == 'init_set_upper':
        if len(ARGS) > 2:
            try:
                TARGET_YEAR = int(ARGS[2])
                init(TARGET_YEAR, method='upper')
            except ValueError:
                print('対象年度を入力してください。')
        else:
            print('対象年度を入力してください。')
        sys.exit()

    lambda_handler(None, None)
