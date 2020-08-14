""""
Firebase Functions:
     get(location, id=None): gives dict of table keys which map the values (of id if given)
     post(location, str): creates a new child of the location entry in table with str value
     put(location, key, value): makes a key-value entry of inputted data in table
     delete(location, id): deletes entry with inputted key id
"""

from firebase import firebase

database_loc = "https://questions-21.firebaseio.com/"
firebase = firebase.FirebaseApplication(database_loc, None)
player_num = -1

"""After a game is finished, this function is called to set the Firebase realtime database
   back to its inital state (before the game started) """
def reset_DB():
  firebase.put(database_loc, "p1", 0)
  firebase.put(database_loc, "p2", 0)
  firebase.put(database_loc, "status", 0)
  firebase.put(database_loc, "response","-1")
  firebase.put(database_loc, "question", "")
  firebase.put(database_loc, "word", "")

"""Returns which player number you are depending on the p1 and p2 flags on the database
   Returns 1 = player 1, returns 2 = player 2, returns -1 = cannot play right now """
def getPlayerNum():
    db_player_1 = firebase.get(database_loc, "p1")
    db_player_2 = firebase.get(database_loc, "p2")

    if db_player_1 == 0: 
        print("You are player 1")
        firebase.put(database_loc,"p1", 1) 
        return 1
    elif db_player_2 == 0:
        print("You are player 2")
        firebase.put(database_loc, "p2", 1)
        firebase.put(database_loc, "status", 1)
        return 2
    return -1

"""This function is for the game logic of a player 1 (selecting a word for player 2 to
   guess and responding to player 2 questions). This function is only called if a player's variable,
   player_num == 1"""
def gameplay_1():
  word = input("Enter the word -> ")
  firebase.put(database_loc, "word", word)

  tries = 21
  while tries > 0:
    print("Waiting for p2 to send their question: ")
    while firebase.get(database_loc, "question") == "":
      continue
      
    question = firebase.get(database_loc, "question")
    #if p2 is attemping to guess the word
    if question[0] == "!":
      if word == question[1:]:
        print("Player 2 guessed the word correctly")
        firebase.put(database_loc, "response", 2)
        firebase.put(database_loc, "question", "")
        return

      print("Player 2 quessed the word was " + question[1:])
      firebase.put(database_loc,"response",0)
    #p2 ask a question about the word
    else:
      print(question)
      response = input("Answer with either yes or no (y/n)")
      if response == "y":
        firebase.put(database_loc,"response", 1)
      else:
        firebase.put(database_loc,"response", 0)

    firebase.put(database_loc,"question","")
    tries -= 1

  print("Player 2 ran out of tries to guess the word")

"""This function is for the game logic of a player 2 (Trying to guess the word player 1 is     thinking about in 21 tries). This function is only called if a player's variable,           player_num == 2"""
def gameplay_2():
  print("Waiting for player 1 to choose their word...")
  while firebase.get(database_loc, "word") == "":
    continue
  p1_word = firebase.get(database_loc,"word")

  tries = 21
  while tries > 0:
    choice = input("Would you like to guess the word (enter 1) or ask a question about it (enter 0) -> ")
    if choice == '1':
      word = input("Enter what you think the word is -> ")
      firebase.put(database_loc, "question", "!"+word)
    else:
      question = input("Enter your question -> ")
      firebase.put(database_loc, "question", question)
    
    print("Waiting for player 1 to respond to your question")
    while firebase.get(database_loc, "question") != "":
      continue

    response = firebase.get(database_loc, "response")
    if response == 0:
      print("P1 answered no to your question")
    elif response == 1:
      print("P1 answered yes to your question")
    elif response == 2:
      print("You guessed the word correctly")
      return
      
    tries -= 1

  print("You ran out of questions to ask!")
  print("The word was " + p1_word)


"""This function allows each player to the their proper tasks. 
    If player 1,do player 1 logic. Same applies to player 2. If unable to play,
    wait till there is an openning"""
def main():
    player_num = getPlayerNum()

    if player_num == -1:
      print("Waiting for the current game to finish. Thank you for ur patience...")
      while firebase.get(database_loc, "status") != 0:
        continue
      main()

    if player_num == 1:
      while firebase.get(database_loc, "p2") == 0:
        continue
      gameplay_1()
    else:
      gameplay_2()
      reset_DB()

"""This method defines the instructions on how to play our game. Anyone confused about the directions simply have to press the '?' button and read the directions"""
def directions():
  print("In this game, there are two players")
  print("Player 1 has to think of a word while Player 2 can ask up to 21 questions to guess that word")
  print("Player 2 has the option to either ask about characteristics of the word or take an attempt to guess the word")

"""This is the main sequence that executes when players run our game. It is similar to a main menu where players can join a game, ask for help or quit the game"""
if __name__ == "__main__":
    print("Welcome to 21-Questions!")
    cmd = input("Enter 'r' to search for a match, enter '?' for help, or enter 'q' to quit -> ")
    while cmd != 'q':
      if cmd == 'r':
        main()
      elif cmd == '?':
        directions()
      cmd = input("Enter 'r' to search for a match, enter '?' for help, or enter 'q' to quit -> ")
