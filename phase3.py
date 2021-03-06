

# ************************************ THE CIMPLE LANGUAGE ************************************* #
# ******************************************* PHASE 3 ****************************************** #


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
                    return Token(String, 'id', file_line)

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
    global token, func_name
    global token_object

    token_object = lex()
    token = token_object.String
    current_line = token_object.lineNo
    if token == 'program':
        token_object = lex()
        token = token_object.String
        func_name = token_object.tokenType

        if token == 'id':
            token_object = lex()
            token = token_object.String
            block(func_name)
        else:
            print('Please give an < id > name in the beginning of your program.')
            sys.exit()
    else:
        print('Please begin your program with the keyword < program >.At line: ' + str(current_line))
        sys.exit()


def block(block_name):
    global token, func_name
    global token_object
    global framelength,nestingLevel,offset,init_quad

    declarations()
    subprograms()
    genquad('begin_block', block_name, '_', '_')
    init_quad = len(quads) - 1
    statements()
    if block_name == func_name:
        framelength = offset[nestingLevel]
        finalCode(init_quad)
        recordScopeStack.pop(nestingLevel)
        del offset[nestingLevel]
        nestingLevel = nestingLevel - 1
        genquad('halt', '_', '_', '_')
        mips_code.write('L_'+str(nextquad()-1)+':\n')
    genquad('end_block', block_name, '_', '_')


def declarations():
    global token
    global token_object

    while token == 'declare':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        varlist()
        if token == ';':
            token_object = lex()
            token = token_object.String
        elif token == '{':
            print('Expected ; at the end line: ' + str(current_line) + '.\n')
            sys.exit()
        else:
            print('Expected ; at the end line: ' + str(current_line) + '.\n')
            sys.exit()


def varlist():
    global token
    global token_object
    global record_entity_list, record_argument_list
    global offset, nestingLevel#, startQuad

    if token == 'id':
        var_name = token_object.tokenType
        if var_name not in temp_varlist:
            temp_varlist.append(var_name)
        recordEntity(var_name, 'id', '')
        token_object = lex()
        token = token_object.String
        while token == ',':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            if token == 'id':
                # ***********************
                var_name = token_object.tokenType
                if var_name not in temp_varlist:
                    temp_varlist.append(var_name)
                # ***********************
                recordEntity(var_name,'id', '')
                token_object = lex()
                token = token_object.String
            else:
                print('Expected id at line: ' + str(current_line) + '.\n')
                sys.exit()


def subprograms():
    global token
    global token_object

    while token == 'function' or token == 'procedure':
        offset.append(12)
        subprogram()


