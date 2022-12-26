#!/usr/bin/env python3
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
import json
from schedule import repeat, every, run_pending
import datetime
from datetime import date
import pytz
import paramiko
from scp import SCPClient
import logging

class Main:
    def __init__(self):
        self.url = "https://www.weibo.com/login.php"
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-notifications")
        self.bot = webdriver.Remote(
            command_executor=f"http://chrome:4444", options=chrome_options
        )

        self.bot.get(self.url)

    def bot_quit(self):
        self.bot.quit()

    def initial_login(self):
        try:
            print('Initial login called!')
            if not os.path.exists('cookies.json'):
                # Use your phone to authenticate yourself within this time period. 
                time.sleep(25)
                ###############

                with open('cookies.json', 'w+') as f:
                    f.write(json.dumps(self.bot.get_cookies()))
                    f.close()
                print('Initial cookies extracted!')
                self.ssh_scp_files()
        except Exception as e:
            print(e)
            self.bot_quit()
    
    def extract_cookies(self):
        try:
            print("Extract cookies called!")
            self.bot.refresh()
            self.bot.get(self.url)
            time.sleep(20)
            with open('cookies.json', 'w') as f:
                f.write(json.dumps(self.bot.get_cookies()))
                f.close()
            print('New cookie values added! Sending over to dev server...')
            self.ssh_scp_files()
        except Exception:
            self.bot_quit()
    
    def ssh_scp_files(self):
        try:
            print('Sending over to dev...')
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect('ip add', username='#', password='#')

            with SCPClient(ssh.get_transport()) as scp:
                scp.put('cookies.json', recursive=True, remote_path='C:/Users/#')
            print('Cookies files sent!')
        except Exception as e:
            print(e)
    
extract_cookie = Main()

@repeat(every(1).hours, extract_cookie)
def start_main(main_class: Main):
    if os.path.exists('cookies.json'):
        main_class.extract_cookies()
    else:
        main_class.initial_login()
    
    # tomororw = datetime.date.today() + datetime.timedelta(days=1)
    
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
    later = now + datetime.timedelta(hours=1)
    
    print(f'Going to sleep. Next job scheduled at: {now} : {later.strftime("%H:%M")}')

count = 0
while True:
    if count == 0:
        print('Initial run')
        start_main(extract_cookie)
    count += 1
    run_pending()
    today = datetime.date.today()
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
    
    # Testing.. Output should show cookie files being to send over to my the ip address at every hourly interval
    print(f"Count: {count}. Date: {today} : Time: {now.strftime('%H:%M')}\n")
    time.sleep(3600)






