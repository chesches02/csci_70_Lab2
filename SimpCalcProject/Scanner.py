import re #for determining the different symbol groups

LETTER_PATTERN = "[A-z]"
DIGIT_PATTERN = "[0-9]"

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
        '[+]' : "PLUS"
        #maybe I'll put the end_of_file symbol later, or not depends. I just put this here to say that it will depend later
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
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "RAISE" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "LT_EQUAL" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "GT_EQUAL" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "NOT_EQUAL" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "SEMICOLON" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "COMMA" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "MINUS" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "END_OF_FILE" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "RIGHTPAREN" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "LEFTPAREN" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "EQUAL" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },
    "PLUS" : {
        '.' : 'start', # regex for any value
        'pushback' : 0,
    },

    # Tokens (pushback)===================================

    "IDENTIFIER" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },

    "NUM" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },

    "STRING" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },

    "COLON" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },

    "MULTIPLY" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },
    
    "LESS_THAN" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },
    
    "GREATER_THAN" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },
    
    "DIVIDE" : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },
    
    15 : {
        '.' : 'start', # regex for any value
        'pushback' : -1,
    },

    # ERROR NODES =======================

    "ERROR_1" : {
        'description' :  'Lexical Error : expected closing parenthesis (") here',
        '.' : "ERROR",
    },

    "ERROR_2" : {
        'description' :  'Lexical Error: invalid token (!)',
        '.' : "ERROR",
    }, 

    "ERROR_3" : {
        'description' :  'Lexical Error: incorrect exponential float format',
        '.' : "ERROR",
    }, 

}

def main():
    input_file_path = 'SimpCalcProject/test_inp.txt'
    #output_file_path = 'scanner_out.txt'

    with open(input_file_path, 'r') as file:
        input_string = file.read().strip()

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

        
        #calculate the next state
        for pattern in states[currentState]:
            # if pattern matches the string
            if re.search(pattern, currentChar):
                nextState = states[currentState][pattern]
        
        # evaluating the currentState
        # tokens
        if (nextState == 'start'): # if the nextState leads back to the start, check for the name because it's probably a token now
            print(tempBuiltString)
            stringCollection.append((tempBuiltString,currentState))
            tempBuiltString = ""
            pushback = states[currentState]['pushback']
        elif (nextState == 'ERROR'):
            print(states[currentState]['description'])
        else:
            tempBuiltString += currentChar

        currentState = nextState
        i+=1 # end of loop, just to start again
        i+=pushback # see if it moves or nah
    
    print(stringCollection)


if __name__ == '__main__':
    main()