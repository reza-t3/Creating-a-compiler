import re

class Table:
    def __init__(self, table_name, col_lenth, row_length):
        self.table = [['None' for _ in range(col_lenth)] for _ in range(row_length)]
        table_dict[table_name] = self
    def set_in_table(self, column, row, value):
        self.table[row][column] = value

def context(table_name):
    global current_table
    current_table = table_dict[table_name] 

def PrintEror():
    print('Error')
    quit()
#_________________________________________________________________________
def white_space(inp):
    while True:
        m0 = re.search(r'\s+[=*/+-]', inp)
        if not m0:
            break
        a = m0.span()[1]
        inp = re.sub(r'\s+[=*/+-]', inp[a-1], inp, 1)
    while True:
        m1 = re.search(r'[=*/+-]\s+', inp)
        if not m1:
            break
        b = m1.span()[0]
        inp = re.sub(r'[=*/+-]\s+', inp[b], inp, 1)
    return inp

def mult_div(inp):
    m1 = re.search(r'[*/]', inp)
    if m1 is None:
        return inp
    else:
        m2 = re.search(r'\d+[*/]\d+', inp)
        if m2 is None:
            PrintEror
        else:
            a1 = m1.span()
            a2 = m2.span()
            if inp[a1[0]] == '*':
                res = int(inp[a2[0]:a1[0]]) * int(inp[a1[1]:a2[1]])
                inp = re.sub(r'\d+\*\d+', str(res), inp, 1)
            elif inp[a1[0]] == '/':
                res = int(inp[a2[0]:a1[0]]) // int(inp[a1[1]:a2[1]])
                inp = re.sub(r'\d+/\d+', str(res), inp, 1)
            m3 = re.search(r'[*/]', inp)
            if m3 is None:
                return inp
            else:
                return mult_div(inp)

def add_sub(inp):
    m1 = re.search(r'[+-]', inp)
    if m1 is None:
        return inp
    else:
        m2 = re.search(r'\d+[+-]\d+', inp)
        if m2 is None:
            PrintEror
        else:
            a1 = m1.span()
            a2 = m2.span()
            if inp[a1[0]] == '+':
                res = int(inp[a2[0]:a1[0]]) + int(inp[a1[1]:a2[1]])
                inp = re.sub(r'\d+\+\d+', str(res), inp, 1)
            elif inp[a1[0]] == '-':
                res = int(inp[a2[0]:a1[0]]) - int(inp[a1[1]:a2[1]])
                inp = re.sub(r'\d+-\d+', str(res), inp, 1)
            return inp

def is_int(inp):
    m = re.match(r'\d+', inp)
    if m is None:
        return False
    else:
        return True

def is_int_In_string(inp):
    m = re.search(r'"?\d+"?', inp)
    if m is None:
        return False
    else:
        return True

def is_srting_capital(inp):
    m = re.search(r'[A-Z]', inp) 
    if m:
        return True
    else:
        return False

def is_string_small(inp):
    m = re.search(r'[a-z]', inp)
    if m:
        return True
    else:
        return False

def num_to_let(inp):
    inp = int(inp)
    remainder_list = []
    i = 0
    while True:
        i += 1
        q = inp // 26
        r = inp % 26
        inp = q - 1
        remainder_list.append(r) 
        if q == 0:
            break
    index_list = []
    for i in range(len(remainder_list)-1,-1,-1):
        index_list.append(remainder_list[i])
    mystring = ''
    for i in range(len(index_list)):
        mystring += chr(index_list[i]+65)
    return mystring    

def let_to_num(inp):
    inp_list = list(inp)
    if len(inp_list) == 1:
        return ord(inp_list[0])-65
    else:
        ans = 0
        for i in range(len(inp_list)):
            if i == len(inp_list) - 1:
                ans *= 26
                ans += ord(inp_list[i])-65
            else:
                ans *= 26
                ans += ord(inp_list[i])-64
        return ans

