import task

class SyncTask(task):

    def __init__(self, *remotes):
        '''Init this task with all of the remote tasks'''
        self.remote_tasks = []
        self.remote_tasks += remotes

        for task in self.remote_tasks:
            print # todo remote_tasks.a

    def reset_updated(self):
        '''resets the updated flag on all of the remote tasks'''
        for task in self.remote_tasks:
            self.updated = False

    def has_remote(self, remote_task):
        return remote_task in self.remote_tasks

    def has_stale_remotes(self):
        '''returns a bool indicating if any of the remotes are stale since the last update'''
        for task in self.remote_tasks:
            if task.updated == False:
                return True

        self.reset_updated()

        return False