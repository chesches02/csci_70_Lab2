import re
import sys

sys.setrecursionlimit(30)

char_match = {
    ""
}

# def is a special state where it doesn't get what it wants
grammar_rules = {
    "Prg" : {
        "default" : "Blk EndOfFile",
        },
    "Blk" : {
        "Identifier" : "Stm Blk",
        "Print" : "Stm Blk",
        "If" : "Stm Blk",
        "default" : "",  
    },
    "Stm" : {
        "Identifier" : "Identifier Assign Exp Semicolon",
        "Print" : "Print LeftParen Arg Argfollow RightParen Semicolon",
        "If" : "If Cnd Colon Blk Iffollow",
    },
    "Argfollow" : {
        "Comma" : "Comma Arg Argfollow",
        "default" : "",
    },
    "Arg" : {
        "String" : "String",
        "default" : "Exp",
    },
    "Iffollow" : {
        "Endif" : "Endif Semicolon",
        "Else" : "Else Blk Endif Semicolon",
    },
    "Exp" : {
        "default" : "Trm Trmfollow",
    },
    "Trmfollow" : {
        "Plus" : "Plus Trm Trmfollow",
        "Minus" : "Minus Trm Trmfollow",
        "default" : "",
    },
    "Trm" : {
        "default" : "Fac Facfollow",
    },
    "Facfollow" : {
        "Multiply" : "Multiply Fac Facfollow",
        "Divide" : "Divide Fac Facfollow",
        "default" : "",
    },
    "Fac" : {
        "default" : "Lit Litfollow",
    },
    "Litfollow" : {
        "Raise" : "Raise Lit Litfollow",
        "default" : "",
    },
    "Lit" : {
        "Minus" : "Minus Val",
        "default" : "Val",
    },
    "Val" : {
        "Identifier" : "Identifier",
        "Number" : "Number",
        "Sqrt" : "Sqrt LeftParen Exp RightParen",
        "default" : "LeftParen Exp RightParen",
    },
    "Cnd" : {
        "default" : "Exp Rel Exp",
    },
    "Rel" : {
        "LessThan" : "LessThan",
        "Equal" : "Equal",
        "GreaterThan" : "GreaterThan",
        "GTEqual" : "GTEqual",
        "NotEqual" : "NotEqual",
        "LTEqual" : "LTEqual",
    }
}

grammar_keys = grammar_rules.keys()
tokenList_index = 0
tokenList = []
writeToFile = []
hasError = False

def recursive_descent_parser(parsetree="Prg"):
    global tokenList_index
    global hasError

    print("{:<50}{:<15}{}\n".format(parsetree,tokenList[tokenList_index],tokenList_index+1))

    if parsetree == "If Cnd Colon Blk Iffollow":
        print("If Statement Begins")
        writeToFile.append("If Statement Begins")

    token_list = parsetree.split(' ')

    final_token_list = ["" for i in range(len(token_list))]

    # Recursive case
    i=0
    while i < len(token_list) and not hasError:
        print("now splitting: {:<35}".format(token_list[i]))

        # check if we still have token. just give it blanks when the tokens run out
        if tokenList_index >= len(tokenList):
            tokenList.append("")
        # check if it's equal to the token we are currently looking at
        if token_list[i] == tokenList[tokenList_index]:
            # annihilate it
            print(f"matches {token_list[i]}")
            tokenList_index += 1 
            i+=1
            #token_list[i] = ""

        # if not, check if it can be decomposed
        elif token_list[i] in grammar_keys:
            if tokenList[tokenList_index] in grammar_rules[token_list[i]].keys(): # rule based decomposition
                final_token_list[i] = (recursive_descent_parser(grammar_rules[token_list[i]][tokenList[tokenList_index]]))
            elif "default" in grammar_rules[token_list[i]].keys(): #default is the part where it just decomposes on its own
                final_token_list[i]  = (recursive_descent_parser(grammar_rules[token_list[i]]["default"]))
            else:
                print("Missing relational operator") 
                writeToFile("Missing relational operator")
                hasError = True
                break
            i += 1

        # if it's blank caused by a function decomposing to nothing, skip it.
        elif(token_list[i] == ""): 
            print("just a blank. skipping")
            i += 1

        # it is done
        elif(token_list[i] == "EndOfFile"): 
            print("Congratulations, you reached the end of file")
            i += 1
        
        #if for some reason, it can't be decomposed and it doesn't match the token we're currently looking at, there's probably an error
        else:
            print(f"Parse Error: {token_list[i]} expected. (line #{tokenList_index}) ")
            hasError = True
            writeToFile.append(f"Parse Error: {token_list[i]}      expected.")
            i += 1
            break
    
    # clean up final_token_list
    o = 0
    while o < len(final_token_list):
        if(final_token_list[o] == "" or final_token_list[o] == []):
            final_token_list.pop(o)
        else:
            o+=1

    # check for successes
    resolved = len(final_token_list)==0
    if parsetree == "Identifier Assign Exp Semicolon" and resolved and not hasError:
        print("Assignment Statement Recognized")
        writeToFile.append("Assignment Statement Recognized")
    elif parsetree == "Identifier Assign Exp Semicolon" and hasError:
        print("Assignment statement error")

    if parsetree == "Print LeftParen Arg Argfollow RightParen Semicolon" and resolved and not hasError:
        print("Print Statement Recognized")
        writeToFile.append("Print Statement Recognized")
    elif parsetree == "Print LeftParen Arg Argfollow RightParen Semicolon" and not resolved:
        print("Print Statement Error")

    if parsetree == "If Cnd Colon Blk Iffollow" and resolved and not hasError:
        print("If Statement Ends")
        writeToFile.append("If Statement Ends")
    if parsetree == "Else Blk EndIf Semicolon" and not resolved:
        print("Incomplete If Statement")

    #if not resolved:
        #print("STM failed")

    
    return final_token_list

if __name__ == "__main__":
    with open('SimpCalcProject/9Scanner.txt', 'r') as file:

        #turn it into a list of tokens
        for line in file:
            a = line.strip()
            tokenList.append(a.split(' ')[0])
        tokenList_index = 0
        isValid = len(recursive_descent_parser("Prg")) == 0
        with open('SimpCalcProject/parser_out.txt', 'w') as outp:
            for i in writeToFile:
                outp.write(i + "\n")
            if isValid and not hasError:
                outp.write(outp.name + " is a valid SimpCalc file")
