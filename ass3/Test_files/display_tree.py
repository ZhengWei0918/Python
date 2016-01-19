import sys
import os

def check_text(input_file_name):
    # Function which checks whether the input txt file is valid or not
    # by the way, generate a list in order to use next function generate(input_list, result_list, step_depth) easily
    # the list is like
    #               ['A', ' B', '  C', ' D', '  E', '  F', ' G', ' H', '  I', '   J'] in tree_1.txt
    #               ['This', ' is the', '  2nd', '   example', '   of a', '   \x0e', ' tree', '  given', '  
    #               \x05', ' for the', '  fourth', '   assignment', '    this session', ' in s2, 2009'] in tree_2.txt
    #               ['A', ' B', ' \x05', ' \x05', ' \x0e', '  D', ' E', '  F'] in tree_3.txt
    #               ['0 0 0', ' 1 1 1', ' 2 2 2', '  3 3 3', '  4 4 4', ' 5 5 5', ' \x0e', '  6 6 6', '  7 7 7'] in tree_4.txt
    #               ['0', ' 1', '  2', '   3', ' 4', ' 5', '  6', '   7', ' 8'] in tree_5.txt
    x = -1
    y = -1
    initial_list = []
    line_index = 0
    with open(input_file_name, 'r') as file:
        for line in file:
            white_space = 0
            for index, item in enumerate(line):
                if item.isspace():
                    white_space += 1
                else:
                    line_index += 1
                    if x == -1:
                        x = white_space
                        initial_list.append(line[x:].rstrip())                        
                        break
                    elif y == -1:
                        y = white_space - x
                        last_white_space = white_space                        
                        if y < 1:
                            print('Wrong number of leading spaces on nonblank line', line_index)
                            sys.exit()
                        initial_list.append(line[x + y - 1:].rstrip())                        
                        break
                    else:
                        if white_space - x <=0 or (white_space - x) % y != 0 or \
                           (white_space - last_white_space) / y > 1:
                            print('Wrong number of leading spaces on nonblank line', line_index)
                            sys.exit()                        
                        initial_list.append(line[x + (y - 1) * ((white_space - x) // y):].rstrip())                        
                        last_white_space = white_space
                        break
    return initial_list

current_depth = 0
i = 0
last_flag = False
def generate(input_list, result_list, step_depth):
    # Function which generates a list of output content
    # like  ['A',['B',['C'],'D',['E','F'],'G','H',['I',['J']]]] in tree_1.txt
    #       ['This', ['is the', ['2nd', ['example', 'of a', '^N']], 'tree',['given','^E'], 
    #           'for the', ['fourth', ['assignment', ['this session']]], 'in s2, 2009']] in tree_2.txt
    #       ['A', ['B', '^E', '^E', '^N', ['D'], 'E', ['F']]] in tree_3.txt
    #       ['0 0 0', ['1 1 1', '2 2 2', ['3 3 3', '4 4 4'], '5 5 5', '^N', ['6 6 6', '7 7 7']]] in tree_4.txt
    #       ['0', ['1', ['2', ['3']], '4', '5', ['6', ['7']], '8']] in tree_5.txt
    # in order to implement recursion easily

    global i
    global current_depth
    global last_flag    
    while i <= len(input_list):
        current_depth = 0
        for item in input_list[i]:
            if item.isspace():
                current_depth += 1
            else:
                break
        if current_depth == step_depth:
            if i == len(input_list) - 1 and last_flag:
                return result_list
            elif i == len(input_list) - 1:
                result_list.append(input_list[i].lstrip())
                last_flag = True
                return result_list            
            result_list.append(input_list[i].lstrip())            
            i += 1
        elif current_depth > step_depth:            
            if i == len(input_list) - 1 and last_flag:
                return result_list
            elif i == len(input_list) - 1:                
                result_list.append([input_list[i].lstrip()])                
                last_flag = True                
                return result_list            
            result_list.append([input_list[i].lstrip()])                       
            i += 1            
            generate(input_list, result_list[-1], step_depth + 1)
        elif current_depth < step_depth:           
            return result_list        
    return result_list

depth = 0
line_flag = False
output_list = []
output_string = ''
def re_list(input_list):
    # Use the output list after function generate(input_list, result_list, step_depth)
    # to write the main recursion content in it
    global depth
    global line_flag
    global output_list
    global output_string
    for index, item in enumerate(input_list):
        if type(item) is list:
            depth += 1
            re_list(item)
            if depth > 0:
                output_string += '\n'
                output_list.append(output_string)
                output_string = ''
                for i in range(depth):
                    output_string += '    '
                output_string += '}'
        else:
            if depth == 0:
                output_string += '\\node {'
                output_string += item
                output_string += '}\n'
                output_list.append(output_string)
                output_string = ''              
            else:
                if line_flag:
                    output_string += '\n'
                    output_list.append(output_string)
                    output_string = ''
                line_flag = True
                for i in range(depth):
                    output_string += '    '
                if item == '\x05':
                    output_string += 'child[fill=none] {edge from parent[draw=none]}'
                elif item == '\x0e':
                    output_string += 'child'
                    if len(input_list) > index + 1 and type(input_list[index + 1]) is list:
                        output_string += ' {'                    
                else:
                    output_string += 'child {node {'
                    output_string += item
                    output_string += '}'
                    
                if len(input_list) == index + 1 or type(input_list[index + 1]) is not list:
                    if item != '\x05' and item != '\x0e':
                        output_string += '}'                       
    if depth == 0 and line_flag:
        output_string += ';\n'
        output_list.append(output_string)
    depth -= 1
    return output_list

def write_tex(text_name, direction, shape):
    # To create a new file and write details including the recursion content in it
    out_name = text_name[:-2] + 'ex'
    with open(out_name, 'w') as file:
        file.write('\\documentclass[10pt]{article}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes}\n\\pagestyle{empty}\n\n\\begin{document}\n\n\\begin{center}\n\\begin{tikzpicture}\n')
        if not direction is None:
            file.write('[grow\'=' + direction + ']\n')
        if not shape is None:
            file.write('\\tikzstyle{every node}=[' + shape + ',draw]\n')
        for line in re_list(generate(input_check, [], 0)):
            file.write(line)
        file.write('\\end{tikzpicture}\n\\end{center}\n\n\\end{document}\n')


user_direction = None
user_shape = None
# Check user's input
if len(sys.argv) == 2:
    if len(sys.argv[-1]) > 4 and sys.argv[1][-4:] == '.txt':
        if os.path.exists(sys.argv[-1]):
            input_check = check_text(sys.argv[-1])
            write_tex(sys.argv[-1], user_direction, user_shape)
        else:
            print('No file named ' + sys.argv[-1] + ' in current directory')
    else:
        print('Incorrect invocation')
elif len(sys.argv) == 4:
    if sys.argv[1] == '-grow':
        if sys.argv[2] == 'down':
            user_direction = 'down'
        elif sys.argv[2] == 'up':
            user_direction = 'up'
        elif sys.argv[2] == 'left':
            user_direction = 'left'
        elif sys.argv[2] == 'right':
            user_direction = 'right'
    elif sys.argv[1] == '-nodestyle':
        if sys.argv[2] == 'rectangle':
            user_shape = 'rectangle'
        elif sys.argv[2] == 'circle':
            user_shape = 'circle'
        elif sys.argv[2] == 'ellipse':
            user_shape = 'ellipse'
    if user_direction is None and user_shape is None:
        print('Incorrect invocation')
        sys.exit()
    if len(sys.argv[-1]) > 4 and sys.argv[-1][-4:] == '.txt':
        if os.path.exists(sys.argv[-1]):
            input_check = check_text(sys.argv[-1])
            write_tex(sys.argv[-1], user_direction, user_shape)
        else:
            print('No file named ' + sys.argv[-1] + ' in current directory')
    else:
        print('Incorrect invocation')

elif len(sys.argv) == 6:
    if sys.argv[1] == '-grow' and sys.argv[3] == '-nodestyle':
        if sys.argv[2] == 'down':
            user_direction = 'down'
        elif sys.argv[2] == 'up':
            user_direction = 'up'
        elif sys.argv[2] == 'left':
            user_direction = 'left'
        elif sys.argv[2] == 'right':
            user_direction = 'right'
        if sys.argv[4] == 'rectangle':
            user_shape = 'rectangle'
        elif sys.argv[4] == 'circle':
            user_shape = 'circle'
        elif sys.argv[4] == 'ellipse':
            user_shape = 'ellipse'
        if user_direction is None or user_shape is None:
            print('Incorrect invocation')
            sys.exit()
        if len(sys.argv[-1]) > 4 and sys.argv[-1][-4:] == '.txt':
            if os.path.exists(sys.argv[-1]):
                input_check = check_text(sys.argv[-1])
                write_tex(sys.argv[-1], user_direction, user_shape)
            else:
                print('No file named ' + sys.argv[-1] + ' in current directory')
        else:
            print('Incorrect invocation')

    elif sys.argv[1] == '-nodestyle' and sys.argv[3] == '-grow':
        if sys.argv[2] == 'rectangle':
            user_shape = 'rectangle'
        elif sys.argv[2] == 'circle':
            user_shape = 'circle'
        elif sys.argv[2] == 'ellipse':
            user_shape = 'ellipse'
        if sys.argv[4] == 'down':
            user_direction = 'down'
        elif sys.argv[4] == 'up':
            user_direction = 'up'
        elif sys.argv[4] == 'left':
            user_direction = 'left'
        elif sys.argv[4] == 'right':
            user_direction = 'right'
        if user_direction is None or user_shape is None:
            print('Incorrect invocation')
            sys.exit()
        if len(sys.argv[-1]) > 4 and sys.argv[-1][-4:] == '.txt':
            if os.path.exists(sys.argv[-1]):
                input_check = check_text(sys.argv[-1])
                write_tex(sys.argv[-1], user_direction, user_shape)
            else:
                print('No file named ' + sys.argv[-1] + ' in current directory')
        else:
            print('Incorrect invocation')
else:
    print('Incorrect invocation')
