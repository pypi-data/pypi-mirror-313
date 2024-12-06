import re
import pymlogic.instructions as instructions

def parse(code: str) -> list[instructions.Instruction]:
    lines = re.findall(r"\s*(?:(?:#.*?)|([^;\n]+?)\s*(?:#.*)?)(?:\n|;|$)", code)
    insts = []
    labels = {}
    for line in lines:
        if line[-1] == ':':
            labels[line[:-1]] = len(insts)
        else:
            insts.append(re.findall(r'".*?"|\S+', line))
            
    instruction_list = []
    for inst in insts:
        if inst[0] in instructions.INSTRUCTION_LOOKUP:
            instruction_list.append(instructions.INSTRUCTION_LOOKUP[inst[0]].new(inst[1:], labels=labels))
        else:
            instruction_list.append(instructions.I_Noop())
    return instruction_list

def get_label(value, labels):
    if re.match(r"[0-9]+", value):
        return int(value)
    elif value in labels:
        return labels[value]
    else:
        return -1