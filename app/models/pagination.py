SEPARATOR = "..."

class Pagination(object):
    def __init__(self, results):
        self.total = results.get('total',0)
        self.page = results.get('page',0)
        self.pagesize = results.get('pagesize',0)
        self.total_pages = 0 if self.total==0 else 1 if (self.total / self.pagesize == 0) else (self.total / self.pagesize) \
                             if (self.total % self.pagesize == 0) else (self.total / self.pagesize) + 1
        self.separator = SEPARATOR
        
    def has_more_entries(self):
        return (self.page < self.total_pages)
    def has_previous_entries(self):
        return (self.page > 1)
    def get_pretty_pagination(self):
        """
            Return a list of int representing page index like:
            [1, -1 , 6 ,  7 , 8 , -1 , 20]
            -1 is where separator will be placed
        """
        pagination = []
        if self.total_pages == 1:
            return pagination
        pagination.append(1)
        if self.page > 2:
            if ( self.total_pages > 3 and self.page > 3 ):
                pagination.append(-1)
            if self.page == self.total_pages and self.total_pages > 3 :
                pagination.append(self.page - 2)
            pagination.append(self.page - 1)
        if self.page != 1 and self.page != self.total_pages :
            pagination.append(self.page)
        if self.page < self.total_pages - 1 :
            pagination.append(self.page + 1)
            if  self.page == 1 and self.total_pages > 3:
                pagination.append(self.page + 2)
            if ( self.total_pages > 3 and self.page < self.total_pages - 2 ):
                pagination.append(-1)
        pagination.append(self.total_pages)
        return pagination    