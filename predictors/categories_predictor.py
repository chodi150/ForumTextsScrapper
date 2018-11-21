import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from bs4 import BeautifulSoup

class CategoriesPredictor:

    def __init__(self, ):
        self.vectorizer = None
        self.model = None
        self.prepare_model()


    def prepare_model(self):
        data_df = pd.read_csv("config/tagstotal.csv", sep=';', header=None)
        data_df = data_df[np.isnan(data_df[1]) == False]
        values = np.array(data_df[0])
        vectorizer = TfidfVectorizer()
        vectorizer.fit_transform(values)
        vocab = vectorizer.vocabulary_
        self.vectorizer = TfidfVectorizer(vocabulary=vocab)
        bag = vectorizer.fit_transform(values)
        self.model = MultinomialNB().fit(bag, data_df[1])

    def prepare_input_array(self, response_body):
        soup = BeautifulSoup(response_body)
        a_tagged = soup.body.findAll('a')
        h2_tagged = soup.body.findAll('h2')
        h4_tagged = soup.body.findAll('h4')
        a_tagged.extend(h2_tagged)
        a_tagged.extend(h4_tagged)
        return np.array(a_tagged)

    def predict_categories(self, response_body, tag):
        input_array = list(self.prepare_input_array(response_body))
        input_array_str = list(map(lambda x: str(x), input_array))
        test_model = self.vectorizer.fit_transform(input_array_str)
        predicted = self.model.predict(test_model)
        value_predicted = dict(zip(input_array, predicted))
        return list(map(lambda x: x[0], list(filter(lambda x: x[1] == self.get_tag_value(tag), value_predicted.items()))))

    def get_tag_value(self, tag):
        if tag == "category":
            return 1
        if tag == "topic":
            return 2
        if tag == "post":
            return 3
1