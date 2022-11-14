# Arguments:
#       filename: name of file to read in, string
# Returns: a list of strings, each string is one line in the file
#       that has no newlines, and has both a prefix and suffix of '__'
#       and all of the characters should be lowercase
# hints: (1) Consider using '.readlines()' (https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
#       (2) Consider using '.strip()' (https://docs.python.org/3/library/stdtypes.html#str.splitlines)
#       (3) Consider using '.lower()' to help you format all characters to lowercase.
def get_formatted_text(filename):
    lines = []

    with open(filename, "r") as f:
        lines = f.readlines()
        lines = ["__" + line.strip().lower() + "__" for line in lines]

    return lines


# Arguments:
#       line: a string of text, string
#       n : Length of each n-gram (think about it as the sliding window size), int
# Returns: a list of n-grams
# Notes: (1) make sure to pad the beginning and end of the string with '_';
#       (2) make sure to convert the string to lower-case, so "Hello" should be turned into "__hello__" before processing;
def get_ngrams(line, n):
    ngrams = []  # init a list

    N = len(line)
    L = n
    for k in range(N - L + 1):
        ngrams.append(line[k : k + L])

    return ngrams


# Arguments:
#       filename: the filename to create an n-gram dictionary for, string
#       n : Length of each n-gram, int
# Returns: a dictionary, with ngrams as keys, and frequency of that ngram as the value,
#           (the frequency is the number of times a key appears).
#
# Notes: Remember that get_formatted_text gives you a list of lines, and you want the ngrams from
#       all the lines put together. (So please use get_formatted_text and get_ngrams)
# Hint: (1) dict.fromkeys(k, 0) will initialize a dictionary with the keys in k and an initial value of 0,
#      k is an iterable specifying the keys of the new dictionary, it can be a list, tuple or a set;
#      (2) assuming set1 is a set, set1.add(k) can add an element k into set1 only if k does not exist in set1 previously;
#      (3) you can follow the step1,2,3 to help you fill the 'get_dict' function if you want.
def get_dict(filename, n):
    # 1. get lines and combine them to a set of keys
    lines = get_formatted_text(filename)
    ngrams = []
    for i in range(len(lines)):
        ngrams.extend(get_ngrams(lines[i], n))
    ngram_set = set(ngrams)

    # 2. use the set to initialize a dict
    ngram_dict = dict.fromkeys(ngram_set, 0)

    # 3. update the values of the dict
    for i in range(len(ngrams)):
        ngram_dict[ngrams[i]] += 1
    return ngram_dict


# Arguments:
#       filename: the filename to generate a list of top N (most frequent n-gram, count) tuples for, string
#       N: the number of most frequent n-gram tuples to have in the output list, int
#       n : Length of each n-gram, int
# Returns: a list of N tuples representing the (n-gram, count) pairs that are most common in the file.
#         It is highly recommended to sort by numerical value first, and for n-grams with the same count,
#         sort them by name within the sorted dict.
# For example
#         d = {'a':1,'b':4,'c':2,'d':1,'e':3} -> d = {'b':4,'e':3,'c':2,'a':1,'d':1}
#         To clarify, the first tuple in the list represents the most common n-gram,
#         the second tuple the second most common, etc...
# HINT:   (1) You may find the following StackOverflow post helpful for sorting a dictionary by its values:
#          https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
#         (2) Consider the dict method popitem()
#         (3) you can follow the step1,2 to help you fill the 'top_N_common' funtion if you want.
def top_N_common(filename, N, n):
    # 1. sort a dict
    ngram_dict = get_dict(filename, n)
    sorted_dict = {k: v for k, v in sorted(ngram_dict.items(), key=lambda item: (item[1], item[0]), reverse=False)}
    # 2. popitem
    common_N = []
    for i in range(N):
        common_N.append(sorted_dict.popitem())

    return common_N


########################################## Checkpoint, can test code above before proceeding #################################################


