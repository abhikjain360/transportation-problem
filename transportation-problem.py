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


def vogel_approximation(cost, n, m, supply, demand):
    
    # X is storing values of x[i,j]
    X = np.zeros((n,m))

    # keeping track of basic variables
    basics = [[np.nan, np.nan]] * (n+m-1)
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

                cost[least_cost_row_index] = cost_replacement
            
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

                cost[:,t[1]] = cost_replacement

            basics[basics_counter] = [least_cost_row_index, t[1]]
        
        basics_counter += 1

    return X, basics


# North-west method for testing the UV method 
# (VAM almost always gives perfect solution, so can't test further)
def NWmethod(costs, n, m, supply, demand):
    X = np.zeros((n,m))
    basics = []
    x, y = 0, 0

    for i in range(m+n-1):
        basics.append([x,y])
        if supply[x] > demand[y]:
            X[x,y] = demand[y]
            supply[x] -= demand[y]
            demand[y] = 0
            y += 1
        elif demand[y] == supply[x]:
            X[x,y] = demand[y]
            demand[y] = 0
            supply[x] = 0
            x += 1
            y += 1
        else:
            X[x,y] = supply[x]
            demand[y] -= supply[x]
            supply[x] = 0
            x += 1
    
    basics = np.array(basics)
    return X, basics 


# function for loop for find U and V
# function for loop for find U and V
def checkUV(U, V):
    return any(np.isnan(U)) or any(np.isnan(V))


# functiond for UV method
def getProfits(X, basics, cost, n, m):
    U = np.array([np.nan] * n)
    V = np.array([np.nan] * m)

    # setting U_1 to 0 to find rest all
    U[int(basics[0,0])] = 0
    
    # iteratively going over entire U and V to
    # use the one that have solution to sole the rest
    while checkUV(U, V):

        # checking U and V values which are filled
        for i1,j1 in basics:
            i,j = int(i1), int(j1)
            if np.isnan(U[i]) and not np.isnan(V[j]):
                U[i] = cost[i,j] - V[j]
                
            elif np.isnan(V[j]) and not np.isnan(U[i]):
                V[j] = cost[i,j] - U[i]

    profits = np.zeros((n,m))

    for i in range(n):
        for j in range(m):
            profits[i,j] = cost[i,j] - U[i] - V[j]

    return profits


# function to check optimal condition
def checkOptimalCondition(profits):
    for i in profits:
        for j in i:
            if j < 0:
                return True
    return False


# method to count occurences of a single element in 1D array
# because numpy doesn't have one
def getCount(arr, elem):
    count = 0
    for i in arr:
        if i == elem:
            count += 1
    return count

# method to find points that form the loop
def getLoopPoints(X, basics, r, c, n, m):
    X[r,c] = 1
    basics = np.append([r,c], basics, axis=0)

    while True:
        x = basics[:,0]
        y = basics[:,1]
        
    

# main method
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

    # getting profits for the first time
    profits = getProfits(X, basics, cost)

    # applying UV method iteratively
    while checkOptimalCondition(profits):
        t = np.argmin(profits)
        r,c = t//n, t%m
        X2 = getLoopPoints(X, basics, r, c, n, m)

        profits = getProfits(X, basics, cost)

    print(X)
    
if __name__ == '__main__':
    main()