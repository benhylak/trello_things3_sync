from task import Task
# from abc import ABCMeta #todo make this class abstract

class RemoteTask(Task):

    def __init__(self, id, remote_source):
        '''inits the remote task from an object representing some remote source'''
        Task.__init__(self)
        self._uid = id
        self._remote_source = remote_source

    def get_uid(self):
        return self._uid

    def update(self):
        '''Every remote updates differently.'''
        '''For example, thing tasks don't know their list, so you have to check all of the lists for their uid to determine'''
        self._remote_source.update_task(self)


