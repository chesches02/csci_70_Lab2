SimpCalc Parser and Compiler
Made by:
Sy, Star Neptune
Hung, Cheska
Bomediano, Al

How it works (Scanner.py)
1. The Scanner module uses a dictionary in order to build a token.
2. Each key leads to a state depending on its former state
3. Some states requires the pointer to stop and encode the selected state.
4. Other states require looking back to the previous characters. Usually these are the states that wait for an interruption of a defined sequense before encoding the token.
5. Faulty or erroneous tokens are skipped.
6. It has a separate function to format the tokens correctly when it is being printed to a text file.

How it works (Parser.py)
1. It takes the raw tokens from the gettoken() function of Scanner.py.
2. It takes the grammar tokens and recursively checks if they can be removed because of matching the token label or if it could be broken down.
3. Ideally it should return an empty list because it means all tokens are accounted for.
4. It detects errors by finding a mismatch between expected tokens and actual tokens.
5. If no errors are found then it declares that file to be a valid SimpCalc program.

How to run it
1. Paste your sample SimpCalc program into SimpCalc_input.txt.
2. Run Scanner.py
3. Run Parser.py
4. There should be two new files called SimpCalc_output_scan.txt and SimpCalc_output_parse.
5. Have fun!