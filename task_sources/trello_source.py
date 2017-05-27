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

        for list_name in ('Inbox', 'Today', 'Someday', 'Later', ):
            self.list_sources[list_name] = self.get_list_by_name(list_name)

    def get_list_by_name(self, name, board=None):

        if board is None:
            board = self.board

        result = [x for x in board.all_lists() if x.name == name][0]
        return result

    def update(self):

        RemoteSource._init_update_(self) # call before update, maybe good use for wrapper func

        for list_name, list in self.list_sources.items():

            print "Fetched " + list_name
            list.fetch()

            for card in list.list_cards():
                if card.name is not None:
                    remote_task = None

                    if card.id not in self._cache.keys():
                        remote_task = self.add_to_cache(card.id, card)
                        print "New task: " + remote_task.name  # todo 2) save list names somehow, or check what it belongs to? main cache doesn't work?

                    else:
                        remote_task = self._cache[card.id]
                        remote_task._data = card # updates the remote data it holds

                    remote_task.remote_list_name = list_name  # update list name


       # self._seen_ids_new = [card.id for list in self.list_sources.values()
        #                          for card in list.list_cards()]

#        self._newly_added_new = {card.id : card for list in self.list_sources.values()
 #                                           for card in list.list_cards()
  #                                          if card.id not in self._cache.keys()}

   #     self._cache.update(self._newly_added)

        for list in self.list_sources.values():
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
        remote_task.name = card.name
        remote_task.notes = card.description
        remote_task.due_date = card.due_date
        remote_task.lastModifiedDate = card.date_last_activity.time()

        # todo tell remote task that this source was updated