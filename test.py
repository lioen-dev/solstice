#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import sys
import time
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def n():
    print("")

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

variables = {
    "pi": 3.141592653589793,
}

def end_command():
    if len(os.sys.argv) == 1:
        return main()

def help_message(_):
    n()
    for command in commands:
        print(command)
    n()
    end_command()

def clear_screen(_):
    cls()
    end_command()

def math_command(args):
    try:
        safe_chars = set("0123456789+-*/(). %")
        expression = " ".join(args[1:]).replace(" ", "")
        expression = expression.replace(")(", ")*(")
        expression = ''.join(f"{c}*" if i+1 < len(expression) and c.isdigit() and expression[i+1] == '(' else c for i, c in enumerate(expression))

        for var in variables:
            if isinstance(variables[var], (int, float)):
                expression = expression.replace(var, str(variables[var]))

        if not all(c in safe_chars for c in expression):
            raise ValueError("Invalid characters in expression")

        result = eval(expression, {"__builtins__": {}}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        print(result)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        main()
    end_command()

def parrot_command(args):
    try:
        if len(args) <= 1:
            return
        
        message = ' '.join(args[1:])
        if '+' in message:
            parts = message.split('+')
            result = ''
            for part in parts:
                part = part.strip()
                if part.startswith('"') and part.endswith('"'):
                    result += part[1:-1]
                elif part in variables:
                    result += str(variables[part])
                else:
                    result += part
            print(result)
        elif args[1].startswith('"'):
            if message.startswith('"') and message.endswith('"'):
                print(message[1:-1])
        elif args[1].isdigit():
            print(args[1])
        elif args[1] in variables:
            try:
                print(variables[args[1]])
            except:
                print("Variable not found")
        elif args[1] == "math":
            math_command(args[1:])
    except Exception as e:
        print(f"Error: {e}")
        main()
    end_command()

def set_variable_command(args):
    try:
        if len(args) >= 4 and args[2] == "=":
            varname = args[1]
            if args[3] == "input":
                prompt = " ".join(args[4:])
                if prompt.startswith('"') and prompt.endswith('"'):
                    prompt = prompt[1:-1]
                user_input = input(prompt)
                try:
                    value = float(user_input)
                    if value.is_integer():
                        value = int(value)
                    variables[varname] = value
                except ValueError:
                    variables[varname] = user_input

            elif args[3] == "math":
                expression = " ".join(args[4:])
                try:
                    safe_chars = set("0123456789+-*/(). %")
                    for var in variables:
                        if isinstance(variables[var], (int, float)):
                            expression = expression.replace(var, str(variables[var]))

                    if not all(c in safe_chars for c in expression):
                        raise ValueError("Invalid characters in expression")

                    result = eval(expression, {"__builtins__": {}}, {})
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    variables[varname] = result
                except Exception as e:
                    print(f"Error evaluating expression: {e}")

            elif args[3] == "random":
                if len(args) < 5:
                    print("Invalid syntax. Use: variable name = random min max")
                    return
                min_val = int(args[4])
                max_val = int(args[5])
                value = random.randint(min_val, max_val)
                variables[varname] = value
            
            elif args[3] == "im":
                uwu = " ".join(args[3:])
                if uwu == "im addicted to crack cocaine uwu":
                    while True:
                        print("uwu")

            else:
                value = " ".join(args[3:])
                if value.startswith('"') and value.endswith('"'):
                    variables[varname] = value[1:-1]
                else:
                    try:
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                        variables[varname] = value
                    except ValueError:
                        print("Error: String values must be enclosed in quotation marks")
                        end_command()
        else:
            print("Invalid syntax. Use: variable name = value")
    except Exception as e:
        print(f"Error: {e}")
        main()
    end_command()

def wait_command(args):
    try:
        if len(args) <= 1:
            return
        if len(args) > 1 and '.' in args[1]:
            time.sleep(float(args[1]))
        elif len(args) > 1 and args[1].isdigit():
            time.sleep(int(args[1]))
        elif args[1] in variables:
            try:
                time.sleep(variables[args[1]])
            except:
                print("Variable not found")
        else:
            print("Invalid argument")
    except Exception as e:
        print(f"Error: {e}")
        main()
    end_command()

def if_command(args):
    try:
        if len(args) < 4:
            print("Invalid if statement syntax")
            return

        var_name = args[1]
        comparison = args[2]
        value = args[3]
        
        if '{' not in args or '}' not in args:
            print("Missing braces in if statement")
            return

        start_idx = args.index('{')
        brace_count = 0
        end_idx = start_idx

        for i in range(start_idx, len(args)):
            if args[i] == '{':
                brace_count += 1
            elif args[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        try:
            var_value = variables[var_name]
        except KeyError:
            print(f"Variable {var_name} not found")
            return

        try:
            compare_value = float(value)
            if compare_value.is_integer():
                compare_value = int(compare_value)
        except ValueError:
            if value in variables:
                compare_value = variables[value]
            else:
                compare_value = value

        if comparison == "=" and var_value == compare_value:
            commands_to_run = ' '.join(args[start_idx + 1:end_idx])
            for cmd in commands_to_run.split(';'):
                cmd = cmd.strip()
                if cmd:
                    handle_command(cmd.split(' '))
    except Exception as e:
        print(f"Error in if statement: {e}")
        main()
    
    if len(sys.argv) == 1:
        end_command()

def while_command(args):
    try:
        if len(args) < 4:
            print("Invalid while statement syntax")
            return

        var_name = args[1]
        comparison = args[2]
        value = args[3]
        
        if '{' not in args or '}' not in args:
            print("Missing braces in while statement")
            return

        start_idx = args.index('{')
        brace_count = 0
        end_idx = start_idx

        for i in range(start_idx, len(args)):
            if args[i] == '{':
                brace_count += 1
            elif args[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break

        while True:
            try:
                var_value = variables[var_name]
            except KeyError:
                print(f"Variable {var_name} not found")
                return

            try:
                compare_value = float(value)
                if compare_value.is_integer():
                    compare_value = int(compare_value)
            except ValueError:
                if value in variables:
                    compare_value = variables[value]
                else:
                    compare_value = value

            if comparison == "=" and var_value != compare_value:
                break
            elif comparison == ">" and not (var_value > compare_value):
                break
            elif comparison == "<" and not (var_value < compare_value):
                break
            elif comparison == ">=" and not (var_value >= compare_value):
                break
            elif comparison == "<=" and not (var_value <= compare_value):
                break
            elif comparison == "!=" and var_value == compare_value:
                break

            commands_to_run = ' '.join(args[start_idx + 1:end_idx])
            for cmd in commands_to_run.split(';'):
                cmd = cmd.strip()
                if cmd:
                    result = handle_command(cmd.split(' '))
                    if result == "exit":
                        return "exit"

    except Exception as e:
        print(f"Error in while statement: {e}")
        main()
    
    if len(sys.argv) == 1:
        end_command()

def for_command(args):
    if len(args) < 4 or args[2] != "in":
        print("Invalid syntax. Use: for variable in iterable[.keys|.values] {commands}")
        return

    loop_var = args[1]
    iterable_expr = args[3]
    command_block = " ".join(args[4:]).strip("{}").strip()

    parts = iterable_expr.split('.')
    iterable_name = parts[0]
    access_type = parts[1] if len(parts) > 1 else None

    if iterable_name not in variables:
        print(f"Undefined iterable: {iterable_name}")
        return

    iterable = variables[iterable_name]

    if isinstance(iterable, list):
        for item in iterable:
            if isinstance(item, str):
                item = item.strip('"')
            variables[loop_var] = item
            execute_command_block(command_block)

    elif isinstance(iterable, dict):
        if access_type == "values":
            for value in iterable.values():
                if isinstance(value, str):
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                variables[loop_var] = value
                execute_command_block(command_block)
        else:
            for key in iterable.keys():
                if isinstance(key, str):
                    key = key.strip('"')
                variables[loop_var] = key
                execute_command_block(command_block)

    else:
        print(f"Cannot iterate over {iterable_name}. Only lists and dictionaries are supported.")
        return

    end_command()

def make_dict_command(args):
    try:
        if len(args) < 2:
            print("Invalid syntax. Use: makedict dict_name")
            return
        variables[args[1]] = {}
    except Exception as e:
        print(f"Error: {e}")
    end_command()

def dict_command(args):
    try:
        if len(args) < 3:
            print("Invalid syntax. Use: dict dict_name action [key] [value]")
            return

        dict_name = args[1]
        action = args[2]

        if dict_name not in variables or not isinstance(variables[dict_name], dict):
            print(f"{dict_name} is not a dictionary")
            return

        if action == "get":
            if len(args) < 4:
                print("Invalid syntax. Use: dict dict_name get key")
                return
            key = args[3]
            return variables[dict_name].get(key, f"Key '{key}' not found")
        
        elif action == "set":
            if len(args) < 5:
                print("Invalid syntax. Use: dict dict_name set key value")
                return
            key = args[3]
            value = " ".join(args[4:])
            if value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            elif value in variables:
                value = variables[value]
            variables[dict_name][key] = value
        
        elif action == "del":
            if len(args) < 4:
                print("Invalid syntax. Use: dict dict_name del key")
                return
            key = args[3]
            if key in variables[dict_name]:
                del variables[dict_name][key]
            else:
                print(f"Key '{key}' not found")
        
        elif action == "keys":
            return list(variables[dict_name].keys())
        
        elif action == "values":
            return list(variables[dict_name].values())
        
        elif action == "items":
            return list(variables[dict_name].items())
        
        else:
            print(f"Unknown dictionary action: {action}")
    except Exception as e:
        print(f"Error: {e}")
    end_command()

def execute_command(command, args):
    if command in commands:
        return commands[command](args)
    else:
        print(f"Unknown command: {command}")

def assign_command(args):
    if len(args) < 4 or args[2] != "=":
        print("Invalid syntax. Use: variable var_name = value")
        return

    var_name = args[1]
    value_expression = " ".join(args[3:])

    if value_expression.split()[0] in commands:
        command_args = value_expression.split()
        command_name = command_args[0]
        result = execute_command(command_name, command_args)
        if result is not None:
            variables[var_name] = result
    else:
        if value_expression.isdigit():
            value = int(value_expression)
        elif value_expression.replace('.', '', 1).isdigit():
            value = float(value_expression)
        elif value_expression in variables:
            value = variables[value_expression]
        else:
            value = value_expression
        variables[var_name] = value
    end_command()

def execute_command_block(command_block):
    commands_in_block = command_block.split(";")
    for command in commands_in_block:
        command = command.strip()
        if command:
            args = command.split()
            command_name = args[0]
            if command_name in commands:
                commands[command_name](args)
            else:
                print(f"Unknown command: {command_name}")

def execute_command(args):
    cmd = ' '.join(args[1:])
    try:
        os.system(cmd)
    except Exception as e:
        print(f"Error: {e}")
    end_command()

def random_number(args):
    try:
        if len(args) < 3:
            print("Invalid syntax. Use: random min max")
            return
        min_val = int(args[1])
        max_val = int(args[2])
        result = random.randint(min_val, max_val)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    end_command()

def exit_command(_):
    if len(sys.argv) == 1:
        quit()
    return "exit"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

commands = {
    "help": help_message,
    "clear": clear_screen,
    "parrot": parrot_command,
    "math": math_command,
    "variable": set_variable_command,
    "wait": wait_command,
    "if": if_command,
    "while": while_command,
    "for": for_command,
    "exit": exit_command,
    "makedict": make_dict_command,
    "dict": dict_command,
    "run": execute_command,
    "random": random_number,
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def init():
    cls()

    # Set window title
    if os.name == 'nt':  # Windows
        os.system('title Solstice')

    if len(os.sys.argv) > 1:
        try:
            with open(os.sys.argv[1], 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('~'):
                        args = line.split()
                        handle_command(args)
        except FileNotFoundError:
            print(f"File {os.sys.argv[1]} not found")
        except Exception as e:
            print(f"Error reading file: {e}")

    else:
        print("Solstice v0.1")
        n()
        main()

def main():
    command = input(">>> ")
    args = command.split(" ")
    handle_command(args)

def handle_command(args):
    if not args[0]:
        return main()
    if args[0] in commands:
        return commands[args[0]](args)
    else:
        print("Command not found")
        return main()

init()
