import re
from datetime import datetime

pattern = re.compile(r'(?P<description>.*?)\n\nid: (?P<id>.*?)\n.*', flags=re.DOTALL | re.MULTILINE)

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

    def __init__(self, todo=None, card=None):
        super(Task, self).__init__()

        self.id = ''
        self.subject = ''
        self.description = ''
        self.status = ''
        self.activityDate = ''
        self.lastModifiedDate = ''
        self.todo = None
        self.modified = False

        if card:
            self.loadFromCard(card)

        if todo:
            self.loadFromTodo(todo)

    def loadFromTodo(self, todo):
        """ init from a Things todo"""

        self.subject = todo.name()
        self.status = getStatusString(todo.status())
        self.activityDate = str(todo.dueDate())[:10] if todo.dueDate() else None

        try:
            self.lastModifiedDate = datetime.strptime(str(todo.modificationDate())[:-6], '%Y-%m-%d %H:%M:%S')
        except:
            print "Date error"

    def loadFromCard(self, card):
        """not implemented"""
