from trello import TrelloClient
import datetime
import time
import task as TaskLib
import things
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

TRELLO_API_KEY = config.get('trello', 'api_key')
TRELLO_TOKEN = config.get('trello', 'api_token')
GTD_BOARD = config.get('trello', 'gtd_board')

today_cache = {}
later_cache = []
completed_cache = []

last_check = None

client = TrelloClient(
    api_key= TRELLO_API_KEY,
    token=TRELLO_TOKEN
)

board = client.get_board(GTD_BOARD)

def get_list_by_name(board, name):
    result = [x for x in board.all_lists() if x.name == name][0]
    return result

lists = ('Inbox', 'Today', 'This Week', 'Later')

today_list = get_list_by_name(board, 'Today')

def update_from_trello():
    for card in today_list.list_cards():
        if card.name not in today_cache:
            today_cache[card.name] = card

            task = TaskLib.Task()
            task.subject = card.name

            things.addTodo(task=task)

            print card

        today_cache[card.name]._updated = True

    for card in today_cache.values():
        if(not card._updated):
            del today_cache[card.name]
            print 'Removed from cache ' + card.name

def update_from_things():
    for task in things.getTasks():
        if task.subject not in today_cache:  #
            today_cache[task.subject] = task  #
            get_list_by_name(board, 'Today').add_card(task.subject())

            ##add to trello                    #

        today_cache[task.subject]._updated = True

    for task in today_cache.values():
        if (not task._updated):
            del today_cache[task.subject]
            for card in get_list_by_name(board, 'Today'):
                if card.name is task.subject:
                    card.get_list_by_name(board, 'Done')

            print 'Removed from cache ' + task.subject


while (True):

    for card in today_cache.values():
        card._updated = False

    update_from_trello()

    time.sleep(3)
