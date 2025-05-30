import re

# Options:
# - echo.star
# - multiply.star
# - repeater.star
# - reverse.star
# - hello_world.star
file = open("reverse.star", "r")

sample_code = file.read()

file.close()

objects = {}

def is_a_string(data):
    return re.match(r'".*"', data)

def is_a_number(data):
    return re.match(r'^\d+$', data)

def is_add(data):
    return re.match(r'[a-zA-Z() ,]*\s\+\s[a-zA-Z() ,]*', data) is not None

def is_a_multiplication(data):
    result = re.match(r'^[a-zA-Z0-9]* \* [a-zA-Z0-9]*$', data)
    return result is not None

def is_a_comment(data):
    return data.startswith("#")

def is_scan_range(data):
    return data.startswith("scan_range(")

def is_line_readout(data):
    return data.startswith("readout(")

def is_line_lightsaber(data):
    return re.match(r'^lightsaber\(.[^\)]*\)$', data) is not None

split_lines = sample_code.split("\n")
pc = 0

def parse(line):
    global pc
    if isinstance(line, int):
        return line
    line = line.strip()
    if is_a_number(line):
        return int(line)
    if is_a_comment(line):
        return
    if is_a_string(line):
        return line[1:-1]
    elif line == "incoming_comm()":
        return input(">")
    elif is_line_readout(line):
        return len(parse(line[8:-1]))
    elif is_line_lightsaber(line):
        arguments = line[11:-1].split(",")
        return parse(arguments[0])[parse(arguments[1]):parse(arguments[2])]
    elif line in objects:
        return objects[line]
    elif is_a_multiplication(line):
        return int(parse(line.split("*")[0].strip())) * int(parse(line.split("*")[1].strip()))
    elif is_add(line):
        parts = line.split("+")
        datatoreturn = parse(parts[0].strip()) + parse(parts[1].strip())
        return datatoreturn
    elif is_scan_range(line):
        return range(int(parse(line[11:-1])))
    elif line.find("transmit(") != -1:
        transmit_position = line.find("transmit(")
        argument = line[transmit_position+9:line.find(")")]
        data_to_print = parse(argument)
        print(data_to_print)
        return
    elif line.find("datapad") != -1:
        datapad_position = line.find("datapad")
        object_name = line[datapad_position+8:line.find("=")-1]
        object_value = parse(line[line.find("=")+1:line.find(";")])
        objects[object_name] = object_value
        return
    elif line.find("patrol") != -1:
        patrol_parts = line.split(" ") # [patrol, variable, within, range, {]
        if len(patrol_parts) != 5:
            print("ERROR, loop not set up correctly")
            exit(1)
        loop_instructions = []
        # find end of loop
        while split_lines[pc+1].find("}") == -1:
            pc += 1
            loop_instructions.append(split_lines[pc])

        loop_var = patrol_parts[1]
        range_var = patrol_parts[3]
        for i in parse(range_var):
            objects[loop_var] = i
            for instruction in loop_instructions:
                parse(instruction)
            
    return line

while pc < len(split_lines):
    parse(split_lines[pc])
    pc += 1
    