from task import Task
import datetime

class SyncTask(Task):

    def __init__(self, *remotes):
        '''Init this task with all of the remote tasks'''
        super(SyncTask, self).__init__()
        self.remote_tasks = []

        for arg in remotes:
            print arg
            self.remote_tasks.append(arg)

        for task in self.remote_tasks:
            print task.name

        self.update()

    def update_from(self, task):
        '''Use attributes: Takes all of the attributes from a different task and assigns them to self.'''
        # self.id = task.id -- might make sense
        self.description = task.description
        self.name = task.name
        self.lastModifiedDate = task.lastModifiedDate

        ## todo: fill out rest of attributes

    def sync_changes(self):
        for remote in self.remote_tasks:
            remote.set_attributes(self)
            remote.push_changes()

    def update(self, fetch_latest = False):
       ## todo: updating each task from remote (trello) may be more costly then together as a list

        if fetch_latest:
            for remote in self.remote_tasks:
                remote.update()

        latestUpdate = self

        for remote_task in self.remote_tasks:
            if remote_task.modified_later_than(latestUpdate):
                latestUpdate = remote_task

        if latestUpdate is not self:
            self.update_from(latestUpdate)
            self.sync_changes()

    def reset_updated(self):
        '''resets the updated flag on all of the remote tasks'''
        for task in self.remote_tasks:
            self.updated = False

    def has_remote(self, remote_task):
        # todo should compare by uid of card/task/whatever
        return remote_task in self.remote_tasks

    def has_stale_remotes(self):
        '''returns a bool indicating if any of the remotes are stale since the last update'''
        for task in self.remote_tasks:
            if task.updated == False:
                return True

        self.reset_updated()

        return False