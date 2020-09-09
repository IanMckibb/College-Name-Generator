from keras.layers import LSTM, Dense, Softmax
from keras.models import Sequential, Model
from keras.callbacks import LambdaCallback
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np

max_epochs = 100
batch_size = 512

def generate_name_loop(epoch, _):
    if epoch == max_epochs - 1:
        output_file = open("example_names.txt", "w")
        for i in range(100):
            output_file.write(make_name(model) + '\n')
        return
    if epoch % 25 == 0:
        print("\n#################")
        for i in range(3):
            print(make_name(model))
        print("#################\n")

def make_name(model):
    name = []
    x = np.zeros((1, max_char, char_dim))
    end = False
    i = 1
    
    #Get random capitalized letter
    rand_ind = np.random.randint(0, 26)
    x[0, 0, rand_ind] = 1
    name.append(index_to_char[27 + rand_ind])
    
    while end == False:
        probs = list(model.predict(x)[0,i])
        probs = probs / np.sum(probs)
        index = np.random.choice(range(char_dim), p = probs)
        if i == max_char - 2:
            character = '.'
            end = True
        else:
            character = index_to_char[index]
        name.append(character)
        x[0, i + 1, index] = 1
        i += 1
        if character == '.':
            end = True
    
    return(''.join(name))

input_file = open("college_names.txt", 'r')

names = input_file.read().split('\n')

char_to_index = {}
for i in range(1, 27):
    char_to_index[chr(i + 96)] = i
    char_to_index[chr(i + 64)] = i + 26
char_to_index[' '] = 0
char_to_index['-'] = 53
char_to_index['.'] = 54

index_to_char = {}
for i in range(1, 27):
    index_to_char[i] = chr(i + 96)
    index_to_char[i + 26] = chr(i + 64)
index_to_char[0] = ' '
index_to_char[53] = '-'
index_to_char[54] = '.'

print(char_to_index)
print(index_to_char)

max_char = len(max(names, key=len))
m = len(names)
char_dim = len(char_to_index)

X = np.zeros((m, max_char, char_dim))
Y = np.zeros((m, max_char, char_dim))

for i in range(m):
    name = list(names[i])
    for j in range(len(name)):
        X[i, j, char_to_index[name[j]]] = 1
        if j < len(name) - 1:
            Y[i, j, char_to_index[name[j + 1]]] = 1

name_generator = LambdaCallback(on_epoch_end = generate_name_loop)

model = Sequential()
model.add(LSTM(128, input_shape=(max_char, char_dim), return_sequences=True))
model.add(Dense(char_dim, activation='softmax'))

optimizer = Adam(learning_rate=0.05)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.fit(X, Y, batch_size=batch_size, epochs=max_epochs, callbacks=[name_generator])