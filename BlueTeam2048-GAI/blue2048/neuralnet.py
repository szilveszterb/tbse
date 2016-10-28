from argparse import ArgumentParser
from enum import Enum

import numpy as np
from keras.models import load_model, Sequential
from keras.layers import Dense, Activation

from game import Game


def main():
    np.random.seed(3)

    model = get_model()
    fit_model(model, '../data/blueteamdata25.txt')
    save_model(model, 'models/004.txt')

    # model = get_model('models/002.txt')
    test_model(model)


def get_model(weights_file=None):
    if weights_file is not None:
        return load_model(weights_file)
    model = Sequential([
        Dense(20, input_dim=19, init='uniform', activation='relu'),
        Dense(20, init='uniform', activation='relu'),
        Dense(10, init='uniform', activation='relu'),
        Dense(10, init='uniform', activation='relu'),
        Dense(4, activation='hard_sigmoid'),
    ])
    model.compile(loss='msle', optimizer='adam', metrics=['accuracy'])
    return model


def fit_model(model, train_file):
    features, outputs = get_dataset(train_file)
    model.fit(features, outputs, nb_epoch=150, batch_size=10)


def get_dataset(data_file):
    dataset = np.loadtxt(data_file)
    features = get_features(dataset[:,0:16])
    outputs = get_classes(dataset[:,16])
    return features, outputs


def get_features(dataset):
    features = dataset / np.amax(dataset, axis=1)[:,None]

    def max_in_corner(row):
        return int(np.argmax(row) in (0,3,12,15))

    def max_on_edge(row):
        return int(np.argmax(row) not in (5,6,9,10))

    def full_ratio(row):
        return np.count_nonzero(row) / 16

    # def contrast_sum(row):
    #     contrast_sum = 0
    #     for i in range(4):
    #         for j in range(4):
    #             if i > 0: contrast_sum += abs(row[(i-1)*4+j] - row[i*4+j])
    #             if i < 3: contrast_sum += abs(row[(i+1)*4+j] - row[i*4+j])
    #             if j > 0: contrast_sum += abs(row[i*4+j-1] - row[i*4+j])
    #             if j < 3: contrast_sum += abs(row[i*4+j+1] - row[i*4+j])
    #     return contrast_sum

    f1 = np.array([np.apply_along_axis(max_in_corner, 1, features)])
    f2 = np.array([np.apply_along_axis(max_on_edge, 1, features)])
    f3 = np.array([np.apply_along_axis(full_ratio, 1, features)])
    # f4 = np.array([np.apply_along_axis(contrast_sum, 1, features)])
    features = np.concatenate((features, f1.T, f2.T, f3.T), axis=1)

    return features


def get_classes(dataset):
    return np.array([np.array([int(i == row) for i in range(4)]) for row in dataset])


def test_model(model, runs=50):
    scores = []
    for run in range(runs):
        game = Game()
        while not game.is_game_over():
            dataset = np.array([np.array([np.log2(cell) for row in game.game_matrix for cell in row])])
            features = get_features(dataset)
            prob = model.predict(features)[0]
            move = np.argmax(prob)
            game.move(move)
            while game.old_equals_new_game_matrix():
                prob[move] = 0
                move = np.argmax(prob)
                game.move(move)
        scores.append(game.get_highest_value())
        game.print()
        print('score:', game.get_highest_value())
    print('average:', sum(scores) / len(scores))


def save_model(model, model_file):
    model.save(model_file)


if __name__ == '__main__':
    main()
