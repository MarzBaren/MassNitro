from random import choices, choice
from threading import Thread
from time import sleep, time

import requests, os

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

class Main:

    def __init__(self):

        print("""
█   █ █████ █████ ████   ███  
██  █   █     █   █   █ █   █ 
█ █ █   █     █   ████  █   █ 
█  ██   █     █   █   █ █   █ 
█   █ █████   █   █   █  ███  

""")
        os.system('color a')
		
        print('How many threads do you want? (Lower is slower, but saves your cpu) Between 50 and 800')
		
        i = int(input())
		
        self.attempt = 0
        self.works = []
        self.header = {'Pragma': 'no-cache',
                       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

        self.proxy_update()

        Thread(target=self.keep_active, daemon=True).start()
        for _ in range(i):
            Thread(target=self.checking).start()
            sleep(0.01)

    def proxy_update(self):
        self.proxies = []
        while True:
            proxies = []
            try:
                for x in requests.get(url="https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=2000").text.splitlines():
                    if x != '':
                        if ':' in x:
                            if len(proxies) > 4800:
                                break
                            proxies.append(x)
                try:
                    for proxyappend in requests.get('https://www.proxyscan.io/download?type=socks4').text.split('\n'):
                        if len(proxies) > 4800:
                            break
                        proxies.append(proxyappend)
                except:
                    for proxyappend in requests.get('https://www.proxyscan.io/download?type=socks4').text.split('\n'):
                        if len(proxies) > 4800:
                            break
                        proxies.append(proxyappend)
                break
            except:
                pass
        for prox in proxies:
            self.proxies.append(prox)

    def proxy_format(self):
        proxy = choice(self.proxies)
        proxy_form = {
            'http': f"socks4://{proxy}",
            'https': f"socks4://{proxy}"
        }
        return proxy_form

    def keep_active(self):
        last = 0
        tid = time()
        while True:
            for x in range(750):
                sleep(1)
                os.system('cls')
                os.system(f'title Attempts: {self.attempt}    Hits: {len(self.works)}')
                print("""
█   █ █████ █████ ████   ███  
██  █   █     █   █   █ █   █ 
█ █ █   █     █   ████  █   █ 
█  ██   █     █   █   █ █   █ 
█   █ █████   █   █   █  ███  """)
                os.system('color a')
                print('\n\n')
                timeused = str(time() - tid).split(".")
                print(f'Attempt: {self.attempt}        Codes/S: {self.attempt - last}      Time: {timeused[0]}.{timeused[1][0]}')
                print('')
                last = self.attempt
                if len(self.works) > 0:
                    for x in self.works:
                        print(str(x))
            self.proxy_update()

    def checking(self):
        ses = requests.session()
        while True:
            try:
                code = ''.join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=16))
                req = self.check(code, ses)
                if req.text.__contains__('Unknown Gift Code'):
                    continue
                elif req.text.__contains__('<p>The owner of this website (discordapp.com) has banned your IP address'):
                    continue
                elif req.text.status_code == 502:
                    continue
                else:
                    self.works.append(code)
                    with open('codes.txt', 'a') as f:
                        f.write(code + '\n' + 'message: ' + req.text)
            except:
                pass

    def check(self, code, ses):
        try:
            req = ses.get(
				url=f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true',
				proxies=self.proxy_format(), headers=self.header, timeout=6)
            if ('You are being rate limited.' or 'Access denied') in str(req.text):
               return
            self.attempt += 1
            return req
        except:
            return

Main()