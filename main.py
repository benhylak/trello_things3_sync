from ConfigParser import SafeConfigParser

from remote_task import RemoteTask
from trello_source import *
from things_source import ThingsSource

import time

if __name__ == "__main__":

    config = SafeConfigParser()
    config.read('config.ini')

    TRELLO_API_KEY = config.get('trello', 'api_key')  # todo: pass these into the trello remote source
    TRELLO_TOKEN = config.get('trello', 'api_token')
    GTD_BOARD = config.get('trello', 'gtd_board')

    trello_source = TrelloSource(TRELLO_API_KEY, TRELLO_TOKEN, GTD_BOARD)
    things_source = ThingsSource()

    main_cache = []

    while(True):
        trello_source.update()
        things_source.update()

        for task in things_source._newly_added:
            t = RemoteTask(task.id, task, things_source)
            t.update()

            print t.subject

            main_cache.append(t)

        for card in trello_source._newly_added:
            t = RemoteTask(card.id, card, trello_source)
            t.update()

            print t.subject

            main_cache.append(t)

        print len(main_cache)


        time.sleep(3)