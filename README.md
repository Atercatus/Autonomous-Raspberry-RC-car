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


## To do list
- [ ] implement survo motor controller
- [ ] implement dc motor controller
- [ ] merge motor controllers
- [ ] testing web cam
- [ ] implement how to controll our rc car
- [ ] struct our models...

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


## Model Architecture Design
### Autonomous Driving
[End to End Learning for Self-Driving Cars](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf) 

#### Hyperparameter

### Simulation
##### Model


### Object Detection
#### Hyperparameter

## Data Preprocessing

## Model Training
### Image Augumentation

## Simulation
### Udacity simulator

## Video Record