def int_str(inp):
    m1 = re.search(r'[+-]', inp)
    if m1 is None:
        return inp
    else:
        m2 = re.search(r'[^+-]+[+-][^+-]+', inp)
        a1 = m1.span()
        a2 = m2.span()
        el1 = inp[a2[0]:a1[0]]
        el2 = inp[a1[1]:a2[1]]
        if is_int(el1):
            if is_int(el2):
                inp = add_sub(inp)
                return int_str(inp)
            elif is_srting_capital(el2) and not is_string_small(el2):
                el2 = inp[a1[1]+1:a2[1]-1]
                if inp[a1[0]] == '+':
                    inp = re.sub(r'[^+-]+[+-][^+-]+', str(int(el1)+let_to_num(el2)), inp, 1)
                    return int_str(inp)
                else:
                    inp = re.sub(r'[^+-]+[+-][^+-]+', str(int(el1)-let_to_num(el2)), inp, 1)
                    return int_str(inp)
            else:
                PrintEror
        else:
            if is_int(el2):
                if is_srting_capital(el1) and not is_string_small(el1) and not is_int_In_string(el1):
                    el1 = el1[1:len(el1)-1]
                    if inp[a1[0]] == '+':
                        inp = re.sub(r'[^+-]+[+-][^+-]+', '"'+num_to_let(let_to_num(el1)+int(el2))+'"', inp, 1)
                        return int_str(inp)
                    else:
                        inp = re.sub(r'[^+-]+[+-][^+-]+', '"'+num_to_let(let_to_num(el1)-int(el2))+'"', inp, 1)
                        return int_str(inp)
                else:
                    PrintEror
            else:
                m3 = re.search(r'\+', inp)
                if m3:
                    m4 = re.search(r'[^+-]+\+[^+-]+', inp)
                    a3 = m3.span()
                    a4 = m4.span()
                    el1 = inp[a4[0]:a3[0]]
                    el2 = inp[a3[1]:a4[1]]
                    el1 = el1[1:len(el1)-1]
                    el2 = el2[1:len(el2)-1]
                    inp = re.sub(r'[^+-]+\+[^+-]+', '"'+el1+el2+'"', inp, 1)
                    return int_str(inp)
                else:
                    PrintEror

def replace_var(inp, dict):
    for key in dict:
        while True:
            pattern1 = re.search(r'[^\"a-z]'+key, inp)
            pattern2 = re.search(key+r'[^\"a-z]', inp)
            if pattern1:
                start = pattern1.span()[0]
                elem = inp[start]
                inp = re.sub(r'[^\"a-z]'+key, elem+dict[key], inp, 1)
                continue
            elif pattern2:
                end = pattern2.span()[1]
                elem = inp[end-1]
                inp = re.sub(key+r'[^\"a-z]', dict[key]+elem, inp, 1)
                continue
            else:
                break
    return inp

def replace_from_table(inp, matr):
    pattern = re.search(r'([A-Z]+)([0-9]+)', inp)
    if not pattern:
        return inp
    else:    
        letter = pattern.group(1)
        number = pattern.group(2)
        col_num = let_to_num(letter)
        row_num = int(number)
        ans = matr[row_num-1][col_num]
        pattern2 = re.search(r'([A-Z]+)([0-9]+)', ans)
        if pattern2:
            try:
                ans = replace_from_table(ans, matr)
            except:
                PrintEror
            if len(var_dict) != 0:
                ans = replace_var(ans, var_dict)
            ans = replace_bracket(bracket_math(ans))
            try:
                ans = replace_from_table(ans, matr)
            except:
                PrintEror()
            ans = int_str(mult_div(ans))
        start, end = pattern.span()[0], pattern.span()[1]
        inp = re.sub(inp[start:end], ans, inp, 1)
        return replace_from_table(inp, matr)

