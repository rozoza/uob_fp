from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Input
from keras.layers import Embedding, LSTM, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.preprocessing import text
import numpy as np
import csv

def get_data(filename, X, Y):
    with open(filename, "r") as infile:
        reader = csv.DictReader(infile)
        
        #for quick testing
        # cnt = 0
        for row in reader:
            if row['agree'] == 'no match' or row['role'] == '<prep-date>'\
            or row['role'] == '<sub-heading>' or row['role'] == '<separator>' or row['role'] == '<new-case>':
                continue
            X = np.append(X, [row["text"]])

            if row["align"] == "NONE":
                Y = np.append(Y, [0])
            else: 
                Y = np.append(Y, [1])
            # cnt += 1
            # if cnt == 100:
            #     break

        return X, Y

def clean_stopwords(sentence):
    tmp_sent = []
    for token in sentence:
        if token not in stop_words:
            tmp_sent.append(token)
    return tmp_sent
                    
def store_paddedtokens(padded_docs):
    with open('comsum_wordembed.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        for row in padded_docs:
            writer.writerow(row)


X = np.array([])
Y = np.array([], dtype="int16")
filename = "complete_sum.csv"

X, Y = get_data(filename, X, Y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    Y, 
                                                    shuffle=True, 
                                                    test_size = .1, 
                                                    random_state=1000, 
                                                    stratify=Y)

# from nltk import word_tokenize
# X = [word_tokenize(i) for i in X]

# from nltk.corpus import stopwords
# stop_words = stopwords.words("english")
# X = [clean_stopwords(i) for i in X]

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

t = Tokenizer()
t.fit_on_texts(X_train)
# t.fit_on_texts(X)
vocab_size = len(t.word_index) + 1
encoded_X_train = t.texts_to_sequences(X_train)
encoded_X_test = t.texts_to_sequences(X_test)
# encoded_docs = t.texts_to_sequences(X)
max_length = max([len(i) for i in encoded_X_train])
# len_X_train = [len(i) for i in encoded_X_train]
# len_X_test = [len(i) for i in encoded_X_test]
# len_X_docs = [len(i) for i in encoded_docs]
from statistics import mean
# maxlength_X_train = int(mean(len_X_train))
# maxlength_X_test = int(mean(len_X_test))
maxlength_X_train = None
maxlength_X_test = None
# maxlength= None
padded_X_train = pad_sequences(encoded_X_train, maxlen=maxlength_X_train, padding="post")
padded_X_test = pad_sequences(encoded_X_test, maxlen=maxlength_X_test, padding="post")
# padded_docs = pad_sequences(encoded_docs, maxlen=maxlength, padding="post")

# store_paddedtokens(padded_docs)

embeddings_index = dict()
f = open("word2vec.6B.100d.txt", encoding="utf8")
# f = open("./glove.6B/glove.6B.100d.txt")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype="float32")
    embeddings_index[word] = coefs
f.close()

embedding_matrix = np.zeros((vocab_size, 100))
for word, i in t.word_index.items():
	embedding_vector = embeddings_index.get(word)
	if embedding_vector is not None:
		embedding_matrix[i] = embedding_vector

e = Embedding(input_dim=vocab_size, 
            output_dim=100, 
            weights=[embedding_matrix], 
            # input_length=max_length,
            trainable=False)
conv_filters = 300
window_size = 5
mlp_hidden_units=300

# n_timesteps, n_features = padded_X_train.shape[0], padded_X_train[1]
# n_features = np.array(n_features)

model = Sequential()
# model.add(Input(shape=(n_timesteps,), dtype='int32'))
model.add(e)
model.add(Dropout(0.5))
model.add(Conv1D(filters=conv_filters, 
                kernel_size=window_size, 
                padding='same', 
                use_bias=False, 
                activation='relu'))
model.add(MaxPooling1D())
# model.add(Flatten())
model.add(Dense(mlp_hidden_units, activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
print(model.summary())

# history = model.fit(padded_X_train, y_train, epochs=5, verbose=0)
model.fit(padded_X_train, y_train, epochs=5, validation_data=(padded_X_test, y_test), verbose=0)
model.save("cnn_comsum.hdf5")

loss, accuracy = model.evaluate(padded_X_test, y_test, verbose=0)
print('Accuracy: %f' % (accuracy*100))

Y_predict = model.predict_classes(padded_X_test, verbose=0)
# Y_predict = np.argmax(model.predict(padded_X_test), axis=-1)
# Y_predict = np.argmax(model.predict(padded_X_test) > 0.5).astype("int32")
Y_predict = Y_predict[:, 0]

from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, Y_predict)
print('Accuracy: %f' % acc)

from sklearn.metrics import precision_score
prec = precision_score(y_test, Y_predict)
print('Precision: %f' % prec)

from sklearn.metrics import recall_score
recall = recall_score(y_test, Y_predict)
print('Recall %f' % recall)

from sklearn.metrics import f1_score
f1 = f1_score(y_test, Y_predict)
print('f1: %f' % f1)

print("done")