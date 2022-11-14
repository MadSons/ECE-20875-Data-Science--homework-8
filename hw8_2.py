import numpy as np
from helper import remove_punc
from hw8_1 import *
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
from nltk.corpus import stopwords


#   Clean and prepare the contents of a document
# Input:   a filename to read in and clean, string
# Return:    a single string, without stopwords, spaces, and punctuation
# NOTE:     Do not append any directory names to doc -- assume we will give you
#           a string representing a file name that will open correctly
def read_and_clean_doc(doc):
    # 1. Open document, read text into *single* string
    with open(doc, "r") as f:
        allStr = f.read()

    # 2. Filter out punctuation from list of words (use remove_punc)
    all_rm_punc = remove_punc(allStr)

    # 3. Make the words lower case
    all_lower = all_rm_punc.lower()

    # 4. Filter out stopwords
    tok_low = all_lower.split(" ")
    filt_tok = [tok for tok in tok_low if tok not in stopwords.words("english")]
    all_no_stop = "".join(filt_tok)
    
    return all_no_stop


#   Builds a doc-word matrix for a set of documents
# Input:     a *list of filenames* and a number *n* corresponding to the length of each ngram
#
# Returns:    1) a doc-word matrix for the cleaned documents
#   This should be a 2-dimensional numpy array, with one row per document and one
#   column per ngram (there should be as many columns as unique words that appear
#   across *all* documents. Also, Before constructing the doc-word matrix,
#   you should sort the list of ngrams output and construct the doc-word matrix based on the sorted list
#
#            2) a list of ngrams that should correspond to the columns in docword
#
def build_doc_word_matrix(doclist, n):
    # 1. Create the cleaned string for each doc (use read_and_clean_doc)
    docs = []
    for i in range(len(doclist)):
        docs.append(read_and_clean_doc(doclist[i]))
    # 2. Create and use ngram lists to build the doc word matrix
    doc_tokens = [] #list of doc ngrams
    for i in range(len(docs)):
        doc_tokens.append(get_ngrams(docs[i], n))
    
    # Creating the list of all ngrams in all documents, no repeats
    ngramlist = []
    for doc in doc_tokens:
        for ngram in doc:
            if(not(ngram in ngramlist)):
                ngramlist.append(ngram)
    ngramlist = sorted(ngramlist)  # sort ngrams alphabetically
    
    # Creating the doc-word matrix
    ngram_to_ind = {ngram:ind for ind, ngram in enumerate(ngramlist)} 
    docword = np.zeros((len(doc_tokens), len(ngramlist)))
    for doc, doc_vec in zip(doc_tokens, docword):
        for ngram in doc:
            ind = ngram_to_ind[ngram]
            doc_vec[ind] += 1
    
    return docword, ngramlist


#   Builds a term-frequency matrix
# Input:     a doc word matrix (as built in build_doc_word_matrix)
# Returns:    a term-frequency matrix, which should be a 2-dimensional numpy array with the same shape as docword
# HINTs:      You may find np.newaxis helpful
def build_tf_matrix(docword):
    row_sums = docword.sum(axis=1) # sum of each row
    tf = docword / row_sums[:, np.newaxis]
            
    return tf


#   Builds an inverse document frequency matrix
# Input:      a doc word matrix (as built in build_doc_word_matrix)
# Returns:    an inverse document frequency matrix
#            (should be a 1xW numpy array where W is the number of ngrams in the doc word matrix)
#            Don't forget the log factor!
def build_idf_matrix(docword):
    N = len(docword)
    num_doc_occur= np.count_nonzero(docword, axis=0) # number of docs each ngram occurs in
    idf = np.log10(N/num_doc_occur)
    
    return idf.reshape(1,-1)


#   Builds a tf-idf matrix given a doc word matrix
def build_tfidf_matrix(docword):
    tf = build_tf_matrix(docword)
    idf = build_idf_matrix(docword)
    tfidf  = tf*idf
    return tfidf


#   Find the three most distinctive ngrams, according to TFIDF, in each document
# Input:     a docword matrix, a wordlist (corresponding to columns) and a doclist (corresponding to rows)
# Output:    a dictionary, mapping each document name from doclist to an ordered
#           list of the three most unique ngrams in each document
def find_distinctive_ngrams(docword, ngramlist, doclist):
    # you might find numpy.argsort helpful for solving this problem:
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html
    # HINT: the smallest three of -docword correspond to largest 3 of docword
    distinctive_ngrams = {}

    # iterate through each document
    for i in range(len(doclist)):
        # make a dictionary mapping ngrams to the tfidf values of those ngrams
        ngram_scores = {}
        # iterate through each ngram
        for j in range(len(ngramlist)):
            ngram_scores[ngramlist[j]] = tfidf[i][j]
        # sort the list of ngrams by tfidf
        sorted_ngrams = sorted(ngram_scores.items(), key = lambda x:x[1], reverse = True)

        # add the first three ngrams to the distinctive_ngrams dictionary
        distinctive_ngrams[doclist[i]] = []
        for k in range(3):
            distinctive_ngrams[doclist[i]].append(sorted_ngrams[k][0])
    return distinctive_ngrams
    


if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join, splitext

    ### Test Cases ###
    directory = "lecs"
    path1 = join(directory, "1_vidText.txt")
    path2 = join(directory, "2_vidText.txt")

    print("*** Testing build_doc_word_matrix ***")
    doclist = [path1, path2]
    docword, wordlist = build_doc_word_matrix(doclist, 3)
    print(docword.shape)
    print(len(wordlist))
    print(docword[0][0:10])
    print(wordlist[0:10])
    print(docword[1][0:10])
    print("*** Testing build_tf_matrix ***")
    tf = build_tf_matrix(docword)
    print(tf[0][0:10])
    print(tf[1][0:10])
    print(tf.sum(axis=1))
    print("*** Testing build_idf_matrix ***")
    idf = build_idf_matrix(docword)
    print(idf[0][0:10])
    print("*** Testing build_tfidf_matrix ***")
    tfidf = build_tfidf_matrix(docword)
    print(tfidf.shape)
    print(tfidf[0][0:10])
    print(tfidf[1][0:10])
    print("*** Testing find_distinctive_words ***")
    print(find_distinctive_ngrams(docword, wordlist, doclist))
