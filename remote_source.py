from remote_task import *

class RemoteSource(object):

    def __init__(self):
        '''todo'''
        self._cache = {}
        self._newly_added = []
        self._newly_removed = []


    #def add_new(self, task): #todo add function for adding to remote
       # new_card = RemoteTask("", self)

    def update(self):

        self._newly_added = []
        self._newly_removed = []

        print "Started to update lists... Cache size: " + str(len(self._cache))

        '''Rest of function must be implemented'''

    def get_all_tasks(self):
        '''std remote source func'''
        '''returns all cards across all lists'''
        return self._cache

    def update_task(self, remote_task, fetch=False):
        '''abstract func. must be implemented'''

    def _post_update_(self):
        for id, card in self._cache.items():  # not seen in last update, so must be stale
            if card._updated is not True:  # todo: add safety net here
                self._newly_removed.append(card)
                print "Not seen on last update (deleting...): " + card.name
                del self._cache[id]
