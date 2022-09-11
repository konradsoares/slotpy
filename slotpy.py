import random
import drivers
from time import sleep
print('''Welcome to the Slot Machine Simulator
You'll start with $50. You'll be asked if you want to play.
Answer with yes/no. you can also use y/n
No case sensitivity in your answer.
For example you can answer with YEs, yEs, Y, nO, N.
To win you must get one of the following combinations:
BAR\tBAR\tBAR\t\tpays\t$250
BELL\tBELL\tBELL/BAR\tpays\t$20
PLUM\tPLUM\tPLUM/BAR\tpays\t$14
ORANGE\tORANGE\tORANGE/BAR\tpays\t$10
CHERRY\tCHERRY\tCHERRY\t\tpays\t$7
CHERRY\tCHERRY\t  -\t\tpays\t$5
CHERRY\t  -\t  -\t\tpays\t$2
''')
#Constants:
INIT_STAKE = 50
#ITEMS = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR"]

firstWheel = None
secondWheel = None
thirdWheel = None
stake = INIT_STAKE

display = drivers.Lcd()
# Create object with custom characters data
cc = drivers.CustomCharacters(display)

# Redefine the default characters:
# Custom caracter #1. Code {0x00}.
cc.char_1_data = ["01110",
                  "01010",
                  "01110",
                  "00100",
                  "11111",
                  "11111",
                  "11111",
                  "11111"]
# Custom caracter #2. Code {0x01}.
cc.char_2_data = ["11111",
                  "10101",
                  "10101",
                  "11111",
                  "11111",
                  "10101",
                  "10101",
                  "11111"]

# Custom caracter #3. Code {0x02}.
cc.char_3_data = ["10001",
                  "10001",
                  "10001",
                  "11111",
                  "11111",
                  "11111",
                  "11111",
                  "11111"]

# Custom caracter #4. Code {0x03}.
cc.char_4_data = ["11111",
                  "11011",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "11011",
                  "11111"]

# Custom caracter #5. Code {0x04}.
cc.char_5_data = ["00000",
                  "00000",
                  "11011",
                  "11011",
                  "00000",
                  "10001",
                  "01110",
                  "00000"]

# Custom caracter #6. Code {0x05}.
cc.char_6_data = ["01010",
                  "11111",
                  "11111",
                  "01110",
                  "00100",
                  "00000",
                  "00000",
                  "00000"]

# Custom caracter #7. Code {0x06}.
cc.char_7_data = ["11111",
                  "11011",
                  "10001",
                  "10101",
                  "10101",
                  "10101",
                  "11011",
                  "11111"]

# Custom caracter #8. Code {0x07}.
cc.char_8_data = ["11111",
                  "10001",
                  "11111",
                  "00000",
                  "00000",
                  "11111",
                  "10001",
                  "11111"]

#ITEMS = ["1","2","3","4","5","6","7"]
ITEMS = ["{0x00}","{0x01}","{0x02}","{0x03}","{0x04}","{0x05}","{0x06}","{0x07}"]
# Load custom characters data to CG RAM:
cc.load_custom_characters_data()

#display.lcd_display_extended_string("{0x00}{0x01}{0x02}{0x03}{0x04}{0x05}{0x06}{0x07}", 2)

def play():
    global stake, firstWheel, secondWheel, thirdWheel
    playQuestion = askPlayer()
    while(stake != 0 and playQuestion == True):
        firstWheel = spinWheel()
        secondWheel = spinWheel()
        thirdWheel = spinWheel()
        printScore()
        playQuestion = askPlayer()

def askPlayer():
    '''
    Asks the player if he wants to play again.
    expecting from the user to answer with yes, y, no or n
    No case sensitivity in the answer. yes, YeS, y, y, nO . . . all works
    '''
    global stake
    while(True):
        answer = input("You have $" + str(stake) + ". Would you like to play? ")
        answer = answer.lower()
        if(answer == "yes" or answer == "y"):
            display.lcd_display_string('You have $'+str(stake)+'  ',1)
            display.lcd_display_string('Good Luck!',2)
            sleep(5)
            display.lcd_display_string('            ',1)
            display.lcd_display_string('          ',2)
            
            return True
        elif(answer == "no" or answer == "n"):
            display.lcd_display_string('                      ',1)
            display.lcd_display_string('                      ',2)
            display.lcd_display_string("Cash $" + str(stake),2)
            return False
        else:
            display.lcd_display_string("wrong input!",2)

def spinWheel():
    '''
    returns a random item from the wheel
    '''
    randomNumber = random.randint(0, 7)
    return ITEMS[randomNumber]

def printScore():
    '''
    prints the current score
    '''
    global stake, firstWheel, secondWheel, thirdWheel
    if((firstWheel == "{0x00}") and (secondWheel != "{0x00}")):
        win = 2
    elif((firstWheel == "{0x00}") and (secondWheel == "{0x00}") and (thirdWheel != "{0x00}")):
        win = 5
    elif((firstWheel == "{0x00}") and (secondWheel == "{0x00}") and (thirdWheel == "{0x00}")):
        win = 7
    elif((firstWheel == "{0x03}") and (secondWheel == "{0x03}") and ((thirdWheel == "{0x03}") or (thirdWheel == "{0x07}"))):
        win = 10
    elif((firstWheel == "{0x05}") and (secondWheel == "{0x05}") and ((thirdWheel == "{0x05}") or (thirdWheel == "{0x07}"))):
        win = 14
    elif((firstWheel == "{0x06}") and (secondWheel == "{0x06}") and ((thirdWheel == "{0x06}") or (thirdWheel == "{0x07}"))):
        win = 20
    elif((firstWheel == "{0x07}") and (secondWheel == "{0x07}") and (thirdWheel == "{0x07}")):
        win = 250
    else:
        win = -1

    stake += win
    if(win > 0):
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        sleep(1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        sleep(2)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        sleep(1)

        if(stake < 10):
            display.lcd_display_extended_string(firstWheel + '-' + secondWheel + '-' + thirdWheel + ' Cash ' + '$' + str(stake)+" ",1)
        else:
            display.lcd_display_extended_string(firstWheel + '-' + secondWheel + '-' + thirdWheel + ' Cash ' + '$' + str(stake),1)
        display.lcd_display_string('                      ',2)
        display.lcd_display_string('You win $' + str(win),2)

    else:
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        display.lcd_display_extended_string('{0x00}-{0x03}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x00}-{0x05}',1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        display.lcd_display_extended_string('{0x03}-{0x01}-{0x03}',1)
        display.lcd_display_extended_string('{0x01}-{0x05}-{0x04}',1)
        display.lcd_display_extended_string('{0x04}-{0x04}-{0x03}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x03}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        display.lcd_display_extended_string('{0x04}-{0x02}-{0x00}',1)
        display.lcd_display_extended_string('{0x06}-{0x01}-{0x06}',1)
        sleep(1)
        display.lcd_display_extended_string('{0x01}-{0x04}-{0x06}',1)
        sleep(2)
        display.lcd_display_extended_string('{0x02}-{0x01}-{0x02}',1)
        sleep(1)
        if(stake < 10):
            display.lcd_display_extended_string(firstWheel + '-' + secondWheel + '-' + thirdWheel + ' Cash ' + '$' + str(stake)+" ",1)
        else:
            display.lcd_display_extended_string(firstWheel + '-' + secondWheel + '-' + thirdWheel + ' Cash ' + '$' + str(stake),1)
        display.lcd_display_extended_string('                      ',2)
        display.lcd_display_extended_string('You lose',2)


play()
