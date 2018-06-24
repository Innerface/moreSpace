# Author: YuYuE (1019303381@qq.com) 2018.06.11
import DataBaseInitialization as data_handle
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse


def getPage(Q_No, url, data=None):
    page_question_No = 1 + Q_No
    wb_data = requests.get(url)
    wb_data.encoding = 'gbk'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    webdata = soup.select('a.ti')
    agrees = soup.select('span.f-black')
    print(agrees)

    if data is None:
        for title, url in zip(webdata, webdata):
            data = [
                title.get('title'),
                url.get('href')
            ]
            print('\n')
            print(page_question_No)

            page_question_No += 1

            print(title.get_text())
            print(url.get('href'))

            url_sub = url.get('href')
            wb_data_sub = requests.get(url_sub)
            wb_data_sub.encoding = 'gbk'
            soup_sub = BeautifulSoup(wb_data_sub.text, 'lxml')
            best_answer = soup_sub.find('pre', class_="best-text mb-10")

            if best_answer is not None:
                best = best_answer.get_text(strip=True)

                print("\n\nBest Answer Is: \n")
                print(best)
            else:
                print("\nNo Best Answer")
                better_answer = soup_sub.find_all('div', class_="answer-text line")

                if better_answer is not None:
                    for i_better, better_answer_sub in enumerate(better_answer):
                        better = better_answer_sub.get_text(strip=True)

                        print("\nNo.%d Answer" % (i_better + 1))
                        print(better)

                else:
                    print("Unanswered")


# 迭代页数
def getMorePage(url, start, end):
    for one in range(start, end, 10):
        getPage(one, url + str(one))
        time.sleep(2)


def getQAPairsWithKeywords(words):
    pages = 1
    url = "https://zhidao.baidu.com/search?word=" + urllib.parse.quote(words) + "&pn="
    getMorePage(url, 0, int(pages) * 10)


if __name__ == "__main__":
    keywords = '银行'
    getQAPairsWithKeywords(keywords)
