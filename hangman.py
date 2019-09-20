#Display files in current working directory
    #import os
    #os.listdir()
#Display current working directory 名
    #os.getcwd()
#Change working directory
    #os.chdir('/Users/sigRick15/Desktop/Python 6.0001 Files/ps2')

# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word = list(one_of_each(secret_word))
    secret_word_copy = secret_word [:]
    
    for s in secret_word:
        for l in letters_guessed:
            if s == l:
                secret_word_copy.remove(s)
                
    if len(secret_word_copy) == 0:        
        return True
    else:
        return False     


def get_guessed_word(secret_word, letters_guessed, currently):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    currently_copy = []
    
    secret_word = list(secret_word)
    for s in secret_word:
        for l in letters_guessed:
            if s == l:
                currently_copy += s
                break
            elif l != letters_guessed[len(letters_guessed)-1]:
                pass
            else:                    
                currently_copy.append("_ ")
    if "".join(currently_copy) != currently:
        return ("".join(currently_copy), True,)           
    else:
        return ("".join(currently_copy), False,)  

         
def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = list(string.ascii_lowercase)
    for l in letters_guessed:
        for a in alphabet:
            if l == a:
                alphabet.remove(l)
            else:
                pass
    return "".join(alphabet)

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    *** At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    *** The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    letters_guessed_copy = []
    guesses = 6
    warnings = 3
    currently = '_ ' * len(secret_word)

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("------------------------------------")
    
    while is_word_guessed(secret_word, letters_guessed) == False and guesses > 0:
        
        print("You have", guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        x = input("Please guess a letter: ")
        
        #1+ char
        if len(x) > 1:
            print("Oops! Please only guess one letter.")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        #Not char
        elif str.isalpha(x) == False:
            print("Oops! That is not a valid letter.")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        #1 char
        elif str.isalpha(x) == True:
            letters_guessed_copy += str.lower(x)
            #Char duplicate?
            letters_count = 0
            for l in letters_guessed:
                for lc in letters_guessed_copy:
                    if l == lc:
                        letters_count += 1
            if letters_count > len(letters_guessed):
                print("Oops! You've already guessed that letter.")
                (warnings, guesses, currently) = warning(warnings, guesses, currently)
                letters_guessed_copy = letters_guessed[:]
                ### = ≠ == ! ###
                ### Tell it to make a copy [:], not become aliases!! ###
            else:
                letters_guessed += str.lower(x)
                (currently, guessed) = get_guessed_word(secret_word, letters_guessed, currently)                      
                #Char in word?
                if guessed == True:
                    print("Good guess: ", currently)
                #Vowel vs consonant penalty
                else:
                    if x == "a" or x == "e" or x == "i" or x == "o" or x == "u":
                        ### yes, "x ==" for every single one ###
                        print("Oops! That vowel is not in my word: ", currently)
                        guesses -= 2
                    else:
                        print("Oops! That consonant is not in my word: ", currently)
                        guesses -= 1
        else:
            print("Boi what is u doin !!!")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        print("------------------------------------")
        
    #Winning
    if is_word_guessed(secret_word, letters_guessed) == True and guesses > 0:
        secret_word_points = one_of_each(secret_word)
        
        print("Congratulations, you won!")
        print("Your total score for this game is:", guesses*len(secret_word_points))
    
    #StraightOuttaGuesses    
    else:
        print("Oh no, you ran out of guesses ):")
        print("The word was '" + secret_word + "'.")
        print("Game over")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def one_of_each(secret_word):
    secret_letters = ["1"]
    ### Need a value or else it will iterate over nothing...remove later ###
    for sw in secret_word:
        for sl in secret_letters:
            if sw == sl:
                break
            elif sw != sl and sl != secret_letters[len(secret_letters)-1]:
            ### Only move on if last of the secret_letters is checked, could be duplicates later ###
                pass
            else:
                secret_letters += sw
    secret_letters.remove("1")
    ### Initial something val finally removed ###
    return secret_letters


def warning(warnings, guesses, currently): 
    if warnings == 0:
        guesses -= 1
    else:
        warnings -= 1
    print("You have", warnings, "warnings left:", currently)
    return (warnings, guesses, currently)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    #Conversion#
    my_word = list(my_word.replace(" ", ""))
    ### New! 名.replace(x, y) ###
    other_word = list(other_word.replace(" ", ""))
    
    if len(my_word) == len(other_word):
        for x in range(len(my_word)):    
            #Do char match, except for "_"?#
            if my_word[x] != "_":
                if my_word[x] == other_word[x]: 
                    pass
                    #Since x += 1 automatically#
                elif my_word[x] != other_word[x]: 
                    return False
                    x = len(my_word)
                    break
            #Hidden cannot be already revealed letter#
            elif my_word[x] == "_":
                for m in my_word:
                    if other_word[x] == m:
                        return False
                        x = len(my_word)
                        break
                pass
        return True
    else:
        return False
        
#        #Do char match, except for "_"?#
#        my_word_copy = my_word[:]
#        other_word_copy = other_word[:]
#        match = 0
#        #Must analyze and modify copy bc program can only ref to 1st instance of duplicates#
#        while len(other_word_copy) > 0:
#            if my_word_copy[0] == other_word_copy[0] or my_word_copy[0] == "_":
#                match += 1
#                del(my_word_copy[0])
#                del(other_word_copy[0])
#            elif my_word_copy[0] != other_word_copy[0]:
#                del(my_word_copy[0])
#                del(other_word_copy[0])
#            else:
#                print("Uh oh!")
#       
#        if match == len(my_word):
#            #Hidden cannot be already revealed letter#


def show_possible_matches(my_word, false_count):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    for w in wordlist:
        if match_with_gaps(my_word, w) == True:
            print(w)
        else:
            false_count += 1
        
        if false_count == len(wordlist):
            print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    letters_guessed_copy = []
    guesses = 6
    warnings = 3
    currently = '_ ' * len(secret_word)

    print("Welcome to the game Hangman!")
    print("If you ever need a hint, type '*' and then hint enter.")
    print("Otherwise, type the letter you're guessing and then hint enter.")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("------------------------------------")
    
    while is_word_guessed(secret_word, letters_guessed) == False and guesses > 0:
        
        print("You have", guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        x = input("Please guess a letter: ")
        
        #hint time!#
        if x == "*":
            false_count = 0
            #Must be here else reset false_count every time in loop#
            show_possible_matches(currently, false_count)
        
        #1+ char
        elif len(x) > 1:
            print("Oops! Please only guess one letter.")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        #Not char
        elif str.isalpha(x) == False:
            print("Oops! That is not a valid letter.")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        #1 char
        elif str.isalpha(x) == True:
            letters_guessed_copy += str.lower(x)
            #Char duplicate?
            letters_count = 0
            for l in letters_guessed:
                for lc in letters_guessed_copy:
                    if l == lc:
                        letters_count += 1
            if letters_count > len(letters_guessed):
                print("Oops! You've already guessed that letter.")
                (warnings, guesses, currently) = warning(warnings, guesses, currently)
                letters_guessed_copy = letters_guessed[:]
                ### = ≠ == ! ###
                ### Tell it to make a copy [:], not become aliases!! ###
            else:
                letters_guessed += str.lower(x)
                (currently, guessed) = get_guessed_word(secret_word, letters_guessed, currently)                      
                #Char in word?
                if guessed == True:
                    print("Good guess: ", currently)
                #Vowel vs consonant penalty
                else:
                    if x == "a" or x == "e" or x == "i" or x == "o" or x == "u":
                        ### yes, "x ==" for every single one ###
                        print("Oops! That vowel is not in my word. Vowels are expensive! Lose 2 guesses: ", currently)
                        guesses -= 2
                    else:
                        print("Oops! That consonant is not in my word: ", currently)
                        guesses -= 1
        else:
            print("Boi what is u doin !!!")
            (warnings, guesses, currently) = warning(warnings, guesses, currently)
        print("------------------------------------")
        
    #Winning
    if is_word_guessed(secret_word, letters_guessed) == True and guesses > 0:
        secret_word_points = one_of_each(secret_word)
        
        print("Congratulations, you won!")
        print("Your total score for this game is:", guesses*len(secret_word_points))
    
    #StraightOuttaGuesses    
    else:
        print("Oh no, you ran out of guesses ):")
        print("The word was '" + secret_word + "'.")
        print("Game over")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
#    # pass
#
#    # To test part 2, comment out the pass line above and
#    # uncomment the following two lines.
#    
#    secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

