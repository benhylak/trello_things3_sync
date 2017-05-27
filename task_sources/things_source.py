# todo make one file written per service. (remote source)
# remote source would be an object that has a bunch of remote tasks, handles new and deleted, assigning catgs, list names
# remote tasks just call their source for an update as needed

from task_sources.remote_source import RemoteSource
from Foundation import *
from ScriptingBridge import *
from PyObjCTools import Conversion
import objc
from tasks.remote_task import RemoteTask
import re

class ThingsSource(RemoteSource):


    def __init__(self):
        '''init'''

        self.names_to_status = {
            'Inbox': 'Inbox',
            'Today': 'Today',
            'Upcoming': 'Upcoming',
            'Anytime': 'Someday',
            'Someday': 'Someday',
        }

        super(ThingsSource, self).__init__()

        self._app = SBApplication.applicationWithBundleIdentifier_("com.culturedcode.ThingsMac")

        for list_name in self.names_to_status.keys():  # iterate over list names
            self.list_sources[list_name] = self._app.lists().objectWithName_(list_name)

    def update(self):

        RemoteSource._init_update_(self) # call before update, maybe good use for wrapper func

        for list_name, list in self.list_sources.items():
            for thing in list.toDos():
                if thing.name() is not None and len(thing.name()) > 0:
                    remote_task = None

                    print thing.modificationDate()

                    if thing.id() not in self._cache.keys():
                        print "New task: " + str(thing.name)  # todo 2) save list names somehow, or check what it belongs to? main cache doesn't work?
                        remote_task = self.add_to_cache(thing.id(), thing)

                    else:
                        remote_task = self._cache[thing.id()]
                        remote_task._data = thing  # updates the remote data it holds

                    remote_task.remote_list_name = list_name  # update list name
                    self.update_task(remote_task)

                    self._seen_ids.append(thing.id()) ## could be replaced with attribute of remote task

        RemoteSource._post_update_(self) # call after update

    def update_task(self, remote_task, fetch=False):
        '''update the remote task from data'''
        # todo implement fetch=true behavior

        task = remote_task._data

        remote_task._uid = task.id()
        remote_task.name = task.name()
        remote_task.notes = task.notes()
        remote_task.due_date = Conversion.pythonCollectionFromPropertyList(task.dueDate())
        remote_task.lastModifiedDate =  Conversion.pythonCollectionFromPropertyList(task.modificationDate()).time()

        try:
            remote_task.state = self.list_to_state(self.parse_list_name(task))
        except:
            print "Thing Task has no list info yet... Will fix on next refresh"

    def parse_list_name(self, data):

        matchObj = re.search(r" Things3List \"(.*?)\" of", str(data))
        return matchObj.group(1)

    def add_task(self, task):
        '''Add a new task to the remote'''

        print "Adding new task"

        properties = NSDictionary.dictionaryWithObjectsAndKeys_(task.name, 'name',
                                                                task.notes, 'notes',
                                                                task.lastModifiedDate, 'modificationDate'
                                                                #   None)
                                                                )
        todo = self._app.classForScriptingClass_('to do').alloc().initWithProperties_(properties)
        destination_list = self.get_list(self.status_to_names.get("Inbox")) #todo send proper state enum
        destination_list.toDos().addObject_(todo)

        return id, todo

    def push_changes(self, task):

        thing = task._data

        thing.setName_(task.name)
        thing.setNotes_(task.notes)
        thing.setDueDate_(task.due_date)
        thing.setModificationDate_(task.lastModifiedDate)

