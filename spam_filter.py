import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import string

from os import listdir
from os.path import isfile, join

stopwords = set(stopwords.words('english'))

spam_path = 'data/spam/'
easy_ham_path = 'data/easy_ham/'

def tokenize(message):
    
   	#using the default tokenizer
    all_tokens = wordpunct_tokenize(message.lower())

    return_tokens = [w for w in all_tokens if w not in stopwords and w not in string.punctuation]

    return return_tokens


def make_training_set(path):

    # map a training set 

    training_set = {}
    files = []

    # make an array that stores the path of all the files in the path
    # and keep track of the number of files

    for file in listdir(path): 
    	if isfile(join(path, file)): 
    		files.append(file)

    num_files = len(files)
    
    for file in files:

        # open the file and read it into one line
        with open(path + file, 'r') as mail: 
			message = mail.read()
        
        # tokenize the file
        terms = tokenize(message)
        
        # map the frequency of each word
        for term in terms:
            if term in training_set:
                training_set[term] = training_set[term] + 1
            else:
                training_set[term] = 1
    

    
    for word in training_set.keys():
        training_set[word] = float(training_set[word]) / num_files
                            
    return training_set

spam_training_set = make_training_set(spam_path)
ham_training_set = make_training_set(easy_ham_path)



def ham_or_spam(text, training_set, prior = 0.5, c = 3.7e-4): 
	"""
	Return the probability of the text being spam or ham, 
	based on the given data in the training_set.
	c is an experimentally obtained value.
	"""

	tokens = tokenize(text)

	probability = 1

	for token in tokens: 
		if token in training_set: 
			probability *= training_set[token]
		else: 
			probability *= c

	return probability * prior



if __name__ == "__main__": 


	mail_msg = raw_input('Enter the message to be classified:')
	print ''

	# train the spam and ham emails
	spam_probability = ham_or_spam(mail_msg, spam_training_set, 0.2)
	ham_probability = ham_or_spam(mail_msg, ham_training_set, 0.8)

	if spam_probability > ham_probability:
	    print ("Your mail has been classified as SPAM.")
	else:
	    print ("Your mail has been classified as HAM.")
















