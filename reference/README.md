Trello + Things 3
=================
### Get things done across platforms! ###

### Scripting Definitions ###
I've added the scripting definitions file to the project for reference: Things.sdef. This shows everything you can
do/access with ScriptingBridge. (For example, what parameters a task has) Parameters that have a space in the name
will have an underscore when they come into python. So for a task, the parameter "modification date" would be
task.modification_date in python.

### Config File: ###

Config file holds all of your sensitive information. Keep this stuff secret!

#### config.ini format: ####

[trello]<br />
api_key =  < your key here > <br />
api_token = < your token here > <br />
gtd_board = < board id here > <br />

To authorize yourself + get your own key/token, see here: https://developers.trello.com/authorize

## Why I built this ##

#### Here's something you already know: to do lists suck. ####

I've tried them all, and every app is either too complex or not complex enough.

I fell in love with Trello because it was flexible enough to handle every aspect of my life. From startup ideas to
reading lists, there's a place for it on Trello. Setting up a GTD (get things done) board on Trello has enabled me to
take control of my life for the first time.

#### I love Trello because: ####

*Amazing web interface
*Awesome keyboard short cuts
*Intuitive collaboration
*Flexible enough for every aspect of my life

#### but it's not perfect ####

*No tailored notifications
*NO, REALLY, THE ONLY OPTION IS 24 HOURS IN ADVANCE
*Mobile app is too complicated
*No way to quickly see tasks
*Marking a task as completed involves dragging it from one list to another -- not easy on mobile/iPad

You know what is good at those things? The newly released Things 3! It has a stunning mobile app and is simple to navigate.

#### Things 3 isn't perfect either... :( ####

*Can't handle collaboration
*Doesn't handle multimedia well
*Isn't flexible enough for my life
*"Areas" aren't as good as Trello's boards at separating information

So I thought... What if Trello could be a backend to Things 3? Something that I access less frequently, something that
I plan/schedule with, but throughout the day I work with Things 3?

#### Trello as a complex desktop backend, Things 3 as a simplified mobile viewer. ####

Harmony :)