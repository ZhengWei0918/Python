import copy
alphabet_set = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
                'o','p','q','r','s','t','u','v','w','x','y','z',\
                'A','B','C','D','E','F','G','H','I','J','K','L','M','N',\
                'O','P','Q','R','S','T','U','V','W','X','Y','Z'}
digit_set = {'0','1','2','3','4','5','6','7','8','9'}
token_set = alphabet_set | digit_set | {'_'}

#Check whether the input string is a token or not.
def check_token(input_string):
    if input_string == '':
        return False
    if not input_string[0] in alphabet_set | {'_'}:
        return False
    for i in range(len(input_string)):
        if not input_string[i] in token_set:
            return False        
    return True

#Check whether the input string is a symbol or not.
def check_symbol(input_string):
    if len(input_string) != 1:
        return False
    return True
        

#Input a line of string, if it is not correspond with sequence with rule,
#return False, otherwise, return [left_token, right_element_list]
def check_rules(input_string):
    if input_string == '':
        return False
    
    white_space = True
    left_hand_token_acceptable = True
    left_hand_token_exist = False
    left_hand = True
    right_hand_exist = False
    right_hand = False    
    left_token = ''
    right_element = ''
    right_element_list = []
    
    for i in range(len(input_string)):
        if left_hand:
            if i + 1 == len(input_string):
                return False
            
            elif input_string[i] == ' ' and white_space:                
                continue

            elif input_string[i] == ' ' and not white_space:                
                check_left = check_token(left_token)
                if not check_left:
                    return False
                white_space = True
                left_hand_token_acceptable = False
                
            elif input_string[i] != '-' and left_hand_token_acceptable:                
                left_token += input_string[i]
                left_hand_token_exist = True
                white_space = False                
            
            elif input_string[i] != '-' and not left_hand_token_acceptable:
                return False
            
            elif input_string[i] == '-':
                if not left_hand_token_exist:
                    return False
                else:
                    if i + 2 == len(input_string) or input_string[i + 1] != '>':
                        return False
                    check_left = check_token(left_token)
                    if not check_left:
                        return False
                    left_hand = False
                    
        elif not left_hand and not right_hand:
            white_space = True
            right_hand = True
            continue
        
        elif right_hand:
            if input_string[i] == ' ' and white_space:
                if i + 1 == len(input_string):
                    if not right_hand_exist:
                        return False
                    if 'ε' in right_element_list and len(right_element_list) > 1:
                        return False
                    return [left_token, right_element_list]
                continue
            
            elif input_string[i] == ' ' and not white_space:
                if not check_token(right_element) | check_symbol(right_element):
                    return False
                right_element_list.append(right_element)
                if i + 1 == len(input_string):
                    if 'ε' in right_element_list and len(right_element_list) > 1:
                        return False
                    return [left_token, right_element_list]
                white_space = True
                right_element = ''
                
            else:                
                right_element += input_string[i]
                if i + 1 == len(input_string):                    
                    if not check_token(right_element) | check_symbol(right_element):
                        return False
                    else:
                        right_element_list.append(right_element)
                        if 'ε' in right_element_list and len(right_element_list) > 1:
                            return False
                        return [left_token, right_element_list]               
                white_space = False
                right_hand_exist = True


                
def check_table(input_string_list):
    table_list = []
    key_set = set()
    value_set = set()
    for line in input_string_list:
        if not check_rules(line):
            return False
        table_list.append(check_rules(line))
    for i in range(len(input_string_list)):
        key_set.add(table_list[i][0])
        for item in table_list[i][1]:
            value_set.add(item)
    if (len(key_set) != len(input_string_list)) or \
       ('ε' in value_set and len(value_set) != 1):
        return False
    return table_list


def check_axiom_array(input_string_list):
    if input_string_list == []:
        return False

    elememt_list = []
    for i in range(len(input_string_list)):
        elememt_list.append([])
    
    for ii in range(len(input_string_list)):        
        white_space = True
        element_exist = False
        element = ''        
        for i in range(len(input_string_list[ii])):
            
            if input_string_list[ii][i] == ' ' and white_space:
                if i + 1 == len(input_string_list[ii]):
                    if not element_exist:
                        return 1
                    else:                        
                        continue
                continue
            elif input_string_list[ii][i] == ' ' and not white_space:                
                elememt_list[ii].append(element)
                if not check_token(element) | check_symbol(element):
                    return 2
                if i + 1 == len(input_string_list[ii]):
                   continue
                white_space = True
                element = ''
            else:
                element += input_string_list[ii][i]
                if i + 1 == len(input_string_list[ii]):                    
                    if not check_token(element) | check_symbol(element):
                        return 3                    
                    elememt_list[ii].append(element)
                    continue
                element_exist = True
                white_space = False
    length_of_item = len(elememt_list[0])
    for item in elememt_list:
        if not len(item) == length_of_item:
            return False
    return elememt_list            

