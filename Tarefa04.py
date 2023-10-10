
#!/usr/bin/python
# -*- coding: latin-1 -*-

from unittest import skip
import sympy as sp
import re
import sys

# Exemplo de programa (programa (c) da pagina 20 com a macro GOTO expandida)
program = """
        Y = X1
[A]     if (X2 = 0): GOTO E
        Y = Y + 1
        Y = Y + 1
        X2 = X2 - 1
        GOTO A
"""

eip = 0
counter = 0
labels = {}
varss = {}

def parity(x: int, y: int) -> int: 
    return (2 ** x) * (2 * y + 1) - 1 

def l(z: int) -> int:
    for x in range(z + 1):
        for y in range (z + 1):
            if(parity(x, y) == z):
                return x
    raise Exception('?????')

def r(z: int) -> int:
    for y in range(z + 1):
        for x in range (z + 1):
            if(parity(x, y) == z):
                return y
    raise Exception('?????')

def arrayToGodelNumber(arr: list[int]) -> int:
    total = 1
    for i, n in enumerate(arr):
        total *= sp.prime(i + 1) ** n
    return total

def godelNumberToArray(n: int):
    pass

# Dado um número de Godel z e um index t, retorna o inésimo elemento
def godelIndex(z: int, t: int) -> int:
    for i in range(z + 1):
        if(z % (sp.prime(t + 1) ** (i + 1)) != 0):
            return i
    

def godelLen(z: int) -> int:
    for i in range(z + 1):
        if(godelIndex(z, i) != 0):
            isZero = True
            j = i + 1
            while True:
                if(godelIndex(z, j) != 0):
                    isZero = False
                    break
                j += 1
            
            if(isZero):
                return i
    raise Exception('?????')

def printGodelNumber(n: int):
    print("[", end="")
    for i in range(godelLen(n) + 1):
        print(f"{godelIndex(n, i)},", end="")
    print("]")


# Codifica uma variavel
def v(n: int) -> int:
   pass
    
def codeToGodelNumber(code: str) -> str:
    program = []
    
    code = code.split("\n")
    # [L]   X1 = X1 + 1
    #       X2 = X2 - 1
    #       Z1 = Z1 + 1
    # [L]   if(X1 != 0): GOTO L
    # [L]   if(X2 != 0): GOTO E
    # [E]   V = V
    # [L]   Y = Y + 1
    pass


eip = 0
varss = {
    'X1': 2,
    'X2': 3,
}
if __name__ == "__main__":
    print("[i]: Starting program...")
    print(f"{parity(0, 0)}")
    z = arrayToGodelNumber([3, 0, 5, 4, 6])
    print(f"{z}")
    printGodelNumber(z)
    print("[i]: Ending program...")


    


 