# Arguments:
#       filename_list: a list of filepath strings for the different language text files to process, list
#       n : Length of each n-gram, int
# Returns: a list of dictionaries where there is a dictionary for each language file processed. Each dictionary in the list
#       should have keys corresponding to the n-grams, and values corresponding to the count of the n-gram
# HINT:   (1) You should use the 'get_dict' function
def get_all_dicts(filename_list, n):
    lang_dicts = []

    for lang in filename_list:
        langDict = get_dict(lang, n)
        lang_dicts.append(langDict)

    return lang_dicts


# Arguments:
#     listOfDicts: A list of dictionaries where the keys are n-grams and the values are the count of the n-gram
# Returns:
#     An alphabetically sorted list containing all of the n-grams across all of the dictionaries in listOfDicts
# HINT:  (1) do not have duplicates n-grams)
#       (2) It is recommended to use the "set" data type when doing this (look up "set union", or "set update" for python)
#       (3) for alphabetically sorted, we mean that if you have a list of the n-grams altogether across all the languages,
#           and you call sorted() on it, that is the output we want
#       (4) you can follow the step1,2 to help you fill the 'dict_union' funtion if you want.
def dict_union(listOfDicts):
    # you can firstly initalize an empty set by: "union_ngrams = set()" and later convert it to a list
    union_ngrams = set()
    # 1. update the set by using set.update()
    for i in range(len(listOfDicts)):
        union_ngrams.update(set(listOfDicts[i]))

    # 2. sort the set by converting it to a list and then sort
    union_ngrams = sorted(list(union_ngrams))
    return union_ngrams


# Arguments:
#       langFiles: list of filepaths of the languages, list
#       n : Length of each n-gram, int
# Returns:
#       a list of all the n-grams across the six languages'
# HINT:  (1) please use the 'get_all_dicts' and 'dict_union' function
def get_all_ngrams(langFiles, n):
    all_ngrams = []
    all_ngrams = dict_union(get_all_dicts(langFiles, n))

    return all_ngrams


########################################## Checkpoint, can test code above before proceeding #############################################


# Arguments:
#       test_file: mystery file's filepath to determine language of
#       langFiles: list of filepaths of the languages to compare test_file to.
#       N: the number of top n-grams for comparison
#       n: length of n-gram, set to 3
# Returns:
#        the filepath of the language that has the highest number of top N matches that are similar to mystery file.
# HINT: (1) depending how you implemented top_N_common() earlier, you should only need to call it once per language,
#      and doing so avoids a possible error
#      (2) consider using the set method 'intersection()'
#
def compare_langs(test_file, langFiles, N, n=3):
    # 1. get mystery top N using 'top_N_common' function
    mystery_top_N = set([tup[0] for tup in top_N_common(test_file, N, n)])
    
    # 2. cardinalities of intersections, use 'intersection()' and 'top_N_common' function
    langs_top_N = []
    top_match = 0
    for i in range(len(langFiles)):
        langs_top_N.append(set([tup[0] for tup in top_N_common(langFiles[i], N, n)]))
        curr_match = mystery_top_N.intersection(langs_top_N[i])
        if len(curr_match) > top_match:
            top_match = len(curr_match)
            best_index = i
    lang_match = langFiles[best_index]
    return lang_match # it's a string


if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join, splitext

    # Test top20Common()
    path = join("ngrams", "english.txt")
    print(top_N_common(path, 20, 3))

    # Compile ngrams across all 6 languages and find the two most similar languages and their similarity score for various n-gram lengths

    path = "ngrams"
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    file_list.remove("mystery.txt")
    path_list = [join(path, f) for f in file_list]

    print(get_all_ngrams(path_list, 3))  # list of all 3-grams spanning all languages

    # Find the similarity between languages
    test_file = join(path, "mystery.txt")
    print(compare_langs(test_file, path_list, 20))  # determine language of mystery file