def get_grammar(file_name):
    number_of_lines = 0
    current_line = 0
    begin_axiom_array = False    
    begin_row_tables = False    
    begin_column_tables = False

    finish_axiom_array = False
    finish_row_tables = False
    finish_column_tables = False

    axiom_array_continue = False
    
    axiom_array_list = []
    axiom_array_list_return = []
    row_tables = []
    row_tables_list = []
    row_tables_list_return = []
    column_tables = []
    column_tables_list = []
    column_tables_list_return = []
    white_space = True

    with open(file_name, encoding = 'utf-8') as file:
        for line in file:            
            number_of_lines += 1
    
    with open(file_name, encoding = 'utf-8') as file:
        for line in file:
            current_line += 1
            if not begin_axiom_array | begin_row_tables | begin_column_tables:                               
                if line == '\n':                    
                    continue
                elif line[0] == ' ':
                    for item in line[:-1]:
                        if not item == ' ':        
                            print('Incorrect grammar')
                            return
                    continue
                elif not line[0] == '#':                                    
                    print('Incorrect grammar')
                    return
                elif line[0] == '#':                    
                    if len(line) == 14:                        
                        if not line == '# Axiom array\n' or finish_axiom_array:
                            print('Incorrect grammar')
                            return
                        finish_axiom_array = True
                        begin_axiom_array = True                        
                    elif len(line) == 13:
                        if not line == '# Row tables\n' or finish_row_tables:
                            print('Incorrect grammar')
                            return
                        finish_row_tables = True
                        begin_row_tables = True
                    elif len(line) == 16:
                        if not line == '# Column tables\n' or finish_column_tables:
                            print('Incorrect grammar')
                            return
                        finish_column_tables = True
                        begin_column_tables = True
                    else:
                        print('Incorrect grammar')
                        return
                        
            elif begin_axiom_array | begin_row_tables | begin_column_tables:                
                if begin_axiom_array:                    
                    if line == '\n' and white_space:                        
                        continue
                    elif line == '\n' and not white_space:
                        axiom_array_list_return = check_axiom_array(axiom_array_list)
                        if not axiom_array_list_return:
                            print('Incorrect grammar')
                            return
                        begin_axiom_array = False                        
                        white_space = True
                    elif line[0] == ' ':                        
                        if number_of_lines == current_line:
                            axiom_array_list.append(line[:-1])
                            axiom_array_list_return = check_axiom_array(axiom_array_list)
                            finish_axiom_array = True
                            if not axiom_array_list_return:
                                print('Incorrect grammar')
                                return
                        elif white_space:                           
                            for item in line[:-1]:                            
                                if not item == ' ':
                                    axiom_array_list.append(line[:-1])
                                    white_space = False
                                    break
                        elif not white_space:                            
                            for item in line:
                                if not item == ' ':
                                    axiom_array_list.append(line[:-1])
                                    axiom_array_continue = True
                                    break
                                axiom_array_continue = False
                            if axiom_array_continue:
                                continue
                            axiom_array_list_return = check_axiom_array(axiom_array_list)
                            if not axiom_array_list_return:
                                print('Incorrect grammar')
                                return
                            begin_axiom_array = False                            
                            white_space = True                                
                    elif line[0] == '#':                        
                        if line != '# Row tables\n' and line != '# Column tables\n':                                                        
                            print('Incorrect grammar')
                            return
                        elif line == '# Row tables\n' and finish_row_tables:
                            print('Incorrect grammar')
                            return
                        elif line == '# Column tables\n' and finish_column_tables:
                            print('Incorrect grammar')
                            return
                        else:
                            axiom_array_list_return = check_axiom_array(axiom_array_list)
                            if not axiom_array_list_return:
                                print('Incorrect grammar')
                                return
                            elif line == '# Row tables\n':                                                                
                                begin_axiom_array = False
                                finish_row_tables = True
                                white_space = True
                                begin_row_tables = True
                            elif line == '# Column tables\n':
                                begin_axiom_array = False
                                finish_column_tables = True
                                white_space = True
                                begin_column_tables = True
                    else:                        
                        axiom_array_list.append(line[:-1])
                        white_space = False
                        if number_of_lines == current_line:
                            axiom_array_list_return = check_axiom_array(axiom_array_list)
                            if not axiom_array_list_return:
                                print('Incorrect grammar')
                                return                            

                elif begin_row_tables:                    
                    if line == '\n' and white_space:                       
                        continue
                    elif line == '\n' and not white_space:
                        row_tables_list_return = check_table(row_tables)
                        if not row_tables_list_return:                            
                            print('Incorrect grammar')
                            return
                        row_tables_list.append(row_tables_list_return)
                        row_tables = []                                                
                        white_space = True
                    elif line[0] == ' ':
                        if number_of_lines == current_line:
                            row_tables.append(line[:-1])
                            row_tables_list_return = check_table(row_tables)                            
                            if not row_tables_list_return:
                                print('Incorrect grammar')
                                return
                        elif white_space:
                            for item in line[:-1]:                            
                                if not item == ' ':
                                    row_tables.append(line[:-1])
                                    white_space = False
                                    break
                        elif not white_space:
                            for item in line:
                                if not item == ' ':
                                    row_tables.append(line[:-1])                                                                   
                                    break
                            row_tables_list_return = check_table(row_tables)
                            if not row_tables_list_return:
                                print('Incorrect grammar')
                                return
                            row_tables_list.append(row_tables_list_return)
                            row_tables = []                                                        
                            white_space = True                                
                    elif line[0] == '#':              
                        if line != '# Axiom array\n' and line != '# Column tables\n':                                                        
                            print('Incorrect grammar')
                            return
                        elif line == '# Axiom array\n' and finish_axiom_array:
                            print('Incorrect grammar')
                            return
                        elif line == '# Column tables\n' and finish_column_tables:
                            print('Incorrect grammar')
                            return
                        else:
                            row_tables_list_return = check_table(row_tables)                            
                            if not row_tables_list_return and not row_tables == []:
                                print('Incorrect grammar')
                                return
                            elif line == '# Axiom array\n':
                                if not row_tables == []:                                    
                                    row_tables_list.append(row_tables_list_return)
                                begin_row_tables = False
                                finish_axiom_array = True
                                white_space = True
                                begin_axiom_array = True
                            elif line == '# Column tables\n':
                                if not row_tables == []:
                                    row_tables_list.append(row_tables_list_return)
                                begin_row_tables = False
                                finish_column_tables = True
                                white_space = True
                                begin_column_tables = True
                    else:                        
                        row_tables.append(line[:-1])
                        white_space = False
                        if number_of_lines == current_line:
                            row_tables_list_return = check_table(row_tables)
                            if not row_tables_list_return:
                                print('Incorrect grammar')
                                return
                            row_tables_list.append(row_tables_list_return)                            

                elif begin_column_tables:                    
                    if line == '\n' and white_space:                        
                        continue
                    elif line == '\n' and not white_space:
                        column_tables_list_return = check_table(column_tables)
                        if not column_tables_list_return:                            
                            print('Incorrect grammar')
                            return
                        column_tables_list.append(column_tables_list_return)
                        column_tables = []                                                
                        white_space = True
                    elif line[0] == ' ':
                        if number_of_lines == current_line:
                            column_tables.append(line[:-1])
                            column_tables_list_return = check_table(column_tables)                            
                            if not column_tables_list_return:
                                print('Incorrect grammar')
                                return
                        elif white_space:
                            for item in line[:-1]:                            
                                if not item == ' ':
                                    column_tables.append(line[:-1])
                                    white_space = False
                                    break
                        elif not white_space:
                            for item in line:
                                if not item == ' ':
                                    column_tables.append(line[:-1])                                                                   
                                    break
                            column_tables_list_return = check_table(column_tables)
                            if not column_tables_list_return:
                                print('Incorrect grammar')
                                return
                            column_tables_list.append(column_tables_list_return)
                            column_tables = []                                                        
                            white_space = True                            
                    elif line[0] == '#':              
                        if line != '# Row tables\n' and line != '# Axiom array\n':                                                        
                            print('Incorrect grammar')
                            return
                        elif line == '# Row tables\n' and finish_row_tables:
                            print('Incorrect grammar')
                            return
                        elif line == '# Axiom array\n' and finish_axiom_array:
                            print('Incorrect grammar')
                            return
                        else:
                            column_tables_list_return = check_table(column_tables)                        
                            if not column_tables_list_return and not column_tables == []:
                                print(column_tables)
                                print(current_line)
                                print('Incorrect grammar')
                                return
                            elif line == '# Axiom array\n':
                                if not column_tables == []:                                    
                                    column_tables_list.append(column_tables_list_return)
                                begin_column_tables = False
                                finish_axiom_array = True
                                white_space = True
                                begin_axiom_array = True
                            elif line == '# Row tables\n':
                                if not column_tables == []:
                                    column_tables_list.append(column_tables_list_return)
                                begin_column_tables = False
                                finish_row_tables = True
                                white_space = True
                                begin_row_tables = True
                    else:                        
                        column_tables.append(line[:-1])
                        white_space = False
                        if number_of_lines == current_line:
                            column_tables_list_return = check_table(column_tables)
                            if not column_tables_list_return:
                                print('Incorrect grammar')
                                return
                            column_tables_list.append(column_tables_list_return)                                              

    if not finish_axiom_array & finish_row_tables & finish_column_tables:
        print('Incorrect grammar')
        return

    row_tables_empty = False
    column_tables_empty = False
    
    for item1 in row_tables_list:
        for item2 in item1:
            for item3 in item2:
                for item4 in item3:
                    if item4 == 'ε':
                        row_tables_empty = True

    for item1 in column_tables_list:
        for item2 in item1:
            for item3 in item2:
                for item4 in item3:
                    if item4 == 'ε':
                        column_tables_empty = True
                        
    if row_tables_empty & column_tables_empty:
        print('Incorrect grammar')
        return
    
    return axiom_array_list_return,row_tables_list,column_tables_list                                                          

