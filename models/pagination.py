class Pagination(object):
    def __init__(self, results):
        self.total = results.get('total',0)
        self.page = results.get('page',0)
        self.pagesize = results.get('pagesize',0)
    def has_more_entries(self):
        return (self.pagesize * self.page < self.total)
    def has_previous_entries(self):
        return (self.page > 1)    