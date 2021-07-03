import os


VERSION = '1.0.0'
TOKEN = os.environ.get('TOKEN2')
LAVALINK = os.environ.get('LAVALINK')

# DEV_IDS allows the use of
# bot commands in any channel
DEV_IDS = [
    os.environ.get('DEV_ID'),
]

OWNER_PERMS = [
    2081422591,
]

BASIC_ROLE = 'Associate'

CATEGORY = 'pkbot channels'
GENERAL = 'pkb-general'
BROADCAST = 'pkb-broadcast'
LOG = 'pkb-modlog'

MESSAGES = {
    "on_guild_join":"",
    "on_member_join":"",
    "welcome_general_channel":"pkb-general channel created!\nThis channel is used to process PKB commands",
    "welcome_broadcast_channel":"pkb-broadcast channel created!\nThis channel is used to broadcast events like lottery drawings and achievements",
    "welcome_log_channel":"pkb-modlog channel created!\nThis channel is used to to log auto moderation activites"
}

WARNINGS = {
    "warning":"",
    "mute":"",
    "ban":""
}

DAILY_REWARD = 100
DAILY_MAX_STARS = 10
DAILY_ICON = '⭐'

POINTS_RATE = 100

LOTTO_MAX_TICKETS = 1
LOTTO_TICKET_PRICE = 100
LOTTO_DRAW_TIME = 1
