# ANNA AIKATERINI TSIALIOU, 4188, username: cse74188
# EVANGELIA ANASTASIA GKOGKOU, 4045, username: cse74045

# ************************************* THE CIMPLE LANGUAGE ************************************** #

# *************************************** PHASE 1 ************************************************ #
import sys

class Token:
    # Properties: tokenType, tokenString, lineNo
    def __init__(self, tokenType, tokenString, lineNo):
        self.tokenType = tokenType
        self.String = tokenString
        self.lineNo = lineNo

print()

# THE LEXICAL ANALYZER
def lex():
    global String
    global file_line

    state = 'start'
    String = ''

    while state != 'eof' and state != 'OK' and state != 'error':

        token_char = fp.read(1)

        if state == 'start':

            if token_char.isspace():
                if token_char == '\n':
                    file_line += 1
                state = 'start'

            elif token_char.isdigit():
                String += token_char
                state = 'dig'

            elif token_char.isalpha():
                String += token_char
                state = 'idk'

            elif token_char == '+':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '-':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '*':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '/':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '{':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '}':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '(':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == ')':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '[':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == ']':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == ',':
                # print('comma')
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == ';':
                # print(token_char)
                String += token_char
                return Token('string', String, file_line)

            elif token_char == ':':
                # print('the dot')
                String += token_char
                state = 'asgn'

            elif token_char == '<':
                String += token_char
                state = 'smaller'

            elif token_char == '>':
                String += token_char
                state = 'larger'

            elif token_char == '=':
                String += token_char
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '.':
                String += token_char
                state = 'eof'
                # print(String)
                return Token('string', String, file_line)

            elif token_char == '#':
                state = 'rem'

            else:
                print('Incorrect character at line: ' + str(file_line))
                # print(token_char)
                sys.exit()

        elif state == 'dig':
            if token_char.isdigit():
                String += token_char
                if int(String) > max_int_limit or int(String) < lower_int_limit:
                    print('Input integer has reached maximum bounds at line: ' + str(file_line))
                    print('Try a smaller integer')
                    sys.exit()
            elif token_char.isalpha():
                print('No letters after numbers are allowed at line: ' + str(file_line))
                sys.exit()

            else:
                # print(String)
                fp.seek(fp.tell() - 1)
                return Token('string', String, str(file_line))

        elif state == 'idk':

            if token_char.isdigit() or token_char.isalpha():

                if len(String) > max_id_limit:
                    print('Input integer has reached maximum bounds at line: ' + str(file_line))
                    print('Try a smaller integer')
                String += token_char

            else:

                fp.seek(fp.tell() - 1)

                if String in committed_words:
                    # print('committed: ' + String)
                    return Token('string', String, file_line)
                else:
                    # print('id: ' + String)
                    String = 'id'
                    return Token('string', String, file_line)

        elif state == 'asgn':
            if token_char == '=':
                String += token_char
                # print(String)
                return Token('string', String, str(file_line))
            else:
                print('Error at line: ' + str(file_line))
                print('Incorrect assignment symbol. Expected =  after ')
                sys.exit()

        elif state == 'smaller':
            if token_char == '=':
                String += token_char
                # print(String)
                return Token('string', String, file_line)
            elif token_char == '>':
                String += token_char
                # print(String)
                return Token('string', String, file_line)
            else:
                # print(String)
                fp.seek(fp.tell() - 1)
                return Token('string', String, file_line)

        elif state == 'larger':
            if token_char == '=':
                String += token_char
                # print(String)
                return Token('string', String, file_line)
            else:
                # print(String)
                fp.seek(fp.tell() - 1)
                return Token('string', String, file_line)

        elif state == 'rem':
            if token_char == '#':
                state = 'start'
            else:
                if token_char == '\n':
                    print('Error at line ' + str(file_line))
                    print('Please close the comment section with a # character \n')
                    sys.exit()

                continue

# THE SYNTAX ANALYZER ******************************************************************

def program():
    global token
    global file_line
    token_object = lex()
    token = token_object.String
    if token == 'program':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
            block()
        else:
            print('Please give an < id > name in the beginning of your program.')
            sys.exit()
    else:
        print('Please begin your program with the keyword < program >.At line: ' + str(token_object.lineNo))
        sys.exit()


def block():
    declarations()
    subprograms()
    statements()

