import numpy as np


# method to return the row/column for vogel's approximation
def vogel_penalties(cost, n, m):
    row_penalties, col_penalties = np.array([0] * n), np.array([0] * m)

    # getting penalties for rows
    for i in range(n):
        row = np.sort(cost[i])
        row_penalties[i] = row[-1] - row[-2]
    cost = cost.transpose()

    # getting penalties for columns
    for i in range(m):
        col = np.sort(cost[i])
        col_penalties[i] = col[-1] - col[-2]
    
    row_max = np.argmax(row_penalties)
    col_max = np.argmax(col_penalties)

    if row_penalties[row_max] > col_penalties[col_max]:
        return (0, row_max)
    else:
        return (1, col_max)


# method to perform vogel's approximation
def vogel_approximation(cost, n, m, supply, demand):
    
    # X is storing values of x[i,j]
    X = np.zeros((n,m))

    cost_t = cost.transpose()

    # applying till all supplies are transported, as problem is balanced
    while sum(supply) > 0:

        # getting the penalties
        t = vogel_penalties(cost, n, m)

        # if one of the rows has greatest pernalty
        if t[0] == 0:
            least_cost_index = np.argmin(cost[t[1]])

            if supply[t[1]] > demand[least_cost_index]:
                X[t[1], least_cost_index] = demand[least_cost_index]

                supply[t[1]] -= demand[least_cost_index]
                demand = np.append(demand[:least_cost_index], demand[least_cost_index+1:], axis=0)
            
            elif supply[t[1]] == demand[least_cost_index]:
                X[t[1], least_cost_index] = demand[least_cost_index]

                supply[t[1]] = 0
                demand = np.append(demand[:least_cost_index], demand[least_cost_index+1:], axis=0)

            else:
                X[t[1], least_cost_index] = supply[t[1]]

                demand[least_cost_index] -= supply[t[1]]
                supply = np.append(supply[:t[1]], supply[t[1]+1:], axis=0)

        # if one of the columns has the greatest penalties
        else:
            least_cost_index = np.argmin(cost_t[t[1]])
            if demand[t[1]] > supply[least_cost_index]:
                X[least_cost_index, t[1]] = supply[least_cost_index]

                demand[t[1]] -= supply[least_cost_index]
                supply = np.append(supply[:least_cost_index], supply[least_cost_index+1:], axis=0)
            
            elif demand[t[1]] == supply[least_cost_index]:
                X[least_cost_index, t[1]] = demand[least_cost_index]

                supply = np.append(supply[:least_cost_index], supply[least_cost_index+1:], axis=0)
                demand = np.append(demand[:t[1]], demand[t[1]+1:], axis=0)

            else:
                X[least_cost_index, t[1]] = demand[t[1]]
                
                supply[least_cost_index] -= demand[t[1]]
                demand = np.append(demand[:t[1]], demand[t[1]+1:], axis=0)

    return X


def main():
    # getting input from user
    print('Only for balanced problems!!')
    print('Enter the number of warehouses : ', end='')
    n = int(input())
    print('Enter the number of markets : ', end = '')
    m = int(input())
    
    # getting demand and supply as input
    print('Enter the demands at marketplaces : ', end='')
    demand = np.array(list(map(int, input().split())))
    print('Enter the supplies at warehouses : ', end='')
    supply = np.array(list(map(int, input().split())))
    
    # getting the costs as input
    print('Enter the costs as', str(n)+'X'+str(m), 'matrix :')
    cost = np.array([list(map(int,input().split())) for i in range(n)])
    
    # performing vogel's approximation for initial basic feasible solution
    X = vogel_approximation(cost, n, m, supply, demand)
    
if __name__ == '__main__':
    main()