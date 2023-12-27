# NAME: Marian Rempola
# CLASS: CMPSC 461
# PROJECT: Creating a Parser

#References: I got help from various resourcs including GeeksforGeeks, my brother, and TAs in Office hours

####################################################################################################
# TOKENS: models smallest units of input 
####################################################################################################

class Token: 
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False
    
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

####################################################################################################
# LEXER: tokenize
####################################################################################################

class Lexer: 
    #initialization
    def __init__(self, str):
        #look at each char in the input from position 0
        self.input = str
        self.position = 0

    #tokenize = identify type and value :
    def tokenize(self):
        tokens = []

        #while we are still traversing each char of the input
        while self.position < len(self.input):
            char = self.input[self.position]

            if char.isalpha():
                token_type = 'VARIABLE'
                token_value = ''
                while self.position < len(self.input) and self.input[self.position].isalnum():
                    token_value += self.input[self.position]
                    self.position += 1
                tokens.append(Token(token_type, token_value))

            elif char.isdigit():
                token_type = 'INTEGER'
                token_value = ''
                while self.position < len(self.input) and self.input[self.position].isdigit():
                    token_value += self.input[self.position]
                    self.position += 1
                tokens.append(Token(token_type, int (token_value)))

            elif char in ('+', '-', '*', '/'):
                tokens.append(Token('OPERATOR', char))
                self.position += 1

            elif char == '=':
                tokens.append(Token('ASSIGN', '='))
                self.position += 1

            elif char == ';':
                tokens.append(Token('SEMICOLON', ';'))
                self.position += 1

            elif char == '(':
                tokens.append(Token('PARENTHESIS', '('))
                self.position += 1

            elif char == ')':
                tokens.append(Token('PARENTHESIS', ')'))
                self.position += 1

            else:
                raise Exception(f'Invalid character: {char}')

        return tokens

####################################################################################################
# NODE: node in AST (holds type, value, and children of each node in the tree)
####################################################################################################

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

####################################################################################################
# PARSER: convert tokens into AST 
####################################################################################################

class Parser:
    #initializaition
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    #read current valid token and move to next position; if invalid, throw a syntax error
    def consume(self, type):
        current_token = self.current_token()

        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            self.position += 1
            return current_token
        
        elif current_token.type == type:
            self.position += 1
            return current_token
        
        else:
            raise SyntaxError("Invalid Token")

    #examine type and value of current token without moving to the next one
    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return None

    #make root of AST and parse each statement in token list
    def parse(self):
        ast = []
        root = Node('PROGRAM', children = ast)
        node = self.parse_statement()
        root.children.append(node)
        return root
    
    #determine type of current statement and refer to appropriate function
    def parse_statement(self): 
        if (self.peek().type == 'VARIABLE'):
            return Node ('STATEMENT', children = self.parse_assignment())
        else:
            raise SyntaxError("Wrong syntax")

    #parse assignment statements
    def parse_assignment(self):
        #check every element
        i = []
        while (self.position < len(self.tokens)):
            if (self.position < len(self.token)):
                node = Node('ASSIGNMENT', 
                    children = [ Node("VARIABLE", self.consume("VARIABLE").value),
                    Node("ASSIGN", self.consume("ASSIGN").value),
                    Node("EXPRESSION", children=[self.parse_expression()])
                    ])
                i.append(node)
            raise SyntaxError("Wrong syntax")
        return i

    #parse expsns w/ arithematic 
    def parse_expression(self):
        #check bound
        if (self.position == len(self.tokens)):
            raise SyntaxError("Wrong syntax")
        elif (self.peek().type == 'VARIABLE' ):
            return Node('EXPRESSION', 
                    children = [ Node('TERM',children=[self.parse_term()]),
                    Node('EXPRESSION', children=[self.parse_expression()])
            ])
        elif (self.peek().type == 'INTEGER' ):
            return Node('EXPRESSION', 
                    children = [ Node('TERM',children=[self.parse_term()]),
                    Node('EXPRESSION', children=[self.parse_expression()])
            ])
        elif (self.peek().type == "PARENTHESIS"):
            return Node('EXPRESSION', children=[
                Node("PARENTHESIS", self.consume("PARENTHESIS").value),
                Node('EXPRESSION', children=[self.parse_expression()]),
            ])
        elif (self.peek().type == "SEMICOLON"):
            return Node("SEMICOLON", self.consume("SEMICOLON").value)
        elif (self.peek().type == "OPERATOR" and self.tokens[self.position+1].value != ")"):     
            return Node('EXPRESSION', children=[
                    Node('OPERATOR', self.consume("OPERATOR").value),
                    Node('TERM',children=[self.parse_term()]),
                    Node('EXPRESSION', children=[self.parse_expression()])
            ])
        else:
            raise SyntaxError("Wrong syntax")

    #parse individual terms in expn
    def parse_term(self):
        if self.peek().type == 'INTEGER':
            return Node('INTEGER', value=[self.consume('INTEGER').value])
        elif self.current_token().type == 'VARIABLE':
            return Node('VARIABLE', value=[self.consume('VARIABLE').value])
        elif self.current_token().type == 'PARENTHESIS' and self.current_token().value == '(':
            self.consume('PARENTHESIS') #this one is OK
            expression = self.parse_expression()
            self.consume('PARENTHESIS')
            return expression
        else:
            raise SyntaxError("Wrong syntax")