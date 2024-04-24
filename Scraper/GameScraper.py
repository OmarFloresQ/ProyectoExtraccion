from sys import exit as sys_exit
from fake_useragent import UserAgent
from time import sleep
from bs4 import BeautifulSoup as bs
import html5lib
from selenium import webdriver
from pandas import DataFrame
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from requests import get, Session
from os import environ
from os.path import join as join_path
def debug(t):print(t);input("<press enter>")
class LittleGamingGeek:
    # gamestop https://www.gamestop.com/video-games
    # pricegrabber https://www.pricegrabber.com/videogames1/browse/
    # steam https://store.steampowered.com/search/?filter=topsellers&os=win
    gaming_information_web_sites = {"metacritic":{"main_url":"https://www.metacritic.com", "filtered":False}, "gamespot":{"main_url":"https://www.gamespot.com", "filtered":False}, "ign":{"main_url":"https://www.ign.com", "filtered":False}}
    s = Session()
    useragent = UserAgent()
    s.headers.update({"User-Agent":useragent.random})
    data = {
        "gamename": [],
        "releasedate": [],
        "rating": []
    }
    #proxy_url = "http://127.0.0.1:8080" # burptest
    #s.verify = False
    #, proxies={"http":LittleGamingGeek.proxy_url, "https":LittleGamingGeek.proxy_url}
    def __init__(self):

        def mark_filtered(web_name):
            LittleGamingGeek.gaming_information_web_sites[web_name]["filtered"] = True
        for web_name, web_info in LittleGamingGeek.gaming_information_web_sites.copy().items():
            for field, value in web_info.items():
                if field == "main_url":
                    try:
                        r = LittleGamingGeek.s.get(value)
                    except:
                        mark_filtered(web_name=web_name)
                    else:
                        if r.status_code == 404 or r.status_code == 403 : mark_filtered(web_name=web_name)
                    finally:
                        if r : r.close()
        validation = [i["filtered"] for i in LittleGamingGeek.gaming_information_web_sites.copy().values()]
        if all(validation):
            print("All the web pages are filtered")
            sys_exit(1)
        else:
            print(f"Available {validation.count(False)} of {len(validation)}")
            for available, info in LittleGamingGeek.gaming_information_web_sites.copy().items():
                if not info["filtered"] : print(available, info["main_url"])
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument(f"--useragent={self.useragent.random}")
            self.browser = webdriver.Chrome(options=options)
            del validation

    def scrap(self, limit=10):
        scrap_url = "https://www.metacritic.com/browse/game"
        scrap_url = f"{scrap_url}/?releaseYearMin={self.filterDate[0]}&releaseMaxYear={self.filterDate[1]}"
        for platform, filter in self.filters.items():
            if filter["selected"] == True:
                scrap_url += filter["added_url"]
        self.browser.get(scrap_url + "&page=1")
        try:
            pageLimits = bs(self.browser.page_source, "html5lib").find_all("span", {"class":"c-navigationPagination_itemButtonContent u-flexbox u-flexbox-alignCenter u-flexbox-justifyCenter"})
        except:
            print("No results found for this filter combination")
        else:
            max_found = 0
            for page_number in pageLimits:
                try:
                    testing = page_number.get_text().strip()
                    testing = int(testing)
                except:
                    continue
                else:
                    max_found = testing if testing > max_found else max_found
            if max_found > 0:
                if not limit:
                    for i in range(0, max_found):
                        self.add_game(scrap_url + f"&page={i}")
                else:
                    if limit > max_found:
                        limit = pageLimit
                    for i in range(0, limit):
                        self.add_game(scrap_url + f"&page={i}")
            else:
                print("No results...")

    def add_game(self, url):
        self.browser.get(url)
        productBlockInformation = bs(self.browser.page_source, "html.parser").find_all("div", {
            "class": "c-finderProductCard c-finderProductCard-game"})

        for productInfo in productBlockInformation:
            game_name_span = productInfo.find("div", {"class": "c-finderProductCard_title"}).find_all("span")[1]
            game_name = game_name_span.get_text(strip=True) if game_name_span else "N/A"
            game_date_span = productInfo.find("div", {"class":"c-finderProductCard_meta"}).find_all("span")[0]
            game_date = game_date_span.get_text(strip=True) if game_name_span else "N/A"
            game_rating_span = productInfo.find("span", {"class":"c-finderProductCard_metaItem c-finderProductCard_score"}).find_all("span")[0]
            game_rating = game_rating_span.get_text(strip=True) if game_name_span else "N/A"
            #debug(game_rating)
            self.data["gamename"].append(game_name)
            self.data["releasedate"].append(game_date)
            self.data["rating"].append(game_rating)
        self.saveDate()

    def getPageFilters(self):
        # metacritic filter example url ---> https://www.metacritic.com/browse/game/?releaseYearMin=1997&releaseYearMax=2024&platform=xbox-series-x&platform=nintendo-switch&platform=meta-quest&platform=gamecube&genre=beat---%27em---up&genre=board-or-card-game&genre=first---person-shooter&genre=exercise-or-fitness&genre=open---world&genre=fighting&genre=real---time-strategy&genre=third---person-shooter&genre=party-or-minigame&genre=trivia-or-game-show&genre=turn---based-strategy&genre=shooter&page=1
        # https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2017&platform=ps5&platform=xbox-series-x&platform=nintendo-switch&platform=pc&page=1
        # https://www.metacritic.com/browse/game/all/adventure/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2017&platform=ps5&platform=xbox-series-x&platform=nintendo-switch&platform=pc&genre=adventure&page=1
        # https://www.metacritic.com/browse/game/xbox-one/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2024&platform=xbox-one&page=1
        # https://www.metacritic.com/browse/game/ps5/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2017&platform=ps5&page=1
        # LittleGamingGeek.s.get()
        self.browser.get("https://metacritic.com/browse/game/")
        filterDate = bs(self.browser.page_source, "html5lib").find("input", {"name":"releaseYearMin"})
        self.filterDate = (filterDate["min"], filterDate["max"])
        all_filters = bs(self.browser.page_source, "html5lib").find_all("div", {"class":"c-filterInput u-grid"})
        self.filters = {}
        def format_text_filter(filters_names, filterTitle, prefix):
            for filter_value_name in filters_names:
                    valueName = filter_value_name.get_text()
                    # Printable text and url encode for filter -> Nintendo Switch / &pataform=nintento-switch
                    replacements = {
                        "'":"%27",
                        "-":"---",
                        " ":"-",
                        "/":"or"
                    }
                    #replace(*[(old, new) for old, new in replacements.items()]) to avoid replace().replace().raplace()
                    formated = valueName
                    for original, replacement in replacements.items():
                        formated = formated.replace(original, replacement).strip().lower()
                    print(f"Trying to add {prefix + formated} to {filterTitle} from {valueName}")
                    self.filters[filterTitle] = {"name":valueName, "added_url":prefix + formated, "selected":False}

        for filter in all_filters:
            filterTitle = bs(str(filter), "html5lib").find("h4").get_text().strip()
            self.filters[filterTitle] = {}
            filter_values = bs(str(filter), "html5lib").find_all("div", {"class":"c-filterInput_content_row u-flexbox"})
            if filterTitle.lower() == "platforms":
                format_text_filter(filter_values, filterTitle=filterTitle, prefix="&platform=")
            elif filterTitle.lower() == "genre":
                format_text_filter(filter_values, filterTitle=filterTitle, prefix="&genre=")
            elif filterTitle.lower() == "release type":
                format_text_filter(filter_values, filterTitle=filterTitle, prefix="&releaseType=")

        self.scrap()
    def saveDate(self):
        DataFrame(self.data).to_csv(join_path(environ["USERPROFILE"], "Desktop/scrap.test.csv"))
        # simulating no filter selected --> https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page=2
        # c-navigationPagination_itemButtonContent u-flexbox u-flexbox-alignCenter u-flexbox-justifyCenter filter for



            # c-filterInput_content_row u-flexbox
            # the c-filterInput_content u-grid

class BigFiveResponder:
    class Amazon:
        pass
    class GoogleShopping:
        pass



if __name__ == "__main__":
    gameinfo = LittleGamingGeek()
    gameinfo.getPageFilters()
