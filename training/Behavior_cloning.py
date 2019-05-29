import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import keras
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from imgaug import augmenters as iaa
import cv2
import pandas as pd
import random
import ntpath

model_input_width = 200
model_input_height = 70

datadir = 'dataset'
# columns = ['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
columns = ['left', 'center', 'right', 'steering']
pd.set_option('display.max_colwidth', -1)
data = pd.read_csv(os.path.join(datadir, 'driving_log.csv'), names = columns, header=None)
# print(data.head())

# def path_leaf(path):
#   head, tail = ntpath.split(path)
#   return tail
#
# data['center'] = data['center'].apply(path_leaf)
# data['left'] = data['left'].apply(path_leaf)
# data['right'] = data['right'].apply(path_leaf)
# # print(data.head())

num_bins = 25
samples_per_bin = 600
# hist: 도수분포표의 각 구간에 있는 data의 수, bins: 도수분포 구간
hist, bins = np.histogram(data['steering'], num_bins)
center = (bins[:-1] + bins[1:]) * 0.5
# print(bins)
# print(bins[:-1])
# print(bins[1:])
# print(center)
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['steering']), np.max(data['steering'])), (samples_per_bin, samples_per_bin))
plt.plot((5, 7), (1000, 1000))
# plt.show()

print('total data:', len(data))
removed_list = []
for j in range(num_bins):
  list_ = []
  for i in range(len(data['steering'])):
    if data['steering'][i] >= bins[j] and data['steering'][i] <= bins[j+1] :
      list_.append(i)

  list_ = shuffle(list_)
  list_ = list_[samples_per_bin:]  # 400 부터 뒤까지 제거하기 위해
  removed_list.extend(list_)
  # append는 뒤에 object를 추가, extend는 iterable 객체의 엘리먼트를 뒤에 append한다

print('removed:', len(removed_list))
data.drop(data.index[removed_list], inplace=True) # drop한 후의 데이터프레임으로 기존 데이터프레임을 대체하겠다는 뜻
print('remaining', len(data))

hist, _ = np.histogram(data['steering'], (num_bins))
plt.bar(center, hist, width=0.05)
plt.plot((np.min(data['steering']), np.max(data['steering'])), (samples_per_bin, samples_per_bin))
# plt.show()

# print(data.iloc[1])
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
print(image_paths)
print(steerings)


X_train, X_valid, Y_train, Y_valid = train_test_split(image_paths, steerings, test_size=0.2, random_state=6) # random_state: seed
print("Training samples: {}\nValid samples: {}".format(len(X_train), len(X_valid)))
print(X_train)

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
axs[0].hist(Y_train, bins=num_bins, width=0.05, color='blue')
axs[0].set_title('Training set')
axs[1].hist(Y_valid, bins=num_bins, width=0.05, color='red')
axs[1].set_title('Validation set')
# plt.show()

def zoom(image):
  zoom = iaa.Affine(scale=(1, 1.3))
  image = zoom.augment_image(image)
  return image

image = image_paths[random.randint(0, 1000)]
original_image = mpimg.imread(image)
zoomed_image = zoom(original_image)

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()

axs[0].imshow(original_image)
axs[0].set_title('Original Image')

axs[1].imshow(zoomed_image)
axs[1].set_title('Zoomed Image')
# plt.show()

def pan(image):
  pan = iaa.Affine(translate_percent = {"x" : (-0.1, 0.1), "y": (-0.1, 0.1)})
  image = pan.augment_image(image)
  return image

image = image_paths[random.randint(0, 1000)]
original_image = mpimg.imread(image)
panned_image = pan(original_image)

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()

axs[0].imshow(original_image)
axs[0].set_title('Original Image')

axs[1].imshow(panned_image)
axs[1].set_title('Panned Image')
# plt.show()

def img_random_brightness(image): # multiplies all the pixel intensities inside the image, thus any pixel intensity multiplied by a value less than 1 will become darker
  brightness = iaa.Multiply((0.2, 1.2))
  image = brightness.augment_image(image)
  return image

image = image_paths[random.randint(0, 1000)]
original_image = mpimg.imread(image)
brightness_altered_image = img_random_brightness(original_image)
fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()
axs[0].imshow(original_image)
axs[0].set_title('Original Image')
axs[1].imshow(brightness_altered_image)
axs[1].set_title('Brightness altered Image')
# plt.show()

def img_random_flip(image, steering_angle):
  image = cv2.flip(image, 1) # 0: vertical flip, 1: horizontal flip, -1: combination of both horizontal and vertical
  steering_angle = -steering_angle
  return image, steering_angle

random_index = random.randint(0, 1000)
image = image_paths[random_index]
steering_angle = steerings[random_index]


