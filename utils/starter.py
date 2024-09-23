import random

from data.config import DELAYS
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
        func_all = [banana.start_quest, banana.claim_banana_quest, banana.claim_lottery, banana.claim_banana,
                banana.click, banana.logout]
        for func in func_all:
            await func()
            await sleep(random.randint(*DELAYS["FUNC"]))
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
