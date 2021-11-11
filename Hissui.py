from sly import Lexer
from sly import Parser


# Creating a Lexer who inherits from sly's lexer.oy class
class HissuiLexer(Lexer):
    # Inputting the tokens that the parser will be able to use.
    # Temporarily REMOVED TOKENS:
    #   SQUARE, CIRCLE, RECTANGLE, TRIANGLE, VECTOR, MATRIX, NEW, FOR,
    #   ELSEIF, IN, COMMA, COLON, RETURN,
    # Tokens that were transferred to "literals": ASSIGN, RP, LP, RB, LB
    tokens = {ID, NUMBER, STRING, EQUAL,
              # statement tokens
              IF, THEN, ELSE, FOR, TO,

              # Comparison tokens
              GREATEREQ, LESSEQ,

              # Shape Tokens
              SQUARE, RECTANGLE, TRIANGLE, CIRCLE,

              # Extra Structure Tokens
              MATRIX, VECTOR,
              # List Tokens
              LIST, SIZE, REMOVE, ADD, SORT}

    # Lexer can read letters and combinations of letters and numbers
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # ignore whitespaces or tabs.
    ignore = ' \t'

    # Reads single digits or multiple digits.
    NUMBER = r'\d+'

    # making the values inside the token integers
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Defining strings
    STRING = r'\".*?\"'

    # stating the operators
    literals = {'+', '-', '/', '*', '^', '=', '(', ')', '<', '>', '%', '[', ']', '.'}

    # establishing function characters
    GREATEREQ = r'>='
    LESSEQ = r'<='
    EQUAL = r'=='
    # COLON = r':'

    # implementing standard language clauses.
    ID['if'] = IF
    ID['then'] = THEN
    ID["else"] = ELSE
    ID['list'] = LIST
    ID['for'] = FOR
    ID['to'] = TO

    # List methods
    ID['list'] = LIST
    ID['size'] = SIZE
    ID['remove'] = REMOVE
    ID['add'] = ADD
    ID['sort'] = SORT

    # Adding different functional objects
    ID['square'] = SQUARE
    ID["rectangle"] = RECTANGLE
    ID['triangle'] = TRIANGLE
    ID['circle'] = CIRCLE
    ID['matrix'] = MATRIX
    ID['vector'] = VECTOR

    # new token for object creation
    # ID['new'] = NEW

    # error handling
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class HissuiParser(Parser):
    tokens = HissuiLexer.tokens

    # Tells code to use proper order of operation while doing math operations
    precedence = (
        ('left', '+', '-'),
        ('left', '%', '*', '/', '^', GREATEREQ, LESSEQ, '<', '>', EQUAL),
        ('right', 'UMINUS'),
    )

    # Old middle row of precedence: ('left', '%', '*', '/', '^', GREATEREQ, LESSEQ, '<', '>', EQUAL),

    def __init__(self):
        self.env = { }

    # Ignores whitespace
    @_('')
    def statement(self, p):
        pass

    # @_('FUN ID "(" ")" ARROW statement')
    # def statement(self, p):
    #     return ('fun_def', p.ID, p.statement)

    # @_('ID "(" ")"')
    # def statement(self, p):
    #     return ('fun_call', p.ID)

