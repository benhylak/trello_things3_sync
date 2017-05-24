# todo make one file written per service. (remote source)
# remote source would be an object that has a bunch of remote tasks, handles new and deleted, assigning catgs, list names
# remote tasks just call their source for an update as needed

from remote_source import RemoteSource
from Foundation import *
from ScriptingBridge import *

class ThingsSource(RemoteSource):

    def __init__(self):
        '''todo'''
        super(ThingsSource, self).__init__()

        self._app = SBApplication.applicationWithBundleIdentifier_("com.culturedcode.ThingsMac")

        for list_name in ('Inbox', 'Today', 'Upcoming', 'Anytime', 'Someday', 'Logbook'):
            self.list_sources.append(self._app.lists().objectWithName_(list_name))

    def update(self):

        RemoteSource.update(self) # call before update, maybe good use for wrapper func

        print 'Things updated!'

        for list in self.list_sources:
            for task in list.toDos():
                if task.id() not in self._cache.keys(): # todo 1) change task attrib to name rather than subject
                    self._cache[task.id()] = task
                    self._newly_added.append(task)
                    print "New task: " + task.name()

                self._seen_ids.append(task.id())

        RemoteSource._post_update_(self) # call after update

    def update_task(self, remote_task):
        '''update the remote task'''

        task = remote_task._data

        remote_task._uid = task.id()
        remote_task.subject = task.name()
        remote_task.notes = task.notes()
        remote_task.due_date = task.dueDate()
        remote_task.last_modified = task.modificationDate()
