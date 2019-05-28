from keras.models import model_from_json
from keras.models import Sequential
from keras.optimizers import Adam
import cv2
import numpy as np

class ModelLoader:
    def __init__(self):
        #Model reconstruction from JSON file
        with open('model_architecture.json', 'r') as f:
            self.model = model_from_json(f.read())

        # Load weights into the new model
        self.model.load_weights('model_weights.h5')
        optimizer = Adam(lr=1e-4)
        self.model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])
        self.model_input_width = 200
        self.model_input_height = 70

    def img_preprocess(self, img):
      img = img[225:500, :, :] # height, width, channel # 카메라에 투영되는 차량의 앞부분을 제거한다
      img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) # nvidia model에서 추천함 ㅎ
      img = cv2.GaussianBlur(img, (3, 3), 0)
      img = cv2.resize(img, (self.model_input_width, self.model_input_height))
      img = img/255

      return img

    def predict(self, img):
        X = np.expand_dims(self.img_preprocess(img), axis=0)
        ret = self.model.predict(X, verbose=0)

        return ret
