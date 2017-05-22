# todo make one file written per service. (remote source)
# remote source would be an object that has a bunch of remote tasks, handles new and deleted, assigning catgs, list names
# remote tasks just call their source for an update as needed
from remote_task import *
import trello

class trello_source:

    def __init__(self):
        '''todo'''
        self._cache = []
        self._newly_added = []
        self._newly_removed = []

    def add_new(self):
        new_card = RemoteTask("", trello_source)

    def update(self):
        self._newly_added = []
        self._newly_removed = []

    def update_task(self, remote_task):
        '''update the remote task'''
        card = self._remote_source
        card.fetch()  # updates from remote

        self._uid = card.id
        self.subject = card.name
        self.notes = card.description
        self.due_date = card.due_date
        self.last_modified = card.date_last_activity

    def __eq__(self, other):
        if isinstance(other, trello.Card):  # "raw" trello card, from py-trello class
            return other.id is self._uid
       # elif isinstance(other, TrelloCard):  # Our custom trello class

        #    return RemoteTask.__eq__(self, other)  # use base class equality
                                                    # todo: determine if instance should be comp'd
