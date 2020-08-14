# **Online 21-Questions Game**

#### *Welcome to our online game, 21-Questions! This is a python program that was developed and powered by Google Firebase's realtime databse. This project was part of the 2020 HackIllinois' HackThis hackathon*  

#### How it works:
###### The online game works by having both players on the game transfer data between each other through the Firebase database. Player 1 choose a word which gets posted on the database that triggers Player 2 to start asking a question (which also gets posted on the database). The question then triggers Player 1 to respond to the question which then triggers Player 2 to ask a question again. It is a cycle which only ends when Player 2 runs out of tries or Player 2 guesses the word correctly

#### How to download:
- Download Python 3 and PIP package manager. Here is a link for a [video instruction](https://youtu.be/Ko9b_vC6XY0)
- Next install the requests and python-firebase module by typing the following command in Terminal/Shell: 
```bash 
pip install requests
pip install python-firebase
```
- Once python-firebase module is installed, located its directory on your computer and find the async.py file. Rename that file to whatever you like.

- Afterwards open firebase.py and visit line 12 and replace the async to whatever you renamed the async.py file to It should like this: 
```python
from .async import process_pool 
```

- Now similar to the step above, visit the __init__.py file and replace the async word with whatver you renamed the file to. Don't forget to save changes

- You are ready to play!

###### Contributers: Rishabh Mehta, Natasha Mohanty
