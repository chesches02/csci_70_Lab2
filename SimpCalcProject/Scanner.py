import re #for determining the different symbol groups

def printResults(ans):
    with open('SimpCalcProject/scanner_out.txt', 'w') as file:
        for i in ans:
            if(i[1] == "Identifier"):
                if(i[0] == "PRINT"):
                    file.write("{:<12}{:<12}\n".format("Print",i[0]))
                elif(i[0] == "IF"):
                    file.write("{:<12}{:<12}\n".format("If",i[0]))
                elif(i[0] == "ELSE"):
                    file.write("{:<12}{:<12}\n".format("Else",i[0]))
                elif(i[0] == "ENDIF"):
                    file.write("{:<12}{:<12}\n".format("Endif",i[0]))
                elif(i[0] == "AND"):
                    file.write("{:<12}{:<12}\n".format("And",i[0]))
                elif(i[0] == "OR"):
                    file.write("{:<12}{:<12}\n".format("Or",i[0]))
                elif(i[0] == "NOT"):
                    file.write("{:<12}{:<12}\n".format("Not",i[0]))
                else:
                    file.write("{:<12}{:<12}\n".format(i[1],i[0]))
            elif (i[1] != 15):
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
        '[;]' : "Semicolon",
        '[,]' : "Comma",
        '[-]' : "Minus",
        '[)]' : "RightParen",
        '[(]' : "LeftParen",
        '[=]' : "Equal",
        '[+]' : "Plus",
        '[ \n]' : 'start', # fsr wala pala spacebar and newline
        '[.?&@$%]' : 'ERROR_4', # not within the allowed symbols
    },

    1 : {
        LETTER_PATTERN : 1,
        DIGIT_PATTERN : 1,
        '[_]' : 1,
        '[^A-Za-z_0-9]' : "Identifier", # the key is just ReGex for:  NOT a letter (uppercase or lowercase) or a number.
    },

    2 : {
        DIGIT_PATTERN : 2,
        '[.]' : 4,
        '[eE]' :12,
        '[^,.eE0-9]' : "Number", # the key is ReGex for NOT a dot, comma, e or E
    },

    3 : {
        '[\n]' : "ERROR_1", #error for an unclosed quotation
        '[^\"\n]' : 3, # ReGex for NOT a quotation mark or a newline
        '\"' : "String",  
    },

    4 : {
        DIGIT_PATTERN : 4,
        '[eE]' : 12,
        '[^0-9eE]' : "Number", # NOT DIGIT
    },

    5 : {
        '[=]' : "Assign",
        '[^=]' : "Colon", 
    },

    6 : {
        '[*]' : "Raise",
        '[^*]' : "Multiply",
    },

    7 : {
        '[=]' : "LTEqual",
        '[^=]' : "LessThan", # NOT =
    },

    8 : {
        '[=]' : "GTEqual",
        '[^=]' : "GreaterThan", # NOT =
    },

    9 : {
        '[=]' : "NotEqual",
        '[^=]' : "ERROR_2", # NOT =, error invalid token for !
    },

    10 : {
        '[/]' : 11,
        '[^/]' : "Divide"
    },

    11 : {
        '[^\n]' : 11,
        '[\n]' : 15,
    },

    12 : {
        '[+-]' : 16,
        DIGIT_PATTERN : 13,
        '[^0-9+-]' : "ERROR_3", # NOT DIGIT or NOT whitespace
    },

    13 : {
        DIGIT_PATTERN : 13,
        '.' : 14,
        '[^0-9.]' : "Number", # NOT DIGIT
    },

    14 : {
        DIGIT_PATTERN : 14,
        '[^0-9]' : "Number", # NOT DIGIT
    },

    16 : {
        DIGIT_PATTERN : 13,
        '[^0-9]' : "ERROR_3", # NOT DIGIT, Exponential format error
    },

    # Tokens (not pushback) ====================

    "Assign" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Raise" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "LTEqual" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "GTEqual" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "NotEqual" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Semicolon" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Comma" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Minus" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "END_OF_FILE" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "RightParen" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "LeftParen" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Equal" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "Plus" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },
    "String" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -1,
    },

    # Tokens (pushback)===================================

    "Identifier" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "Number" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "Colon" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },

    "Multiply" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "LessThan" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "GreaterThan" : {
        ANY_OR_NEWLINE : 'start', # regex for any value
        'pushback' : -2,
    },
    
    "Divide" : {
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
        ANY_OR_NEWLINE : "skipLine",
        'pushback' : -1,
    },

    "ERROR_2" : {
        'description' :  'Lexical Error: invalid token (!)',
        ANY_OR_NEWLINE : "skipLine",
        'pushback' : -1,
    }, 

    "ERROR_3" : {
        'description' :  'Lexical Error: incorrect number format',
        ANY_OR_NEWLINE : "skipLine",
        'pushback' : -1,
    }, 

    "ERROR_4" : {
        'description' :  'Lexical Error: illegal character sequence',
        ANY_OR_NEWLINE : "skipLine",
        'pushback' : -1,
    }, 

    "skipLine" : { # not that the line is invalid, just repeat until the next line
        '[^\n]' : "skipLine",
        '[\n]' : 'start'
    }

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
                if ("ERROR" not in str(currentState)):
                    print(f"StringBuilt: {tempBuiltString[:len(tempBuiltString)]}")
                    stringCollection.append((tempBuiltString[:len(tempBuiltString)],currentState))
                else:
                    print(states[currentState]['description'])
                    stringCollection.append((states[currentState]['description'],"Error"))
                
            tempBuiltString = ""
            pushback = states[currentState]['pushback']
        elif (currentState == "skipLine"):
            tempBuiltString = ""
        elif (currentState == 'start' and nextState =='start'): # if you are in start and it's a whitespace, skip it
            pass
        else:
            tempBuiltString += currentChar

        currentState = nextState
        i+=(1+pushback) # end of loop, just to start again; see if it moves or nah


    # if the tempBuiltString still has elements, run it one more iteration. It's for the pushback
    if len(tempBuiltString) > 0:
        print(tempBuiltString)
        print(currentState)
        # check if it's a pushback state of -2
        if 'pushback' in states[currentState]:
            if states[currentState]['pushback'] == -2:
                stringCollection.append((tempBuiltString[:len(tempBuiltString)-1],currentState))
        

    currentState = "END_OF_FILE"

    #stringCollection.append((ENDOFFILE))
    
    print(stringCollection)
    printResults(stringCollection)


if __name__ == '__main__':
    main()