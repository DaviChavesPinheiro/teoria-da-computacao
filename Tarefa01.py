#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import sys

# Exemplo de programa (programa (c) da pagina 20 com a macro GOTO expandida)
program = """
        X = X + 1
        X = X + 1
        X = X + 1
        X = X + 1
        Y = X
        X = X + 1
        Z = X * Y
"""

DLABEL = "\s*(?:\[(\w+)\])?\s*"
GOTO = "\s*GOTO\s*(\w+)\s*"
VAR = "\s*([a-zA-Z]+(?:\w*#*)*)\s*"
LABEL = "\s*([a-zA-Z]\d*)\s*"

macros = [
    {
        "pattern": "^\s*$", # \n
    },
    {
        "pattern": f"\s*{DLABEL}\s*$", # [A] \n
    },
    {
        "pattern": f"{DLABEL}if\s*\({VAR}!=\s*0\s*\):\s*GOTO\s*{LABEL}\s*$", # [A] if (x != 0): GOTO A
    },
    {
        "pattern": f"{DLABEL}\s*GOTO\s*{LABEL}\s*$", # GOTO A
        "expanded": """
        K = K + 1
        if (K != 0): GOTO S1
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\s*$", # [A] S1 = S2
        "expanded": """
        S1 = 0
[A]     if (S2 != 0): GOTO B
        GOTO C
[B]     S2 = S2 - 1
        S1 = S1 + 1
        K1 = K1 + 1
        GOTO A
[C]     if (K1 != 0): GOTO D
        GOTO E
[D]     K1 = K1 - 1
        S2 = S2 + 1
        GOTO C
[E]
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\+{VAR}$", # [A] S1 = S2 + S3
        "expanded": """
        K1 = S1
        K2 = S2
        K3 = S3
        
        K1 = K3
[A]     if (K2 != 0): GOTO B
        GOTO C
[B]     K2 = K2 - 1
        K1 = K1 + 1
        K4 = K4 + 1
        GOTO A
[C]     if (K4 != 0): GOTO D
        GOTO E
[D]     K4 = K4 - 1
        K2 = K2 + 1
        GOTO C
[E]     S1 = K1
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\*{VAR}$", # [A] S1 = S2 + S3
        "expanded": """
        K2 = S2
        K3 = S3
        
[A]     if (K2 != 0): GOTO B
        GOTO C
[B]     K2 = K2 - 1
        K1 = K1 + K3
        GOTO A
[C]     S1 = K1
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\s*\+\s*1\s*$", # [A] S1 = S1 + 1
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\s*\-\s*1\s*$", # [A] S1 = S1 - 1
    },
    {
        "pattern": f"{DLABEL}{VAR}=\s*0\s*$", # S1 = 0
        "expanded": """
[A]     S1 = S1 - 1
        if (S1 != 0): GOTO A
        """
    }
]

eip = 0
counter = 0
labels = {}
varss = {}


if __name__ == "__main__":
    print("[i]: Starting program...")

    # ------- Parser -------#
    program = program.split("\n")
    
    eip = 0
    while(eip < len(program)):
        ###
        ### Expanssão macro
        ###
        line = program[eip]
        
        # Search for a match
        match = False
        for macro in macros:
            match = re.match(macro["pattern"], line)
            if (match):
                # Match found
                match = {**macro, **{"captures": match.groups()}} ## Retrieve the captures inside the match
                break
        # Match not found
        if (not match):
            sys.exit(f"[!]: Macro not found: {line} (at line {eip})")

        # Save labels if exist
        captures = list(match["captures"])
        if (match["captures"]):
            label = captures[0]
            if (label and label not in labels):
                labels[label] = eip
        
        
        # Macro expansion
        if ("expanded" in match):
            #
            # Make labels and local vars unique
            # 

            # Make labels unique
            mlabel = False
            mlabel = re.findall("\s*(?:\[(\w+)\])?\s*", match["expanded"])
            for ml in mlabel:
                if(not ml):
                    continue
                match["expanded"] = match["expanded"].replace(ml, f"{ml}{counter}")
                counter += 1
            # Make local vars unique
            mvars = False
            mvars = re.findall("K\d*", match["expanded"])
            mvars = list(set(mvars))
            for mv in mvars:
                if(not mv):
                    continue
                match["expanded"] = match["expanded"].replace(mv, f"{mv}#{counter}")
                counter += 1

            # Vars substituition
            captures = list(match["captures"]) # TODO: Verificar se captures não é vazio
            label = captures[0]

            # Iterate S1 S2 S3... and replace by C1 C2 C3
            for k in range(1, len(captures)):
                match["expanded"] = match["expanded"].replace(f"S{k}", captures[k])
                counter += 1
            # Macro replace
            match["expanded"] = match["expanded"].split("\n")
            
            #TODO: Verificar se não existe uma label na mesma linha do macro com expansão
            program[eip] = match["expanded"][0] # Replace macro with the first line of expanded
            for offset, mline in enumerate(match["expanded"], 1):
                program.insert(eip + offset, mline)
        eip += 1
    
    # Print program
    for i, line in enumerate(program):
        print(f"{i}\t{line}")
    
    # ------- Interpreter -------#
    eip = 0
    while(eip < len(program)):
        line = program[eip]
        
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
                continue
        eip += 1
    print(varss)
    print("[i]: Ending program...")


    