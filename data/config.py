# api id, hash
API_ID = 1488
API_HASH = 'abcde1488'


ADD_TASK = []
# "TASK" - Complete tasks and collect tickets for every 3 tasks
# "CLAIM_TICKET" -Collect a ticket every 8 hours
# "CLAIM_REFF" - Collect a ticket for referrals
# "CLAIM_BANANA" - Unpacking tickets in BANANA
# "CLICK_BANANA" - Clicking points

WHILE = True  # True / False (constant turning on and off of the work cycle)

TIME_WHILE = [400, 450]  # if WHILE is equal to True, then we set the cycle time in minutes

DELAYS = {
    "ACCOUNT": [10, 20],  # delay at the start
    "RELOGIN": [20, 30],  # reconnection delay
    'FUNC': [120, 180],  # The delay between actions to avoid IP ban should not be less than 60 seconds
    'TASK': [60, 80],  # delay after completed the task
}
# Important: It is not recommended to reduce the specified delay values, as this may lead to account bans.
# Reducing the delay times increases the suspiciousness of activity, which could trigger sanctions from the system.


# blacklist tasks
BLACKLIST_TASK = ['Bind CARV ID', 'CARV Newbie SBT On CARV Mobile', 'Complete any quest in Infinite Play Mobile',
                  'Bind TON Wallet', 'Bind Your Email', 'Bind Your X', 'TG Premium Verify',
                  "CARV 'CARV Pass Cyber Pioneers' Badge", "CARV 'CARV Quiz Challenge' Badge",
                  "CARV 'Bridge gaming experience into Web3' Badge"]

PROXY = {
    "TYPE": {
        "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
