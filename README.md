<h1 align="center">
  Autonomous-Driving 
</h1>
<h3 align="center">
	Autonomous RC car project using Python3 on raspberry pi 3
</h3>

## Problems
- [ ] 보조배터리 사용 시 완충 균일한 전력 공급이 불가해 자주 장비가 정지하는 경우가 발생한다.
- [ ] 서보 모터에서 저전력이 발생했다는 경고가 자주 뜸
- [ ] 서보 보터의 잦은 떨림 

## Overview
* **Use raspberry pi 3**
* **Use 2 motors** 1 DC motor and 1 Servo motor
* **Behavior cloning** we use [The NVIDIA model](https://devblogs.nvidia.com/parallelforall/deep-learning-self-driving-cars/)
* **Object Detect** we use YOLO algorithm v3
* **Remote control** control rc car using dualshock4 (here driver => [ds4drv](https://github.com/chrippa/ds4drv))

## RC car Structure
![Raspberry_pi_rc_car_bb](https://user-images.githubusercontent.com/32104982/56851686-c2e92100-694c-11e9-9622-1ea69148ac64.jpg)

### Motor Detail

#### MDD10A
![image](https://user-images.githubusercontent.com/32104982/56851707-2b380280-694d-11e9-8a9e-5b5693c8ebb7.png)

* **M1A, M1B :** Output motor 1
* **M2A, M2B :** Output motor 2
* **B+, B- :** PowerInput Max 25V, 10A
* **PWR :** Green LED, Power
* **M1A, M1B:** Test Button Motor1
* **M2A, M2B:** Test Button Motor2

###### Input Pins
![image](https://user-images.githubusercontent.com/32104982/56851797-2162cf00-694e-11e9-8669-84af1ce24ad3.png)

* **DIR1 :** Direction input(motor1). low(0 - 0.5v),  high(3 - 5.5v)
* **PWM1 :** PWM input for speed control (Motor 1). Max 20Hz
* **DIR2 :** Direction input(motor1). low(0 - 0.5v) , high(3 - 5.5v)
* **PWM2 :** PWM input for speed control (Motor 2). Max 20Hz
* **GND :** Ground

###### PWM & DIR control
|-  	| Input	| DIR 		| Output A	| Output B|
|:----: 	| :----:| :----:	| :----:	| :----:|
|PWM	| off	| X		| off 		| off|
|PWM 	| on 	| off		| on		| off|
|PWM 	| on	| on		| off		| on|


## Autonomous Driving
[End to End Learning for Self-Driving Cars](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf)

#### Block Diagram of DAVE-2
![image](https://user-images.githubusercontent.com/32104982/56863005-e0b99300-69eb-11e9-920f-b34d3d14d2c5.png)



#### Neural Network Architecture
![image](https://user-images.githubusercontent.com/32104982/56852670-0f3a5e00-6959-11e9-9e7f-3e540e0b0814.png)

* **[source](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf)** </br>

The network consists of 9 layers, including a normalization layer, 5 convolutional layers and 3 fully connected layers. The input image is split into **YUV** planes and passed to the network.
They use strided confolutions in the first three convolutional layers with a 2x2 stride and a 5x5 kernel and a non-strided convolution with a 3x3 kernel size in the last two convolutional layers.


#### Model Summary
| Layer (type)			| Output Shape 			| Param # 	| Units | Kernel size | Activation |
| :----:			| :----:			| :----:  	| :----:| :----:	| :----:     |
| conv2d_1(Conv2D)		| (None, 31, 98, 24)		| 1824	  	| 24	  | 5, 5	| relu	     |
| conv2d_2(Conv2D)		| (None, 14, 47, 36)		| 21636	  	| 36	  | 5, 5	| elu	     |
| conv2d_3(Conv2D)		| (None, 5, 22, 48)		| 43248	  	| 48 	  | 5, 5	| elu	     |
| conv2d_4(Conv2D)		| (None, 3, 20, 64)		| 27712	  	| 64	  | 3, 3 	| elu	     |
| conv2d_5(Conv2D)		| (None, 1, 18, 64)		| 36928	  	| 64	  | 3, 3	| elu	     |
| flatten_1(Flatten)		| (None, 1152)			| 0	  	| 	  | 		| 	     |
| dense_1(Dense)		| (None, 100)			| 115300	| 100	  | -		| elu	     |
| dense_2(Dense)		| (None, 50)			| 5050	  	| 50	  | -		| elu	     |
| dense_3(Dense)		| (None, 10)			| 510	  	| 10	  | -		| elu	     |
| dense_4(Dense)		| (None, 1)			| 11	  	| 1	  | -		| 	     |

Total params: 252,219 </br>
Trainable params: 252,219 </br>
Non-trainable params: 0 </br>

* **Optimizer:** Adam
* **Learning rate:** 1e-4
* **loss function:** MSE
* **Batch size:** 100
* **Steps per epoch:** 200
* **epochs:** 10

### Simulation
[Detail](https://github.com/Atercatus/Autonomous-Raspberry-RC-car/tree/develop/Simulator) for simulation </br>
Player plays the [simulation game](https://github.com/udacity/self-driving-car-sim) manually and records car's information. Use 3 cameras(left, center, right)

#### Preprocessing
| Original Image | Preprocessed Image |
| :----:	 | :----:
|![image](https://user-images.githubusercontent.com/32104982/56852793-773d7400-695a-11e9-8891-db1bad43acbf.png)|![image](https://user-images.githubusercontent.com/32104982/56852796-86242680-695a-11e9-80d8-6f4c2b787d9d.png)

```python
def img_preprocess(img):
  img = img[60:135, :, :] # height, width, channel # 카메라에 투영되는 차량의 앞부분을 제거한다
  img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) # recommended(nvidia model)
  img = cv2.GaussianBlur(img, (3, 3), 0)
  img = cv2.resize(img, (200, 66))
  img = img/255  
  
  return img

```

#### Data Augment
* **[imgaug](https://imgaug.readthedocs.io/en/latest/)** is a library for image augmentation in machine learning experiments. It supports a wide range of augmentation techniques, allows to easily combine these and to execute them in random order or on multiple CPU cores, has a simple yet powerful stochastic interface and can not only augment images, but also keypoints/landmarks, bounding boxes, heatmaps and segmentation maps.

#### Results
TODO: add youtube video

## Object Detection
#### Hyperparameter

#### Data Preprocessing

## Model Training
### Image Augumentation

## Simulation
### Udacity simulator

## Video Record
