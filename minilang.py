# Define token types
INTEGER = 'INTEGER'
IDENTIFIER = 'IDENTIFIER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EQUALS = 'EQUALS'
IF = 'IF'
ELSE = 'ELSE'
PRINT = 'PRINT'
EOF = 'EOF'

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            if current_char.isspace():
                self.pos += 1
                continue

            if current_char.isdigit():
                return self.number()

            if current_char.isalpha():
                return self.keyword_or_identifier()

            if current_char == '+':
                self.pos += 1
                return Token(PLUS, '+')
            elif current_char == '-':
                self.pos += 1
                return Token(MINUS, '-')
            elif current_char == '*':
                self.pos += 1
                return Token(MULTIPLY, '*')
            elif current_char == '/':
                self.pos += 1
                return Token(DIVIDE, '/')
            elif current_char == '(':
                self.pos += 1
                return Token(LPAREN, '(')
            elif current_char == ')':
                self.pos += 1
                return Token(RPAREN, ')')
            elif current_char == '=':
                self.pos += 1
                return Token(EQUALS, '=')
            else:
                self.error()

        return Token(EOF, None)

    def number(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            result += self.text[self.pos]
            self.pos += 1
        return Token(INTEGER, int(result))

    def keyword_or_identifier(self):
        result = ''
        while self.pos < len(self.text) and (self.text[self.pos].isalpha() or self.text[self.pos].isdigit()):
            result += self.text[self.pos]
            self.pos += 1
        if result == 'if':
            return Token(IF, result)
        elif result == 'else':
            return Token(ELSE, result)
        elif result == 'print':
            return Token(PRINT, result)
        else:
            return Token(IDENTIFIER, result)

# Parser class
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg="Invalid syntax"):
        raise Exception(msg)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == IDENTIFIER:
            value = token.value
            self.eat(IDENTIFIER)
            return value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
            self.error("Invalid factor")

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    self.error("Division by zero")
                result /= divisor

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result

    def assignment(self):
        identifier = self.current_token.value
        self.eat(IDENTIFIER)
        self.eat(EQUALS)
        value = self.expr()
        return ('assignment', identifier, value)

    def if_else(self):
        self.eat(IF)
        condition = self.expr()
        self.eat(ELSE)
        false_stmt = self.statement()
        return ('if-else', condition, false_stmt)

    def print_statement(self):
        self.eat(PRINT)
        value = self.expr()
        return ('print', value)

    def statement(self):
        if self.current_token.type == IDENTIFIER:
            return self.assignment()
        elif self.current_token.type == IF:
            return self.if_else()
        elif self.current_token.type == PRINT:
            return self.print_statement()
        else:
            self.error("Invalid statement")

    def parse(self):
        statements = []
        while self.current_token.type != EOF:
            statements.append(self.statement())
        return statements

# Print the parse tree
def print_parse_tree(tree, level=0):
    if isinstance(tree, tuple):
        print('  ' * level + tree[0])
        for item in tree[1:]:
            print_parse_tree(item, level + 1)
    else:
        print('  ' * level + str(tree))

# Test the parser
def main():
    while True:
        try:
            text = input('MiniLang > ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        try:
            parse_tree = parser.parse()
            print_parse_tree(parse_tree)
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    main()
