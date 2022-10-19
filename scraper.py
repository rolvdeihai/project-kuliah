import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from collections import Counter
import random
from instabot import Bot
#from main import USERNAME, PASSWORD

# Complete these 2 fields ==================
#USERNAME = 'your instagram username'
#PASSWORD = 'your instagram password'
# ==========================================

TIMEOUT = 50

def interact(user, pw):
    bot = Bot();
    bot.login(username = user, password = pw);
    f = open("followers.txt", "r");
    followers_list = str(list(f));
    followers_list = list(followers_list.split("\n"))

    for j in range(0, len(followers_list)):
        followers_amount = bot.get_user_followers(followers_list[j])
        length = len(followers_amount)
        if(length >= 50 and length <= 5000):
            bot.follow(followers_list[j])
            time.sleep(2)
            bot.like_user(followers_list[j], amount = 4)
            time.sleep(2)
            media = bot.get_last_user_medias(user_id=bot.get_user_id_from_username(followers_list[j]))
            bot.comment(media, "Mantapp!!")
            time.sleep(3)
            bot.send_message("Permisi kak, minta tolong follbacknya boleh ya kalo enjoy sama konten kami :)", followers_list[j])
            time.sleep(10)

def shuffle_list(x):
    f = open(x, "r")
    random.shuffle(f)
    f.close()

def remove_duplicates():
    f = open("followers_link.txt", "r")
    new_file = str(list(dict.fromkeys(f)))
    new_file = new_file.replace("https://www.instagram.com/", "")
    new_file = new_file.replace("/\\n", "")
    new_file = new_file.replace("[", "")
    new_file = new_file.replace("]", "")
    new_file = new_file.replace(",", "")
    new_file = new_file.replace("'", "")
    new_file = list(new_file.split(" "))

    for j in range(0, len(new_file)):
        with open('followers.txt', 'a') as file:
            file.write(new_file[j] + "\n");

    # print(new_file)
    # f = open("\n".join(new_file), "w");
    # f = open("followers.txt", "w")
    # f.write(new_file)
    f.close()

def scrape(username, password):
    usr = input('[Required] - Whose followers do you want to scrape: ')

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(executable_path=CM().install(), options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(2)

    print("[Info] - Logging in...")

    user_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))

    user_element.send_keys(username)

    pass_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))

    pass_element.send_keys(password)

    login_button = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]/button')))

    time.sleep(0.4)

    login_button.click()

    time.sleep(5)

    alert = WebDriverWait(bot, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

    time.sleep(3)

    bot.get('https://www.instagram.com/{}'.format(usr))

    time.sleep(3.5)

    WebDriverWait(bot, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "followers")]'))).click()

    time.sleep(2)

    print('[Info] - Scraping...')

    # scroll down 2 times
    # increase the range to sroll more
    time.sleep(5)

    n_scrolls = 2
    for j in range(0, n_scrolls):
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # target all the link elements on the page
    followers = bot.find_elements_by_tag_name('a')
    followers = [a.get_attribute('href') for a in followers]
    # narrow down all links to image links only
    followers = [a for a in followers if str(a).startswith("https://www.instagram.com/")]

    print('Found ' + str(len(followers)) + ' links to images')
    followers[:5]

    for j in range(0, len(followers)):

        freq = followers[j].count('/');

        if freq == 4:
            print(followers[j]);
            with open('followers_link.txt', 'a') as file:
                file.write(followers[j] + "\n");
    # users = set()
    #
    # for _ in range(round(user_input // 10)):
    #
    #     ActionChains(bot).send_keys(Keys.END).perform()
    #
    #     time.sleep(2)
    #
    #     followers = bot.find_elements_by_css_selector(
    #         'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd')
    #
    #     # Getting url from href attribute
    #     for i in followers:
    #         if i.get_attribute('href'):
    #             users.add(i.get_attribute('href').split("/")[3])
    #         else:
    #             continue
    #
    # print('[Info] - Saving...')
    # print('[DONE] - Your followers are saved in followers.txt file!')
    #
    # with open('followers.txt', 'a') as file:
    #     file.write('\n'.join(users) + "\n")


if __name__ == '__main__':
    scrape()
