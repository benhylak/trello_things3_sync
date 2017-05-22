from trello import TrelloClient
import datetime
import time
import task as TaskLib
import things
from ConfigParser import SafeConfigParser

  # update status: deleted, date, moved, notes, name
  # one lists of task. each task has a catg. just if tasks doesn't contain this card add it.
  # otherwise, update all of the tasks individ
  # removes dependency on setup + services?

# future flow:

# for each of my remote sources
# update them

# for any newly added in both, add them.
# don't handle removal here tho

# for each of my sync tasks
# check mod date to see if info needs updating
# if catg changed, move remote_tasks as appropriate
# if remote is deleted (archived or in log), delete other remotes
#           todo: handle cards from trello that have been legit deleted? or just don't do that?

config = SafeConfigParser()
config.read('config.ini')

TRELLO_API_KEY = config.get('trello', 'api_key')  #todo: pass these into the trello remote source
TRELLO_TOKEN = config.get('trello', 'api_token')
GTD_BOARD = config.get('trello', 'gtd_board')

today_cache = {}  #todo: change to just one cache for all sync tasks e
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
