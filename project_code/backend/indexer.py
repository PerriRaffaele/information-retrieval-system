import pyterrier as pt
import pandas as pd
import re

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('punkt')

import sklearn
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer


# DEFINING HELPER FUNCTIONS

def get_exp_title(docid):
  id = int(docid[1:])
  return exp_title[id]

def get_exp_link(docid):
  id = int(docid[1:])
  return exp_link[id]

def get_exp_description(docid):
  id = int(docid[1:])
  return exp_desc[id]

def get_exp_subject(docid):
  id = int(docid[1:])
  return exp_subj[id]

def get_exp_explanation(docid):
  id = int(docid[1:])
  return exp_expl[id]

def retrieve_exp(df):
  title = []
  link = []
  desc = []
  subject = []
  explanation = []
  for i in range(df.shape[0]):
    docid = df.loc[i, 'docno']
    title.append(get_exp_title(docid))
    link.append(get_exp_link(docid))
    desc.append(get_exp_description(docid))
    subject.append(get_exp_subject(docid))
    explanation.append(get_exp_explanation(docid))
  df['title'] = title
  df['link'] = link
  df['description'] = desc
  df['subject'] = subject
  df['explanation'] = explanation
  return df

# CLUSTERING HELPER FUNCTIONS
def apply_stem(text, stemmer):
  words = word_tokenize(text)
  stemmed_text = ' '.join([stemmer.stem(word) for word in words])
  return stemmed_text

# Start pyterrier
if not pt.started():
  pt.init()


# Get and merge all json files
docs_df = pd.read_json("./science_experiments/experiment_archive.json")

docs_df_2 = pd.read_json("./science_experiments/steve_spangler.json")
docs_df_3 = pd.read_json("./science_experiments/science_buddies.json")

docs_df = pd.concat([docs_df, docs_df_2], ignore_index=True)
docs_df = pd.concat([docs_df, docs_df_3], ignore_index=True)
docs_df = docs_df.loc[docs_df["explanation"] != ""]
docs_df = docs_df.loc[docs_df["title"] != ""]
docs_df = docs_df.fillna('')

docs_df = docs_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


docno = ['d'+ str(i) for i in range(docs_df.shape[0])]
docs_df['docno'] = docno

docs_df['text'] = docs_df['title'] + ' ' + docs_df['subject'] + ' ' + docs_df['explanation']

# CLUSTERING

doc_ids = docs_df['docno'].tolist()
texts = docs_df['text'].str.lower()

subjects = docs_df['subject'].unique().tolist()

stemmer = PorterStemmer()
stemmed_text = [apply_stem(str(text), stemmer) for text in texts]

tfidf = TfidfVectorizer(stop_words='english', lowercase = True, max_df = .9, min_df = 0.01, max_features = 1000)

X = tfidf.fit_transform(stemmed_text)

# K-Means
n_clusters = len(subjects) #set the number of clusters that you want
kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(X)

clustering_labels = kmeans.labels_ #clustering labels
km_lab = kmeans.labels_

docs_df['cluster'] = km_lab

modified_docs_df = docs_df[docs_df['subject'] != '']  # remove empty subjects' rows
cluster_df = modified_docs_df.groupby(['cluster'])['subject'].agg(lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
founded_clusters = cluster_df['cluster'].tolist()

# IF NOT ABLE TO FIND THE CLUSTER, ASSIGN IT TO GENERAL SCIENCE
missing_clusters = [i for i in range(n_clusters) if i not in founded_clusters]
miss_clus_subj = ['General Science'for i in range(len(missing_clusters))]
d = {'cluster': missing_clusters, 'subject': miss_clus_subj}
missing_df = pd.DataFrame(d)

cluster_df = pd.concat([cluster_df, missing_df], ignore_index=True)

# ASSIGN CLUSTER SUBJECT ONLY WHERE SUBJECT IS MISSING
empty_subject_mask = docs_df['subject'] == ''
docs_df.loc[empty_subject_mask, 'subject'] = docs_df.loc[empty_subject_mask, 'cluster'].map(cluster_df.set_index('cluster')['subject'])



# INDEXING
docs_df['text'] = docs_df['title'] + ' ' + docs_df['subject'] + ' ' + docs_df['explanation']

exp_title = docs_df.title.values
exp_link = docs_df.link.values
exp_desc = docs_df.description.values
exp_subj = docs_df.subject.values
exp_expl = docs_df.explanation.values

# index every science experiment
indexer = pt.DFIndexer("./index_3docs", overwrite=True)
index_ref = indexer.index(docs_df['text'], docs_df['docno'])
index = pt.IndexFactory.of(index_ref)

# define retrieval function
br = pt.BatchRetrieve(index, wmodel="BM25")

