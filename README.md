# information-retrieval-system

The project is dedicated to crafting an information retrieval system tailored specifically for scientific exper-
iments. The system employs advanced web crawling techniques to collect data from designated scientific
experiment archive websites.
Following this, a rigorous pre-indexing process ensures the quality of the gathered data. By implementing
clustering methods, we tackle missing information issues and refine subject classification, resulting in a ro-
bust indexing phase. To enhance user interaction, we’ve developed a user-friendly interface that adheres to
fundamental design principles and incorporates essential visual elements.

2.1 Crawling
We conducted web crawling on three selected websites to gather information from their scientific experiments
archive sections. The chosen websites are as follows:
 https://www.experimentarchive.com/
 https://www.sciencebuddies.org/science-experiments?p=1
 https://stevespangler.com/experiments/
Our objective was to retrieve specific details from each site, focusing on the scientific experiments archive
section. The targeted information includes the experiment title, scientific topic (if available), a brief descrip-
tion/introduction, and a detailed explanation.

2.2 Pre-Indexing
Prior to advancing to the indexing phase, a pre-processing step is undertaken on the extracted documents.
This stage is crucial for ensuring that the data is clean and structured for effective indexing.

2.3 Clustering
In an effort to assign subjects to documents lacking this information, we employed the k-means clustering
method on all documents. The implementation utilized Python’s NLTK library for tokenization and the
scikit-learn library for clustering.

2.4 Indexing
For indexing, we utilized the DFIndexer and IndexFactory.of functions from the pyterrier framework.
We exploited the concatenation of the title, subject, description, and explanation fields to incorporate as
much information as possible into creating the index.
To set the retrieval function, we employed pyterrier’s BatchRetrieve function. BM25 model is used
to resolve queries. When a query is generated, this retrieval function is employed to rank and extract the
relevant documents from the indexing table.
