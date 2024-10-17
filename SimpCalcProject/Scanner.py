import re #for determining the different symbol groups

LETTER_PATTERN = "[A-z]"
DIGIT_PATTERN = "[0-9]"

states = {
    'start' : {
        LETTER_PATTERN : 1,
        '_' : 1,
        DIGIT_PATTERN : 2, 
        '"' : 3,
        ':' : 5,
        '*' : 6,
        '<' : 7,
        '>' : 8,
        '!' : 9,
        '/' : 10,
        ';' : "SEMICOLON",
        ',' : "COMMA",
        '-' : "MINUS",
        ')' : "RIGHTPAREN",
        '(' : "LEFTPAREN",
        '=' : "EQUAL",
        '+' : "PLUS"
        #maybe I'll put the end_of_file symbol later, or not depends. I just put this here to say that it will depend later
    },

    1 : {
        LETTER_PATTERN : 1,
        DIGIT_PATTERN : 1,
        '_' : 1,
        '[^A-Za-z_0-9]' : "IDENTIFIER", # the key is just ReGex for:  NOT a letter (uppercase or lowercase) or a number.
    },

    2 : {
        DIGIT_PATTERN : 2,
        '.' : 4,
        '[^,.eE0-9]' : "NUM", # the key is ReGex for NOT a dot, comma, e or E
    },

    3 : {
        '\n' : "ERROR_1", #error for an unclosed quotation
        '[^"]' : 3, # ReGex for NOT a quotation mark
        '"' : "STRING",  
    },

    4 : {
        DIGIT_PATTERN : 4,
        '[eE]' : 12,
        '[^0-9]' : "NUM", # NOT DIGIT
    },

    5 : {
        '=' : "ASSIGN",
        '[^=]' : "COLON", 
    },

    6 : {
        '*' : "RAISE",
        '[^*]' : "MULTIPLY",
    },

    7 : {
        '=' : "LT_EQUAL",
        '[^=]' : "LESS_THAN", # NOT =
    },

    8 : {
        '=' : "GT_EQUAL",
        '[^=]' : "GREATER_THAN", # NOT =
    },

    9 : {
        '=' : "NOT_EQUAL",
        '[^=]' : "ERROR_2", # NOT =, error invalid token for !
    },

    10 : {
        '/' : 11,
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

    # Tokens (not pushback) ====================

    "ASSIGN" : {},
    "RAISE" : {},
    "LT_EQUAL" : {},
    "GT_EQUAL" : {},
    "NOT_EQUAL" : {},
    "SEMICOLON" : {},
    "COMMA" : {},
    "MINUS" : {},
    "END_OF_FILE" : {},
    "RIGHTPAREN" : {},
    "LEFTPAREN" : {},
    "EQUAL" : {},
    "PLUS" : {},



}

def main():
    input_file_path = 'SimpCalcProject/test_inp.txt'
    #output_file_path = 'scanner_out.txt'

    with open(input_file_path, 'r') as file:
        input_string = file.read().strip()

    i = 0

    lenProg = len(input_string)

    while i < lenProg: # the main loop


if __name__ == '__main__':
    main()