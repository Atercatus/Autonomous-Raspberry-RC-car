import os
import numpy as np
import matplotlib.image as mpimg
from keras.models import Sequential
from keras.models import model_from_json
from keras.optimizers import Adam
import pandas as pd
import cv2

model_input_width = 200
model_input_height = 70

datadir = 'dataset'
columns = ['left', 'center', 'right', 'steering']
pd.set_option('display.max_colwidth', -1)
data = pd.read_csv(os.path.join(datadir, 'driving_log.csv'), names = columns, header=None)

def load_img_steering(datadir, df):
  image_path = []
  steering = []
  for i in range(len(df)):
    indexed_data = df.iloc[i] # integer positon를 통해 값을 찾을 수 있다. label로는 찾을 수 없다
    center, left, right = indexed_data[0], indexed_data[1], indexed_data[2]
    image_path.append(os.path.join(datadir, center.strip())) # strip: 공백제거
    steering.append(float(indexed_data[3]))
  image_paths = np.asarray(image_path) # copy가 true인 array
  steerings = np.asarray(steering)
  return image_paths, steerings
image_paths, steerings = load_img_steering(datadir + '/images', data)
# print(image_paths)
# print(steerings)

def img_preprocess(img):
  img = img[225:500, :, :] # height, width, channel # 카메라에 투영되는 차량의 앞부분을 제거한다
  img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) # nvidia model에서 추천함 ㅎ
  img = cv2.GaussianBlur(img, (3, 3), 0)
  # img = cv2.resize(img, (630, 200))
  img = cv2.resize(img, (model_input_width, model_input_height))
  img = img/255

  return img

print(steerings.shape)

image = image_paths[1884]
original_image = mpimg.imread(image)
preprocessed_image = img_preprocess(original_image)

#Model reconstruction from JSON file
with open('model_architecture.json', 'r') as f:
    model = model_from_json(f.read())

# Load weights into the new model
model.load_weights('model_weights.h5')
optimizer = Adam(lr=1e-4)
model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])

X = np.expand_dims(preprocessed_image, axis=0)
ret = model.predict(X, verbose=0)
print(ret)
print(steerings[1884])
