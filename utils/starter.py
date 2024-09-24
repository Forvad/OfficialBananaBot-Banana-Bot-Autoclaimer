import random

from data.config import DELAYS, WHILE
from utils.banana import BananaBot
from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import datetime
import pandas as pd
from utils.core.telegram import Accounts
import asyncio
from aiohttp.client_exceptions import ContentTypeError
from utils.core.file_manager import save_csv


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    banana = BananaBot(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    await sleep(uniform(*config.DELAYS['ACCOUNT']))
    if WHILE:
        num = 999
    else:
        num = 1
    for _ in range(num):

        attempts = 3
        while attempts:
            try:
                await banana.login()
                logger.success(f"Thread {thread} | {account} | Login")
                break
            except Exception as e:
                logger.error(f"Thread {thread} | {account} | Left login attempts: {attempts}, error: {e}")
                await asyncio.sleep(uniform(*config.DELAYS['RELOGIN']))
                attempts -= 1
        else:
            logger.error(f"Thread {thread} | {account} | Couldn't login")
            await banana.logout()
            return

        # while True:
        try:
            await asyncio.sleep(5)
            if await banana.login() is None:
                return
            func_all = {'TASK': [banana.start_quest, banana.claim_banana_quest],
                        'CLAIM_TICKET': banana.claim_lottery,
                        'CLAIM_REFF': banana.claim_ref,
                        'CLAIM_BANANA': banana.claim_banana,
                        'CLICK_BANANA': banana.click
                        }
            for func in config.ADD_TASK:
                if isinstance(func_all[func], list):
                    for i in func_all[func]:
                        await i()
                        await sleep(random.randint(*DELAYS["FUNC"]))
                else:
                    await func_all[func]()
                await sleep(random.randint(*DELAYS["FUNC"]))
            if WHILE:
                await banana.sleep_to_claim()
                await func_all['CLAIM_BANANA']()
            await banana.logout()
        except ContentTypeError as e:
            logger.error(f"Thread {thread} | {account} | Error: {e}")
            await asyncio.sleep(120)

        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Error: {e}")


async def stats():
    accounts = await Accounts().get_accounts()

    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(BananaBot(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy).stats()))

    data = await asyncio.gather(*tasks)
    save_csv(data)
