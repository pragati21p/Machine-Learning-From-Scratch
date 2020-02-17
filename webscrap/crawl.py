from webscrap import wlog
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv

url_aj   = 'https://www.flipkart.com/furniture/~living-room-furniture-/pr?sid=wwe&otracker=nmenu_sub_Home%20%26%20Furniture_0_Living%20Room%20Furniture'
class NewsScraper:
    __url = ''
    __data = ''
    __wlog = None
    __soup = None

    url_aj = 'https://www.flipkart.com/furniture/~living-room-furniture-/pr?sid=wwe&otracker=nmenu_sub_Home%20%26%20Furniture_0_Living%20Room%20Furniture'
    filepath = 'html/aj.html'

    def __init__(self, url, wlog):
        self.__url = url
        self.__wlog = wlog

    def retrieve_webpage(self):
        try:
            html = urlopen(self.__url)
        except Exception as e:
            print(e)
            self.__wlog.report(str(e))
        else:
            self.__data = html.read()
            if len(self.__data) > 0:
                print("Retrieved successfully")

    def write_webpage_as_html(self, filepath=filepath, data=''):
        try:
            with open(filepath, 'wb') as fobj:
                if data:
                    fobj.write(data)
                else:
                    fobj.write(self.__data)
        except Exception as e:
            print(e)
            self.__wlog.report(str(e))

    def read_webpage_from_html(self, filepath=filepath):
        try:
            with open(filepath) as fobj:
                self.__data = fobj.read()
        except Exception as e:
            print(e)
            self.__wlog.report(str(e))

    def convert_data_to_bs4(self):
        self.__soup = BeautifulSoup(self.__data, "html.parser")

    def change_url(self, url):
        self.__url = url

    def print_data(self):
        print(self.__data)

    def parse_soup_to_simple_html(self):
        news_list = self.__soup.find_all('div', {"class": "_3liAhj"})  # a

        # print (news_list)Zhf2z-

        # print(csv)

        filename = "html/data.csv"
        csv_writer = csv.writer(open(filename, 'w'))

        csv_writer.writerow(['Heading', 'Link', 'Description', 'Price', 'Number of Reviews'])

        for tag in news_list:

            title = tag.findChild('a', {'class':'_2cLu-l'})
            link = 'www.flipkart.com' + title['href']
            heading = title.text
            nprice = tag.findChild('div', {'class':'_1vC4OE'}).text.strip()
            nprice = re.sub(r'[^a-zA-Z0-9.,]', '', nprice)
            desc = tag.findChild('div', {'class':'_1rcHFq'}).text
            nrev = tag.findChild('span', {'class':'_38sUEc'}).text
            nrev = re.sub(r'[^0-9]', '', nrev)

            csv_writer.writerow([heading,link,desc,nprice,nrev])


# Define log file location
wlog.set_custom_log_info('html/error.log')
'''
# Testing log file reporting
try:
    raise Exception
except Exception as e:
    wlog.report(str(e))
'''

news_scrap = NewsScraper(url_aj, wlog)
news_scrap.retrieve_webpage()
news_scrap.write_webpage_as_html()
news_scrap.read_webpage_from_html()
news_scrap.convert_data_to_bs4()
#news_scrap.print_beautiful_soup()
news_scrap.parse_soup_to_simple_html()