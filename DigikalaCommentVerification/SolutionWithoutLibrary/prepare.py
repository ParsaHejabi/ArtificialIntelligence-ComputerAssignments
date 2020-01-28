import pandas
import re

NUM_OF_TRAIN_COMMENTS = 180000
NUM_OF_TEST_COMMENTS = 18000

train_comments = pandas.read_csv('Files/train.csv', index_col='id')
# concat title and comment into new column
train_comments['full_comment'] = train_comments['title'] + ' ' + train_comments['comment']
train_comments['full_comment'] = train_comments['full_comment'].astype(str)
train_comments = train_comments.drop(columns=['rate'])

test_comments = pandas.read_csv('Files/test.csv', index_col='id')
# concat title and comment into new column
test_comments['full_comment'] = test_comments['title'] + ' ' + test_comments['comment']
test_comments['full_comment'] = test_comments['full_comment'].astype(str)
test_comments = test_comments.drop(columns=['rate'])

test_comments['verification_status'] = 0

spam_comments = train_comments[train_comments.verification_status == 1]
ham_comments = train_comments[train_comments.verification_status == 0]

num_of_spam_train = len(spam_comments)
num_of_ham_train = len(ham_comments)

# probability if a comment is ham
probability_of_being_ham = num_of_ham_train / len(train_comments)

# probability if a comment is spam
probability_of_being_spam = num_of_spam_train / len(train_comments)

word_dictionary = dict()
ham_word_dictionary = dict()
spam_word_dictionary = dict()

# not unique words in spam comments
num_of_words_in_spam_comments = 0
# not unique words in ham comments
num_of_words_in_ham_comments = 0

for index, row in train_comments.iterrows():
    print(index)
    full_comment = row['full_comment'].split()
    for word in full_comment:
        # Take out emails, urls and numbers from words
        if re.match(r'^[-+]?[0-9]+$', word) or re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', word) or re.match(
                r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{'
                r'|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\['
                r'\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*['
                r'a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4]['
                r'0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]['
                r'0-9]?|[a-z0-9-]*[a-z0-9]:(?:['
                r'\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\['
                r'\x01-\x09\x0b\x0c\x0e-\x7f])+)\])', word) or re.match(r'[.!?\\-]', word):
            continue
        # number of occurrences of each word in ham comments
        else:
            if row.verification_status == 0:
                ham_word_dictionary[word] = ham_word_dictionary.get(word, 0) + 1
                num_of_words_in_ham_comments += 1
            else:
                spam_word_dictionary[word] = spam_word_dictionary.get(word, 0) + 1
                num_of_words_in_spam_comments += 1
        word_dictionary[word] = word_dictionary.get(word, 0) + 1

# unique words or V
num_of_unique_words_in_train_comments = len(word_dictionary.keys())

for index, row in test_comments.iterrows():
    print(index)
    full_comment = row['full_comment'].split()
    ham_probability = probability_of_being_ham
    spam_probability = probability_of_being_spam
    for word in full_comment:
        # Take out emails, urls and numbers from words
        if re.match(r'^[-+]?[0-9]+$', word) or re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', word) or re.match(
                r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{'
                r'|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\['
                r'\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*['
                r'a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4]['
                r'0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]['
                r'0-9]?|[a-z0-9-]*[a-z0-9]:(?:['
                r'\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\['
                r'\x01-\x09\x0b\x0c\x0e-\x7f])+)\])', word) or re.match(r'[.!?\\-]', word):
            continue
        # number of occurrences of each word in ham comments
        else:
            if word_dictionary.get(word, 0) == 0:
                continue
            else:
                ham_probability *= ((ham_word_dictionary.get(word, 0) + 1) / (
                        num_of_words_in_ham_comments + num_of_unique_words_in_train_comments))
                spam_probability *= ((spam_word_dictionary.get(word, 0) + 1) / (
                        num_of_words_in_spam_comments + num_of_unique_words_in_train_comments))
    if ham_probability > spam_probability:
        test_comments.loc[index, 'verification_status'] = 0
    else:
        test_comments.loc[index, 'verification_status'] = 1

test_comments = test_comments.drop(['title', 'comment', 'full_comment'], 1)
test_comments.to_csv(
    r'/Users/parsahejabi/University/Term7/Artificial '
    r'Intelligence/Homeworks/ComputerAssignments/Projects/DigikalaCommentVerification/SolutionWithoutLibrary/ans.csv')
