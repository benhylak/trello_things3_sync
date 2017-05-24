class RemoteSource(object):

    def __init__(self):
        '''todo'''
        self._cache = {}
        self._newly_added = []
        self._newly_removed = []
        self._seen_ids = []
        self.list_sources = []

    #def add_new(self, task): #todo add function for adding to remote
       # new_card = RemoteTask("", self)

    def update(self):

        self._newly_added = []
        self._newly_removed = []
        self._seen_ids = []

        print "Started to update lists... Cache size: " + str(len(self._cache))

        '''Rest of function must be implemented'''

    def get_all_tasks(self):
        '''std remote source func'''
        '''returns all cards across all lists'''
        return self._cache

    def update_task(self, remote_task, fetch=False):
        '''abstract func. must be implemented'''

    def _post_update_(self):

        to_delete = []

        for id in self._cache:
            if id not in self._seen_ids:  # not seen in last update, so must be stale
                to_delete.append(id)

        for id in to_delete:
            del self._cache[id]
            print "Deleted " + id

