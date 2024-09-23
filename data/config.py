# api id, hash
API_ID = 1488
API_HASH = 'abcde1488'

DELAYS = {
    "ACCOUNT": [10, 20],  # delay at the start
    "RELOGIN": [20, 30],  # reconnection delay
    'FUNC': [120, 180],  # delay between functions
    'TASK': [60, 80],  # delay after completed the task
}


# blacklist tasks
BLACKLIST_TASK = ['Bind CARV ID', 'CARV Newbie SBT On CARV Mobile', 'Complete any quest in Infinite Play Mobile',
                  'Bind TON Wallet', 'Bind Your Email', 'Bind Your X', 'TG Premium Verify',
                  "CARV 'CARV Pass Cyber Pioneers' Badge", "CARV 'CARV Quiz Challenge' Badge",
                  "CARV 'Bridge gaming experience into Web3' Badge"]

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
