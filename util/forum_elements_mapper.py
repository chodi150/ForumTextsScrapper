from properties import mapping as m


class ForumElementsMapper:

    def __init__(self):
        self.mappings = dict()
        self.inverted_mappings = dict()
        self.tags = dict()
        self.classes = dict()
        self.mappings[m.category_whole] = 0
        self.mappings[m.category_title] = 1
        self.mappings[m.topic_whole] = 2
        self.mappings[m.topic_title] = 3
        self.mappings[m.topic_date] = 4
        self.mappings[m.topic_author] = 5
        self.mappings[m.post_whole] = 6
        self.mappings[m.post_body] = 7
        self.mappings[m.post_date] = 8
        self.mappings[m.post_author] = 9
        self.mappings[m.next_page] = 10
        self.mappings[m.next_page_link] = 11

        for key, value in self.mappings.items():
            self.inverted_mappings[value] = key

    def initialize_tag_mapper(self, arr):
        unique_tags = set(arr)
        i = 0
        for tag in unique_tags:
            self.tags[tag] = i
            i = i+1

    def initialize_class_mapper(self, arr):
        unique_classes = set(arr)
        i = 0
        for cl in unique_classes:
            self.classes[cl] = i
            i = i +1

    def get_mapping(self, key):
        if key not in self.mappings:
            return 12
        return self.mappings[key]