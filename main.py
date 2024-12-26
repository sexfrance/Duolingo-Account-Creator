import tls_client 
import uuid
import random
import time
import re
import toml
import string
import ctypes
import threading
import concurrent.futures

from collections import namedtuple
from TempMail import TempMail
from functools import wraps
from logmagix import Logger, Home


with open('input/config.toml') as f:
    config = toml.load(f)

DEBUG = config['dev'].get('Debug', False)
log = Logger()
tmp = TempMail(config['email'].get('tempmail_lol_api_key'))

def debug(func_or_message, *args, **kwargs) -> callable:
    if callable(func_or_message):
        @wraps(func_or_message)
        def wrapper(*args, **kwargs):
            result = func_or_message(*args, **kwargs)
            if DEBUG:
                log.debug(f"{func_or_message.__name__} returned: {result}")
            return result
        return wrapper
    else:
        if DEBUG:
            log.debug(f"Debug: {func_or_message}")

def debug_response(response) -> None:
    debug(response.text)
    debug(response.status_code)
    debug(response.headers)


class Miscellaneous:
    @debug 
    def randomize_mobile_user_agent(self) -> str:
        duolingo_version = "6.11.4" #! --------------------------------- IF YOU CANNOT GENERATE (500 status in create unclaimed) YOU WILL NEED TO CHANGE THE VERSION YOU CAN FIND IT HERE: https://apkpure.com/fr/duolingo-language-lessons/com.duolingo/versions
        android_version = random.randint(14, 15)
        build_codes = ['AE3A', 'TQ3A', 'TP1A', 'SP2A']
        build_date = f"{random.randint(220000, 240806)}"
        build_suffix = f"{random.randint(1, 999):03d}"
        
        devices = [
            'sdk_gphone64_x86_64',
            'Pixel 6',
            'Pixel 7',
            'SM-A536B',
            'SM-S918B'
        ]
        
        device = random.choice(devices)
        build_code = random.choice(build_codes)
        
        user_agent = f"Duodroid/{duolingo_version} Dalvik/2.1.0 (Linux; U; Android {android_version}; {device} Build/{build_code}.{build_date}.{build_suffix})"
        return user_agent

    @debug
    def randomize_computer_user_agent(self) -> str:
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Linux i686",
            "X11; Ubuntu; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
            ("Firefox", f"{random.randint(80, 115)}.0"),
            ("Safari", f"{random.randint(13, 16)}.{random.randint(0, 3)}"),
            ("Edge", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
        ]
        
        webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 99)}"
        platform = random.choice(platforms)
        browser_name, browser_version = random.choice(browsers)
        
        if browser_name == "Safari":
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"Version/{browser_version} Safari/{webkit_version}"
            )
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({platform}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        else:
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"{browser_name}/{browser_version} Safari/{webkit_version}"
            )
        
        return user_agent

    @debug 
    def generate_password(self) -> str:
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/", k=16))
        return password
    
    @debug 
    def generate_first_name(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

    @debug
    def generate_last_name(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    @debug 
    def generate_email(self, domain: str = "gmail.com"):
        username = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=20))}"
        email = f"{username}@{domain}"
        return email

    @debug 
    def generate_inbox(self, domain: str = None, prefix: str = None) -> tuple :
        inbox = tmp.createInbox(domain, prefix)
        return inbox

    @debug
    def get_proxies(self) -> dict:
        try:
            if config['dev'].get('Proxyless', False):
                return None
                
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    log.warning("No proxies available. Running in proxyless mode.")
                    return None
                
                proxy_choice = random.choice(proxies)
                proxy_dict = {
                    "http": f"http://{proxy_choice}",
                    "https": f"http://{proxy_choice}"
                }
                log.debug(f"Using proxy: {proxy_choice}")
                return proxy_dict
        except FileNotFoundError:
            log.failure("Proxy file not found. Running in proxyless mode.")
            return None
    
    class Title:
        def __init__(self):
            self.running = False

        def start_title_updates(self, total, start_time):
            self.running = True
            def updater():
                while self.running:
                    self.update_title(total, start_time)
                    time.sleep(0.5)
            threading.Thread(target=updater, daemon=True).start()

        def stop_title_updates(self):
            self.running = False

        def update_title(self, total, start_time):
            try:
                elapsed_time = round(time.time() - start_time, 2)
                title = f'discord.cyberious.xyz | Total: {total} | Time Elapsed: {elapsed_time}s'

                sanitized_title = ''.join(c if c.isprintable() else '?' for c in title)
                ctypes.windll.kernel32.SetConsoleTitleW(sanitized_title)
            except Exception as e:
                log.debug(f"Failed to update console title: {e}")

