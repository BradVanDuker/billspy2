import re
from collections import defaultdict
from string import punctuation, digits, ascii_letters

import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

from Models.dataSource import DataSource
from Control.textCleaner import TextCleaner


class TrainingController:
    def __init__(self, datasource: DataSource):
        self.datasource = datasource
        self.vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

    def run(self, list_of_bill_ids, num_of_clusters):
        # get the data
        all_texts = []
        for bill_id in list_of_bill_ids:
            full_text = self.datasource.get(bill_id)
            # clean up the data
            if 'A BILL' in full_text:
                text = TextCleaner.get_bill_text(full_text)
            elif 'RESOLUTION' in full_text:
                text = TextCleaner.get_resolution_text(full_text)
            else:
                text = TextCleaner.get_act_text(full_text)
            all_texts.append(text)

        # find the clusters using kmeans
        clusters, model = self.find_clusters(all_texts, self.vectorizer, num_of_clusters)

        # sort the texts into their clusters
        texts = dict()
        for i, cluster in enumerate(model.labels_):
            print(f'{i}:  {cluster}')
            one_bill = all_texts[i]
            # todo replace with defaultdict
            if cluster not in texts.keys():
                texts[cluster] = one_bill
            else:
                texts[cluster] += one_bill

        # find the most frequent words in each cluster
        most_frequent_keywords = self.find_most_frequent_words(num_of_clusters, texts)
        print(most_frequent_keywords)
        return most_frequent_keywords

    @staticmethod
    def find_clusters(all_texts, vectorizer, num_of_clusters):
        X = vectorizer.fit_transform(all_texts)
        kmeans = KMeans(n_clusters=num_of_clusters, init='k-means++', max_iter=100, n_init=1)
        estimator = kmeans.fit(X)
        clusters = np.unique(kmeans.labels_, return_counts=True)
        # print(clusters)
        return clusters, estimator

    @staticmethod
    def get_stopwords():
        other_stopwords = ['--', '``', 'section', 'shall', 'act', "''", 'paragraph',
                          'united', 'states', 'code', 'may', 'subsection', 'state', 'following',
                          'mr.', 'ms.', 'mrs.', 'whereas', 'congress', '2020', 'government', "'s",
                          'sec', 'described', 'date', 'program', 'title', 'described', 'including',
                          'subparagraph', 'amended']
        other_stopwords.extend(list(digits))
        other_stopwords.extend(list(punctuation))
        other_stopwords.extend(list(ascii_letters))
        other_stopwords.extend(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'])

        stopwords_ = set(stopwords.words('english') + other_stopwords)

        return stopwords_



    def find_most_frequent_words(self, num_of_clusters, cluster_text_dict: dict[int, str]):
        stopwords_ = self.get_stopwords()
        keywords = dict()
        counts = dict()

        # for each cluster, find the top 100 most frequently used words and their counts
        for cluster_num in range(num_of_clusters):
            words_in_sentence = word_tokenize(cluster_text_dict[cluster_num].lower())
            words_in_sentence = [word for word in words_in_sentence if word not in stopwords_]
            freq = FreqDist(words_in_sentence)
            keywords[cluster_num] = nlargest(100, freq, key=freq.get)
            counts[cluster_num] = freq

        # find the top keywords unique to each cluster
        unique_keywords = dict()
        for cluster_num in range(num_of_clusters):
            # collect keywords present in other clusters
            # other_clusters = list(set(range(num_of_clusters)) - {cluster_num})
            # keys_other_clusters = set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
            unique = set(keywords[cluster_num])
            for i in range(num_of_clusters):
                if i != cluster_num:
                    unique = unique - set(keywords[i])
            unique_keywords[cluster_num] = nlargest(20, unique, key=counts[cluster_num].get)
        return unique_keywords