class ForumElement:
    def __init__(self, id, content, link, subcategories=None, topics=None):
        if topics is None:
            topics = []
        if subcategories is None:
            subcategories = []
        self.content = content
        self.link = link
        self.id = id
        self.subcategories = subcategories
        self.topics = topics

class Post():
    def __init__(self, id, content, date, author):
        self.content = content
        self.id = id
        self.date = date
        self.author = author

class Topic(ForumElement):
    def __init__(self, id, content, link, date, author, number_of_posts):
        ForumElement.__init__(self, id, content, link)
        self.content = content
        self.link = link
        self.id = id
        self.date = date
        self.author = author
        self.number_of_posts = number_of_posts