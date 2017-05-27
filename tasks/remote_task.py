from task import Task
from trello import Card

# from abc import ABCMeta #todo make this class abstract

class RemoteTask(Task):

    @staticmethod
    def from_task(existing_task, remote_source):
        result = remote_source.add_task(existing_task)
        id = result[0]
        data = result[1]

        return RemoteTask(id, data, remote_source)

    def __init__(self, id, data, remote_source):
        '''inits the remote task from an object representing some remote source'''
        Task.__init__(self)

        self._uid = id
        self._remote_source = remote_source
        self._data = data

        self.update(fetch=False)

    def get_uid(self):
        return self._uid

    def update(self, fetch=False):
        '''Every remote updates differently.'''
        '''For example, thing tasks don't know their list, so you have to check all of the lists for their uid to determine'''
        self._remote_source.update_task(self, fetch=False)

    def push_changes(self):
        self._remote_source.push_changes(self)

    def __eq__(self, other):
        if isinstance(other, Card):  # "raw" trello card, from py-trello class
            return other.id is self._uid
        elif isinstance(other, RemoteTask):
            return other.id == self.id
        else:
            return False

            #    return RemoteTask.__eq__(self, other)  # use base class equality
            # todo: determine if instance should be comp'd