def print_pattern(input_pattern_copy):

    input_pattern = copy.deepcopy(input_pattern_copy)
    width_of_each_element = []
    width_of_pattern = len(input_pattern[0])
    number_of_line = len(input_pattern)

    for i in range(width_of_pattern):
        width_of_each_element.append(0)
        for j in range(number_of_line):
            if width_of_each_element[i] < len(input_pattern[j][i]):
                width_of_each_element[i] = len(input_pattern[j][i])

    for i in range(number_of_line):
        for j in range(width_of_pattern):
            if j < width_of_pattern - 1:
                while len(input_pattern[i][j]) <= width_of_each_element[j]:
                    input_pattern[i][j] += ' '
            print(input_pattern[i][j], end = '')
        print()

def print_tables(input_tables_copy):
    
    input_tables = copy.deepcopy(input_tables_copy)
    output_tables = []        
    if input_tables == []:
        return    
    for tables in input_tables:        
        output_element = []
        while not tables == []:
            first_out_table_element = tables[0][0]
            first_out_table = tables[0]            
            pop_index = 0
            for i in range(len(tables)):                
                if tables[i][0] < first_out_table_element:                    
                    first_out_table_element = tables[i][0]
                    first_out_table = tables[i]
                    pop_index = i            
            output_element.append(first_out_table)
            tables.pop(pop_index)            
        output_tables.append(output_element)
                
    width_of_left = []
    width_of_right = []
    number_of_tables = len(output_tables)
    for i in range(number_of_tables):        
        width_of_left.append(0)
        width_of_right.append([])
        for j in range(len(output_tables[i][0][1])):            
            width_of_right[i].append(0)
            
    for i in range(number_of_tables):
        for j in range(len(output_tables[i])):
            if width_of_left[i] < len(output_tables[i][j][0]):
                width_of_left[i] = len(output_tables[i][j][0])
            for k in range(len(output_tables[i][0][1])):
                if width_of_right[i][k] < len(output_tables[i][j][1][k]):
                    width_of_right[i][k] = (len(output_tables[i][j][1][k]))
    width_of_left,width_of_right

    for i in range(number_of_tables):
        for j in range(len(output_tables[i])):
            while len(output_tables[i][j][0]) < width_of_left[i]:                
                output_tables[i][j][0] += ' '
            print(output_tables[i][j][0],'->',end = '')
            if output_tables[i][j][1][0] == 'ε':
                if j < len(output_tables[i]) -1:
                    print('\n', end = '')
                    continue
                print()
                break
            
            for k in range(len(output_tables[i][j][1])):
                if k < len(output_tables[i][j][1]) - 1:                   
                    while len(output_tables[i][j][1][k]) < width_of_right[i][k]:
                        output_tables[i][j][1][k] += ' '
                print(' ' + output_tables[i][j][1][k], end = '')
            print()
        if i < number_of_tables - 1:
            print()

