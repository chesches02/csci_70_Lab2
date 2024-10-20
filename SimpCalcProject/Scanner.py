import re #for determining the different symbol groups

def printResults(ans):
    with open('SimpCalcProject/scanner_out.txt', 'w') as file:
        for i in ans:
            if (i[1] != 15):
                file.write("{:<12}{:<12}\n".format(i[1],i[0]))

LETTER_PATTERN = "[A-z]"
DIGIT_PATTERN = "[0-9]"
ANY_OR_NEWLINE = '.| |\n'

states = {
    'start' : {
        LETTER_PATTERN : 1,
        '[_]' : 1,
        DIGIT_PATTERN : 2, 
        '["]' : 3,
        '[:]' : 5,
        '[*]' : 6,
        '[<]' : 7,
        '[>]' : 8,
        '[!]' : 9,
        '[/]' : 10,
        '[;]' : "SEMICOLON",
        '[,]' : "COMMA",
        '[-]' : "MINUS",
        '[)]' : "RIGHTPAREN",
        '[(]' : "LEFTPAREN",
        '[=]' : "EQUAL",
        '[+]' : "PLUS",
        '[ \n]' : 'start' # fsr wala pala spacebar and newline
    },

    1 : {
        LETTER_PATTERN : 1,
        DIGIT_PATTERN : 1,
        '[_]' : 1,
        '[^A-Za-z_0-9]' : "IDENTIFIER", # the key is just ReGex for:  NOT a letter (uppercase or lowercase) or a number.
    },

    2 : {
        DIGIT_PATTERN : 2,
        '[.]' : 4,
        '[^,.eE0-9]' : "NUM", # the key is ReGex for NOT a dot, comma, e or E
    },

    3 : {
        '[\n]' : "ERROR_1", #error for an unclosed quotation
        '[^"]' : 3, # ReGex for NOT a quotation mark
        '"' : "STRING",  
    },

    4 : {
        DIGIT_PATTERN : 4,
        '[eE]' : 12,
        '[^0-9]' : "NUM", # NOT DIGIT
    },

    5 : {
        '[=]' : "ASSIGN",
        '[^=]' : "COLON", 
    },

    6 : {
        '[*]' : "RAISE",
        '[^*]' : "MULTIPLY",
    },

    7 : {
        '[=]' : "LT_EQUAL",
        '[^=]' : "LESS_THAN", # NOT =
    },

    8 : {
        '[=]' : "GT_EQUAL",
        '[^=]' : "GREATER_THAN", # NOT =
    },

    9 : {
        '[=]' : "NOT_EQUAL",
        '[^=]' : "ERROR_2", # NOT =, error invalid token for !
    },

    10 : {
        '[/]' : 11,
        '[^/]' : "DIVIDE"
    },

    11 : {
        '[^\n]' : 11,
        '[\n]' : 15,
    },

    12 : {
        '[+-]' : 16,
        DIGIT_PATTERN : 13,
        '[^0-9]' : "NUM", # NOT DIGIT
    },

    13 : {
        DIGIT_PATTERN : 13,
        '.' : 14,
        '[^0-9.]' : "NUM", # NOT DIGIT
    },

    14 : {
        DIGIT_PATTERN : 14,
        '[^0-9]' : "NUM", # NOT DIGIT
    },

    16 : {
        DIGIT_PATTERN : 13,
        '[^0-9]' : "ERROR_3", # NOT DIGIT, Exponential format error
    },

    # Tokens (not pushback) ====================

    "ASSIGN" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "RAISE" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "LT_EQUAL" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "GT_EQUAL" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "NOT_EQUAL" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "SEMICOLON" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "COMMA" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "MINUS" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "END_OF_FILE" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "RIGHTPAREN" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "LEFTPAREN" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "EQUAL" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "PLUS" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },

    # Tokens (pushback)===================================

    "IDENTIFIER" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "NUM" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "STRING" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "COLON" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "MULTIPLY" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "LESS_THAN" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "GREATER_THAN" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "DIVIDE" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    15 : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },

    # ERROR NODES =======================

    "ERROR_1" : {
        'description' :  'Lexical Error : expected closing parenthesis (") here',
        ANY_OR_NEWLINE : "ERROR",
    },

    "ERROR_2" : {
        'description' :  'Lexical Error: invalid token (!)',
        ANY_OR_NEWLINE : "ERROR",
    }, 

    "ERROR_3" : {
        'description' :  'Lexical Error: incorrect exponential float format',
        ANY_OR_NEWLINE : "ERROR",
    }, 

}

def main():
    input_file_path = 'SimpCalcProject/test_inp.txt'

    with open(input_file_path, 'r') as file:
        input_string = file.read().strip()
    
    input_string += "?" #this serves as the end of file character

    i = 0
    lenProg = len(input_string)
    currentState = "start"
    tempBuiltString = ""
    stringCollection = []

    while i < lenProg: # the main loop
        currentChar = input_string[i]
        pushback = 0
        nextState = None

        print(f"State: {currentState}   input: {currentChar}")

        # check if we're at the last character
        #if i == (lenProg-1): 
        
        #calculate the next state
        for pattern in states[currentState]:
            # if pattern matches the string
            if re.search(pattern, currentChar):
                nextState = states[currentState][pattern]
        
        # evaluating the currentState
        # tokens
        if ('pushback' in states[currentState]): # check if the pushback key is here.
            if (states[currentState]['pushback'] == -2):
                print(f"StringBuilt: {tempBuiltString[:len(tempBuiltString)-1]}") # prune the last
                stringCollection.append((tempBuiltString[:len(tempBuiltString)-1],currentState))
            elif(states[currentState]['pushback'] == -1):
                print(f"StringBuilt: {tempBuiltString}") # prune the last
                stringCollection.append((tempBuiltString,currentState))
            tempBuiltString = ""
            pushback = states[currentState]['pushback']
        elif (nextState == 'ERROR'):
            print(states[currentState]['description'])
        elif (currentState == 'start' and nextState =='start'): # if you are in start and it's a whitespace, skip it
            pass
        else:
            tempBuiltString += currentChar

        currentState = nextState
        i+=(1+pushback) # end of loop, just to start again; see if it moves or nah
    
    currentState = "END_OF_FILE"

    #stringCollection.append((ENDOFFILE))
    
    print(stringCollection)
    printResults(stringCollection)


if __name__ == '__main__':
    main()