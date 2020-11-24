from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import models, layers
import pandas as pd
import numpy as np

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
        gtzanData = pd.read_csv('./iamusic/data/gtzan.csv')

        # Dropping unneccesary columns
        gtzanData2 = gtzanData.drop(['filename', 'silence'], axis=1)

        # Encode genres into integers
        self.genre_list = list(np.unique(gtzanData2.iloc[:, -1].to_numpy()))
        gtzanY = np.array([self.genre_list.index(g) for g in gtzanData2.iloc[:, -1]])

        # Split dataset
        gtzanX = np.array(gtzanData2.iloc[:, :-1], dtype = float)

        # Normalize the dataset
        self.scaler = StandardScaler()
        gtzanX = self.scaler.fit_transform(gtzanX)

        # Create the genres model
        self.gtzanModel = models.Sequential()
        self.gtzanModel.add(layers.Dense(256, activation='relu', input_shape=(gtzanX.shape[1],)))
        self.gtzanModel.add(layers.Dense(128, activation='relu'))
        self.gtzanModel.add(layers.Dense(64, activation='relu'))
        self.gtzanModel.add(layers.Dense(10, activation='softmax'))
        self.gtzanModel.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train genres model
        self.gtzanModel.fit(gtzanX, gtzanY, epochs=15, batch_size=128)
    
    def predict(self, X):
        return self.gtzanModel.predict(self.scaler.transform(X))