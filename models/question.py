class Question(object):
    def __init__(self, question_id, url, title, tags_list, creation_date, service, up_vote_count = 0, down_vote_count = 0, answer_count = 0 ):
        self.question_id = question_id
        self.url = url
        self.title = title
        self.tags_list = tags_list
        self.creation_date = creation_date
        self.service = service
        self.up_vote_count = up_vote_count
        self.down_vote_count = down_vote_count
        self.answer_count = answer_count
    def get_votes(self):
        return '%s%d' % (['','+'][self.up_vote_count-self.down_vote_count > 0],self.up_vote_count-self.down_vote_count)
        