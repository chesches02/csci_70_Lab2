import re

def tokenize(input_string):
    tokens = []
    state = 'A'
    num_buffer = ''
    
    def emit_token(token_type, value=''):
        tokens.append(f'{token_type:<6}\t{value}')
    
    i = 0
    while i < len(input_string):
        char = input_string[i]
        
        if state == 'A':
            if char.isdigit():
                state = 'B'
                num_buffer += char
            elif char in [' ', '\t', '\n']:
                pass  # Ignore whitespace
            elif char == '=':
                state = 'E'
            elif char == '+':
                emit_token('PLUS', '+')
            elif char == '-':
                emit_token('MINUS', '-')
            else:
                emit_token('ERROR', f'Lexical Error reading character "{char}"')
                break
        
        elif state == 'B':
            if char.isdigit():
                num_buffer += char
            else:
                emit_token('NUM', num_buffer)
                num_buffer = ''
                state = 'A'
                i -= 1  # Pushback
        
        elif state == 'E':
            if char == '=':
                emit_token('ASSIGN', '==')
                state = 'A'
            else:
                emit_token('ERROR', f'Lexical Error reading character "{char}"')
                break
        
        i += 1
    
    # Handle any remaining number in the buffer
    if num_buffer:
        emit_token('NUM', num_buffer)
    
    return tokens

def main():
    input_file_path = 'input2.txt'
    output_file_path = 'output2.txt'

    for i in range(1,4):
        # Read the input file
        with open(input_file_path, 'r') as file:
            input_string = file.read().strip()

        # Tokenize the input string
        tokens = tokenize(input_string)

        # Write tokens to the output file
        with open(output_file_path, 'w') as file:
            for token in tokens:
                file.write(token + '\n')

if __name__ == '__main__':
    main()