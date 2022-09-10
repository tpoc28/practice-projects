import random
from allwords import words
from hang_lives import hang_lives
import string
import os

play = True

while play == True:
    os.system('clear')
    lives = 5
    wrong = 0
    word = random.choice(words)
    alphabet = set(string.ascii_lowercase)

    invalid_char = ["'", '-', ' ', ',']
    while any(x in word for x in invalid_char): #choose valid word
        word = random.choice(words)
        print(word)
    else: pass

    spaces = len(word)
    letters = list(word.strip())

    with open('insults.txt') as file:
        insult = random.choice(list(file.read().upper().split('\n')))

    for i in range(0,spaces):
        print("_",end=' ')

    print(hang_lives.get(wrong))

    user_input = input('Guess a letter: ').lower()


    def validInput(user_input):
        a = False
        while a is False:
            if (user_input not in alphabet or len(user_input) > 1):
                with open('insults.txt') as file:
                    insult = random.choice(list(file.read().upper().split('\n')))
                print("TRY AGAIN ",insult,": ",sep="",end="")
                user_input = input()
            else: a = True
        return user_input

    user_input = validInput(user_input)

    guessed_letters = []
    guessed_letters.append(user_input)
    wrong_letters = set(guessed_letters).difference(letters)
    wrong = len(wrong_letters)

    

    while wrong < lives:        #check if game lost
        os.system('clear')
        for i in range(0,spaces): #print remaining word
            if letters[i] in guessed_letters:
                print(letters[i],end=" ")
            else: print("_",end=" ")

        if user_input in letters:
            print('\n\nGood job!')
        else: 
            with open('insults.txt') as file:
                insult = random.choice(list(file.read().upper().split('\n')))
            print('\n\nWRONG! Do better ',insult,'!',sep="")
        
        print(hang_lives.get(wrong)) #print new hangman

        user_input = input('Guess again: ').lower()
        user_input = validInput(user_input)
        
        guessed_letters.append(user_input)
        wrong_letters = set(guessed_letters).difference(letters)
        wrong = len(wrong_letters)
        

        if set(guessed_letters).intersection(letters) == set(letters): #check if game won
            print('Congratulations! You are the champion of the world!')
            print('The word is:',word)
            exit()
        else: continue
    
    
    print(hang_lives.get(wrong))    
    with open('insults.txt') as file:
            insult = random.choice(list(file.read().upper().split('\n')))
    print('YOU SUCK ',insult,'!!! YOU KILLED HIM, LOSER!',sep="")

    play_again = input("Play again (y/n)? ").lower()
    while play_again not in ['y','n']:
        print('What?\n')
        play_again = input("Play again (y/n)? ").lower()
    if play_again == 'y':
        play = True
    else: play = False

    



