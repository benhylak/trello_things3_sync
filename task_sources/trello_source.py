# todo make one file written per service. (remote source)
# remote source would be an object that has a bunch of remote tasks, handles new and deleted, assigning catgs, list names
# remote tasks just call their source for an update as needed

import trello

from task_sources.remote_source import RemoteSource

class TrelloSource(RemoteSource):

    def __init__(self, API_Key, API_Token, Board_ID):
        '''todo'''
        super(TrelloSource, self).__init__()

        self.client = trello.TrelloClient(
            api_key=API_Key,
            token=API_Token
        )

        self.board = self.client.get_board(Board_ID)

        for list_name in ('Inbox', 'Today', 'This Week', 'Later', 'Someday'):
            self.list_sources.append(self.get_list_by_name(list_name))

    def get_list_by_name(self, name, board=None):

        if board is None:
            board = self.board

        result = [x for x in board.all_lists() if x.name == name][0]
        return result

    def update(self):

        RemoteSource.update(self) # call before update, maybe good use for wrapper func

        for list in self.list_sources:
            print "Fetched " + list.name
            list.fetch()

        for list in self.list_sources:
            for card in list.list_cards():
                if card.id not in self._cache.keys():
                    self._cache[card.id] = card
                    self._newly_added.append(card)
                    print "New card: " + card.name

                self._seen_ids.append(card.id)

        RemoteSource._post_update_(self) # call after update

    def update_task(self, remote_task, fetch=False):
        '''update the remote task'''
        card = remote_task._data

        if fetch:
            card.fetch()  # updates from remote

        remote_task._uid = card.id
        remote_task.subject = card.name
        remote_task.notes = card.description
        remote_task.due_date = card.due_date
        remote_task.last_modified = card.date_last_activity

        # todo tell remote task that this source was updated