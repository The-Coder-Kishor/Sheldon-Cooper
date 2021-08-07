# Chemistry equation balancer
# By Adin Ackerman
# https://github.com/AdinAck

import sys
import numpy as np
from sympy import Matrix, fraction

def printMsg(msg):
    print("\n/////////////////////////\n")
    print(msg)
    print("\n/////////////////////////")

def solve(eq):
    exclude = [str(i) for i in range(10)]+[")", "+", "=", ">", " "]
    n = list(range(1, len(eq)))

    for i in n:
        char = eq[i]
        if char not in exclude:
            if char == char.upper():
                if eq[i-1] not in "( ":
                    eq = eq[:i] + " " + eq[i:]
                    n += [len(eq)-1]

    for char in eq:
        if not ((char.isdigit() or char.isalpha()) or char in "() +=>"):
            return(f"[{eq}]:\nEquation is not formatted correctly:\nIllegal characters ({char}).")
            exit()

    components = [i.split(" + ") for i in eq.split(' => ')]
    componentsOriginal = [i.split(" + ") for i in eq.split(' => ')]

    componentsDict = [[],[]]
    for i in [0,1]:
        for _ in range(len(components[i])):
            componentsDict[i].append({})

    alphabet = list(
        dict.fromkeys([
            i for i in "".join([
                i for i in eq if i not in "()+=>" and not i.isdigit()
            ]).split(" ") if i != ""
        ])
    )

    for i in range(len(components)):
        for j in range(len(components[i])):
            for k in alphabet:
                if k in components[i][j]:
                    componentsDict[i][j][k] = 0

    for i in range(len(components)):
        for j in range(len(components[i])):
            start, end = -1,-1
            for k in range(len(components[i][j])):
                if components[i][j][k] == "(":
                    start = k+1
                elif components[i][j][k] == ")":
                    end = k
                    for l in range(end+1,len(components[i][j])):
                        if components[i][j][l] == " ":
                            break
                        else:
                            val = int(components[i][j][end+1:l+1])
                            valEnd = l+1
                    for l in components[i][j][start:end].split(" "):
                        num = "".join([i for i in l if i.isdigit()])
                        if num == "":
                            num = 1
                        else:
                            num = int(num)
                        componentsDict[i][j]["".join([i for i in l if not i.isdigit()])] += num*val
                    components[i][j] = components[i][j][:start-1]+" "*(valEnd-start+1)+components[i][j][valEnd:]

    for i in range(len(components)):
        for j in range(len(components[i])):
            for k in components[i][j].split(" "):
                if k != "":
                    e = "".join([char for char in k if not char.isdigit()])
                    num = "".join([char for char in k if char.isdigit()])
                    if num == "":
                        num = 1
                    else:
                        num = int(num)
                    try:
                        componentsDict[i][j][e] += num
                    except KeyError:
                        return(f"[{eq}]:\nEquation is not formatted correctly:\nContains coefficients.")
                        exit()

    matrix = np.zeros((len(alphabet),len(components[0])+len(components[1])))

    lut = {}
    for i in range(len(alphabet)-1,-1,-1):
        lut[alphabet[i]] = i

    for i in range(len(componentsDict)):
        for j in range(len(componentsDict[i])):
            for e,v in componentsDict[i][j].items():
                # print(i,j,e,v)
                matrix[lut[e],j+i*len(componentsDict[0])] = v

    m1 = matrix[:,:len(componentsDict[0])]
    m2 = matrix[:,len(componentsDict[0]):]
    m2 = -m2

    matrix = np.concatenate((m1,m2), axis=1)

    try:
        ns = [i[0] for i in np.array(Matrix([[int(j) for j in list(i)] for i in matrix]).nullspace())[0]]
    except IndexError:
        return(f"[{eq}]:\nFailed to balance equation:\nNo solution exists.")
        exit()

    coeffs = ns
    while True:
        fracts = [i[1] for i in [fraction(j) for j in coeffs] if i[1] != 1]
        if len(fracts) == 0:
            denominator = 1
            break
        else:
            denominator = max(fracts)
        coeffs = [j * denominator for j in coeffs]
    if 0 in coeffs:
        return(f"[{eq}]:\nFailed to balance equation:\nNo solution exists.")
        exit()
    ca = coeffs[:len(componentsDict[0])],coeffs[len(componentsDict[0]):]

    result = " => ".join([
        " + ".join([
            f'{k}{j.replace(" ", "")}' if k != 1 else j.replace(" ", "") for j,k in zip(i, ca[n])
        ]) for i,n in zip(componentsOriginal, [0,1])
    ])
    return(f"Coeffs: {coeffs}\nEquation: " + result)