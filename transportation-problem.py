import numpy as np


# method to return the row/column for vogel's approximation
def max_penalty_index(table, n, m):
    row_penalties, col_penalties = np.array([0] * n), np.array([0] * m)

    # calculating penalties for rows
    for i in range(n):
        row = np.sort(table[i])
        row_penalties[i] = row[1] - row[0]
    table = table.transpose()

    # calculating penalties for columns
    for i in range(m):
        col = np.sort(table[i])
        col_penalties[i] = col[1] - col[0]

    # return the row/column with greatest penalty
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

    # keeping track of basic variables
    basics = [[-1, -1]] * (n+m-1)
    basics = np.array(basics)
    basics_counter = 0

    cost_replacement = np.amax(cost) + 1

    # applying till all supplies are transported, as problem is balanced
    while basics_counter < n+m-1:

        # getting the penalties
        t = max_penalty_index(cost, n, m)

        # if one of the rows has greatest penalty
        # meaning t[1] will correspond to a row index
        if t[0] == 0:
            least_cost_col_index = np.argmin(cost[t[1]])

            # if supply > demand
            if supply[t[1]] > demand[least_cost_col_index]:
                X[t[1], least_cost_col_index] = demand[least_cost_col_index]

                supply[t[1]] -= demand[least_cost_col_index]
                demand[least_cost_col_index] = 0

                cost[:, least_cost_col_index] = cost_replacement
            
            # if supply == demand are equal at that point
            elif supply[t[1]] == demand[least_cost_col_index]:
                X[t[1], least_cost_col_index] = demand[least_cost_col_index]

                supply[t[1]] = 0
                demand[least_cost_col_index] = 0

                cost[t[1]] = cost_replacement
                cost[:, least_cost_col_index] = cost_replacement

            # if demand > supply
            else:
                X[t[1], least_cost_col_index] = supply[t[1]]

                demand[least_cost_col_index] -= supply[t[1]]
                supply[t[1]] = 0

                cost[t[1]] = cost_replacement

            basics[basics_counter] = [t[1], least_cost_col_index]

        # if one of the columns has the greatest penalties
        # meaning t[1] will correspond to a column index
        else:
            least_cost_row_index = np.argmin(cost[:,t[1]])

            # if demand > supply
            if demand[t[1]] > supply[least_cost_row_index]:
                X[least_cost_row_index, t[1]] = supply[least_cost_row_index]

                demand[t[1]] -= supply[least_cost_row_index]
                supply[least_cost_row_index] = 0

                cost[:,t[1]] = cost_replacement
            
            # if demand == supply
            elif demand[t[1]] == supply[least_cost_row_index]:
                X[least_cost_row_index, t[1]] = demand[t[1]]

                supply[least_cost_row_index] = 0
                demand[t[1]] = 0
                
                cost[:,t[1]] = cost_replacement
                cost[least_cost_row_index] = cost_replacement

            # if demand < supply
            else:
                X[least_cost_row_index, t[1]] = demand[t[1]]
                
                supply[least_cost_row_index] -= demand[t[1]]
                demand[t[1]] = 0

                cost[t[1]] = cost_replacement
                cost[:, least_cost_row_index] = cost_replacement

            basics[basics_counter] = [least_cost_row_index, t[1]]
        
        basics_counter += 1

    return X, basics


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
    X, basics = vogel_approximation(cost, n, m, supply, demand)
    
if __name__ == '__main__':
    main()