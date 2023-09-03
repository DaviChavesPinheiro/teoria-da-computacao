#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import sys

# Exemplo de programa (programa (c) da pagina 20 com a macro GOTO expandida)
program = """
        X = X + 1
        Y = Y + 1
        Z = Z + 1
        
        if (Z = X): GOTO E
        Y = Y + 1
[E]      
        
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
        "pattern": f"{DLABEL}if\s*\({VAR}!=\s*0\s*\):\s*GOTO\s*{LABEL}\s*$", # [S0] if (S1 != 0): GOTO S2
    },
    {
        "pattern": f"{DLABEL}if\s*\({VAR}=\s*0\s*\):\s*GOTO\s*{LABEL}\s*$", #  [S0] if (S1 = 0): GOTO S2
        "expanded": """
        if (S1 != 0): GOTO E
        GOTO S2
[E]
        """
    },
    {
        "pattern": f"{DLABEL}if\s*\({VAR}=\s*{VAR}\s*\):\s*GOTO\s*{LABEL}\s*$", #  [S0] if (S1 = S2): GOTO S3
        "expanded": """
        K0 = 0
        K1 = S1
        K2 = S2
        
        K0 = K1 == K2
        if (K0 != 0): GOTO S3
        """
    },
    {
        "pattern": f"{DLABEL}\s*GOTO\s*{LABEL}\s*$", # GOTO A
        "expanded": """
        K1 = K1 + 1
        if (K1 != 0): GOTO S1
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\s*$", # [A] S1 = S2
        "expanded": """
        S1 = 0
        K1 = 0
[A]     
        if (S2 = 0): GOTO B
        S2 = S2 - 1
        S1 = S1 + 1
        K1 = K1 + 1
        GOTO A
[B]     
        if (K1 = 0): GOTO E
        K1 = K1 - 1
        S2 = S2 + 1
        GOTO B
[E]
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\+{VAR}$", # [A] S1 = S2 + S3
        "expanded": """
        K0 = 0
        K1 = S1
        K2 = S2
        K3 = S3
        
        K0 = K3
[A]     
        if (K2 = 0): GOTO E
        K2 = K2 - 1
        K0 = K0 + 1
        GOTO A
[E]     
        S1 = K0
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\=\={VAR}$", # [A] S1 = S2 == S3
        "expanded": """
        K0 = 0
        K1 = S1
        K2 = S2
        K3 = S3
[A]     
        if (K2 = 0): GOTO B
        if (K3 = 0): GOTO E
        K2 = K2 - 1
        K3 = K3 - 1
        GOTO A
[B]     
        if (K3 = 0): GOTO E1
        GOTO E
[E1]     
        K0 = K0 + 1
[E]     
        S1 = K0
        """
    },
    {
        "pattern": f"{DLABEL}{VAR}={VAR}\*{VAR}$", # [A] S1 = S2 * S3
        "expanded": """
        K0 = 0
        K1 = S1
        K2 = S2
        K3 = S3
[A]     
        if (K2 = 0): GOTO E
        K2 = K2 - 1
        K0 = K0 + K3
        GOTO A
[E]     
        S1 = K0
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
    
    peip = 0
    while(peip < len(program)):
        ###
        ### Expanss�o macro
        ###
        line = program[peip]
        
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
            sys.exit(f"[!]: Macro not found: {line} (at line {peip})")

        # Save label if exist
        captures = list(match["captures"])
        if (match["captures"]):
            label = captures[0]
            if (label and label not in labels):
                labels[label] = peip
        
        
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
            captures = list(match["captures"]) # TODO: Verificar se captures n�o � vazio
            label = captures[0]

            # Iterate S1 S2 S3... and replace by C1 C2 C3
            for k in range(1, len(captures)):
                match["expanded"] = match["expanded"].replace(f"S{k}", captures[k])
                counter += 1
            # Macro replace
            match["expanded"] = match["expanded"].split("\n")
            
            #TODO: Verificar se n�o existe uma label na mesma linha do macro com expans�o
            program[peip] = match["expanded"][0] # Replace macro with the first line of expanded
            for offset, mline in enumerate(match["expanded"], 1):
                program.insert(peip + offset, mline)
        peip += 1
    
    # Print program
    for i, line in enumerate(program):
        print(f"{i}\t{line}")
    
    # ------- Interpreter -------#
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


    