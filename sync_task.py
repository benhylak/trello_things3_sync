from task import Task

class SyncTask(Task):

    def __init__(self, *remotes):
        '''Init this task with all of the remote tasks'''
        self.remote_tasks = []
        self.remote_tasks += remotes

        for task in self.remote_tasks:
            print # todo remote_tasks.a

    def use_attrs(self, task):
        '''Use attributes: Takes all of the attributes from a different task and assigns them to self.'''
        self.id = task.id
        self.description = task.description
        self.subject = task.subject
        self.lastModifiedDate = task.lastModifiedDate

        ## todo: fill out rest of attributes

        #if classification changed, handle appropriately and send to both of my remotes. event goes h

    def update(self):
       ## todo: updating each task from remote (trello) may be more costly then together as a list
        for remote in self.remote_tasks:
            remote.update()

            if remote.lastModifiedData > self.lastModifiedDate:
                self.use_attrs(remote)


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