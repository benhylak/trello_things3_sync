from task import Task
from Foundation import *
from ScriptingBridge import *
import ScriptingBridge

things =   SBApplication.applicationWithBundleIdentifier_("com.culturedcode.ThingsMac")
inboxList = things.lists().objectWithName_('Inbox')
todayList = things.lists().objectWithName_('Today')
nextList = things.lists().objectWithName_('Upcoming')

def hasTag(todo, tagName):
    """Check if the todo has a specific tag"""
    for tag in todo.tags():
        if tag.name() == tagName:
            return True

    return False

def getInboxTasks():
    """Get all the tasks from things inbox"""

    inbox = []

    for raw_todo in inboxList.toDos():
        '''todo.setName_("Working! A lot!")'''

        if raw_todo.name().strip(): #not just whitespace
            todo = Task(todo=raw_todo)
        #print todo.description
            inbox.append(todo)
        #print todo.subject

    return inbox

def addTodo(task):
    """Create a new todo in Things"""
    properties = None
    if task.activityDate:
        date = NSDate.dateWithString_(task.activityDate + ' 04:00:00 +0000')
        properties = NSDictionary.dictionaryWithObjectsAndKeys_(task.subject, 'name',
                                                              #  task.expandedNote, 'notes',
                                                              #  date, 'dueDate',
                                                             #   None)
                                                                )
    else:
        properties = NSDictionary.dictionaryWithObjectsAndKeys_(task.subject, 'name',
                                                             #   task.expandedNote, 'notes',
                                                             #   None)
                                                                )

    todo = things.classForScriptingClass_('to do').alloc().initWithProperties_(properties)
    inboxList.toDos().addObject_(todo)
   # todo.setStatus_(task.statusId)


def modifyTodo(todo, task):
    if task.activityDate and task.activityDate != str(todo.dueDate())[:10]:
        date = NSDate.dateWithString_(task.activityDate + ' 04:00:00 +0000')
        todo.setDueDate_(date)

    if todo.name() != task.subject:
        todo.setName_(task.subject)

    if todo.status() != task.statusId:
        todo.setStatus_(task.statusId)

    todo.setNotes_(task.expandedNote)