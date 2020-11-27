import random
import pandas as pd
import numpy as np
from keras import models, layers
from iamusic.models import gtzan_model

class UserSession:
    def __init__(self):
        self.next_id = 0
        self.is_finished = False
        self.is_calibration = True
        self.completed_count = 0
        
        # Create new ML models
        self.model = models.Sequential()
        self.model.add(layers.Dense(256, activation='relu', input_shape=(75,)))
        self.model.add(layers.Dense(128, activation='relu'))
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(2, activation='softmax'))
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.gtzan = gtzan_model.GtzanModel()

        # Load all musics data
        self.data = pd.read_csv('./iamusic/data/musics.csv')
        self.allData = pd.read_csv('./iamusic/data/musics.csv')
        self.yt_shortcodes = list(self.data['yt_shortcode'])
        self.data = self.data.drop(['yt_shortcode'], axis=1)
        self.data['user_preference'] = -1

    def userDataX(self):
        return self.data[self.data['user_preference'] != -1].drop(['user_preference'], axis=1)

    def userDataY(self):
        return np.array(self.data[self.data['user_preference'] != -1]['user_preference'])

    def userLikedDataX(self):
        return self.data[self.data['user_preference'] == 1].drop(['user_preference'], axis=1)

    def allDataX(self):
        return self.data.drop(['user_preference'], axis=1)

    def noPreferenceDataX(self, ):
        return self.data[self.data['user_preference'] == -1].drop(['user_preference'], axis=1)

    def setUserPreference(self, preference):
        self.data.at[self.next_id, 'user_preference'] = preference
        self.completed_count += 1

    def fitUserModel(self):
        # Fit model only every 3 points
        if self.completed_count%3 == 0:
            self.model.fit(self.gtzan.scaler_transform(self.userDataX()), self.userDataY(), epochs=3)

    def nextYtShortcode(self):
        return self.yt_shortcodes[self.next_id]

    def generateNextId(self):
        # Finished if completed greater than equal to 30
        if self.completed_count >= 30:
            self.is_finished = True

        # Calibration
        elif self.is_calibration:
            if self.next_id < 9:
                self.next_id += 1
            else:
                self.is_calibration = False
                self.generateNextId()
        
        # Random
        elif self.completed_count % 3 == 0:
            no_preference_data = self.noPreferenceDataX()
            self.next_id = no_preference_data.index[random.randint(0, len(no_preference_data))]

        # Liked
        else:
            no_preference_data = self.noPreferenceDataX()
            pred = self.model.predict(self.gtzan.scaler_transform(no_preference_data))
            should_like = 1
            self.next_id = no_preference_data.index[pred[:,should_like].argmax()]

    def getResults(self):
        genres_stats = self.gtzan.predict(self.gtzan.scaler_transform(self.userLikedDataX()))
        total_predictions = len(genres_stats)

        user_genres = {g: 0 for g in self.gtzan.genre_list}
        for stat in genres_stats:
            for i in range(len(stat)):
                genre = self.gtzan.genre_list[i]
                user_genres[genre] += float(stat[i]) / float(total_predictions)

        return user_genres

    def getNextPrediction(self):
        df = self.data[self.next_id:self.next_id+1].drop(['user_preference'], axis=1)
        tf = self.gtzan.scaler_transform(df)
        pred = self.gtzan.predict(tf)[0]
        return self.gtzan.genre_list[pred.argmax()]
