# Davi Chaves Pinheiro - 500187

def recursive_1(f, g):
    def h(x):
        if x==0:
            return f(x)
        return g(x-1, h(x-1))
    return h

def recursive_2(f, g):
    def h(x, y):
        if y==0:
            return f(x)
        return g(y-1, h(x, y-1), x)
    return h

def composition(f, g):
    def func(*x):
        return f(*[gi(*x) for gi in g])
    return func

# Funcao Zero
def n0(x) :
    return 0

def n1(x):
    return 1

# Funcao Sucessor
def s(x) :
    return x + 1
    
# Funcoes de Projecao
def u1_1(x) :
    return x

def u2_1(x1, x2) :
    return x1

def u2_2(x1, x2) :
    return x2

def u3_1(x1, x2, x3):
    return x1

def u3_2(x1, x2, x3):
    return x2

def u3_3(x1, x2, x3):
    return x3

comp_sum = composition(s, [u3_2])
sum = recursive_2(u1_1, comp_sum)
print(sum(3, 2))

comp_mul = composition(sum, [u3_2, u3_3])
mul = recursive_2(n0, comp_mul)
print(mul(2,8))

comp_fact = composition( mul, [composition(s, [u2_1]), u2_2])
fact = recursive_1(n1, comp_fact)
print(fact(4))

comp_power = composition(mul, [u3_2, u3_3])
power = recursive_2(n1, comp_power)
print(power(3,2))

pred = recursive_1(n0, u2_1)
print(pred(20))

comp_subt = composition(pred, [u3_2])
subt = recursive_2(u1_1, comp_subt)
print(subt(10, 5))

mod = composition(subt, [u2_2, u2_1])
print(mod(7, 10))

comp_alpha = composition(n0, [u2_1])
alpha = recursive_1(n1, comp_alpha)
print(alpha(10))

equal = composition(alpha, [mod])
print(equal(10, 10))

lessthan = composition(alpha, [subt])
print(lessthan(10, 5))

 



