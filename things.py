from task import Task
from Foundation import *
from ScriptingBridge import *
import ScriptingBridge


def hasTag(todo, tagName):
    """Check if the todo has a specific tag"""
    for tag in todo.tags():
        if tag.name() == tagName:
            return True

    return False

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