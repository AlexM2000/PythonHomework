﻿import math as m

func_dictionary = {'sin': m.sin,
                   'cos': m.cos,
                   'tan': m.tan,
                   'atan': m.atan,
                   'asin': m.asin,
                   'acos': m.acos,
                   'degrees': m.degrees,
                   'radians': m.radians,
                   'exp': m.exp,
                   'sqrt': m.sqrt,
                   'log': m.log,
                   'log10': m.log10,
                   'fabs': m.fabs,
                   'round': round,
                   'fsum': m.fsum,
                   'frexp': m.frexp,
                   'ceil': m.ceil,
                   'copysigh': m.copysign,
                   'floor': m.floor,
                   'fmod': m.fmod,
                   'gcd': m.gcd,
                   'isclose': m.isclose,
                   'isfinite': m.isfinite,
                   'isinf': m.isinf,
                   'isnan': m.isnan,
                   'ldexp': m.ldexp,
                   'trunc': m.trunc,
                   'pow': m.pow,
                   'abs': abs
                   }


def skip_space(eval_string, index):
    while index < len(eval_string) and eval_string[index] == ' ':
        index += 1
    if index > len(eval_string):
        raise ValueError("ERROR: invalid argument")
    return index


def call_func_with_args(Func, Args):
    return Func(*Args)


def get_arguments(eval_string, index):
    params = []
    while index < len(eval_string) and eval_string[index] != ')':
        temp = solve_equality(eval_string, index)
        index = temp[1]
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (',', ')'):
            raise ValueError("ERROR: no zapyataya")
        elif index < len(eval_string) and eval_string[index] == ',':
            index += 1
        params.append(temp[0])
    if index < len(eval_string) and eval_string[index] == ')':
        return params, index
    else:
        raise ValueError('ERROR: no closing bracket')


def error(args):
    raise Exception("ERROR: invalid argument")


def search_float(eval_string, index):
    num = ""
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '-':
        num = '-'
        index += 1
    index = skip_space(eval_string, index)
    while index < len(eval_string):
        if eval_string[index].isdigit():
            num += eval_string[index]
            index += 1
        elif (eval_string[index].isalpha()):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        else:
            break
    if (index < len(eval_string) and eval_string[index] == '.'):
        num += eval_string[index]
        index += 1
        while index < len(eval_string):
            if eval_string[index].isdigit():
                num += eval_string[index]
                index += 1
            else:
                break
        return (float(num), index)
    else:
        return (int(num), index)


def get_bracket(eval_string, index):
    result, num1 = 0, 0
    index += 1
    result, index = solve_equality(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == ')':
        index += 1
        return result, index
    else:
        raise ValueError("ERROR: invalid argument on position {}".format(index))


def number_sign(eval_string, index):
    if eval_string[index] == '+':
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result, index = get_variable(eval_string, index)
    elif eval_string[index] == '-':
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result, index = get_variable(eval_string, index)
        result *= -1
    return result, index


def get_variable(eval_string, index):
    index = skip_space(eval_string, index)
    variable = ""
    if index < len(eval_string) and (eval_string[index].isdigit() or eval_string[index] == '.'):
        variable, index = search_float(eval_string, index)
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (
                                           '+', '-', '*', '/', '%', '^',
                                           '>', '<', '=', ')', '!', ','
                                           ):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
    elif index < len(eval_string) and eval_string[index] in ('-', '+'):
        variable, index = number_sign(eval_string, index)
    elif index < len(eval_string) and eval_string[index] == '(':
        variable, index = get_bracket(eval_string, index)
    elif index < len(eval_string) and eval_string[index].isalpha():
        math_object = ""
        while index < len(eval_string) and (eval_string[index].isalpha() or eval_string[index].isdigit()):
            math_object += eval_string[index]
            index += 1
        if (math_object == 'pi'):
            variable = m.pi
        elif (math_object == 'e'):
            variable = m.e
        elif (math_object == 'tau'):
            variable = m.tau
        else:
            if index < len(eval_string) and eval_string[index] == '(':
                index += 1
                tmp = get_arguments(eval_string, index)
                variable = call_func_with_args(func_dictionary.get(math_object.lower(), error), tmp[0])
                index = tmp[1]
                if index < len(eval_string) and eval_string[index] == ')':
                    index += 1
                    index = skip_space(eval_string, index)
            else:
                raise ValueError("ERROR: Invalid argument (index {})".format(index))
    elif index < len(eval_string) and eval_string[index] == ',':
        return variable, index
    else:
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    return (variable, index)


def get_degree(eval_string, index):
    result, num1, index = 0, 0, skip_space(eval_string, index)
    result, index = get_variable(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '^':
        index += 1
        num1, index = get_degree(eval_string, index)
        if (result == 0 and num1 == 0):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result **= num1
        index = skip_space(eval_string, index)
    return result, index


def multiply(eval_string, index):
    mult, num1, index = 1, 0, skip_space(eval_string, index)
    mult, index = get_degree(eval_string, index)
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("*", "/", "%"):
        number_sign = ""
        while eval_string[index] in ("*", "/", "%"):
            number_sign += eval_string[index]
            index += 1
        num1, index = get_degree(eval_string, index)
        if (number_sign == '*'):
            mult *= num1
        elif (number_sign == '/'):
            mult /= num1
        elif (number_sign == "//"):
            mult //= num1
        elif (number_sign == '%'):
            mult %= num1
        else:
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        index = skip_space(eval_string, index)
    return mult, index


def add_math_objects(eval_string, index):
    total, num1 = 0, 0
    total, index = multiply(eval_string, index)
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("+", "-"):
        number_sign = eval_string[index]
        index += 1
        num1, index = multiply(eval_string, index)
        if(number_sign == '+'):
            total += num1
        elif(number_sign == '-'):
            total -= num1
        index = skip_space(eval_string, index)
    return total, index


def solve_equality(eval_string, index):
    num1, num2, number_sign = 0, 0, ""
    num1, index = add_math_objects(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] not in (">", "=", "<", "!", ")", ","):
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    while index < len(eval_string) and eval_string[index] in (">", "=", "<", "!"):
        while index < len(eval_string) and eval_string[index] in ('>', '=', '<', '!'):
            number_sign += eval_string[index]
            index += 1
        num2, index = add_math_objects(eval_string, index)
        if (number_sign == '>='):
            result = (num1 >= num2)
        elif (number_sign == '>'):
            result = (num1 > num2)
        elif (number_sign == '=='):
            result = (num1 == num2)
        elif (number_sign == '<'):
            result = (num1 < num2)
        elif (number_sign == '<='):
            result = (num1 <= num2)
        elif (number_sign == '!='):
            result = (num1 != num2)
        else:
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        return result, index
    return num1, index


def solve(eval_string, index=0):
    index = skip_space(eval_string, index)
    if index >= len(eval_string):
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    result, index = solve_equality(eval_string, index)
    return result