######################################################################################################

    # Variable Declaration ====================================================================

    # Assigns value to a variable
    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('ID "=" expr')
    def var_assign(self, p):
        return 'var_assign', p.ID, p.expr

    @_('ID "=" STRING')
    def var_assign(self, p):
        return 'var_assign', p.ID, p.STRING

    #
    # @_('ID "=" RECTANGLE')
    # def statement(self, p):
    #     self.ids[p.ID] = p.RECTANGLE
    #     return p.ID, p.RECTANGLE
    #
    # @_('ID "=" SQUARE')
    # def statement(self, p):
    #     self.ids[p.ID] = p.SQUARE
    #     return p.ID, p.SQUARE
    #
    # @_('ID "=" CIRCLE')
    # def statement(self, p):
    #     self.ids[p.ID] = p.CIRCLE
    #     return p.ID, p.CIRCLE
    #
    # @_('ID "=" TRIANGLE')
    # def statement(self, p):
    #     self.ids[p.ID] = p.TRIANGLE
    #     return p.ID, p.TRIANGLE
    #
    # @_('ID "=" MATRIX')
    # def statement(self, p):
    #     self.ids[p.ID] = p.MATRIX
    #     return p.ID, p.MATRIX
    #
    # @_('ID "=" VECTOR')
    # def statement(self, p):
    #     self.ids[p.ID] = p.VECTOR
    #     return p.ID, p.VECTOR

    # Prints out expression once it no longer has any operations left
    @_('expr')
    def statement(self, p):
        return p.expr

    # Expression Handling =======================================================================================
    # Does addition
    @_('expr "+" expr')
    def expr(self, p):
        return 'add', p.expr0, p.expr1

    # Does subtraction
    @_('expr "-" expr')
    def expr(self, p):
        return 'sub', p.expr0, p.expr1

    # Does multiplication
    @_('expr "*" expr')
    def expr(self, p):
        return 'mul', p.expr0, p.expr1

    # Does division
    @_('expr "/" expr')
    def expr(self, p):
        return 'div', p.expr0, p.expr1

    # Does module
    @_('expr "%" expr')
    def expr(self, p):
        return 'mod', p.expr0, p.expr1

    # Does exponent TO BE ADDED
    @_('expr "^" expr')
    def expr(self, p):
        return 'exp', p.expr0, p.expr1

    # Parses individual negative numbers
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    # Parses expressions inside parenthesis
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    # Parses numbers
    @_('NUMBER')
    def expr(self, p):
        return 'num', p.NUMBER

    # # Parses strings
    # @_('STRING')
    # def expr(self, p):
    #     return 'str', p.STRING

    # Parses variables
    @_('ID')
    def expr(self, p):
        return 'var', p.ID

    # Condition Handling ====================================================================

    # Parses the EQUAL token
    @_('expr EQUAL expr')
    def condition(self, p):
        return 'equal', p.expr0, p.expr1

    # Parses greater-than or equal token.
    @_('expr GREATEREQ expr')
    def condition(self, p):
        return 'greater_eq', p.expr0, p.expr1

    # Parses less-than or equal token.
    @_('expr LESSEQ expr')
    def condition(self, p):
        return 'less_eq', p.expr0, p.expr1

    # Parses greater-than token.
    @_('expr ">" expr')
    def condition(self, p):
        return 'greater', p.expr0, p.expr1

    # Parses less-than token.
    @_('expr "<" expr')
    def condition(self, p):
        return 'less', p.expr0, p.expr1

    # If statements =====================================================================================

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return 'if_stmt', p.condition, ('branch', p.statement0, p.statement1)

    # Loops =============================================================================

    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return 'for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement

    # Lists===========================================================================================

    # @_('ID "=" LIST "[" "]"')
    # def statement(self, p):
    #     try:
    #         inp = input("Enter List Elements: ")
    #         if inp != "":
    #             lst = list(map(int, inp.split(",")))
    #         else:
    #             lst = []
    #         self.ids[p.ID] = lst
    #         return p.ID, lst
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "[" NUMBER "]"')
    # def expr(self, p):
    #     try:
    #         index = self.ids[p.ID][p.NUMBER]
    #         return index
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "." SIZE "("  ")" ')
    # def expr(self, p):
    #     try:
    #         size = len(self.ids[p.ID])
    #         return size
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "." REMOVE "(" NUMBER ")"')
    # def expr(self, p):
    #     try:
    #         del self.ids[p.ID][p.NUMBER]
    #         return self.ids[p.ID]
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "." ADD "(" expr ")"')
    # def expr(self, p):
    #     try:
    #         self.ids[p.ID].append(p.expr)
    #         return self.ids[p.ID]
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "[" NUMBER "]" "=" expr')
    # def expr(self, p):
    #     try:
    #         self.ids[p.ID][p.NUMBER] = p.expr
    #         return self.ids[p.ID]
    #     except TypeError:
    #         print("Error variable is not a list")
    #
    # @_('ID "." SORT "("  ")"')
    # def expr(self, p):
    #     try:
    #         self.ids[p.ID].sort()
    #         return self.ids[p.ID]
    #     except TypeError:
    #         print("Error variable is not a list")


class HussuiInterpreter:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        # Node base cases ======================================================================

        # Reached node with number value
        if isinstance(node, int):
            return node

        # Reached node with string value
        if isinstance(node, str):
            return node

        # Reached empty node
        if node is None:
            return None

        # Tree algorithms =============================================================================

        # Goes down the tree nodes
        if node[0] == 'program':
            if node[1] is None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        # Interprets if statements
        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        # Checks if two numbers are equal to each other
        if node[0] == 'equal':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        elif node[0] == 'greater_eq':
            return self.walkTree(node[1]) >= self.walkTree(node[2])
        elif node[0] == 'less_eq':
            return self.walkTree(node[1]) <= self.walkTree(node[2])
        elif node[0] == 'greater':
            return self.walkTree(node[1]) > self.walkTree(node[2])
        elif node[0] == 'less':
            return self.walkTree(node[1]) < self.walkTree(node[2])

        # Handles the creation of user functions:
        # if node[0] == 'fun_def':
        #     self.env[node[1]] = node[2]
        #
        # if node[0] == 'fun_call':
        #     try:
        #         return self.walkTree(self.env[node[1]])
        #     except LookupError:
        #         print("Undefined function '%s'" % node[1])
        #         return 0

        # Handles math operations
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'mod':
            return self.walkTree(node[1]) % self.walkTree(node[2])
        elif node[0] == 'exp':
            return self.walkTree(node[1]) ** self.walkTree(node[2])

        # Assigns value to variables ===========================================================================
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

        # For loop algorithms =======================d=============================================================
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return self.walkTree(node[1]), self.walkTree(node[2])


if __name__ == '__main__':
    lexer = HissuiLexer()
    parser = HissuiParser()
    env = {}
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            HussuiInterpreter(tree, env)