import pandas as pd
from sklearn import tree
import numpy as np
from properties import mapping as m
from sklearn import preprocessing

class RuleProvider:

    def __init__(self):
        self.rules = None
        self.classifier = None
        self.possible_tags = None
        self.possible_tags_topics = None
        self.possible_tags_posts = None
        self.possible_classes = None
        self.class_encoder = preprocessing.LabelEncoder()
        self.tag_encoder = preprocessing.LabelEncoder()
        self.value_encoder = preprocessing.LabelEncoder()



    def initialize_rules(self):
        self.rules = pd.read_csv("config/rules.csv", sep=';', header=None, names = ['tag', 'class', 'value'])
        self.initialize_possible_elements()

        self.value_encoder.fit(m.all_mappings)
        self.rules['value'] = self.value_encoder.transform(self.rules['value'])

        self.tag_encoder.fit(self.rules["tag"])
        self.rules['tag'] = self.tag_encoder.transform(self.rules['tag'])

        classes_with_deleted_spaces = self.rules['class'].map(lambda a: a.replace(" ", ""))
        self.class_encoder.fit(classes_with_deleted_spaces)
        self.rules['class'] = self.class_encoder.transform(classes_with_deleted_spaces)

    def prepare_model(self):
        self.initialize_rules()
        self.classifier = tree.DecisionTreeClassifier()
        np_rules = np.array(self.rules)
        self.classifier.fit = self.classifier.fit(np_rules[:,0:2], np_rules[:,2])

    def predict(self, tag, classes):
        classes_as_string = "".join(classes)

        if classes_as_string.replace(" ", "") not in self.possible_classes:
            return max(self.value_encoder.transform(self.value_encoder.classes_)) + 1
        return self.classifier.predict([[self.tag_encoder.transform([tag])[0],
                                         self.class_encoder.transform([classes_as_string])[0]]])

    def initialize_possible_elements(self):
        self.possible_tags = set(self.rules['tag'])
        self.possible_tags_topics = set(self.rules[self.rules['value'].str.contains('topic')]['tag'])
        self.possible_tags_posts = set(self.rules[self.rules['value'].str.contains('post')]['tag'])
        classes_with_deleted_spaces = self.rules['class'].map(lambda a: a.replace(" ", ""))
        self.possible_classes = set(classes_with_deleted_spaces)


    def get_mapping(self, key):
        if key not in self.value_encoder.classes_:
            return max(self.value_encoder.transform(self.value_encoder.classes_)) + 1
        return self.value_encoder.transform([key])[0]