#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import sys

# Exemplo de programa (programa (c) da pagina 20 com a macro GOTO expandida)
program = """
[A2]    S1 = S1 - 1
        if (S1 != 0): GOTO A2
        
[A]     if (S2 != 0): GOTO B

        K = K + 1
        if (K != 0): GOTO C
        
[B]     S2 = S2 - 1
        S1 = S1 + 1
        K1 = K1 + 1
        
        K = K + 1
        if (K != 0): GOTO A
        
[C]     if (K1 != 0): GOTO D

        K = K + 1
        if (K != 0): GOTO E
        
[D]     K1 = K1 - 1
        S2 = S2 + 1
        
        K = K + 1
        if (K != 0): GOTO C
[E]
"""

DLABEL = "\s*(?:\[(\w+)\])?\s*"
GOTO = "\s*GOTO\s*(\w+)\s*"
VAR = "\s*([a-zA-Z]+(?:\w*#*)*)\s*"
LABEL = "\s*([a-zA-Z]\d*)\s*"

eip = 3
counter = 0
labels = {}
varss = {
    'S1': 5,    
    'S2': 10,    
}


if __name__ == "__main__":
    print("[i]: Starting program...")

    # ------- Parser -------#
    program = program.split("\n")
    
    peip = 0
    while(peip < len(program)):
        ###
        ### Expanssão macro
        ###
        line = program[peip]
        
        # Search for a match
        match = re.match(f"\s*(?:\[(\w+)\])?\s*", line)
        (label,) = match.groups()
        
        if (label and label not in labels):
            labels[label] = peip
       
        peip += 1
    
    # Print program
    for i, line in enumerate(program):
        print(f"{i}\t{line}")
    
    # ------- Interpreter -------#
    while(eip < len(program)):
        line = program[eip]
        
        l = line.replace('\n', '')
        print(f"({eip})\t{varss}  -->", end="")
        
        # Search for a match
        match = False
        
        # X = X + 1 | X = X - 1
        match = re.match(f"{DLABEL}{VAR}={VAR}\s*(\+|\-)\s*1\s*$", line)
        if match:
            (_, v, _, op) = match.groups()
            if (v not in varss):
                varss[v] = 0
            if (op == '+'):
                varss[v] += 1
            elif (op == '-'):
                if(varss[v] > 0):
                    varss[v] -= 1
            
        # if (X != 0): GOTO A
        match = re.match(f"{DLABEL}if\s*\({VAR}!=\s*0\s*\):\s*GOTO\s*{LABEL}\s*$", line)
        if match:
            (_, v, label) = match.groups()
            if varss.get(v, 0) != 0:
                if label not in labels:
                    break
                eip = labels[label]
                print(f"  {varss}")
                continue
        print(f"  {varss}")
        eip += 1
    
    print(varss)
    print("[i]: Ending program...")


    