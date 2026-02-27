# wordle
##### A wordle-clone for a console near you

## Description

Console-based game where the player guesses a five-letter word; each successive guess reveals more information about the answer.

The essential game works, although many nice features like winning streak were not implemented.

## Installation

Use Python3.
Install required modules with

```
pip3 install -r requirements.txt
```

If you feel like it, to protect your system environment against newfangled python versions, install to a virtual environment using

```
python3 -m venv wordle
```

to create the environment, and

```
source ./wordle/bin/activate
```

to activate the environment.

## Presentation

The presentation detailing the development process was made in markdown and is intended to be built with [marp-cli](https://github.com/marp-team/marp-cli).  
Doing so will yield ie a pdf file with presentation slides.