def bracket_math(inp):
    pattern = re.search(r'\[([^\[\]]+[*/+-][^\[\]]+)\]', inp)
    if not pattern:
        return inp
    else:
        ans = white_space(pattern.group(1))
        ans = mult_div(ans)
        if not mult_div(ans):
            PrintEror
        else:
            ans = int_str(ans)
            if not int_str(ans):
                PrintEror
        inp = re.sub(r'\[([^\[\]]+[*/+-][^\[\]]+)\]', '['+ans+']', inp, 1)
        return bracket_math(inp)

def replace_bracket(inp):
    pattern1 = re.search(r'\[([^\[\]]+)\]', inp)
    if not pattern1:
        return inp
    else:
        pattern2 = re.search(r'\[\"([A-Z]+)\"\]', inp)
        if pattern2:
            letter = pattern2.group(1)
            inp = re.sub(r'\[\"([A-Z]+)\"\]', letter, inp, 1)
            return replace_bracket(inp)
        else:
            pattern3 = re.search(r'\[([0-9]+)\]', inp)
            if not pattern3:
                return inp
            else:
                number = pattern3.group(1)
                inp = re.sub(r'\[([0-9]+)\]', number, inp, 1)
                return replace_bracket(inp)

def find_index(inp):
    pattern1 = re.search(r'([A-Z]+)([0-9]+)', inp)
    letter = pattern1.group(1)
    number = pattern1.group(2)
    col_num = let_to_num(letter)
    row_num = int(number)
    return col_num, row_num
#_________________________________________________________________________
def create_func(inp):
    create_pattern = re.search(r'create\((\w+),(\d+),(\d+)\)', inp)
    table_name = create_pattern.group(1)
    col_length = create_pattern.group(2)
    row_length = create_pattern.group(3)
    mytable = Table(table_name, int(col_length), int(row_length))
    return
def context_func(inp):
    context_pattern = re.search(r'context\((\w+)+\)', inp)
    try:
        context(context_pattern.group(1))
        return
    except:
        PrintEror()
def table_func(inp):
    table_pattern = re.search(r'(^[A-Z]\w+)=(.+)', inp)
    left1 = table_pattern.group(1)
    right1 = table_pattern.group(2)
    try:
        right1 = replace_from_table(right1, current_table.table)
    except:
        PrintEror
    if len(var_dict) != 0:
        right1 = replace_var(right1, var_dict)
    right1 = replace_bracket(bracket_math(right1))
    try:
        right1 = replace_from_table(right1, current_table.table)
    except:
        PrintEror()
    right1 = int_str(mult_div(right1))
    col, row = find_index(left1)
    try:
        current_table.set_in_table(col, row-1, right1)
    except:
        PrintEror()
    return
def var_func(inp):
    var_pattern = re.search(r'(^[a-z]\w*)=(.+)', inp)
    left2 = var_pattern.group(1)
    right2 = var_pattern.group(2)
    pattern1 = re.search(r'[A-Z]+[0-9]+', inp)
    if pattern1:
        try:
            right2 = replace_from_table(right2, current_table.table)
        except:
            PrintEror()
    if len(var_dict) != 0:
        right2 = replace_var(right2, var_dict)
    right2 = replace_bracket(bracket_math(right2))
    if pattern1:
        try:
            right2 = replace_from_table(right2, current_table.table)
        except:
            PrintEror()
    right2 = int_str(mult_div(right2))
    var_dict[left2] = right2
    return
def set_func(inp):
    setfunc_pattern = re.search(r'setFunc\((.+),(.+)\)', inp)
    left = setfunc_pattern.group(1)
    right = setfunc_pattern.group(2)
    if len(var_dict) != 0:
        left = replace_var(left, var_dict)
        right = replace_var(right, var_dict)
    left = replace_bracket(bracket_math(left))
    right = replace_bracket(bracket_math(right))
    col, row = find_index(left)
    try:
        current_table.set_in_table(col, row-1, right)
    except:
        PrintEror()
    return