def symbols(input_grammar):
    input_row_tables = input_grammar[1]
    input_column_tables = input_grammar[2]
    left_hand_set = set()
    right_hand_set = set()
    for row_tables in input_row_tables:
        for rules in row_tables:
            left_hand_set.add(rules[0])
            for items in rules[1]:
                right_hand_set.add(items)
                
    for column_tables in input_column_tables:
        for rules in column_tables:
            left_hand_set.add(rules[0])
            for items in rules[1]:
                right_hand_set.add(items)
                
    terminals_set = right_hand_set - left_hand_set
    non_terminals = list(left_hand_set)
    terminals = list(terminals_set)
    non_terminals_out = []
    terminals_out = []
    for item in non_terminals:
        if check_token(item):
            non_terminals_out.append(item)
    for item in terminals:
        if check_symbol(item):
            terminals_out.append(item)        
    non_terminals_out.sort()
    terminals_out.sort()    
    return non_terminals_out, terminals_out

longest_step = 0
final_process = []
current_step = 0
current_process = []
excluded_picture = []
more_way = False

def generate_detail(input_grammar, final_list):
    
    non_terminals, terminals = symbols(input_grammar)
    input_axiom_array, input_row_tables, input_column_tables = input_grammar    
    row_keys = []
    column_keys = []
    final_hieght = len(final_list)
    final_length = len(final_list[0])        
    for i in range(len(input_row_tables)):
        row_keys.append([])
        for j in range(len(input_row_tables[i])):
            row_keys[i].append(input_row_tables[i][j][0])        
    for i in range(len(input_column_tables)):
        column_keys.append([])
        for j in range(len(input_column_tables[i])):
            column_keys[i].append(input_column_tables[i][j][0])

    def table_change(iinput_axiom_array):
        global longest_step
        global final_process
        global current_step
        global current_process
        global excluded_picture
        global more_way       
        flag = False        
        excluded_picture.append(input_axiom_array)
        iinput_axiom_array_copy = copy.deepcopy(iinput_axiom_array)        
        for ii in range(len(iinput_axiom_array_copy)):
            for i in range(len(row_keys)):
                if set(iinput_axiom_array_copy[ii]).issubset(set(row_keys[i])):                    
                    flag = False
                    my_iinput_axiom_array_copy = copy.deepcopy(iinput_axiom_array_copy)
                    for jj in range(len(input_row_tables[i][0][1]) - 1):
                        my_iinput_axiom_array_copy.insert(ii + 1, [0] * len(my_iinput_axiom_array_copy[0]))                    
                    for jjj in range(len(my_iinput_axiom_array_copy[ii])):                        
                        for j in range(len(input_row_tables[i])):
                            if my_iinput_axiom_array_copy[ii][jjj] == input_row_tables[i][j][0]:                                    
                                for kk in range(len(input_row_tables[i][j][1])):                                        
                                    my_iinput_axiom_array_copy[ii + kk][jjj] = input_row_tables[i][j][1][kk]
                                break
                    current_process.append(copy.deepcopy(my_iinput_axiom_array_copy))
                    
                    current_step += 1
                    if current_process in excluded_picture:
                        
                        current_step -= 1
                        del current_process[-1]
                        continue
                    excluded_picture.append(copy.deepcopy(current_process))
                    if my_iinput_axiom_array_copy == final_list:
                        if not longest_step == 0:
                            more_way = True                        
                        if current_step > longest_step:
                            longest_step = current_step
                            final_process = copy.deepcopy(current_process)                        
                        current_step -= 1
                        del current_process[-1]
                        continue
                    elif len(my_iinput_axiom_array_copy) > final_hieght or len(my_iinput_axiom_array_copy[0]) > final_length:
                        current_step -= 1
                        del current_process[-1]
                        continue                    
                    table_change(my_iinput_axiom_array_copy)                
        flag = True        
        for iii in range(len(iinput_axiom_array_copy[0])):            
            L = []            
            for ii in range(len(iinput_axiom_array_copy)):
                L.append(iinput_axiom_array_copy[ii][iii])
            for i in range(len(column_keys)):
                if set(L).issubset(set(column_keys[i])):                    
                    flag = False                    
                    my_iinput_axiom_array_copy = copy.deepcopy(iinput_axiom_array_copy)                    
                    for jj in range(len(my_iinput_axiom_array_copy)):
                        for jjj in range(len(input_column_tables[i][0][1]) - 1):
                            my_iinput_axiom_array_copy[jj].insert(iii + 1, 0)                  
                    for j in range(len(my_iinput_axiom_array_copy)):
                        for k in range(len(input_column_tables[i])):                            
                            if my_iinput_axiom_array_copy[j][iii] == input_column_tables[i][k][0]:
                                for kk in range(len(input_column_tables[i][k][1])):
                                    my_iinput_axiom_array_copy[j][iii + kk] = input_column_tables[i][k][1][kk]
                                break                                           
                    current_process.append(copy.deepcopy(my_iinput_axiom_array_copy))                    
                    current_step += 1
                    if current_process in excluded_picture:
                        
                        current_step -= 1
                        del current_process[-1]
                        continue
                    excluded_picture.append(copy.deepcopy(current_process))
                    if my_iinput_axiom_array_copy == final_list:                        
                        if current_step > longest_step:
                            if not longest_step == 0:
                                more_way = True
                            longest_step = current_step
                            final_process = copy.deepcopy(current_process)                       
                        current_step -= 1
                        del current_process[-1]
                        continue
                    elif len(my_iinput_axiom_array_copy) > final_hieght or len(my_iinput_axiom_array_copy[0]) > final_length:                        
                        current_step -= 1
                        del current_process[-1]
                        continue                    
                    table_change(my_iinput_axiom_array_copy)
        if flag:
            if current_process == []:
                return False
            current_step -= 1
            del current_process[-1]           
    table_change(input_axiom_array)
    if final_process == []:
        return False        
    final_process.insert(0, input_axiom_array)
    return final_process

