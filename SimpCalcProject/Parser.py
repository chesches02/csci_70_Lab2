class Token:
    def __init__(self, type, value, line_number=1):
        self.type = type
        self.value = value
        self.line_number = line_number

class Parser:
    def __init__(self):
        self.current_token = None
        self.tokens = []
        self.current_index = 0
        self.output = []
        self.line_number = 1
        self.has_error = False
        self.filename = ""
        self.error_encountered = False
    def parse_scanner_output(self, scanner_lines, filename=""):
        self.filename = filename
        # Convert scanner output to tokens
        current_line = 1
        for line in scanner_lines:
            if not line.strip():
                continue
            parts = line.strip().split(None, 1)  # Split into max 2 parts
            if len(parts) >= 2:
                token_type = parts[0]
                token_value = parts[1]

                # Check for lexical errors
                if token_type == "Lexical" and "Error" in token_value:
                    self.has_error = True
                    self.error_encountered = True
                    self.output.append(f"Parse Error: Assign expected.")
                    break
                elif token_type == "Error":
                    self.has_error = True
                    self.error_encountered = True
                    break
                self.tokens.append(Token(token_type, token_value, current_line))
                current_line += 1
    def get_next_token(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.line_number = self.current_token.line_number
            self.current_index += 1
            return self.current_token
        return None

    def peek_next_token(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def parse(self):
        # Handle empty file case
        if not self.tokens:
            return ""
            
        self.program()
        if not self.has_error and self.tokens:
            if self.filename:
                self.output.append(f"{self.filename} is a valid SimpCalc program")
            else:
                self.output.append("Input is a valid SimpCalc program")
        return '\n'.join(self.output)

    def error(self, message):
        self.has_error = True
        if not self.error_encountered:
            self.output.append(f"Parse Error: {message} expected.")
            self.error_encountered = True
    def program(self):
        while self.current_index < len(self.tokens) and not self.error_encountered:
            if self.statement():
                continue
            else:
                if not self.has_error:
                    token = self.peek_next_token()
                    if token and token.type != "Error":
                        self.error(f"Valid statement")
                break

    def statement(self):
        token = self.peek_next_token()
        if not token:
            return False

        if token.type == "Identifier":
            return self.assignment_statement()
        elif token.type == "If":
            return self.if_statement()
        elif token.type == "Print":
            return self.print_statement()
        elif token.type == "Error":
            self.has_error = True
            return False
        return False

    def assignment_statement(self):
        token = self.get_next_token()  # Identifier
        if not token or token.type != "Identifier":
            return False

        token = self.get_next_token()  # Assign
        if not token or token.type != "Assign":
            self.error("Assign")
            return False

        if not self.expression():
            return False

        token = self.get_next_token()  # Semicolon
        if not token or token.type != "Semicolon":
            self.error("Semicolon")
            return False

        self.output.append("Assignment Statement Recognized")
        return True

    def if_statement(self):
        token = self.get_next_token()  # IF
        if not token or token.type != "If":
            return False

        self.output.append("If Statement Begins")

        if not self.condition():
            return False

        token = self.get_next_token()  # Colon
        if not token or token.type != "Colon":
            self.error("Colon")
            return False

        while True:
            token = self.peek_next_token()
            if not token or token.type in ["Endif", "Else"]:
                break
            if not self.statement():
                if self.error_encountered:
                    return False
                break


        token = self.peek_next_token()
        if token and token.type == "Else":
            self.get_next_token()  # consume ELSE
            while True:
                token = self.peek_next_token()
                if not token or token.type == "Endif":
                    break
                if not self.statement():
                    if self.error_encountered:
                        return False
                    break

        token = self.get_next_token()  # ENDIF
        if not token or token.type != "Endif":
            self.error("ENDIF")
            return False

        token = self.get_next_token()  # Semicolon
        if not token or token.type != "Semicolon":
            self.error("Semicolon")
            return False

        if not self.error_encountered:
            self.output.append("If Statement Ends")
        return True
    def print_statement(self):
        token = self.get_next_token()  # PRINT
        if not token or token.type != "Print":
            return False

        token = self.get_next_token()  # LeftParen
        if not token or token.type != "LeftParen":
            self.error("Left parenthesis")
            return False

        if not self.print_list():
            return False

        token = self.get_next_token()  # RightParen
        if not token or token.type != "RightParen":
            self.error("Right parenthesis")
            return False

        token = self.get_next_token()  # Semicolon
        if not token or token.type != "Semicolon":
            self.error("Semicolon")
            return False
        
        self.output.append("Print Statement Recognized")
        return True
    
    def condition(self):
        if not self.subcondition():
            return False

        and_count = 0
        or_count = 0

        while True:
            token = self.peek_next_token()
            if not token or token.type not in ["And", "Or"]:
                break

            if token.type == "And":
                and_count += 1
            elif token.type == "Or":
                or_count += 1

            if and_count + or_count > 1 or and_count > 1 or or_count > 1:
                self.error("Colon")
                return False

            self.get_next_token()  # consume AND/OR
            if not self.subcondition():
                return False

        return True

    def subcondition(self):
        if not self.expression():
            return False

        token = self.get_next_token()
        if not token or token.type not in ["Equal", "NotEqual", "LessThan", "GreaterThan", "GTEqual", "LTEqual"]:
            self.error("Comparison operator")
            return False

        if not self.expression():
            return False

        return True

    def expression(self):
        if not self.term():
            return False

        while True:
            token = self.peek_next_token()
            if not token or token.type not in ["Plus", "Minus"]:
                break
            self.get_next_token()
            if not self.term():
                return False
        return True

    def term(self):
        if not self.factor():
            return False

        while True:
            token = self.peek_next_token()
            if not token or token.type not in ["Multiply", "Divide"]:
                break
            self.get_next_token()
            if not self.factor():
                return False
        return True

    def factor(self):
        token = self.peek_next_token()
        if not token:
            return False

        if token.type in ["Number", "Identifier"]:
            self.get_next_token()
            token = self.peek_next_token()
            if token and token.type == "Raise":
                self.get_next_token()  # consume **
                return self.factor()
            return True
        elif token.type == "LeftParen":
            self.get_next_token()  # consume (
            if not self.expression():
                return False
            token = self.get_next_token()  # consume )
            if not token or token.type != "RightParen":
                self.error("Right parenthesis")
                return False
            return True
        elif token.type in ["Plus", "Minus"]:
            self.get_next_token()  # consume +/-
            return self.factor()
        elif token.type == "Sqrt":
            self.get_next_token()  # consume SQRT
            return self.factor()
        return False

    def print_statement(self):
        token = self.get_next_token()  # PRINT
        if not token or token.type != "Print":
            return False

        token = self.get_next_token()  # LeftParen
        if not token or token.type != "LeftParen":
            self.error("Left parenthesis")
            return False

        if not self.print_list():
            return False

        token = self.get_next_token()  # RightParen
        if not token or token.type != "RightParen":
            self.error("Right parenthesis")
            return False

        token = self.get_next_token()  # Semicolon
        if not token or token.type != "Semicolon":
            self.error("Semicolon")
            return False

        self.output.append("Print Statement Recognized")
        return True

    def print_list(self):
        if not self.print_item():
            return False

        while True:
            token = self.peek_next_token()
            if not token or token.type != "Comma":
                break
            self.get_next_token()  # consume comma
            if not self.print_item():
                return False
        return True

    def print_item(self):
        token = self.peek_next_token()
        if not token:
            return False
        if token.type in ["String", "Identifier"]:
            self.get_next_token()
            return True
        return self.expression()

def process_scanner_file(scanner_content, filename=""):
    parser = Parser()
    scanner_lines = scanner_content.strip().split('\n')
    parser.parse_scanner_output(scanner_lines, filename)
    return parser.parse()

# Function to process a file and create output
def process_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Extract base filename without extension
        base_filename = filename.split('/')[-1].split('.')[0]
        
        # Generate parser output
        result = process_scanner_file(content, f"sample{base_filename}.txt")
        
        # Create parser output filename
        parser_filename = f"{base_filename}Parser.txt"
        
        # Write to parser output file
        with open(parser_filename, 'w') as f:
            f.write(result)
            
    except FileNotFoundError:
        print(f"File {filename} not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    with open('SimpCalcProject/scanner_out.txt', 'r') as file:
        # Example usage
        test_input = file.read()
    
        result = process_scanner_file(test_input, file.name)
        with open('SimpCalcProject/parser_out.txt', 'w') as outp:
            outp.write(result)