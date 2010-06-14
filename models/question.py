class Question(object):
    def __init__(self, question_id, url, title, tags_list, creation_date, service ):
        self.question_id = question_id
        self.url = url
        self.title = title
        self.tags_list = tags_list
        self.creation_date = creation_date
        self.service = service