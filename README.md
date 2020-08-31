# Enhance net deployment

This is a small AI deployment demo with Flask + Keras + Gunicorn + nginx + docker.

The project consists in a LSTM network to create a IRM in order to extract the voice in the audio file, it's a similar approach taken in [https://arxiv.org/pdf/2002.11241.pdf](https://arxiv.org/pdf/2002.11241.pdf).  

Here you will find an `` app/main.py `` file that contains all the functionalities related to the IA model, a keras model in `` app/test.json `` and weights in `` app/test.h5 `` .

The main purpose of the system is to separate the voice from everything else, with few computational resources (currently 16mb), here you will find the project in deployment mode.

Frameworks and technologies used:

* Framework: Flask + Keras
* Servers: Gunicorn + nginx

## How to use

## Prerequisites

* Docker
* docker-compose

## Instructions

In this repository, copy the file named .env.example to .env and adjust file variables.

```
cp .env.example .env
```

Open a terminal, run the built container and build the code.

```
sudo docker-compose up --build
```

wait until installation is complete (the first time it can take a couple of minutes), then go to localhost:9000 in your browser and enjoy!.

Debug mode (python 3.6 >= strongly recommended).

```
cd app
conda env create -f environment.yml
conda activate audio_enviroment
python main.py
```

Demo:<br/>
![image](https://github.com/sralex/voice_extractor/blob/master/demo.png)