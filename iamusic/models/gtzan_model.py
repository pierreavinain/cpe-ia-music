from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import models, layers
import pandas as pd
import numpy as np
import sys

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GtzanModel(metaclass=SingletonMeta):
    def __init__(self):
        # Read GTZAN csv
        gtzanData = pd.read_csv('./iamusic/data/gtzan_genres.csv')
        ytData = pd.read_csv('./iamusic/data/yt_genres.csv')

        # Dropping unneccesary columns
        gtzanData2 = pd.concat([
            # gtzanData.drop(['filename', 'silence'], axis=1),
            ytData.drop(['yt_shortcode'], axis=1)
        ])

        # Encode genres into integers
        self.genre_list = list(np.unique(gtzanData2.iloc[:, -1].to_numpy()))
        gtzanY = np.array([self.genre_list.index(g) for g in gtzanData2.iloc[:, -1]])

        # Split dataset
        gtzanX = np.array(gtzanData2.iloc[:, :-1], dtype = float)
        gtzanX_train, gtzanX_test, gtzanY_train, gtzanY_test = train_test_split(gtzanX, gtzanY, test_size=0.01)

        # Normalize the dataset
        self.scaler = StandardScaler()
        # gtzanX = self.scaler.fit_transform(gtzanX)
        gtzanX_train = self.scaler.fit_transform(gtzanX_train)
        gtzanX_test = self.scaler.transform(gtzanX_test)

        # Create the genres model
        self.gtzanModel = models.Sequential()
        self.gtzanModel.add(layers.Dense(256, activation='relu', input_shape=(gtzanX.shape[1],)))
        self.gtzanModel.add(layers.Dense(128, activation='relu'))
        self.gtzanModel.add(layers.Dense(64, activation='relu'))
        self.gtzanModel.add(layers.Dense(10, activation='softmax'))
        self.gtzanModel.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train genres model
        self.gtzanModel.fit(gtzanX_train, gtzanY_train, epochs=10, batch_size=128, validation_split=0.2)

        # Test with YTDATA
        print("------ TEST WITH YT DATA -------")
        ytData2 = ytData.drop(['yt_shortcode'], axis=1)
        ytDataX = self.scaler.fit_transform(np.array(ytData2.iloc[:, :-1], dtype = float))
        ytDataY = np.array([self.genre_list.index(g) for g in ytData2.iloc[:, -1]])
        test_loss, test_acc = self.gtzanModel.evaluate(ytDataX[0:10], ytDataY[0:10])

    def scaler_transform(self, X):
        return self.scaler.transform(X)
    
    def predict(self, X):
        return self.gtzanModel.predict(X)