def subprogram():

    global token
    global token_object
    global enableProc
    global record_entity_list, record_argument_list
    global nestingLevel, init_quad

    if token == 'function':
        enableProc = True
        offset.append(12)
        nestingLevel += 1
        record_entity_list = []
        record_argument_list = []
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        var_name = token_object.tokenType

        if token == 'id':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            if token == '(':
                token_object = lex()
                token = token_object.String
                current_line = token_object.lineNo

                formalparlist()
                recordEntity('', 'subprogram', record_argument_list)
                recordEntity(var_name, 'function', record_argument_list)
                if token == ')':
                    block(var_name)
                    finalCode(init_quad)
                    recordScopeStack[nestingLevel-1][-1].append(offset[nestingLevel])
                    recordScopeStack.pop(nestingLevel)
                    del offset[nestingLevel]
                    nestingLevel -= 1
                    record_entity_list = recordScopeStack[nestingLevel]

                    token_object = lex()
                    token = token_object.String
                    enableProc = False
                else:
                    print('Expected ) at line: ' + str(current_line) + '.\n')
                    sys.exit()
            else:
                print('Expected ( at line: ' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Please give a correct id at line: ' + str(current_line) + '.\n')
            sys.exit()
    elif token == 'procedure':
        enableProc = True
        offset.append(12)
        nestingLevel += 1
        record_entity_list = []
        record_argument_list = []
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        var_name = token_object.tokenType

        if token == 'id':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            if token == '(':
                token_object = lex()
                token = token_object.String
                current_line = token_object.lineNo
                formalparlist()
                # hereee
                recordEntity('', 'subprogram', record_argument_list)
                recordEntity(var_name, 'procedure', record_argument_list)
                if token == ')':
                    block(var_name)
                    finalCode(init_quad)
                    recordScopeStack[nestingLevel-1][-1].append(offset[nestingLevel])
                    recordScopeStack.pop(nestingLevel)
                    del offset[nestingLevel]
                    nestingLevel = nestingLevel - 1
                    record_entity_list = recordScopeStack[nestingLevel]
                    token_object = lex()
                    token = token_object.String
                else:
                    print('Expected ) at line' + str(current_line) + '.\n')
                    sys.exit()
            else:
                print('Expected ( at line' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Please give a correct procedure name at line' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Please call a function or a procedure at line' + str(token_object.lineNo) + '.\n')
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
        current_line = token_object.lineNo

        if token == 'id':
            var_name = token_object.tokenType
            record_arguments('in',var_name)
            token_object = lex()
            token = token_object.String
        else:
            print('Please give a correct id at line: ' + str(current_line) + '.\n')
            sys.exit()
    elif token == 'inout':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo
        if token == 'id':
            var_name = token_object.tokenType
            record_arguments('inout',var_name)
            token_object = lex()
            token = token_object.String
        else:
            print('Please give a correct id at line: ' + str(current_line) + '.\n')
            sys.exit()

    else:
        print('Expected an -in- or -inout- statement at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

def statements():

    global token
    global token_object
    global current_line

    statement()
    if token == ';':
        token_object = lex()
        token = token_object.String
    elif token == '{':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo
        statement()
        if token == '}':
            print('Expected ; at line ' + str(current_line) + '.\n')
            sys.exit()

        while token == ';':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            before = token
            statement()
            after = token

            if (before in committed_words) and after == '}':
                print('Expected ; at line ' + str(current_line) + '.\n')
                sys.exit()
            elif before == 'id' and after == '}':
                print('Expected ; at line ' + str(current_line) + '.\n')
                sys.exit()
            elif before == ';' and after == ';':
                print('Expected } at line ' + str(current_line) + '.\n')
                sys.exit()

        if token == '}':
            token_object = lex()
            token = token_object.String

        elif token == '.':
            print('Expected } at line ' + str(current_line) + '.\n')
            sys.exit()
        else:
            print('Expected } or ; at line ' + str(current_line) + '.\n')
            sys.exit()

def statement():
    global token

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
    global token_object

    var_name = token_object.tokenType
    if var_name not in temp_varlist:
        temp_varlist.append(var_name)
    E1 = var_name

    token_object = lex()
    token = token_object.String

    if token == ':=':
        token_object = lex()
        token = token_object.String
        E2 = expression()
        genquad(':=', E2, '_', E1)
    else:
        print('Expected assign symbol := at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def ifStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String
    if token == '(':

        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo
        is_true, is_false = condition()

        if token == ')':

            token_object = lex()
            token = token_object.String
            backpatch(is_true, nextquad())
            statements()
            if_list = makelist(nextquad())
            genquad('jump', '_', '_', '_')
            backpatch(is_false, nextquad())
            elsepart()
            backpatch(if_list, nextquad())

        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def elsepart():
    global token
    global token_object

    if token == 'else':
        token_object = lex()
        token = token_object.String
        statements()


def whileStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo
        w_quad = nextquad()
        is_true, is_false = condition()
        if token == ')':
            backpatch(is_true, nextquad())
            token_object = lex()
            token = token_object.String
            statements()
            genquad('jump', '_', '_', w_quad)
            backpatch(is_false, nextquad())
        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

def switchcaseStat():
    global token
    global token_object

    case_temp = newtemp()
    case_quad = nextquad()
    genquad(':=', '0', '_', case_temp)

    token_object = lex()
    token = token_object.String
    while token == 'case':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == '(':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            id_true, is_false = condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
                genquad(':=', '1', '_', case_temp)
                backpatch(is_false, nextquad())
            else:
                print('Expected ) at line' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line' + str(current_line) + '.\n')
            sys.exit()

    if token == 'default':
        genquad('=', case_temp, '1', case_quad)
        token_object = lex()
        token = token_object.String
        statements()
    else:
        print('Expected default at line' + str(token_object.lineNo) + '.\n')
        sys.exit()


def forcaseStat():

    global token
    global token_object

    case_temp = newtemp()
    case_quad = nextquad()
    genquad(':=', '0', '_', case_temp)
    token_object = lex()
    token = token_object.String
    current_line = token_object.lineNo

    while token == 'case':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == '(':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            is_true, is_false = condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
                genquad(':=', '1', '_', case_temp)
                backpatch(is_false, nextquad())
            else:
                print('Expected ) at line: ' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(current_line) + '.\n')
            sys.exit()

    if token == 'default':
        genquad('=', case_temp, '1', case_quad)
        token_object = lex()
        token = token_object.String
        statements()
    else:
        print('Expected default in forcase statement at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

def incaseStat():
    global token
    global token_object
    case_temp = newtemp()
    # case_quad = nextquad()
    genquad(':=', '0', '_', case_temp)

    token_object = lex()
    token = token_object.String
    while token == 'case':
        token_object = lex()
        token = token_object.String
        if token == '(':
            token_object = lex()
            token = token_object.String
            is_true, is_false = condition()
            if token == ')':
                token_object = lex()
                token = token_object.String
                statements()
                genquad(':=', '1', '_', case_temp)
                backpatch(is_false, nextquad())
            else:
                print('Expected ) at line: ' + str(token_object.lineNo) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
            sys.exit()


def returnStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String
    current_line = token_object.lineNo

    if token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        exp = expression()
        genquad('retv', exp, '_', '_')
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(current_line) + '.\n')
        sys.exit()


def callStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String

    if token == 'id':
        var_name = token_object.tokenType
        call_id = var_name

        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == '(':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            actualparlist()
            genquad('call', call_id, '_', '_')
            if token == ')':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ) at line: ' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Expected ( at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected a correct id at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def printStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String
    if token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        print_exp = expression()
        genquad('print', print_exp, '_', '_')
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def inputStat():
    global token
    global token_object

    token_object = lex()
    token = token_object.String
    current_line = token_object.lineNo

    if token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == 'id':

            var_name = token_object.tokenType
            if var_name not in temp_varlist:
                temp_varlist.append(var_name)

            input_id = var_name

            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            if token == ')':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ) at line: ' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Expected an appropriate id at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        print('Expected ( at line: ' + str(current_line) + '.\n')
        sys.exit()

    genquad('input', input_id, '_', '_')


def actualparlist():
    global token
    global token_object
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
        in_exp = expression()
        genquad('par', in_exp, 'CV', '_')

    elif token == 'inout':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == 'id':
            var_name = token_object.tokenType
            inout_exp = var_name
            genquad('par', inout_exp, 'REF', '_')
            token_object = lex()
            token = token_object.String
        else:
            print('Expected an appropriate id at line: ' + str(current_line) + '.\n')
            sys.exit()

    else:
        print('Expected an -in-  or -inout-  statement at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()


def condition():
    global token
    global token_object

    is_true, is_false = boolterm()
    while token == 'or':
        token_object = lex()
        token = token_object.String
        backpatch(is_false, nextquad())
        bool_true, bool_false = boolterm()
        is_true = merge(is_true, bool_true)
        is_false = bool_false
    return is_true, is_false

def boolterm():
    global token
    global token_object

    is_true, is_false = boolfactor()

    while token == 'and':
        token_object = lex()
        token = token_object.String
        backpatch(is_true, nextquad())
        bterm_true, bterm_false = boolfactor()
        is_false = merge(is_false, bterm_false)
        is_true = bterm_true

    return is_true, is_false


def boolfactor():
    global token
    global token_object

    if token == 'not':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        if token == '[':
            token_object = lex()
            token = token_object.String
            current_line = token_object.lineNo

            is_true, is_false = condition()
            if token == ']':
                token_object = lex()
                token = token_object.String
            else:
                print('Expected ] at line: ' + str(current_line) + '.\n')
                sys.exit()
        else:
            print('Expected [ at line: ' + str(current_line) + '.\n')
            sys.exit()

    elif token == '[':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        is_true, is_false = condition()
        if token == ']':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ] at line: ' + str(current_line) + '.\n')
            sys.exit()
    else:
        exp_a = expression()

        rel_oper = rel_op()
        exp_b = expression()
        is_true = makelist(nextquad())
        genquad(rel_oper, exp_a, exp_b, '_')
        is_false = makelist(nextquad())
        genquad('jump', '_', '_', '_')

    return is_true, is_false


def expression():
    global token
    global token_object

    optionalSign()
    T1 = term()

    while token == '+' or token == '-':
        symbol_add = add_op()
        T2place = term()
        w = newtemp()
        genquad(symbol_add, T1, T2place, w)
        T1 = w

    eplace = T1
    return eplace


def term():
    global token
    global token_object

    T1 = factor()

    while token == '*' or token == '/':
        symbol_mul = mul_op()
        T2 = factor()
        w = newtemp()
        genquad(symbol_mul, T1, T2, w)
        T1 = w

    eplace = T1
    return eplace


def factor():
    global token
    global token_object

    if token.isdigit():
        factor_list = token
        token_object = lex()
        token = token_object.String
    elif token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        factor_list = expression()
        if token == ')':
            token_object = lex()
            token = token_object.String
        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()

    elif token == 'id':
        var_name = token_object.tokenType
        factor_list = var_name

        token_object = lex()
        token = token_object.String

        if idtail():
            genquad('call', factor_list, '_', '_')
    else:
        print('Expected (, or id symbol, or integer at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

    return factor_list

def idtail():
    global token
    global token_object

    if token == '(':
        token_object = lex()
        token = token_object.String
        current_line = token_object.lineNo

        actualparlist()
        if token == ')':
            token_object = lex()
            token = token_object.String
            return True
        else:
            print('Expected ) at line: ' + str(current_line) + '.\n')
            sys.exit()

def optionalSign():
    global token
    global token_object
    add_op()

def rel_op():
    global token
    global token_object

    if token == '=' or token == '<=' or token == '>=' or token == '>' or token == '<' or token == '<>':
        relation_symbol = token
        token_object = lex()
        token = token_object.String

    else:
        print('Expected a real optional character from (<,>,>=, <=, <>) at line: ' + str(token_object.lineNo) + '.\n')
        sys.exit()

    return relation_symbol

def add_op():
    global token
    global token_object

    if token == '+' or token == '-':
        add_symbol = token
        token_object = lex()
        token = token_object.String
        return add_symbol
    else:
        return False


def mul_op():
    global token
    global token_object

    if token == '*' or token == '/':
        mul_symbol=token
        token_object = lex()
        token = token_object.String
        return mul_symbol
    else:
        return False

# *****************************ENDIAMESOS KWDIKAS******************************** #

def nextquad():
    global quadcounter
    return quadcounter + 1


def genquad(op, x, y, z):
    global quadcounter
    global quads

    quadcounter = nextquad()
    quads[quadcounter] = [str(op), str(x), str(y), str(z)]


def print_quads():
    print('this is quads ')
    print(quads)

def print_temp_varlist():
    print('this is the temp_varlist ')
    print(temp_varlist)

def newtemp():
    global temp_counter
    global temp_varlist, record_entity_list,nestingLevel

    temp_counter = temp_counter+1
    # *****************************
    # temp_varlist.append('T_'+str(temp_counter))
    # *****************************
    tempName = "T_"+str(temp_counter)
    recordEntity(tempName , 'temp','')
    # return 'T_'+str(temp_counter)
    return tempName

def emptylist():
    empty_list = []
    return empty_list

def makelist(x):
    make_list = []
    make_list.append(x)
    return make_list

def merge(list1, list2):
    mergedlist = []
    list1.append(list2)
    mergedlist.append(list1)
    return mergedlist

def backpatch(list, z):
    for i in list:
        quads[i][3] = z

def write_quads():
    for key, value in quads.items():
        interval_code.write(str(key) + ':' + str(value) + '\n')

# def write_c_body():
#     for counter in range(1, len(quads)):
#         if quads[counter][0] == ':=':
#             c_code.write('  L_'+str(counter) + ': '+quads[counter][3] + '=' + quads[counter][1] + ';' + '  // ' + str(quads[counter]) + '\n')
#
#         elif quads[counter][0] == '+' or quads[counter][0] == '-' or quads[counter][0] == '*' or quads[counter][0] == '/':
#             c_code.write('  L_'+str(counter)+': '+quads[counter][3] + '=' + quads[counter][1] + quads[counter][0]+quads[counter][2] + ';' + '  // ' + str(quads[counter]) + '\n')
#
#         elif quads[counter][0] == 'jump':
#             c_code.write('  L_'+str(counter)+': '+'goto '+'L_'+str(quads[counter][3]) + ';' + '  // ' + str(quads[counter]) + '\n')
#
#         elif quads[counter][0] == '=' or quads[counter][0] == '<>' or quads[counter][0]== '>=' or quads[counter][0] == '<' or quads[counter][0] == '>' or quads[counter][0] == '<=' :
#             if quads[counter][0] == '=':
#                 c_code.write('  L_'+str(counter)+': '+str('if')+'('+str(quads[counter][1])+'=='+str(quads[counter][2])+')' + ' goto L_' + str(quads[counter][3]) + ';' + '  // ' + str(quads[counter])  + '\n')
#             elif quads[counter][0] == '<>':
#                 c_code.write('  L_'+str(counter)+': '+str('if')+'('+str(quads[counter][1])+'!='+str(quads[counter][2])+')' + ' goto L_' + str(quads[counter][3])  + ';' + '  // ' + str(quads[counter]) + '\n')
#             else:
#                 c_code.write('  L_'+str(counter)+': '+str('if')+'('+str(quads[counter][1])+str(quads[counter][0])+str(quads[counter][2])+')' + ' goto L_' + str(quads[counter][3])  + ';' + '  // ' + str(quads[counter]) + '\n')
#
#         elif quads[counter][0] == 'halt':
#             c_code.write('  L_'+str(counter)+':  {}\n')
#
#         elif quads[counter][0] == 'begin_block':
#             c_code.write('  L_'+str(counter)+':  \n')
#
#         elif quads[counter][0] == 'end_block':
#             continue
#
#         elif quads[counter][0] == 'out':
#             c_code.write('  L_'+str(counter)+': printf("%d""\\n",' + str(quads[counter][1])+');\n')
#
#         else:
#             c_code.write(
#                 '  L_' + str(counter) + ': ' + str(quads[counter][0]) + ' ' +str(quads[counter][1]) + ';' + '  // ' + str(
#                     quads[counter]) + '\n')
#
#     c_code.write('}\n')

# def write_c():
#
#     c_code.write('#include <stdio.h> \n')
#     c_code.write('int main(){\n')
#     c_code.write('  int ')
#     i = 0
#     for i in range(len(temp_varlist)-1):
#         c_code.write(temp_varlist[i] + ',')
#     c_code.write(temp_varlist[i + 1] + ';\n')
#
#     write_c_body()


# semantic analysis *************************************************************
# def semantic_analysis(enableSem,quads_number):
#     global  quads, enableProc
#     global token
#     global token_object
#
#     current_line = token_object.lineNo
#     if enableSem==False and enableProc==False:
#         print('Syntax Error at line '+str(current_line)+'. A return statement is outside the function.')
#         sys.exit()
#     elif enableSem==True and enableProc==True:
#         print('quads number : '+ str(quads_number))
#         print('len(quads) : '+ str(len(quads)))
#
#         while True:
#             if quads_number < len(quads):
#                 if quads[quads_number][0] != 'retv':
#                     quads_number= quads_number + 1
#                 else:
#                     break
#             else:
#                 print('Syntax Error at line '+str(current_line)+'. A return statement should be inside the function loop.')
#                 sys.exit()

# end of semantic analysis ******************************************************


# entity list ******************************************************************
#def recordScope(list_entity,nestingLevel):

def recordEntity(entity_name,type,entity_list):
    global record_entity_list, record_argument_list
    global offset, nestingLevel#, startQuad

    if type=='id':
        # record_entity_list.append([entity_name,offset[nestingLevel]])
        record_entity_list.append([entity_name, offset[nestingLevel]])
        # print(record_entity_list)
        recordScopeStack[nestingLevel] = record_entity_list
        offset[nestingLevel]+=4
    elif type == 'subprogram':
        for i in range(len(record_argument_list)):
            record_entity_list.append([record_argument_list[i][0],record_argument_list[i][1],offset[nestingLevel]])
            # print(record_entity_list)

            offset[nestingLevel] += 4
        recordScopeStack[nestingLevel] = record_entity_list

    elif type == 'function' or  type == 'procedure':
        function_list = []
        function_list.append(entity_name)
        for i in range(len(entity_list)):
            function_list.append(entity_list[i])
        function_list.append(type)
        recordScopeStack[nestingLevel-1].append(function_list)

    elif type == 'temp':
        record_entity_list.append([entity_name,offset[nestingLevel]])
        offset[nestingLevel]+=4

def record_arguments(parMode,type):
    global record_argument_list
    record_argument_list.append([type,parMode])


# final code **********************************************************************
def gnlvcode(v):
    a, b = locateVariable(v)
    mips_code.write('lw $t0,-4($sp)\n')
    if (a + 1) < nestingLevel:
        while a > 0:
            mips_code.write('lw $t0,-4($t0)\n')
            a = a - 1
    mips_code.write('add $t0,$t0 ,-'+str(recordScopeStack[a][b][-1]) + '\n')

def loadvr(v,r):
    global nestingLevel, recordScopeStack
    a, b = locateVariable(v)
    # print(recordScopeStack)

    if v.isdigit() or v.lstrip("-").isdigit():
        mips_code.write('li $t'+str(r) +', '+ str(v) + '\n')
    elif a==0: #nesting level 0, global variable
        mips_code.write('lw $t'+str(r)+' , -'+ str(recordScopeStack[a][b][len(recordScopeStack[a][b])-1]) +'($s0)\n')
    elif a == nestingLevel: #call by value
        if recordScopeStack[a][b][0]=='in': #???????????????? in/inout?
            mips_code.write('lw $t' + str(r) + ' , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b]) - 1]) + '($s0)\n')
        else: #call by ref
            mips_code.write('lw $t0 , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b]) - 1]) + '($sp)\n')
            mips_code.write('lw $t' + str(r) + ' , ($t0)\n')
    elif a < nestingLevel: # local var in ancestor
        if recordScopeStack[a][b][0] == 'in': #call by value
            gnlvcode(recordScopeStack[a][b][1])
            mips_code.write('lw $t' + str(r) + ' , ($t0)\n')
        else: #  call by ref
            gnlvcode(recordScopeStack[a][b][1])
            mips_code.write('lw $t0 , ($t0)\n')
            mips_code.write('lw $t' + str(r) + ' , ($t0)\n')


def storevr(r,v):
    global nestingLevel, recordScopeStack
    a,b=locateVariable(v)
    if a==0: #global var
        mips_code.write('sw $t'+str(r)+' , -'+ str(recordScopeStack[a][b][len(recordScopeStack[a][b])-1]) +'($s0)\n')
    if a==nestingLevel: #local var as value
        if recordScopeStack[a][b][1]=='in':
             mips_code.write('sw $t' + str(r) + ' , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b]) - 1]) + '($sp)\n')
        else: #local var as ref
            mips_code.write('lw $t0 , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b]) - 1]) + '($sp)\n')
            mips_code.write('sw $t' + str(r) + ' , ($t0)\n')
    elif a < nestingLevel: #call as value or local var in ancestor
        if recordScopeStack[a][b][0] == 'in':
            gnlvcode(recordScopeStack[a][b][1])
            mips_code.write('sw $t' + str(r) + ' , ($t0)\n')
        else: #call by ref in ancestor
            gnlvcode(recordScopeStack[a][b][1])
            mips_code.write('lw $t0 , ($t0)\n')
            mips_code.write('sw $t' + str(r) + ' , ($t0)\n')

#find the variable in the scope stack
def locateVariable(v):
    global nestingLevel,recordScopeStack
    for i in range(len(recordScopeStack)-1,-1,-1):
        for j in range(len(recordScopeStack[i])):
            if v==recordScopeStack[i][j][0]:
                return i,j

    if not v.isdigit():
        pass
    return -1,-1


def parameterOffset(i,quads_number):

    global framelength,offset,nestingLevel,recordScopeStack
    if i== 0:
        while True:
            if quads[quads_number][0] == 'par':
                quads_number= quads_number + 1

            elif quads[quads_number][0] == 'call':
                a,b = locateVariable(quads[quads_number][1])
                break

        if not str(recordScopeStack[a][b][-1]).isdigit():
            mips_code.write('addi $fp,$sp , '+ str(offset[nestingLevel]) +'\n')
            framelength = offset[nestingLevel]

        else:
            mips_code.write('addi $fp,$sp , '+ str(recordScopeStack[a][b][-1]) +'\n')
            framelength = recordScopeStack[a][b][-1]


def finalCode(init):

    # global token
    # global token_object
    global nestingLevel, recordScopeStack, framelength
    global mips_code,enableProc
    param_offset = 0
    # current_line = token_object.lineNo

    # semantic_analysis(True,init)
    #convert quads into assembly
    for i in range(len(quads)):
        mips_data = quads[i]
        if mips_data[0] == 'jump':
            mips_code.write('L_' + str(i) + ': j L_' + str(mips_data[3]) + '\n')
        elif mips_data[0] == '==' or mips_data[0] == '<>' or mips_data[0] == '>' or mips_data[0] == '<' or mips_data[0] == '>=' or mips_data[0] == '<=':
            mips_code.write('L_' + str(i) + ':\n')
            loadvr(mips_data[1], 1)
            loadvr(mips_data[2], 2)
            if mips_data[0] == '==':
                mips_code.write('beq $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
            elif mips_data[0] == '<>':
                mips_code.write('bne $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
            elif mips_data[0] == '>':
                mips_code.write('bgt $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
            elif mips_data[0] == '<':
                mips_code.write('blt $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
            elif mips_data[0] == '>=':
                mips_code.write('bge $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
            elif mips_data[0] == '<=':
                mips_code.write('ble $t1,$t2,' + 'L_' + str(mips_data[3]) + '\n')
        elif mips_data[0] == ':=':
            mips_code.write('L_' + str(i) + ':\n')
            loadvr(mips_data[1], 1)
            storevr(1, mips_data[3])
        elif mips_data[0] == '+' or mips_data[0] == '-' or mips_data[0] == '*' or mips_data[0] == '/':
            mips_code.write('L_' + str(i) + ':\n')
            loadvr(mips_data[1], 1)
            loadvr(mips_data[2], 2)
            if mips_data[0] == '+':
                mips_code.write('add $t1,$t1,$t2\n')
            elif mips_data[0] == '-':
                mips_code.write('sub $t1,$t1,$t2\n')
            elif mips_data[0] == '*':
                mips_code.write('mul $t1,$t1,$t2\n')
            elif mips_data[0] == '/':
                mips_code.write('div $t1,$t1,$t2\n')
            storevr(1, mips_data[3])
        elif mips_data[0] == 'print': # was out
            mips_code.write('L_' + str(i) + ':\nli $v0,1\n')
            loadvr(mips_data[3],1)
            mips_code.write('syscall\n')

            mips_code.write('li $v0, 4 \t #These 3 commands are for write a "newline"\n')
            mips_code.write('la $a0, newline\n')
            mips_code.write('syscall\n')

        elif mips_data[0] == 'input':
            mips_code.write('L_' + str(i) + ':\nli $v0,5\n')
            mips_code.write('syscall\n')
            storevr(1, mips_data[3])
        elif mips_data[0] == 'retv':
            # semantic_analysis(False, i)
            mips_code.write('L_' + str(i) + ':\n')
            loadvr(mips_data[3], 1)
            mips_code.write('lw $t0,-8($sp)\n')
            mips_code.write('sw $t1,($t0)\n')
        elif mips_data[0] == 'begin_block':
            if mips_data[1] == func_name: #main
                mips_code.write('LMain:\n')
                mips_code.write('addi $fp,$sp , ' + str(param_offset) + ' \n')
            else: #function or procedure
                mips_code.write('L_' + mips_data[1] + ':\n')
                mips_code.write('L_' + str(i) + ':\n')
                mips_code.write('sw $ra,($sp)\n')

        elif mips_data[0] == 'end_block':
            if mips_data[1] != func_name:
                mips_code.write('L_' + str(i) + ':\n')
                mips_code.write('lw $ra,($sp)\n')
                mips_code.write('jr $ra\n')

        elif mips_data[0] == 'par' or mips_data[2] == 'CV':
            mips_code.write('L_' + str(i) + ':\n')
            parameterOffset(param_offset, i)
            loadvr(mips_data[1], 0)
            mips_code.write('sw $t0, ' + str(-(12+(4*param_offset))) + ' ($fp)\n')
            param_offset += 1

        elif mips_data[0] == 'par' or mips_data[2] == 'REF':
            mips_code.write('L_' + str(i) + ':\n')
            a,b= locateVariable(mips_data[1])
            parameterOffset(param_offset, i)
            if a==nestingLevel: #local var
                if recordScopeStack[a][b][1] == 'inout': #local var as ref
                    mips_code.write('lw $t0 , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b]) - 1]) + '($sp)\n')
                    mips_code.write('sw $t0 , ' + str(-(12+(4*param_offset))) + ' ($fp)\n')
                else:
                    mips_code.write('add $t0,$sp , -' + str(recordScopeStack[a][b][-1]) + '\n')
                    mips_code.write('sw $t0, ' + str(-(12+(4*param_offset))) + ' ($fp)\n')

            else: #local var as cv
                if recordScopeStack[a][b][-1] == 'inout':
                    gnlvcode(recordScopeStack[a][b][0])
                    mips_code.write('lw $t0,($t0)\n')
                    mips_code.write('sw $t0, ' + str(-(12+(4*param_offset))) + '($fp)\n')

                else:
                    gnlvcode(recordScopeStack[a][b][0])
                    mips_code.write('sw $t0 , ' + str(-(12+(4*param_offset))) + ' ($fp)\n')
            param_offset += 1

        elif mips_data[0] == 'par' and mips_data[2] == 'RET': #???????? retv
            a,b=locateVariable(mips_data[1])
            mips_code.write('L_' + str(i) + ':\n')
            mips_code.write('add $t0,$sp , -' + str(recordScopeStack[a][b][len(recordScopeStack[a][b])-1]) + '\n')
            mips_code.write('sw $t0,-8($fp)\n')

        elif mips_data[0]== 'call':
            mips_code.write('L_' + str(i) + ':\n')
            a,b=locateVariable(mips_data[3])
            if a==nestingLevel:
                mips_code.write('lw $t0,-4($sp)\n')
                mips_code.write('sw $t0,-4($fp)\n')
            else:
                mips_code.write('sw $sp , -4($fp)\n')

            mips_code.write('add $sp,$sp , ' + str(framelength) + '\n')
            mips_code.write('jal L_' + mips_data[1] + '\n')
            mips_code.write('add $sp,$sp , -' + str(framelength) + '\n')
            param_offset = 0


# **********************************************************************************


# GLOBAL VARIABLES AND MAIN *******************************************************

# array of the committed words
committed_words =  ["program", "if", "switchcase", "not", "function", "input",
                   "declare", "else", "forcase", "and", "procedure", "print",
                   "while", "incase", "or", "call", "case",
                   "return", "default", "in", "inout"]

# CONSTANTS
lower_int_limit = -(2 ^ 32 - 1)
max_int_limit = 2 ^ 32 - 1
max_id_limit = 30
file_line = 1
quads = {}
quadcounter = -1
temp_varlist = []
temp_counter = -1
enableProc = False

record_entity_list = []
record_argument_list = []
recordScopeStack={}
nestingLevel = 0
framelength = 0
offset = []
offset.append(12)

# check the number of arguments in terminal
if len(sys.argv) >= 3:
    print('You must give exactly 2 argv\n')
    sys.exit()

filename = sys.argv[1]
filename_list = filename.split('.')

# check type of input file
if filename_list[1] != 'ci':
    print('Input file must be of cimple type (.ci)\n')
    sys.exit()

fp = open(filename, 'r')

path = filename_list[0] + '.int'
interval_code = open(path, 'w')

# Create an assembly file
mips_code=open('assemblyfile.asm', 'w')
mips_code.write('.data\nnewline: .asciiz "\\n"\n\n.text\n\n')
mips_code.write('j L_Main\n')


# initialize Syntax Analyzer
program()
print('Syntax Analysis completed successfully.')
print('No lexical or syntax errors found.')
# print_temp_varlist()
# print_quads()

# write the quads in a file
write_quads()

# create a C file
# if enableProc == False:
#     path = filename_list[0] + '.c'
#     c_code = open(path, 'w')
#     write_c()
#     print("A C-file has been created")
#     c_code.close()

# finalCode()
interval_code.close()
fp.close()

# *********************************************** The End ***********************************************************