class AccountCreator:
    def __init__(self, proxy_dict: dict = None):
        self.session = tls_client.Session("okhttp4_android_13", random_tls_extension_order=True)
        self.misc = Miscellaneous()
        self.session.headers = {
            'accept': 'application/json',
            'connection': 'Keep-Alive',
            'content-type': 'application/json',
            'host': 'android-api-cf.duolingo.com',
            'user-agent': self.misc.randomize_mobile_user_agent(),
            'x-amzn-trace-id': 'User=0',
        }

        self.session.proxies = proxy_dict

    @debug
    def create_unclaimed(self, currentCourseId: str  = "DUOLINGO_EN_FR", from_language: str = "fr") -> tuple:
        debug("Sending request to create_unclaimed")
        debug(f"create_unclaimed called with currentCourseId={currentCourseId}, from_language={from_language}")
        debug(f"Using Headers: {self.session.headers}")
        
        params = {
            'fields': 'id,creationDate,fromLanguage,courses{alphabetsPathProgressKey,id,subject,topic,xp,authorId,healthEnabled,fromLanguage,learningLanguage},currentCourseId,username,health{eligibleForFreeRefill,healthEnabled,useHealth,hearts,maxHearts,secondsPerHeartSegment,secondsUntilNextHeartSegment,nextHeartEpochTimeMs,unlimitedHeartsAvailable},zhTw,hasPlus,joinedClassroomIds,observedClassroomIds,roles',
        }
        
        
        json_data = {
            'currentCourseId': currentCourseId ,
            'distinctId': str(uuid.uuid4),
            'fromLanguage': from_language,
            'timezone': 'GMT',
            'zhTw': False,
        }

        response = self.session.post('https://android-api-cf.duolingo.com/2023-05-23/users', params=params, json=json_data)

        debug_response(response)

        if response.status_code == 200:
            user_id = response.json().get("id")
            jwt = response.headers.get("Jwt")

            ResponseData = namedtuple("ResponseData", ["id", "jwt"])
            return ResponseData(user_id, jwt)
        elif response.status_code == 500:
            log.failure("Failed to create an account, server returned 500. Probable cause: Bad useragent try increasing Duodroid version")
        else:
            log.failure(f"Failed to create an unclaimed account: {response.text}, {response.status_code}")
        
        return None
    
    @debug
    def claim_account(self, userid: str, email: str, password: str, first_name: str, last_name: str, jwt: str) -> bool:
            debug("Sending request to claim_account")
            debug(f"Claim account beeing called with: {userid}, {email}, {password}, {first_name}, {last_name}, {jwt}")
            debug(f"Using Headers: {self.session.headers}")
            
            self.session.headers.update({
                'authorization': f'Bearer {jwt.strip()}',
                'x-amzn-trace-id': f'User={userid}',
            })

            json_data = {
                'requests': [
                    {
                        'body': f'{{"age":"{random.randint(18, 80)}", "distinctId": "UserId(id={userid})","email": "{email}","emailPromotion": true,"name": "{first_name} {last_name}","firstName": "{first_name}","lastName": "{last_name}", "password": "{password}", "pushPromotion": true, "timezone":"GMT"}}',

                        'bodyContentType': 'application/json',
                        'method': 'PATCH',
                        'url': f'/2023-05-23/users/{userid}?fields=adsConfig%7Bunits%7D%2Cid%2CbetaStatus%2CblockerUserIds%2CblockedUserIds%2CclassroomLeaderboardsEnabled%2Ccourses%7BalphabetsPathProgressKey%2Cid%2Csubject%2Ctopic%2Cxp%2CauthorId%2ChealthEnabled%2CfromLanguage%2ClearningLanguage%7D%2CcreationDate%2CcurrentCourseId%2Cemail%2CemailAnnouncement%2CemailFollow%2CemailPass%2CemailPromotion%2CemailResearch%2CemailStreakFreezeUsed%2CemailWeeklyProgressReport%2CfacebookId%2CfeedbackProperties%2CfromLanguage%2CgemsConfig%7Bgems%2CgemsPerSkill%2CuseGems%7D%2CgoogleId%2ChasFacebookId%2ChasGoogleId%2ChasRecentActivity15%2Chealth%7BeligibleForFreeRefill%2ChealthEnabled%2CuseHealth%2Chearts%2CmaxHearts%2CsecondsPerHeartSegment%2CsecondsUntilNextHeartSegment%2CnextHeartEpochTimeMs%2CunlimitedHeartsAvailable%7D%2CinviteURL%2CemailUniversalPractice%2CpushUniversalPractice%2CjoinedClassroomIds%2ClastResurrectionTimestamp%2ClearningLanguage%2Cname%2CfirstName%2ClastName%2CobservedClassroomIds%2CoptionalFeatures%7Bid%2Cstatus%7D%2CpersistentNotifications%2CphoneNumber%2Cpicture%2CplusDiscounts%7BexpirationEpochTime%2CdiscountType%2CsecondsUntilExpiration%2CisActivated%7D%2CprivacySettings%2CpushAnnouncement%2CpushEarlyBird%2CpushNightOwl%2CpushFollow%2CpushLeaderboards%2CpushLiveUpdates%2CpushPassed%2CpushPromotion%2CpushStreakFreezeUsed%2CpushStreakSaver%2CpushSchoolsAssignment%2CrewardBundles%7Bid%2CrewardBundleType%2Crewards%7Bid%2Cconsumed%2CitemId%2Ccurrency%2Camount%2CrewardType%7D%7D%2Croles%2CshakeToReportEnabled%2CshouldForceConnectPhoneNumber%2CsmsAll%2CshopItems%7Bid%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CpurchasedByUserId%2CremainingEffectDurationInSeconds%2CxpBoostMultiplier%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%2CsubscriptionItemType%2CsentTime%7D%7D%7D%2Cstreak%2CstreakData%7Blength%2CstartTimestamp%2CupdatedTimestamp%2CupdatedTimeZone%2CxpGoal%7D%2CsubscriptionConfigs%7BisInBillingRetryPeriod%2CisInGracePeriod%2CvendorPurchaseId%2CproductId%2CpauseStart%2CpauseEnd%2CreceiptSource%7D%2Ctimezone%2CtotalXp%2CtrackingProperties%2CuniversalPracticeNotifyTime%2Cusername%2CuseUniversalSmartReminderTime%2CxpGains%7Btime%2Cxp%2CeventType%2CskillId%7D%2CxpGoal%2CzhTw%2CtimerBoostConfig%7BtimerBoosts%2CtimePerBoost%2ChasFreeTimerBoost%7D%2CenableSpeaker%2CenableMicrophone%2CchinaUserModerationRecords%7Bcontent%2Cdecision%2Crecord_identifier%2Crecord_type%2Csubmission_time%2Cuser_id%7D%2ChasPlus%2CsubscriberLevel',
                        'origin': 'https://android-api-cf.duolingo.com',
                    },
                ],
                'includeHeaders': False,
            }

            response = self.session.post('https://android-api-cf.duolingo.com/2017-06-30/batch', params={'fields': 'responses{body,status,headers}'}, json=json_data)

            debug_response(response)

            if response.status_code == 200:
                if response.json().get("responses")[0].get("status") == 200:
                    return True
            elif response.status_code == 429:
                log.warning("Rate limited!")
            else:
                log.failure(f"Failed to create a claimed account: {response.text} {response.status_code}")
        
            return False
    
    @debug
    def get_verification_link(self, inbox: tuple, max_attempt: int = 10) -> str:
        attempt = 0

        log.info(f"Searching email for verification link...")
        emails = tmp.getEmails(inbox)
        while attempt < max_attempt:
            for email in emails:
                debug(email)
                if email.sender.endswith("duolingo.com"):
                    match = re.search(r"https://www\.duolingo\.com/verify/\S+", email.body)
                    if match:
                        return match.group(0)   
        
            attempt += 1
            time.sleep(1.5)
        
        debug(f"No verification message found after {attempt} attempts")
        return None
    
    @debug
    def verify_account(self, url: str) -> bool:

        debug("Sending request to verify_account")

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'connection': 'keep-alive',
            'host': 'www.duolingo.com',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.misc.randomize_computer_user_agent()
        }

        response = self.session.get(url, headers=headers)

        debug_response(response)

        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            log.warning("Rate limited!")
        else:
            log.failure(f"Failed to create a claimed account: {response.text} {response.status_code}")
        
        return False

