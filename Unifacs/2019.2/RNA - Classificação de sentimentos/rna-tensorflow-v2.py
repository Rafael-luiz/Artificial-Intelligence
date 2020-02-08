import tensorflow as tf
from tensorflow import keras
import numpy as np
from pprint import pprint
import json

# Criando o DataSet =======================================================
reviews_full = []
labels_reviews_full = []

reviews_json = json.load(open('reviews/reviews_test.json', 'r', encoding="utf8"))

reviews_test_pos = reviews_json['positivas'][:5000]
labels_reviews_test_pos = []

reviews_test_neg = reviews_json['negativas'][:5000]
labels_reviews_test_neg = []

for review in reviews_test_pos:
    reviews_full.append(str(review).strip())
    labels_reviews_test_pos.append('positiva')

for label_pos in labels_reviews_test_pos:
    labels_reviews_full.append(label_pos)

for review in reviews_test_neg:
    reviews_full.append(str(review).strip())
    labels_reviews_test_neg.append('negativa')

for label_neg in labels_reviews_test_neg:
    labels_reviews_full.append(label_neg)

# craindo mapa de palavras


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


palavras_pt_br = []
for review in reviews_full:
    words = set(review.split())
    for word in words:
        if not hasNumbers(word):
            palavras_pt_br.append(word)

word_index = {}
for palavra in palavras_pt_br:
    word_index[palavra] = palavras_pt_br.index(palavra)

word_index = {k: (v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# Adaptando reviews para o tensorflow
reviews_full_adaptado = []
for review in reviews_full:
    words = review.split()
    review_adaptada = []
    for word in words:
        if not hasNumbers(word):
            review_adaptada += (word_index[word], )

    reviews_full_adaptado.append(review_adaptada)


# Adaptando labels para o tensorflow
labels_reviews_full_adaptado = []
for label in labels_reviews_full:
    label_adaptado = 0
    if label == "positiva":
        label_adaptado = 1

    labels_reviews_full_adaptado.append(label_adaptado)


(train_data, train_labels) = (reviews_full_adaptado[:3000] + reviews_full_adaptado[5001:8001], labels_reviews_full_adaptado[:3000] + labels_reviews_full_adaptado[5001:8001])
(test_data, test_labels) = (reviews_full_adaptado[3001:5000] + reviews_full_adaptado[8002:], labels_reviews_full_adaptado[3001:5000] + labels_reviews_full_adaptado[8002:])

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Criando a RNA ==========================================================
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post", maxlen=50)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding="post", maxlen=50)


def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])


# Model
model = keras.Sequential()
model.add(keras.layers.Embedding(200000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.summary()

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

x_val = train_data[:2000]
x_train = train_data[2000:]

y_val = train_labels[:2000]
y_train = train_labels[2000:]


fitModel = model.fit(x_train, y_train, epochs=45, batch_size=20, validation_data=(x_val, y_val), verbose=1)

results = model.evaluate(test_data, test_labels)

test_review_i = [388, 479, 1860, 3748, 3847, 3951]
test_review_1 = test_data[test_review_i[0]]
test_review_2 = test_data[test_review_i[1]]
test_review_3 = test_data[test_review_i[2]]
test_review_4 = test_data[test_review_i[3]]
test_review_5 = test_data[test_review_i[4]]
test_review_6 = test_data[test_review_i[5]]

predict_1 = model.predict([test_review_1])
predict_2 = model.predict([test_review_2])
predict_3 = model.predict([test_review_3])
predict_4 = model.predict([test_review_4])
predict_5 = model.predict([test_review_5])
predict_6 = model.predict([test_review_6])
print()
print("___________________________________________________________________________________________________________________________________")
print()
print()
print()
print("  Os seguintes comentarios seram analisados pela RNA: ")
print()
print("  test_data[388]  = {}".format(decode_review(test_review_1).split('<PAD>')[0]))
print("  test_data[479]  = {}".format(decode_review(test_review_2).split('<PAD>')[0]))
print("  test_data[1860] = {}".format(decode_review(test_review_3).split('<PAD>')[0]))
print()
print("  test_data[3748] = {}".format(decode_review(test_review_4).split('<PAD>')[0]))
print("  test_data[3844] = {}".format(decode_review(test_review_5).split('<PAD>')[0]))
print("  test_data[3951] = {}".format(decode_review(test_review_6).split('<PAD>')[0]))
print()
print()
print()
print("  =====================================================")
input("  |     Pressione ENTER para iniciar a analise        | \n  ===================================================== \n \n \n ")


# test_data[388]  = Adorei
# test_data[479]  = Tudo certo, estou muito satisfeito.
# test_data[1860] = Tudo perfeito, prazo exato e produto de acordo com minha expectativa
# test_data[3748] = Péssima compra!
# test_data[3844] = termometro veio quebrado, preciso de outro.
# test_data[3951] = Estou aguardando contato para saber o que aconteceu com o produto. Pois pedi dois e chegou apenas um.

estimativa_label = {1: "Comentario positivo", 0: "Comentario negativo"}
print()
print()
print("  -----------------------------------------------------")
print("  |                 Iniciando Analise                 |")
print("  -----------------------------------------------------")
print()
print()
print("  Comentario 1 ________________________________________")
print()
print("  " + decode_review(test_review_1).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_1[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[0]])])
print()
print()
print("  Comentario 2 ________________________________________")
print()
print("  " + decode_review(test_review_2).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_2[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[1]])])
print()
print()
print("  Comentario 3 ________________________________________")
print()
print("  " + decode_review(test_review_3).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_3[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[2]])])
print()
print()
print("  Comentario 4 ________________________________________")
print()
print("  " + decode_review(test_review_4).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_4[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[3]])])
print()
print()
print("  Comentario 5 ________________________________________")
print()
print("  " + decode_review(test_review_5).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_5[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[4]])])
print()
print()
print("  Comentario 6 ________________________________________")
print()
print("  " + decode_review(test_review_6).split('<PAD>')[0])
print()
print("  Estimativa da RNA: " + estimativa_label[int(np.round(predict_6[0]))])
print("  Real:              " + estimativa_label[int(test_labels[test_review_i[5]])])
print()
print()
print("  -----------------------------------------------------")
print("  |                 Analise Concluida                 |")
print("  -----------------------------------------------------")