def generate(input_grammar, input_string):
    global longest_step
    global final_process
    global current_step
    global current_process
    global excluded_picture
    global deterministic_flag
    global more_way
    non_terminals, terminals = symbols(input_grammar)
    input_axiom_array, input_row_tables, input_column_tables = input_grammar
    output_final_list = []
    output_final_element_list = []
    for i in range(len(input_string)):
        if input_string[i] in terminals:
            output_final_element_list.append(input_string[i])
        elif input_string[i] == '\n':
            output_final_list.append(output_final_element_list)
            output_final_element_list = []
        else:
            print('Picture is invalid.')
            return
        if i == len(input_string) - 1:
            output_final_list.append(output_final_element_list)
    S = set()
    for sub_list in output_final_list:
        S.add(len(sub_list))
        if sub_list == []:
            print('Picture is invalid.')
            return
    if not len(S) == 1 and not output_final_list == []:
        print('Picture is invalid.')
        return
    if output_final_list == []:
        print('Picture cannot be generated.')
        return
    result = generate_detail(input_grammar, output_final_list)
    if not result:
        print('Picture cannot be generated.')
    else:    
        if more_way:
            print('Picture cannot be generated in only one way.')
            print('Here is the final deterministic part:')
        else:
            print('Picture can be generated in only one way.')
            print('Here it is:')
        
        max_length = [0] * len(result)
        for i in range(len(result)):
            for line in result[i]:
                for item in line:
                    if len(item) > max_length[i]:
                        max_length[i] = len(item)

        for i in range(len(result)):
            for j in range(len(result[i])):
                for k in range(len(result[i][j])):
                    if k < len(result[i][j]) - 1:
                        while len(result[i][j][k]) < max_length[i]:
                            result[i][j][k] += ' '                    
                        print(result[i][j][k], end = ' ')
                    else:
                        print(result[i][j][k])                
            if i < len(result) - 1:
                print()   
    longest_step = 0
    final_process = []
    current_step = 0
    current_process = []
    excluded_picture = []
    more_way = False
