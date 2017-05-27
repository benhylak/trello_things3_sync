import re
import datetime

pattern = re.compile(r'(?P<description>.*?)\n\nid: (?P<id>.*?)\n.*', flags=re.DOTALL | re.MULTILINE)

## todo: enum for list locations, map names to the enum in extending classes

# Seems like the Python scripting bridge does not support enum
# as they are non-introspectable types. We need to hardcode them
# See: https://developer.apple.com/library/Mac/DOCUMENTATION/Cocoa/Conceptual/ScriptingBridgeConcepts/AboutScriptingBridge/AboutScriptingBridge.html
status = {'Open': 1952737647, 'Completed': 1952736109, 'Cancelled': 1952736108}

def getStatusString(id):
    """Return the equivalent string"""
    for key, value in status.iteritems():
        if value == id:
            return key

    return ''


class Task(object):
    """Represent a task"""

    def __init__(self):

        self.id = ''
        self.name = ''
        self.description = ''
        self.status = ''
        self.dueDate = ''
        self.lastModifiedDate = datetime.time(0,0,0)
        self.notes = None

        self.main_attributes = ('name', 'description', 'status', 'dueDate', 'lastModifiedDate', 'notes')

    def modified_later_than(self, task):
        return self.lastModifiedDate > task.lastModifiedDate

    def set_attributes(self, task):
        '''sets most of the attributes of this task from another task (besides id)'''

        for attr_name in self.main_attributes:
            self.__setattr__(attr_name, task.__getattribute__(attr_name))
