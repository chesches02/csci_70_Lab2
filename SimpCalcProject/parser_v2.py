import regex

# def is a special state where it doesn't get what it wants
grammar_rules = {
    "Prg" : {
        "default" : "Blk EndOfFile",
        },
    "Blk" : {
        "Identifier" : "Stm Blk",
        "print" : "Stm Blk",
        "if" : "Stm Blk",
        "default" : "",  
    },
    "Stm" : {
        "Identifier" : "Identifier Assign Exp Semicolon",
        "print" : "PRINT(Arg Argfollow) Semicolon",
        "if" : "if Cnd : Blk Iffollow",
        "default" : "-1"
    },
    "Argfollow" : {
        "Comma" : "Arg Argfollow",
        "default" : "",
    },
    "Arg" : {
        "String" : "String",
        "default" : "Exp",
    },
    "Iffollow" : {
        "ENDIF" : "ENDIF Semicolon",
        "ELSE" : "ELSE Blk ENDIF Semicolon",
    },
    "Exp" : {
        "default" : "Trm Trmfollow",
    },
    "Trmfollow" : {
        "Plus" : "+ Trm Trmfollow",
        "Minus" : "Minus Trm Trmfollow",
        "default" : "",
    },
    "Trm" : {
        "default" : "Fac Facfollow",
    },
    "Facfollow" : {
        "Multiply" : "∗ Fac Facfollow",
        "Divide" : "/ Fac Facfollow",
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
        "default" : "Val,"
    },
    "Val" : {
        "Identifier" : "Identifier",
        "Number" : "Number",
        "sqrt" : "sqrt LeftParen Exp RightParen",
        "default" : "Exp",
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

grammar_keys = grammar_rules.keys

def recursive_descent_parser(parsetree="Prg",tokenlist):
    currentText = parsetree
    for key in grammar_keys:
        if key in currentText: #if 



if __name__ == "__main__":
    with open('SimpCalcProject/scanner_out.txt', 'r') as file:
        # Example usage
        test_input = file.read()
    
        result = process_scanner_file(test_input, file.name)
        with open('SimpCalcProject/parser_out.txt', 'w') as outp:
            outp.write(result)
