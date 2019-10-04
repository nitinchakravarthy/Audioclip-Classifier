# Audio classifier
This repository contains Neural networks for classification of Audio clips. Works with structured(one word human commands) and unstructured data (urban Noises).
The project was done as a part of the course CECE 636 @ TAMU

## Project descrtiption
In this project various configuraions of neural networks were developed for classifying audio data.

## Datasets used
Two datasets were used for this project. [Tensorflow speech recognition dataset](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge) and [urbansound8k](https://urbansounddataset.weebly.com/urbansound8k.html). Tensorflow speech recognition dataset contains 30 classes of single word human sounds such as UP, DOWN, LEFT,ONE. Each sample is a 1sec audio clip. The dataset contains approimately 80,000 training samples. Urbansound8k project contains everyday urban noises such as Dog bark, car horn. Each sample is 4 seconds long audio clip of one class. This dataset contains approximately 8k samples. 
The sampling frequency of both the datasets is different. For this project we divided both the datasets into Training, validation and testing datasets and then merged the corresponding datasets. Then merged dataset is then used to traing the models to that they would work for both the cases. 

## Feature extraction
Spectral features such as MFCCs ans mel spectrogram were extracted from the data and 2D CNNs were trained on these spectral feautes.
The images give an idea of the features used for both the datasets.

![Dog Bark](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark.png)  
![Dog bark - CENS](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark_cens.png)
![Dog bark - Chromogram](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark_chrom.png)
![Dog bark - Chromogram cqt](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark_cqt.png)
![Dog bark - MFCC](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark_mfcc.png)
![Dog bark - Mel spectrogram](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/bark_spec.png)


## Project Structure
### Code Structure
* ```GUI```: This folder contains a gui that uses the model and predicts the audio samples. Built using Tkinter[Demo](https://www.youtube.com/watch?time_continue=10&v=AOFCgibb-6Y)
* ```Code```: Code for various models and training and feature extraction
* ```data```: Extracted features
* ```imgs```: Model training plots and feature example images
* ```models ```: Some pretrained models

### Model training
The models were trained on a Dell G7 with 16Gb ram and 4gb Nvidia-1060 graphic card for around 2000 epochs. Some models were stopped before that. The training takes arroximately 12-14 hours for the whole 2000 epocs to complete. Th training and validation plots for one the models is shown below.
![Model3 accuracy](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/model3_accuracy.png)
![Model3 loss](https://github.com/nitinchakravarthy/Audioclip-Classifier/blob/master/images/model3_loss.png)

## Data Augmentation
Further to make the models more robust, we augmented the data with random background noise and random time shift. This improved the accuracy from 88% to 91%.