def declarations():
    global token
    while token == 'declare':
        token_object = lex()
        token = token_object.String
        varlist()
        if token == ';':
            token_object = lex()
            token = token_object.String
        elif token == '{':
            print('Expected ; at the end line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
        else:
            print('Expected ; at the end line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()


def varlist():
    global token
    if token == 'id':
        token_object = lex()
        token = token_object.String
        while token == ',':
            token_object = lex()
            token = token_object.String
            if token == 'id':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected id at line: ' + str(token_object.lineNo) + '.\n')
                sys.exit()


def subprograms():
    global token
    while token == 'function' or token == 'procedure':
        subprogram()


def subprogram():
    global token
    global token_object

    if token == 'function':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
            if token == '(':
                token_object = lex()
                token = token_object.String
                formalparlist()
                if token == ')':
                    token_object = lex()
                    token = token_object.String
                    block()
                else:
                    print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
                    sys.exit()
            else:
                print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
                sys.exit()
        else:
            print('Please give a correct id at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    elif token == 'procedure':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
            if token == '(':
                token_object = lex()
                token = token_object.String
                formalparlist()
                if token == ')':
                    token_object = lex()
                    token = token_object.String
                    block()
                else:
                    print('Expected ) at line' + str(token_object.lineNo) + '.\n')
                    sys.exit()
            else:
                print('Expected ( at line' + str(token_object.lineNo) + '.\n')
                sys.exit()
        else:
            print('Please give a correct procedure name at line' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Please call a fuction or a procedure at line' + str(token_object.lineNo) + '.\n')
        sys.exit()


def formalparlist():
    global token
    global token_object
    formalparitem()
    while token == ',':
        token_object = lex()
        token = token_object.String
        formalparitem()


def formalparitem():
    global token
    global token_object
    if token == 'in':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
        else:
            print('Please give a correct id at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    elif token == 'inout':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
        else:
            print('Please give a correct id at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()

    else:
        print('Expected an in or inout statement at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

def statements():

    global token
    global file_line
    global token_object

    statement()
    if token == ';':
        token_object = lex()
        token = token_object.String
    elif token == '{':
        token_object = lex()
        token = token_object.String
        statement()
        if token == '}':
            print('Expected  ; at line ' + str(token_object.lineNo) + '.\n')
            sys.exit()

        while token == ';':
            token_object = lex()
            token = token_object.String
            before = token   # token before reading the ;
            statement()
            after = token

            # check if the char right after the statement is a ;,
            # if its a } then print error
            if (before in committed_words) and after == '}':
                print('Expected ; at line ' + str(token_object.lineNo) + '.\n')
                sys.exit()
            elif before == 'id' and after == '}':
                print('Expected ; at line ' + str(token_object.lineNo) + '.\n')
                sys.exit()

            elif before == ';' and after == ';':
                print('Expected } at line ' + str(token_object.lineNo) + '.\n')
                sys.exit()

        if token == '}':
            token_object = lex()
            token = token_object.String
        elif token == '.':
            print('Expected } at line ' + str(token_object.lineNo) + '.\n')
            sys.exit()
        else:
            print('Expected } or ; at line ' + str(file_line-1) + '.\n')
            sys.exit()

def statement():

    if token == 'id':
        assignStat()
    elif token == 'if':
        ifStat()
    elif token == 'while':
        whileStat()
    elif token == 'switchcase':
        switchcaseStat()
    elif token == 'forcase':
        forcaseStat()
    elif token == 'incase':
        incaseStat()
    elif token == 'call':
        callStat()
    elif token == 'return':
        returnStat()
    elif token == 'input':
        inputStat()
    elif token == 'print':
        printStat()


def assignStat():
    global token
    token_object = lex()
    token = token_object.String
    # print(token)
    if token == ':=':
        token_object = lex()
        token = token_object.String
        expression()
    else:
        print('Expected assign symbol := at line: ' + str(file_line) + '.\n')
        sys.exit()


def ifStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        condition()
        if token == ')':
            token_object = lex()
            token = token_object.String
            statements()
            elsepart()
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def elsepart():
    global token

    # print(token)
    if token == 'else':
        token_object = lex()
        token = token_object.String
        statements()


def whileStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        condition()
        if token == ')':
            token_object = lex()
            token = token_object.String
            statements()
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def switchcaseStat():
    global token
    token_object = lex()
    token = token_object.String
    while token == 'case':
        token_object = lex()
        token = token_object.String
        if token == '(':
            token_object = lex()
            token = token_object.String
            condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
            else:
                print('Expected ) at line' + str(file_line-1) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line' + str(file_line-1) + '.\n')
            sys.exit()

    if token == 'default':
        token_object = lex()
        token = token_object.String
        statements()
    else:
        print('Expected default at line' + str(file_line-1) + '.\n')
        sys.exit()


def forcaseStat():
    global token
    token_object = lex()
    token = token_object.String
    while token == 'case':
        token_object = lex()
        token = token_object.String
        if token == '(':
            token_object = lex()
            token = token_object.String
            condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
            else:
                print('Expected ) at line: ' + str(file_line-1) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(file_line-1) + '.\n')
            sys.exit()

    if token == 'default':
        token_object = lex()
        token = token_object.String
        statements()
    else:
        print('Expected default at line: ' + str(file_line-1) + '.\n')
        sys.exit()


def incaseStat():
    global token
    token_object = lex()
    token = token_object.String
    while token == 'case':
        token_object = lex()
        token = token_object.String
        if token == '(':
            token_object = lex()
            token = token_object.String
            condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
            else:
                print('Expected ) at line: ' + str(file_line-1) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(file_line-1) + '.\n')
            sys.exit()


def returnStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        expression()
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def callStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == 'id':
        token_object = lex()
        token = token_object.String
        if token == '(':
            token_object = lex()
            token = token_object.String
            actualparlist()
            if token == ')':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ) at line: ' + str(file_line-1) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(file_line-1) + '.\n')
            sys.exit()
    else:
        print('Expected a correct id at line: ' + str(file_line-1) + '.\n')
        sys.exit()


def printStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        expression()
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def inputStat():
    global token
    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
            if token == ')':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
                sys.exit()
        else:
            print('Expected an appropriate id at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def actualparlist():
    global token
    actualparitem()
    while token == ',':
        token_object = lex()
        token = token_object.String
        actualparitem()


def actualparitem():
    global token
    global token_object

    if token == 'in':
        token_object = lex()
        token = token_object.String
        expression()

    elif token == 'inout':
        token_object = lex()
        token = token_object.String
        if token == 'id':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected an appropriate id at line: ' + str(file_line-1) + '.\n')
            sys.exit()

    else:
        print('Expected an in or inout statement at line: ' + str(file_line-1) + '.\n')
        sys.exit()


def condition():
    global token
    boolterm()
    # print(token)
    while token == 'or':
        token_object = lex()
        token = token_object.String
        boolterm()


def boolterm():
    global token
    boolfactor()
    while token == 'and':
        token_object = lex()
        token = token_object.String
        boolfactor()


def boolfactor():
    global token
    if token == 'not':
        token_object = lex()
        token = token_object.String
        if token == '[':
            token_object = lex()
            token = token_object.String
            condition()
            if token == ']':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ] at line: ' + str(token_object.lineNo) + '.\n')
                sys.exit()
        else:
            print('Expected [ at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()

    elif token == '[':
        token_object = lex()
        token = token_object.String
        condition()
        if token == ']':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ] at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()
    else:
        expression()
        rel_op()
        expression()


def expression():
    global token

    optionalSign()
    term()
    # while token == '+' or token == '-':
    #     token_object = lex()
    #     token = token_object.String
    #     # add_op()
    #     term()
    while add_op():
        term()

def term():
    global token
    factor()
    # while token == '*' or token == '/':
    #     token_object = lex()
    #     token = token_object.String
    #     # mul_op()
    #     term()
    while mul_op():
        factor()

def factor():

    global token
    global token_object

    if token.isdigit():
        token_object = lex()
        token = token_object.String
    elif token == '(':
        token_object = lex()
        token = token_object.String
        expression()
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()

    elif token == 'id':
        token_object = lex()
        token = token_object.String
        idtail()

    else:
        print('Expected (, or id, or integer at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def idtail():
    global token
    if token == '(':
        token_object = lex()
        token = token_object.String
        actualparlist()
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()

def optionalSign():
    global token
    add_op()

def rel_op():
    global token
    global token_object

    if token == '=' or token == '<=' or token == '>=' or token == '>' or token == '<' or token == '<>':
        token_object = lex()
        token = token_object.String
    else:
        print('Expected a real optional character from (<,>,>=, <=, <>) at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

def add_op():
    global token
    if token == '+' or token == '-':
        token_object = lex()
        token = token_object.String
        return True
    else:
        return False


def mul_op():
    global token
    if token == '*' or token == '/':
        token_object = lex()
        token = token_object.String
        return True
    else:
        return False

# GLOBAL VARIABLES AND MAIN *******************************************************

# array of the committed words
committed_words =  ["program", "if", "switchcase", "not", "function", "input",
                   "declare", "else", "forcase", "and", "procedure", "print",
                   "while", "incase", "or", "call", "case",
                   "return", "default", "in", "inout"]

lower_int_limit = -(2 ^ 32 - 1)
max_int_limit = 2 ^ 32 - 1
max_id_limit = 30
file_line = 1

if len(sys.argv) >= 3:
    print('You must give exactly 2 argv\n')
    sys.exit()

filename = sys.argv[1]
fp = open(filename, 'r')

program()
print()
print('Syntax Analysis completed successfully.')
print('No lexical or syntax errors found.')


fp.close()







