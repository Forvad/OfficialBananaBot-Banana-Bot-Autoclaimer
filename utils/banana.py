import random
import string

from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName, InputUser
import asyncio
from urllib.parse import unquote
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from faker import Faker
from data.config import BLACKLIST_TASK, DELAYS, API_ID, API_HASH, PROXY, WORKDIR


def retry_async(max_retries=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            thread, account = args[0].thread, args[0].account
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.error(f"Thread {thread} | {account} | Error: {e}. Retrying {retries}/{max_retries}...")
                    await asyncio.sleep(10)
                    if retries >= max_retries:
                        break
        return wrapper
    return decorator


class BananaBot:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.proxy = f"{PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)

        if proxy:
            proxy = {
                "scheme": PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=API_ID,
            api_hash=API_HASH,
            workdir=WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector,
                                             timeout=aiohttp.ClientTimeout(120))

    async def check_request(self, rep):
        resp_text = rep.text
        if '429 Too Many Requests' in str(resp_text):
            logger.error(f'429 Too Many Requests | {self.account} | sleep 1800 sec....')
            await asyncio.sleep(1800)
            return False
        else:
            return True

    async def logout(self):
        await self.session.close()

    async def login(self):
        self.session.headers.pop('Authorization', None)
        query = await self.get_tg_web_data()

        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        json_data = {"tgInfo": query, "InviteCode": "MFPDOK5"}

        # await self.session.options("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP")

        while True:
            resp = await self.session.post("https://interface.carv.io/banana/login", json=json_data)
            check = await self.check_request(resp)
            if not check:
                return await self.login()
            resp_json = await resp.json()
            if resp_json['msg'] == 'Success':
                break
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error: {resp_json}")
                await asyncio.sleep(10)
                continue

        self.session.headers['Authorization'] = "Bearer " + resp_json.get("data").get("token")
        return True

    async def get_tg_web_data(self):
        try:
            await self.client.connect()

            if not (await self.client.get_me()).username:
                while True:
                    username = Faker('en_US').name().replace(" ", "") + '_' + ''.join(random.choices(string.digits, k=random.randint(3, 6)))
                    if await self.client.set_username(username):
                        logger.success(f"Thread {self.thread} | {self.account} | Set username @{username}")
                        break
                await asyncio.sleep(5)
            bot_id = await self.client.resolve_peer('OfficialBananaBot')

            input_user = InputUser(user_id=bot_id.user_id, access_hash=bot_id.access_hash)

            web_view = await self.client.invoke(RequestAppWebView(
                peer=bot_id,
                app=InputBotAppShortName(bot_id=input_user, short_name="banana"),
                platform='android',
                write_allowed=True,
                start_param='referral=MFPDOK5'
            ))
            await self.client.disconnect()
            auth_url = web_view.url

            query = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            return query
        except:
            return None

    async def get_user_info(self):
        resp = await self.session.get("https://interface.carv.io/banana/get_user_info")
        check = await self.check_request(resp)
        if not check:
            return await self.get_user_info()
        resp_json = await resp.json()
        if resp_json['msg'] == 'Success':
            balance = resp_json['data']['peel']
            lottery = resp_json['data']['lottery_info']['remain_lottery_count']
            need_click = resp_json['data']['max_click_count'] - resp_json['data']['today_click_count']
            logger.info(f'Thread {self.thread} | {self.account} | balance: {balance}, lottery: {lottery}, need_click: {need_click}')
            return balance, lottery, need_click
        else:
            logger.error(f'Thread {self.thread} | {self.account} | get user error: {resp_json}')
            await asyncio.sleep(10)
            return await self.get_user_info()

    async def click(self):
        while True:
            _, _, need_click = await self.get_user_info()
            if need_click >= 10:
                click = random.randint(1, need_click)
            else:
                click = need_click
            if need_click:
                json = {'clickCount': click}
                rep = await self.session.post('https://interface.carv.io/banana/do_click', json=json)
                check = await self.check_request(rep)
                if not check:
                    return await self.click()
                await asyncio.sleep(random.uniform(60, 80))
            else:
                return

    async def claim_banana(self):
        _, lottery, _ = await self.get_user_info()
        if lottery:
            for _ in range(lottery):
                json = {}
                rep = await self.session.post('https://interface.carv.io/banana/do_lottery', json=json)
                check = await self.check_request(rep)
                if not check:
                    return await self.claim_banana()
                rep_json = await rep.json()
                if rep_json['msg'] == 'Success':
                    await asyncio.sleep(20)
                    await self.claim_points_vidio()
                    logger.success(f'Thread {self.thread} | {self.account} | They took the banana')
                    # await asyncio.sleep(7)
                    # await self.go_share(rep_json['data']['banana_id'])
                await asyncio.sleep(60)

            else:
                logger.error(f'error: {rep_json}')
        else:
            logger.info('There are no available tickets for claim')

    async def claim_points_vidio(self):
        json = {'type': 2}

        await self.session.post(f'https://interface.carv.io/banana/claim_ads_income', json=json)
        await self.get_user_info()

    async def go_share(self, id_):
        json = {'banana_id': int(id_)}
        resp = await self.session.post(f'https://interface.carv.io/banana/claim_ads_income', json=json)
        resp_json = await resp.text()
        logger.info(resp_json)
        await self.get_user_info()

    async def claim_lottery(self):
        json = {'claimLotteryType': 1}
        resp = await self.session.post('https://interface.carv.io/banana/claim_lottery', json=json)
        check = await self.check_request(resp)
        if not check:
            return await self.claim_lottery()
        rep_json = await resp.json()
        if rep_json['msg'] == 'Success':
            logger.success(f'Thread {self.thread} | {self.account} | claim lottery ticket')

    async def achieved_quest(self, id_: int, name: str, num: int, all_num: int):
        json = {'quest_id': id_}
        resp = await self.session.post('https://interface.carv.io/banana/achieve_quest', json=json)
        check = await self.check_request(resp)
        if not check:
            return await self.achieved_quest(id_, name, num, all_num)
        rep_json = await resp.json()
        if rep_json['msg'] == 'Success':
            logger.success(f'Thread {self.thread} | {self.account} | {num}/{all_num} | activated the quest | {id_} | {name}')
            return True
        else:
            return False

    async def claim_quest(self, id_: int, name: str, num: int, all_num: int):
        json = {'quest_id': id_}
        resp = await self.session.post('https://interface.carv.io/banana/claim_quest', json=json)
        check = await self.check_request(resp)
        if not check:
            return await self.claim_quest(id_, name, num, all_num)
        rep_json = await resp.json()
        if rep_json['msg'] == 'Success':
            logger.success(f'Thread {self.thread} | {self.account} | {num}/{all_num} | They took away the reward for quest No.| {id_} | {name}')

    async def quest_list(self, quest=None):
        all_quests = []
        resp = await self.session.get('https://interface.carv.io/banana/get_quest_list')
        check = await self.check_request(resp)
        if not check:
            return await self.quest_list()
        rep_json = await resp.json()
        if quest:
            return rep_json['data']['progress']
        quests = rep_json['data']['quest_list']
        for quest in quests:
            if quest['description'] not in BLACKLIST_TASK and not quest['is_claimed']:
                all_quests.append(quest)
        return all_quests

    async def start_quest(self):
        quests = await self.quest_list()
        random.shuffle(quests)
        for _ in range(2):
            for num, quest in enumerate(quests):
                if not quest['is_achieved']:
                    await self.achieved_quest(quest['quest_id'], quest['description'], num + 1, len(quests))
                    await asyncio.sleep(random.randint(60, 80))
                    await self.claim_quest(quest['quest_id'], quest['description'], num + 1, len(quests))
                    await asyncio.sleep(random.randint(*DELAYS["TASK"]))
                elif not quest['is_claimed']:
                    await self.claim_quest(quest['quest_id'], quest['description'], num + 1, len(quests))
                    await asyncio.sleep(random.randint(*DELAYS["TASK"]))

    async def claim_banana_quest(self):
        quest_info = await self.quest_list(True)
        quest_info = int(quest_info.split('/')[0]) // 3
        if quest_info:
            logger.info(f'Thread {self.thread} | {self.account} | We collect {quest_info} bananas of tickets for the tasks')
            await asyncio.sleep(30)
            for _ in range(quest_info):
                resp = await self.session.post('https://interface.carv.io/banana/claim_quest_lottery', json={})
                check = await self.check_request(resp)
                if not check:
                    return await self.claim_banana_quest()
                rep_json = await resp.json()
                if rep_json['msg'] == 'Success':
                    logger.success(f'Thread {self.thread} | {self.account} | they took the ticket for the quest')
                await asyncio.sleep(60)

    async def stats(self):
        await self.login()
        await asyncio.sleep(35)
        balance, lottery, need_click = await self.get_user_info()
        await self.logout()

        return {"name": self.account, "bqlance": balance, "proxy": self.proxy}