def print_func(inp):
    print_pattern = re.search(r'print\((.+)\)', inp)
    ans = print_pattern.group(1)
    pattern1 = re.search(r'[A-Z]+[0-9]+', ans)
    if pattern1:
        try:
            ans = replace_from_table(ans, current_table.table)
        except:
            PrintEror()
    if len(var_dict) != 0:
        ans = replace_var(ans, var_dict)
    ans = replace_bracket(bracket_math(ans))
    if pattern1:
        try:
            ans = replace_from_table(ans, current_table.table)
        except:
            PrintEror()
    ans = int_str(mult_div(ans))
    print('out:'+ans)
    return
def print_table(mat):
    lens = [max(map(len, col)) for col in zip(*mat)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in mat]
    print('\n'.join(table))
    return
def final_change():
    global flag, k, l, value, keyy
    for key in table_dict:
            for i in range(len(table_dict[key].table)):
                for j in range(len(table_dict[key].table[0])):
                    pattern = re.search(r'[A-Z]+[0-9]+', table_dict[key].table[i][j])
                    if pattern:
                        mylist = re.findall(r'[A-Z]+[0-9]+', table_dict[key].table[i][j])
                        flag2 = False
                        for elem in mylist:
                            col, row = find_index(elem)
                            if table_dict[key].table[row-1][col] == 'None':
                                flag2 = True
                                break
                        if not flag2:
                            table_dict[key].table[i][j] = replace_from_table(table_dict[key].table[i][j], table_dict[key].table)
                            if len(var_dict) != 0:
                                table_dict[key].table[i][j] = replace_var(table_dict[key].table[i][j], var_dict)
                            table_dict[key].table[i][j] = int_str(mult_div(table_dict[key].table[i][j]))
                        else:
                            flag = True
                            keyy = key
                            k, l = i, j
                            value = table_dict[key].table[i][j]
                            table_dict[key].table[i][j] = 'None'          
    return     

#_________________________________________________________________________

def read(inp):
    global var_dict, flag, k, l, value, keyy
    inp = white_space(inp)
    create_pattern = re.search(r'create\((\w+),(\d+),(\d+)\)', inp)
    if create_pattern:
        create_func(inp)
        return
    context_pattern = re.search(r'context\((\w+)+\)', inp)
    if context_pattern:
        context_func(inp)
        return
    table_pattern = re.search(r'(^[A-Z]\w+)=(.+)', inp)
    if table_pattern:
        table_func(inp)
        return
    table_bracket_pattern = re.search(r'(^\[.+\]\[.+\])=(.+)', inp)
    if table_bracket_pattern:
        left = table_bracket_pattern.group(1)
        if len(var_dict) != 0:
            left = replace_var(left, var_dict)
        left = replace_bracket(bracket_math(left))
        left = int_str(mult_div(left))
        inp = left + '=' + table_bracket_pattern.group(2)
        table_func(inp)
        return
    var_pattern = re.search(r'(^[a-z]\w*)=(.+)', inp)
    if var_pattern:
        var_func(inp)
        return
    setfunc_pattern = re.search(r'setFunc\((.+),(.+)\)', inp)
    if setfunc_pattern:
        set_func(inp)
        return
    print_pattern = re.search(r'print\((.+)\)', inp)
    if print_pattern:
        print_func(inp)
        return
    display_pattern = re.search(r'display\((.+)\)', inp)
    if display_pattern:
        final_change()
        table_name = display_pattern.group(1)
        m = len(table_dict[table_name].table[0])
        indexes = list()
        for i in range(m):
            indexes.append(num_to_let(i))
        newmatr = [indexes] + table_dict[table_name].table
        v = len(newmatr)
        for j in range(v):
            newmatr[j] = [str(j)] + newmatr[j]
        print_table(newmatr)
        if flag:
            table_dict[keyy].table[k][l] = value
            flag = False
        return

table_dict = dict()
current_table : Table = None
var_dict = dict()
flag, k, l, value, keyy = False, None, None, None, None

n = int(input())
for _ in range(n):
    read(input())
