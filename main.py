from trello_source import *
import time

if __name__ == "__main__":

    config = SafeConfigParser()
    config.read('config.ini')

    TRELLO_API_KEY = config.get('trello', 'api_key')  # todo: pass these into the trello remote source
    TRELLO_TOKEN = config.get('trello', 'api_token')
    GTD_BOARD = config.get('trello', 'gtd_board')

    t_source = TrelloSource(TRELLO_API_KEY, TRELLO_TOKEN, GTD_BOARD)
    main_cache = []

    while(True):
        t_source.update()


        for card in t_source._newly_added:
            t = RemoteTask(card.id, card, t_source)
            t.update()

            print t.subject

            main_cache.append(t)

        print len(main_cache)


        time.sleep(3)