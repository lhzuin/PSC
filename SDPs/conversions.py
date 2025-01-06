from typing import List, Tuple


def base_proba_2_base_correlateur_old(input: List[float]) -> List:
    assert (len(input)==8)
    # The order follows: [p11_11, p11_12, p11_21, p11_22, p1_X1, p_1_X2, p1_Y1, p1_Y2]
    output = []
    for x in range(1,3):
        for y in range(1,3):
            p11_xy = input[2*x+y-3]
            p1_x = input[3+x]
            p1_y = input[5+y]
            output.append(4*p11_xy - 2*p1_x - 2*p1_y + 1)
    
    for x in range(1,3):
        p1_x = input[3+x]
        output.append(1-2*p1_x)
    for y in range(1,3):
        p1_y = input[5+y]
        output.append(1-2*p1_y)

    # Returns in the following order: [A1B1, A1B2, A2B1, A2B2, A1, A2, B1, B2]

    return output

def base_correlateur_2_base_proba(input: List[float]) -> Tuple[List, int]:
    assert (len(input)==8)
    # The order follows: [p11_11, p11_12, p11_21, p11_22, p1_X1, p_1_X2, p1_Y1, p1_Y2]
    output = [0]*8
    constant = 0
    i = 0
    for x in range(1,3):
        for y in range(1,3):
            constant += input[i]
            output[2*x+y-3] += 4*input[i]
            output[3+x] -= 2*input[i]
            output[5+y] -= 2*input[i]
            i += 1
    
    for x in range(1,3):
        constant += input[i]
        output[3+x] -= 2*input[i]
        i += 1
    for y in range(1,3):
        output[5+y] -= 2*input[i]
        constant += input[i]
        i += 1

    # Returns in the following order: [A1B1, A1B2, A2B1, A2B2, A1, A2, B1, B2]

    return (output, constant)

def base_correlateur_2_base_proba2(input: List[float]) -> List:
    # The order follows: [A1B1, A1B2, A2B1, A2B2, A1, A2, B1, B2]
    assert (len(input)==8)

    output = []
    for x in range(1,3):
        for y in range(1,3):
            AxBy = input[2*x+y-3]
            Ax = input[3+x]
            By = input[5+y]
            output.append((AxBy - Ax - By + 1)/4)
    
    for x in range(1,3):
        Ax = input[3+x]
        output.append((1-Ax)/2)
    for y in range(1,3):
        By = input[5+y]
        output.append((1-By)/2)
    

    # Returns in the following order: [p11_11, p11_12, p11_21, p11_22, p1_X1, p_1_X2, p1_Y1, p1_Y2]

    return output


print(base_correlateur_2_base_proba([1,1,1,-1, 0, 0, 0, 0]))

#print(base_proba_2_base_correlateur([1,2,3,4, 5, 6, 7, 8]))

#print(base_proba_2_base_correlateur(base_correlateur_2_base_proba([1,2,3,4, 5, 6, 7, 8])))

#print(base_correlateur_2_base_proba(base_proba_2_base_correlateur([1,2,3,4, 5, 6, 7, 8])))
