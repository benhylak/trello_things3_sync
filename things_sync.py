import time
import things

today_cache = {}

while (True):

    for task in today_cache.values():
        task._updated = False

    for task in things.getInboxTasks():
        if task.subject not in today_cache:

            today_cache[task.subject] = task

            #task = task.Task.__init__()
            #task.subject = card.name
            #things.addTodo(task=task)
            print "Added todo to cache: " + task.subject

        today_cache[task.subject]._updated = True

    for task in today_cache.values():
        if (not task._updated):
            del today_cache[task.subject]
            print 'Removed from cache ' + task.subject

    time.sleep(3)