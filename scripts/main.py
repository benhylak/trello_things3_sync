import time
from ConfigParser import SafeConfigParser

from task_sources.things_source import ThingsSource
from tasks.sync_task import SyncTask

from task_sources.trello_source import *
from tasks.remote_task import RemoteTask

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

        print "Here"

        things_source.update()
        trello_source.update()

        print "Remote Source Update Finished"

        print "Newly added: " + str(len(trello_source._newly_added))

        for task in trello_source._newly_added:

            task.update()

            things_task = RemoteTask.from_task(existing_task=task, remote_source=things_source)

            sync_task = SyncTask(task, things_task)

            main_cache.append(sync_task)

        for sync_task in main_cache:
            sync_task.update()

        time.sleep(3)