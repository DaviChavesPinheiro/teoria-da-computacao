# teoria-da-computacao
Repositorio para as tarefas da cadeira de Teoria da Computação

# Tarefa 01
## Questões 1 - 3

```
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
```
## Questão 4
```
eip = 3
counter = 0
labels = {}
varss = {
    'S1': 5,    
    'S2': 10,    
}
```

# Tarefa 02
## Questão 1
```
eip = 0
counter = 0
labels = {}
varss = {
    "X1": 10,
    "X2": 4,
    "X3": 42,
}
```
## Questões 2 e 3
```
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
```

