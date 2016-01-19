# I: 1
# V: 5
# X: 10
# L: 50
# C: 100
# D: 500
# M: 1000

import sys

def incorrect_arguments():
    print('I expect one, two or three command line arguments,')
    print('the second one being "minimally" in case two of those are provided')
    print('and "using" in case three of those are provided.')
    sys.exit()

def incorrect_sequence():
    print('The provided sequence of so-called generalised roman symbols is invalid,')
    print('either because it does not consist of letters only')
    print('or because some letters are repeated.')
    sys.exit()

def invalid_input():
    print('The input is not a valid arabic number,')
    print('or is too large an arabic number,')
    print('or is not a valid (possibly generalised) roman number,')
    print('depending on what is expected.')
    sys.exit()
    
# input a string to use like 'MDCLXVI'
# then output two initial lists like ['I', 'V', 'X', 'L', 'C', 'D', 'M'], [1, 5, 10, 50, 100, 500, 1000]
def generate_initial_list(input_string):
    initial_roman = []
    initial_arabic = []
    for item in input_string:
        if item.isnumeric():
            incorrect_sequence()
        initial_roman.append(item)
    roman_length = len(input_string)
    if not len(set(initial_roman)) == roman_length:
        incorrect_sequence()
    for i in range(roman_length):
        element = 10 ** ((i + 1) // 2)
        if (i + 1) % 2 == 0:
            element = element // 2
        initial_arabic.append(element)
    initial_roman = list(reversed(initial_roman))
    return initial_roman, initial_arabic

# input a string to use like 'MDCLXVI'
# then output two lists like ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'], [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
def generate_list(input_string):    
    roman_list = []
    arabic_list = []
    roman_subtrahend = ''
    arabic_subtrahend = 0
    roman_length = len(input_string)
    initial_roman, initial_arabic = generate_initial_list(input_string)
    for i in range(roman_length):              
        if not i == 0:
            roman_list.append(roman_subtrahend + initial_roman[i])
            arabic_list.append(initial_arabic[i] - arabic_subtrahend)
        roman_list.append(initial_roman[i])
        arabic_list.append(initial_arabic[i])
        if i % 2 == 0:
            roman_subtrahend = initial_roman[i]
            arabic_subtrahend = initial_arabic[i]
    roman_list = list(reversed(roman_list))
    arabic_list = list(reversed(arabic_list))
    return roman_list, arabic_list

# input an string type integer and a used string, like '49036', 'fFeEdDcCbBaA'
# output the result of generalised roman number like 'EeDEBBBaA'
def arabic_to_roman_using(target_number, used_string):
    if target_number[0] == '0':
        invalid_input()
    initial_roman, initial_arabic = generate_initial_list(used_string)
    roman_list, arabic_list = generate_list(used_string)
    limit = 0
    roman_result = ''
    arabic_result = int(target_number)    
    if len(used_string) % 2 == 0:
        limit = 2 * initial_arabic[-1] - initial_arabic[-2] - 1
    elif len(used_string) % 2 == 1:
        limit = 4 * initial_arabic[-1] - 1
    if arabic_result >  limit or arabic_result < 1:
        invalid_input()
    while True:
        for i in range(len(arabic_list)):
            if arabic_result - arabic_list[i] >= 0:
                arabic_result -= arabic_list[i]
                roman_result += roman_list[i]
                break
        if arabic_result == 0:
            break
    return roman_result

# input an string and a used string, like 'EeDEBBBaA' and 'fFeEdDcCbBaA'
# output the result of generalised arabic number like 49036
def roman_to_arabic_using(target_string, used_string):
    initial_roman, initial_arabic = generate_initial_list(used_string)
    convert_list = []
    previous_number = initial_arabic[-1]
    arabic_result = 0
    triple_record = ''
    triple_count = 0
    for item in target_string:
        if not item == triple_record:
            triple_count = 0
            triple_record = item
        else:            
            triple_count += 1
            if triple_count == 3:
                invalid_input()       
    for item in target_string:
        if not item in initial_roman:
            invalid_input()
        convert_list.append(initial_arabic[initial_roman.index(item)])
    for number in convert_list:
        if number > previous_number:
            arabic_result -= 2 * previous_number         
        arabic_result += number
        previous_number = number
    return arabic_result

# check user's input is valid or not
if len(sys.argv) == 2:
    if sys.argv[1].isnumeric():
        output_roman = arabic_to_roman_using(sys.argv[1], 'MDCLXVI')
        return_arabic = roman_to_arabic_using(output_roman, 'MDCLXVI')
        print(output_roman)
    else:
        output_arabic = roman_to_arabic_using(sys.argv[1], 'MDCLXVI')
        return_roman = arabic_to_roman_using(str(output_arabic), 'MDCLXVI')
        if return_roman == sys.argv[1]:
            print(output_arabic)
        else:
            invalid_input()
elif len(sys.argv) == 4:
    if not sys.argv[2] == 'using':
        incorrect_arguments()
    if sys.argv[1].isnumeric():
        output_roman = arabic_to_roman_using(sys.argv[1], sys.argv[3])
        return_arabic = roman_to_arabic_using(output_roman, sys.argv[3])
        print(output_roman)
    else:
        output_arabic = roman_to_arabic_using(sys.argv[1], sys.argv[3])
        return_roman = arabic_to_roman_using(str(output_arabic), sys.argv[3])
        if return_roman == sys.argv[1]:
            print(output_arabic)
        else:
            invalid_input()

elif len(sys.argv) == 3:
    if not sys.argv[2] == 'minimally':
        incorrect_arguments()

else:
    incorrect_arguments()


