from bs4 import BeautifulSoup
import schedule

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
import time

from random import seed
from random import randint

import os
from datetime import datetime

import shadow_useragent


import smtplib
import config
global subject
global msg



# setup process grab user agent profiles
ua = shadow_useragent.ShadowUserAgent()
ua = ua.firefox

# main class function
class ExpediaBot(object):
    # setup
    def __init__(self):
        self.googlenews_url = "https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en"



        PROXY = "172.102.219.35:21314"
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXY,
            'ftpProxy': PROXY,
            'sslProxy': PROXY
        })

        self.profile = webdriver.FirefoxProfile()
        # self.profile.set_preference("browser.privatebrowsing.autostart", True)
        self.profile.set_preference("general.useragent.override", ua)
        ## Disable CSS
        # self.profile.set_preference('permissions.default.stylesheet', 2)
        ## Disable images
        # self.profile.set_preference('permissions.default.image', 2)
        ## Disable JavaScript
        # self.profile.set_preference('javascript.enabled', False)
        ## Disable Flash
        # self.profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
        self.options = Options()

        self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                        firefox_options=self.options,
                                        proxy=proxy)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1920, 1080)
        # Obtain the source
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.html = self.soup.prettify('utf-8')

    # login step
    def login(self):
        seed(1)
        self.driver.get(self.googlenews_url)
        time.sleep(randint(10, 15))

        new_url = self.driver.current_url

    def searchLinks(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        names = []
        # urls=[]
        # links=[]

        # links =self.driver.find_elements_by_css_selector("a[href*='article']")
        # for i in range(5):
        #     ele = links[i]
        #     ele.click()


        # for d in soup.findAll('a', {'class': {'DY5T1d'}}):
            #name = d.find('h3', attrs={
                #'class': 'truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500'})
            #if name is not None:
                #n = name.text
            # names.append(d)
        for img in soup.select('a[href] img'):
            link = img.find_parent('a', href=True)
            if "articles" in str(link):
                names.append(link)
        return names



    # scroll down gradually
    def scrollDown(self):
        y = 1000
        for timer in range(0,15):
             self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
             y += 1000
             time.sleep(1)

    # helper function to extract only numbers from a string
    def get_num(self, x):
        if "\n" in x:
            s = x.split("\n",1)[1]
            return -1
        else:
            return int(''.join(ele for ele in x if ele.isdigit()))
    '''
    def clickInLink(self, text):
        for i in range(5):
            with open(text):
                self.driver.find_
    '''

    # search flights
    '''
    def search_flight(self, originString, destinationString, startDate, endDate):
        current_url = self.driver.current_url
        self.driver.get(self.expedia_url)
        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in flight search")

        if "wizard-hotel-pwa-v2" in new_url:
            return -1
        else:
            flight_button = self.driver.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
            flight_button.click()
            time.sleep(randint(5, 10))
            origin = self.driver.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
            origin.send_keys(originString)
            origin.send_keys(Keys.CONTROL + "a")
            origin.send_keys(Keys.DELETE)
            origin.send_keys(originString)
            time.sleep(randint(5, 10))
            destination = self.driver.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
            destination.send_keys(destinationString)
            destination.send_keys(Keys.CONTROL + "a")
            destination.send_keys(Keys.DELETE)
            destination.send_keys(destinationString)
            time.sleep(randint(5, 10))
            depart_date = self.driver.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
            depart_date.send_keys(startDate)
            depart_date.send_keys(Keys.CONTROL + "a")
            depart_date.send_keys(Keys.DELETE)
            depart_date.send_keys(startDate)
            time.sleep(randint(5, 10))
            end_date = self.driver.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
            end_date.send_keys(endDate)
            end_date.send_keys(Keys.CONTROL + "a")
            end_date.send_keys(Keys.DELETE)
            end_date.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("/html/body/meso-native-marquee/section/div/div/div[1]/section/div/div[2]/div[2]/section[1]/form/div[8]/label/button")
            search_button.click()
            time.sleep(randint(25, 35))
            self.scrollDown()

            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass

            return 1

    # search vacation rentals
    def search_rental(self, destinationString, startDate, endDate):
        current_url = self.driver.current_url
        self.driver.get(self.expedia_url)
        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in rental search")

        if "wizard-hotel-pwa-v2" in new_url:
            return -1
        else:
            rental_button = self.driver.find_element_by_xpath("//button[@id='tab-vacation-rental-tab-hp']")
            rental_button.click()
            time.sleep(randint(5, 10))
            destination = self.driver.find_element_by_xpath("//input[@id='hotel-destination-hp-vacationRental']")
            destination.send_keys(destinationString)
            destination.send_keys(Keys.CONTROL + "a")
            destination.send_keys(Keys.DELETE)
            destination.send_keys(destinationString)
            time.sleep(randint(5, 10))
            start_date = self.driver.find_element_by_xpath("//input[@id='hotel-checkin-hp-vacationRental']")
            start_date.send_keys(startDate)
            start_date.send_keys(Keys.CONTROL + "a")
            start_date.send_keys(Keys.DELETE)
            start_date.send_keys(startDate)
            time.sleep(randint(5, 10))
            end_date = self.driver.find_element_by_xpath("//input[@id='hotel-checkout-hp-vacationRental']")
            end_date.send_keys(endDate)
            end_date.send_keys(Keys.CONTROL + "a")
            end_date.send_keys(Keys.DELETE)
            end_date.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("//*[@id='gcw-hotel-form-hp-vacationRental']/div[6]/label/button")
            search_button.click()
            time.sleep(randint(25, 35))
            self.scrollDown()

            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass

            return 1

    # search things to do
    def search_to_do(self, destinationString, startDate, endDate):
        current_url = self.driver.current_url
        self.driver.get(self.expedia_url)
        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in todo search")

        if "wizard-hotel-pwa-v2" in new_url:
            return -1
        else:
            to_do_button = self.driver.find_element_by_xpath("//button[@id='tab-activity-tab-hp']")
            to_do_button.click()
            time.sleep(randint(5, 10))
            destination = self.driver.find_element_by_xpath("//input[@id='activity-destination-hp-activity']")
            destination.send_keys(destinationString)
            destination.send_keys(Keys.CONTROL + "a")
            destination.send_keys(Keys.DELETE)
            destination.send_keys(destinationString)
            time.sleep(randint(5, 10))
            start_date = self.driver.find_element_by_xpath("//input[@id='activity-start-hp-activity']")
            start_date.send_keys(startDate)
            start_date.send_keys(Keys.CONTROL + "a")
            start_date.send_keys(Keys.DELETE)
            start_date.send_keys(startDate)
            time.sleep(randint(5, 10))
            end_date = self.driver.find_element_by_xpath("//input[@id='activity-end-hp-activity']")
            end_date.send_keys(endDate)
            end_date.send_keys(Keys.CONTROL + "a")
            end_date.send_keys(Keys.DELETE)
            end_date.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("//*[@id='gcw-activities-form-hp-activity']/div[11]/label/button")
            search_button.click()
            time.sleep(randint(25, 35))
            self.scrollDown()

            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass

            return 1

    # search bundles
    def search_bundles(self, originString, destinationString, startDate, endDate):
        current_url = self.driver.current_url
        self.driver.get(self.expedia_url)
        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in bundle search")

        if "wizard-hotel-pwa-v2" in new_url:
            return -1
        else:
            bundle_button = self.driver.find_element_by_xpath("//button[@id='tab-package-tab-hp']")
            bundle_button.click()
            time.sleep(randint(5, 10))
            origin = self.driver.find_element_by_xpath("//input[@id='package-origin-hp-package']")
            origin.send_keys(originString)
            origin.send_keys(Keys.CONTROL + "a")
            origin.send_keys(Keys.DELETE)
            origin.send_keys(originString)
            destination = self.driver.find_element_by_xpath("//input[@id='package-destination-hp-package']")
            destination.send_keys(destinationString)
            destination.send_keys(Keys.CONTROL + "a")
            destination.send_keys(Keys.DELETE)
            destination.send_keys(destinationString)
            time.sleep(randint(5, 10))
            start_date = self.driver.find_element_by_xpath("//input[@id='package-departing-hp-package']")
            start_date.send_keys(startDate)
            start_date.send_keys(Keys.CONTROL + "a")
            start_date.send_keys(Keys.DELETE)
            start_date.send_keys(startDate)
            time.sleep(randint(5, 10))
            end_date = self.driver.find_element_by_xpath("//input[@id='package-returning-hp-package']")
            end_date.send_keys(endDate)
            end_date.send_keys(Keys.CONTROL + "a")
            end_date.send_keys(Keys.DELETE)
            end_date.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("//button[@id='search-button-hp-package']")
            search_button.click()
            time.sleep(randint(25, 35))
            self.scrollDown()

            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass

            return 1

    # search deals in hotel
    def search_deals(self, destinationString, startDate, endDate):
        current_url = self.driver.current_url
        self.driver.get(self.expedia_url)
        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in deal search")

        if "wizard-hotel-pwa-v2" in new_url:
            return -1
        else:
            self.scrollDown()
            deal_link = self.driver.find_element_by_xpath("//a[@id='primary-header-deals']")
            deal_link.click()
            time.sleep(randint(5, 10))
            destination = self.driver.find_element_by_xpath("//input[@id='H-destination']")
            destination.send_keys(destinationString)
            destination.send_keys(Keys.CONTROL + "a")
            destination.send_keys(Keys.DELETE)
            destination.send_keys(destinationString)
            time.sleep(randint(5, 10))
            start_date = self.driver.find_element_by_xpath("//input[@id='H-fromDate']")
            start_date.send_keys(startDate)
            start_date.send_keys(Keys.CONTROL + "a")
            start_date.send_keys(Keys.DELETE)
            start_date.send_keys(startDate)
            time.sleep(randint(5, 10))
            end_date = self.driver.find_element_by_xpath("//input[@id='H-toDate']")
            end_date.send_keys(endDate)
            end_date.send_keys(Keys.CONTROL + "a")
            end_date.send_keys(Keys.DELETE)
            end_date.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("//button[@id='H-searchButtonExt1']")
            search_button.click()
            time.sleep(randint(25, 35))
            self.scrollDown()

            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass

            return 1

    # search hotels, optional parameter
    def search_hotels(self, destination, startDate, endDate, num = -1, stars = -1, guestRating = -1, sortCriteria = "NO"):
        current_url = self.driver.current_url
        names = []
        urls = []
        prices = []
        lowest = 0
        highest = 0
        hi = 0
        li = 0

        self.driver.get(self.expedia_url)

        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in hotel search")

        if "wizard-hotel-pwa-v2" in new_url:
            return [], [], [], 0, 0
        else:
            print("waiting to check annoying random survey popup")
            time.sleep(10)
            try:
                survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                print("found survey")
                while len(survey_popup) > 0:
                    time.sleep(randint(3,5))
                    self.driver.refresh()
                    survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                pass
            except NoSuchElementException:
                pass

            print(f"Searching for hotels in {destination} from {startDate} to {endDate} with 2 travellers...")
            hotel_button = self.driver.find_element_by_xpath("//button[@id='tab-hotel-tab-hp']")
            hotel_button.click()
            time.sleep(randint(5, 10))

            destination_input = self.driver.find_element_by_xpath("//input[@id='hotel-destination-hp-hotel']")
            destination_input.send_keys(destination)
            destination_input.send_keys(Keys.CONTROL + "a");
            destination_input.send_keys(Keys.DELETE);
            destination_input.send_keys(destination)
            time.sleep(randint(5, 10))
            check_in = self.driver.find_element_by_xpath("//input[@id='hotel-checkin-hp-hotel']")
            check_in.send_keys(startDate)
            check_in.send_keys(Keys.CONTROL + "a");
            check_in.send_keys(Keys.DELETE);
            check_in.send_keys(startDate)
            time.sleep(randint(5, 10))
            check_out = self.driver.find_element_by_xpath("//input[@id='hotel-checkout-hp-hotel']")
            check_out.send_keys(endDate)
            check_out.send_keys(Keys.CONTROL + "a");
            check_out.send_keys(Keys.DELETE);
            check_out.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("/html/body/meso-native-marquee/section/div/div/div[1]/section/div/div[2]/div[2]/section[2]/form/div[13]/label/button")
            ActionChains(self.driver).move_to_element(search_button).click(search_button).perform()

            WebDriverWait(self.driver, 15).until(EC.url_changes(new_url))
            new_url2 = self.driver.current_url
            time.sleep(randint(10, 20))
            self.scrollDown()
            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass


            if num != -1:
                self.choose_budget(num)
                print("changing price level to " + str(num))
                time.sleep(randint(5, 10))
            else:
                pass

            if stars != -1:
                self.choose_star_level(stars)
                print("changing star level to " + str(stars))
                time.sleep(randint(5, 10))

            if guestRating != -1:
                self.choose_guest_rating(guestRating)
                print("changing guest rating to " + str(guestRating))
                time.sleep(randint(5, 10))

            if sortCriteria != "NO":
                self.sort(sortCriteria)
                print("sorting by " + str(sortCriteria))
                time.sleep(randint(5, 10))

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            for d in soup.findAll('li', attrs={'class':'listing uitk-cell xl-cell-1-1 l-cell-1-1 m-cell-1-1 s-cell-1-1'}):
                name = d.find('h3', attrs={'class':'truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500'})
                if name is not None:
                    n = name.text
                    names.append(n)
                price_list = d.findAll('span', attrs={'class':'uitk-cell loyalty-display-price all-cell-shrink'})
                for p in price_list:
                    if p.text is not None:
                        if "Price" not in p.text:
                            price = p.text
                            prices.append(price)
                url = d.find('a', attrs={'class':'listing__link uitk-card-link'})
                if url is not None:
                    u = d.find('a', attrs={'class':'listing__link uitk-card-link'})['href']
                    new_url = self.expedia_url + u
                    urls.append(new_url)

            i = 0
            while i < len(prices):
                prices[i] = prices[i].replace("$", "")
                prices[i] = prices[i].replace(",", "")
                p = float(prices[i])
                if p >= highest:
                    highest = p
                    hi = i

                if p <= lowest:
                    lowest = p
                    li = i

                i = i + 1

            time.sleep(randint(5, 10))
            return names, prices, urls, hi, li

    # search hotels with random click, optional parameter
    def search_hotels_random(self, destination, startDate, endDate, num = -1, stars = -1, guestRating = -1, sortCriteria = "NO"):
        current_url = self.driver.current_url
        names = []
        urls = []
        prices = []
        lowest = 0
        highest = 0
        hi = 0
        li = 0

        self.driver.get(self.expedia_url)

        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in hotel search")

        if "wizard-hotel-pwa-v2" in new_url:
            return [], [], [], 0, 0
        else:
            print("waiting to check annoying random survey popup")
            time.sleep(10)
            try:
                survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                print("found survey")
                while len(survey_popup) > 0:
                    time.sleep(randint(3,5))
                    self.driver.refresh()
                    survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                pass
            except NoSuchElementException:
                pass

            print(f"Searching for hotels in {destination} from {startDate} to {endDate} with 2 travellers...")
            hotel_button = self.driver.find_element_by_xpath("//button[@id='tab-hotel-tab-hp']")
            hotel_button.click()
            time.sleep(randint(5, 10))

            destination_input = self.driver.find_element_by_xpath("//input[@id='hotel-destination-hp-hotel']")
            destination_input.send_keys(destination)
            destination_input.send_keys(Keys.CONTROL + "a");
            destination_input.send_keys(Keys.DELETE);
            destination_input.send_keys(destination)
            time.sleep(randint(5, 10))
            check_in = self.driver.find_element_by_xpath("//input[@id='hotel-checkin-hp-hotel']")
            check_in.send_keys(startDate)
            check_in.send_keys(Keys.CONTROL + "a");
            check_in.send_keys(Keys.DELETE);
            check_in.send_keys(startDate)
            time.sleep(randint(5, 10))
            check_out = self.driver.find_element_by_xpath("//input[@id='hotel-checkout-hp-hotel']")
            check_out.send_keys(endDate)
            check_out.send_keys(Keys.CONTROL + "a");
            check_out.send_keys(Keys.DELETE);
            check_out.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("/html/body/meso-native-marquee/section/div/div/div[1]/section/div/div[2]/div[2]/section[2]/form/div[13]/label/button")
            ActionChains(self.driver).move_to_element(search_button).click(search_button).perform()

            WebDriverWait(self.driver, 15).until(EC.url_changes(new_url))
            new_url2 = self.driver.current_url
            time.sleep(randint(10, 20))
            self.scrollDown()
            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass


            if num != -1:
                self.choose_budget(num)
                print("changing price level to " + str(num))
                time.sleep(randint(5, 10))
            else:
                pass

            if stars != -1:
                self.choose_star_level(stars)
                print("changing star level to " + str(stars))
                time.sleep(randint(5, 10))

            if guestRating != -1:
                self.choose_guest_rating(guestRating)
                print("changing guest rating to " + str(guestRating))
                time.sleep(randint(5, 10))

            if sortCriteria != "NO":
                self.sort(sortCriteria)
                print("sorting by " + str(sortCriteria))
                time.sleep(randint(5, 10))

            self.click_random()

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            for d in soup.findAll('li', attrs={'class':'listing uitk-cell xl-cell-1-1 l-cell-1-1 m-cell-1-1 s-cell-1-1'}):
                name = d.find('h3', attrs={'class':'truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500'})
                if name is not None:
                    n = name.text
                    names.append(n)
                price_list = d.findAll('span', attrs={'class':'uitk-cell loyalty-display-price all-cell-shrink'})
                for p in price_list:
                    if p.text is not None:
                        if "Price" not in p.text:
                            price = p.text
                            prices.append(price)
                url = d.find('a', attrs={'class':'listing__link uitk-card-link'})
                if url is not None:
                    u = d.find('a', attrs={'class':'listing__link uitk-card-link'})['href']
                    new_url = self.expedia_url + u
                    urls.append(new_url)

            i = 0
            while i < len(prices):
                prices[i] = prices[i].replace("$", "")
                prices[i] = prices[i].replace(",", "")
                p = float(prices[i])
                if p >= highest:
                    highest = p
                    hi = i

                if p <= lowest:
                    lowest = p
                    li = i

                i = i + 1

            time.sleep(randint(5, 10))
            return names, prices, urls, hi, li

    def search_hotels_click_low(self, destination, startDate, endDate, num = -1, stars = -1, guestRating = -1, sortCriteria = "NO"):
        current_url = self.driver.current_url
        names = []
        urls = []
        prices = []
        lowest = 0
        highest = 0
        hi = 0
        li = 0

        self.driver.get(self.expedia_url)

        WebDriverWait(self.driver, 20).until(EC.url_changes(current_url))
        new_url = self.driver.current_url

        print("checking ab testing in hotel search")

        if "wizard-hotel-pwa-v2" in new_url:
            return [], [], [], 0, 0
        else:
            print("waiting to check annoying random survey popup")
            time.sleep(10)
            try:
                survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                print("found survey")
                while len(survey_popup) > 0:
                    time.sleep(randint(3,5))
                    self.driver.refresh()
                    survey_popup = self.driver.find_elements_by_xpath("//div[contains(@class, 'QSIWebResponsiveDialog')]")
                pass
            except NoSuchElementException:
                pass

            print(f"Searching for hotels in {destination} from {startDate} to {endDate} with 2 travellers...")
            hotel_button = self.driver.find_element_by_xpath("//button[@id='tab-hotel-tab-hp']")
            hotel_button.click()
            time.sleep(randint(5, 10))

            destination_input = self.driver.find_element_by_xpath("//input[@id='hotel-destination-hp-hotel']")
            destination_input.send_keys(destination)
            destination_input.send_keys(Keys.CONTROL + "a");
            destination_input.send_keys(Keys.DELETE);
            destination_input.send_keys(destination)
            time.sleep(randint(5, 10))
            check_in = self.driver.find_element_by_xpath("//input[@id='hotel-checkin-hp-hotel']")
            check_in.send_keys(startDate)
            check_in.send_keys(Keys.CONTROL + "a");
            check_in.send_keys(Keys.DELETE);
            check_in.send_keys(startDate)
            time.sleep(randint(5, 10))
            check_out = self.driver.find_element_by_xpath("//input[@id='hotel-checkout-hp-hotel']")
            check_out.send_keys(endDate)
            check_out.send_keys(Keys.CONTROL + "a");
            check_out.send_keys(Keys.DELETE);
            check_out.send_keys(endDate)
            time.sleep(randint(5, 10))
            search_button = self.driver.find_element_by_xpath("/html/body/meso-native-marquee/section/div/div/div[1]/section/div/div[2]/div[2]/section[2]/form/div[13]/label/button")
            ActionChains(self.driver).move_to_element(search_button).click(search_button).perform()

            WebDriverWait(self.driver, 15).until(EC.url_changes(new_url))
            new_url2 = self.driver.current_url
            time.sleep(randint(10, 20))
            self.scrollDown()
            try:
                more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
                more_button.click()
                self.scrollDown()
            except:
                pass


            if num != -1:
                self.choose_budget(num)
                print("changing price level to " + str(num))
                time.sleep(randint(5, 10))
            else:
                pass

            if stars != -1:
                self.choose_star_level(stars)
                print("changing star level to " + str(stars))
                time.sleep(randint(5, 10))

            if guestRating != -1:
                self.choose_guest_rating(guestRating)
                print("changing guest rating to " + str(guestRating))
                time.sleep(randint(5, 10))

            if sortCriteria != "NO":
                self.sort(sortCriteria)
                print("sorting by " + str(sortCriteria))
                time.sleep(randint(5, 10))

            plist = self.driver.find_elements_by_xpath("//span[contains(@class, 'uitk-cell') and contains(@class, 'loyalty-display-price') and contains(@class, 'all-cell-shrink')]")
            for p in plist:
                num = self.get_num(p.text)
                count = 0
                if (num < 200 and num > 0 and count < 5):
                    main_window = self.driver.current_window_handle
                    count += 1
                    ActionChains(self.driver).move_to_element(p).click(p).perform()
                    handles = self.driver.window_handles
                    for h in handles:
                        if h != self.driver.current_window_handle:
                            self.driver.switch_to.window(h)
                            self.scrollDown()
                            self.driver.close()
                            self.driver.switch_to.window(main_window)

    # choose budget level from 0 (low)- 4 (high)
    def choose_budget(self, level):
        budget_string = "price-" + str(level) + "-" + str(level)
        try:
            option = self.driver.find_element_by_xpath("//input[@id='" + budget_string + "']")
            option.click()
            self.scrollDown()
        except:
            pass
        try:
            more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
            more_button.click()
            self.scrollDown()
        except:
            pass

    # random click a listing in the search result
    def click_random(self):
        main_window = self.driver.current_window_handle
        list = self.driver.find_elements_by_xpath("//li[contains(@class, 'listing') and contains(@class, 'uitk-cell') and contains(@class, 'xl-cell-1-1') and contains(@class, 'l-cell-1-1') and contains(@class, 'm-cell-1-1') and contains(@class, 's-cell-1-1')]")
        l = len(list)
        index = randint(0, l-1)
        list[index].click()
        time.sleep(20)
        handles = self.driver.window_handles
        for h in handles:
            if h != self.driver.current_window_handle:
                self.driver.switch_to.window(h)
                self.scrollDown()
                self.driver.close()
                self.driver.switch_to.window(main_window)

    # click first 5 listing in the search list
    def click_first_5(self):
        main_window = self.driver.current_window_handle
        list = self.driver.find_elements_by_xpath("//li[contains(@class, 'listing') and contains(@class, 'uitk-cell') and contains(@class, 'xl-cell-1-1') and contains(@class, 'l-cell-1-1') and contains(@class, 'm-cell-1-1') and contains(@class, 's-cell-1-1')]")
        l = len(list)
        index = randint(0, l-1)
        list[index].click()
        time.sleep(20)
        handles = self.driver.window_handles
        for h in handles:
            if h != self.driver.current_window_handle:
                self.driver.switch_to.window(h)
                self.scrollDown()
                self.driver.close()
                self.driver.switch_to.window(main_window)

    # sort by criteria
    # options = [ RECOMMENDED, PRICE_LOW_TO_HIGH, PRICE_RELEVANT, BEST_DEAL, REVIEW, DISTANCE. PROPERTY_CLASS. VACATION_RENTAL]
    def sort(self, criteria):
        select = Select(self.driver.find_element_by_xpath('//select'))
        select.select_by_value(criteria)

    # choose star level: 0 - 4
    def choose_star_level(self, num):
        star_level_string = "star-" + str(num)
        try:
            input = self.driver.find_element_by_xpath("//input[@id='" + star_level_string + "']/parent::*")
            input.click()
            self.scrollDown()
        except:
            pass
        try:
            more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
            more_button.click()
            self.scrollDown()
        except:
            pass

    # choose guest rating: 35, 40, 45
    def choose_guest_rating(self, num):
        guest_rating = "radio-guestRating-" + str(num)
        input = self.driver.find_element_by_xpath("//input[@id='" + guest_rating + "']")
        input.click()
        self.scrollDown()
        try:
            more_button = self.driver.find_element_by_xpath("//button[contains(@class, 'uitk-button-secondary')]")
            more_button.click()
            self.scrollDown()
        except:
            pass

    # end session
    def close_session(self):
        self.driver.close()
    '''

# helper function to write results to a txt file for processing
def write_to_csv(names):
    now = datetime.now()

    # print("now = ", int(now.timestamp()))
    cwd = os.getcwd()
    writepath ="links.txt"
    if os.path.exists(writepath):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(writepath,  append_write) as file1:
        #titleString = "searching for " + title + " at " + dt_string + " using account = " + email
        #file1.write(titleString)
        #file1.write("\n")
        for i in range(0, len(names)):
            file1.write("https://news.google.com"+str(names[i].get('href')).replace('.',''))
            file1.write("\n")

# main function
def operation():
    old_file = 'D:\\CSsourcecodes\\NLP-news-summary\\links.txt'
    if os.path.isfile(old_file):
        os.remove(old_file)

    expedia_bot = ExpediaBot()
    i = expedia_bot.login()
    while i == -1:
       expedia_bot.close_session()
       del expedia_bot
       time.sleep(5)
       expedia_bot = ExpediaBot()
       i = expedia_bot.login()
    names=expedia_bot.searchLinks()
    print(names)
    write_to_csv(names)

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS,config.PASSWORD)
        message ='Subject:{}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAIL_ADDRESS,config.EMAIL_ADDRESS,message)
        server.quit()

        print("Success")
    except:
        print("fail")

def send_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject:{}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
        server.quit()

        print("Success")
    except:
        print("fail")




if __name__ == '__main__':
    subject = "Daily News Update"
    msg = "Here is your news update."
    #schedule.every().day.at("17:30").do(operation)

    # send_email()
    operation()

    while(1):
        schedule.run_pending()
        time.sleep(1)

    # strategy cases

# python3 expedia_bot_chrome.py "expediabot3+18@gmail.com" "lIteRgHEWORMiTERAnDATEATUSeM" "expediabot3+19@gmail.com" "lIteRgHEWORMiTERAnDATEATUSeM" "Boston" "08/01/2020" "08/25/2020" "low_click" 2 30
