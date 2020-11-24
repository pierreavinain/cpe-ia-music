from keras import models, layers

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class UserModel(metaclass=SingletonMeta):
    def __init__(self):
        self.userModel = models.Sequential()
        self.userModel.add(layers.Dense(256, activation='relu', input_shape=(75,)))
        self.userModel.add(layers.Dense(128, activation='relu'))
        self.userModel.add(layers.Dense(64, activation='relu'))
        self.userModel.add(layers.Dense(2, activation='softmax'))
        self.userModel.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])