original_image = mpimg.imread(image)
flipped_image, flipped_steering_angle = img_random_flip(original_image, steering_angle)

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()

axs[0].imshow(original_image)
axs[0].set_title('Original Image - ' + 'Steering Angle: ' + str(steering_angle))

axs[1].imshow(flipped_image)
axs[1].set_title('Flipped Image - ' + 'Steering Angle: ' + str(flipped_steering_angle))
# plt.show()

def random_augment(image, steering_angle):
  image = mpimg.imread(image)

  if np.random.rand() < 0.5:
    image = pan(image)
  if np.random.rand() < 0.5:
    image = zoom(image)
  if np.random.rand() < 0.5:
    image = img_random_brightness(image)
  if np.random.rand() < 0.5:
    image, steering_angle = img_random_flip(image, steering_angle)

  return image, steering_angle


ncol = 2
nrow = 10

fig, axs = plt.subplots(nrow, ncol, figsize=(15, 50))
fig.tight_layout()

for i in range(10):
  randnum = random.randint(0, len(image_paths) - 1)
  random_image = image_paths[randnum]
  random_steering = steerings[randnum]

  original_image = mpimg.imread(random_image)
  augmented_image, steering = random_augment(random_image, random_steering)

  axs[i][0].imshow(original_image)
  axs[i][0].set_title('Original Image')

  axs[i][1].imshow(augmented_image)
  axs[i][1].set_title('Augmented Image')
# plt.show()


def img_preprocess(img):
  img = img[225:500, :, :] # height, width, channel # 카메라에 투영되는 차량의 앞부분을 제거한다
  img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) # nvidia model에서 추천함 ㅎ
  img = cv2.GaussianBlur(img, (3, 3), 0)
  # img = cv2.resize(img, (630, 200))
  img = cv2.resize(img, (model_input_width, model_input_height))
  img = img/255

  return img

image = image_paths[100]
original_image = mpimg.imread(image)
preprocessed_image = img_preprocess(original_image)

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()
axs[0].imshow(original_image)
axs[0].set_title('Original Image')
axs[1].imshow(preprocessed_image)
axs[1].set_title('Preprocessed Image')
# plt.show()

def batch_generator(image_paths, steering_ang, batch_size, istraining):

  while True:
    batch_img = []
    batch_steering = []

    for i in range(batch_size):
      random_index = random.randint(0, len(image_paths) - 1)

      # if istraining:
      #   im, steering = random_augment(image_paths[random_index], steering_ang[random_index])
      # else:
      #   im = mpimg.imread(image_paths[random_index])
      #   steering = steering_ang[random_index]

      im = mpimg.imread(image_paths[random_index])
      steering = steering_ang[random_index]
      im = img_preprocess(im)
      batch_img.append(im)
      batch_steering.append(steering)
    yield (np.asarray(batch_img), np.asarray(batch_steering))

X_train_gen, Y_train_gen = next(batch_generator(X_train, Y_train, 1, 1))
X_valid_gen, Y_valid_gen = next(batch_generator(X_valid, Y_valid, 1, 0))

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
fig.tight_layout()

print(X_train_gen[0])


axs[0].imshow(X_train_gen[0])
axs[0].set_title('Training Image')
axs[1].imshow(X_valid_gen[0])
axs[1].set_title('Validation Image')
plt.show()

def nvidia_model():
  model = Sequential()
  # subsample: (horizontally moving, vertically moving)
  model.add(Convolution2D(24, 5, 5, subsample=(2, 2),
                input_shape=(model_input_height, model_input_width, 3),
                activation='relu',
                init='uniform'))
  model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation='elu'))
  model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation='elu'))
  model.add(Convolution2D(64, 3, 3, activation='elu'))
  model.add(Convolution2D(64, 3, 3, activation='elu'))
#   model.add(Dropout(0.5))

  model.add(Flatten())
  model.add(Dense(100, activation='elu'))
#   model.add(Dropout(0.5))
  model.add(Dense(50, activation='elu'))
#   model.add(Dropout(0.5))
  model.add(Dense(10, activation='elu'))
#   model.add(Dropout(0.5))
  model.add(Dense(1)) # output is steering angle

  optimizer = Adam(lr=1e-4)
  model.compile(loss='mse', optimizer=optimizer)
  return model

model = nvidia_model()
print(model.summary())

history = model.fit_generator(batch_generator(X_train, Y_train, 100, 1),
                             steps_per_epoch=150,
                             epochs=10,
                             validation_data=batch_generator(X_valid, Y_valid, 100, 0),
                             validation_steps=200,
                             verbose=1,
                             shuffle=1)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel("Epoch")
plt.show()

# Save the weights
model.save_weights('model_weights.h5')
# Save the model architecture
with open('model_architecture.json', 'w') as f:
    f.write(model.to_json())