def create_account() -> None:
    try:
        while True:
            account_time = time.time()
            log.info("Starting new account generation...")

            try:
                Misc = Miscellaneous()
                proxies = Misc.get_proxies()
                Account_Generator = AccountCreator(proxies)
                
                # Generate required data
                first_name = Misc.generate_first_name()
                last_name = Misc.generate_last_name()
                password = config["data"].get("password") or Misc.generate_password()
                
                mode = 1 if config["data"]["mode"].strip().lower() in ["unclaimed", "1"] else \
                    2 if config["data"]["mode"].strip().lower() in ["claimed", "2"] else \
                    3 if config["data"]["mode"].strip().lower() in ["verified", "3"] else None
                
                if mode is None:
                    log.failure("Invalid mode specified in config")
                    continue

                if mode == 1:
                    account = Account_Generator.create_unclaimed()
                    if account:
                        with open("output/unclaimed/accounts.txt", "a") as f:
                            f.write(f"{account.id}:{account.jwt}\n")
                        log.message(f"Duolingo", f"Successfully created unclaimed account: {account.id}", account_time, time.time())
                    else:
                        log.failure("Failed to create unclaimed account")
                
                elif mode == 2:
                    email = Misc.generate_email()
                    account = Account_Generator.create_unclaimed()
                    if not account:
                        log.failure("Failed to create initial unclaimed account")
                        continue
                        
                    log.info("Claiming account...")
                    if Account_Generator.claim_account(account.id, email, password, first_name, last_name, account.jwt):
                        with open("output/claimed/accounts.txt", "a") as f:
                            f.write(f"{email}:{password}\n")
                        log.message(f"Duolingo", f'Successfully created claimed account: {email}:{password[:8]}...', account_time, time.time())
                    else:
                        log.failure("Failed to claim account")
                
                elif mode == 3:
                    account = Account_Generator.create_unclaimed()
                    if not account:
                        log.failure("Failed to create initial unclaimed account")
                        continue
                    try:
                        inbox = Misc.generate_inbox()
                        email = inbox.address
                    except Exception as e:
                        log.failure(f"Failed to generate temp email: {str(e)}")
                        continue
                    
                    log.info("Claiming account...")
                    if Account_Generator.claim_account(account.id, email, password, first_name, last_name, account.jwt):
                        url = Account_Generator.get_verification_link(inbox)
                        if not url:
                            log.failure("Failed to receive verification email")
                            continue
                            
                        log.info(f"Verifying account with url: {url}...")
                        if Account_Generator.verify_account(url):
                            with open("output/verified/accounts.txt", "a") as f:
                                f.write(f"{email}:{password}\n")
                            with open("output/verified/full_account_capture.txt", "a") as f:
                                f.write(f"{account.id}:{email}:{password}:{account.jwt}:{inbox.token}\n")
                            log.message(f"Duolingo", f'Successfully created verified account: {email}:{password[:8]}...', account_time, time.time())
                        else:
                            log.failure("Failed to verify account")
                    else:
                        log.failure("Failed to claim account")

            except Exception as e:
                log.failure(f"Error during account creation: {str(e)}")
                continue

    except Exception as e:
        log.failure(f"Critical error in thread: {str(e)}")

def main() -> None:
    try:
        start_time = time.time()
        log.info("Starting Duolingo Account Generator...")
        Banner = Home("Duolingo Generator", align="center", credits="discord.cyberious.xyz")
        Banner.display()

        num_threads = config['dev'].get('Threads', 1)
        debug(f"Initializing {num_threads} threads...")
        
        title_updater = Miscellaneous.Title()
        title_updater.start_title_updates(0, start_time)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            debug("Thread pool created, starting account generation...")
            futures = [executor.submit(create_account) for _ in range(num_threads)]
            concurrent.futures.wait(futures)

    except KeyboardInterrupt:
        log.info("Process interrupted by user. Cleaning up...")
        exit()
    except Exception as e:
        log.failure(f"Critical error in main process: {str(e)}")
    finally:
        title_updater.stop_title_updates()
        log.info("Generator shutdown complete")

if __name__ == "__main__":
    main()

# TODO: Add humanization
