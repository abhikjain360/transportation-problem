import numpy as np

def vogel_approximation(table):
    


def main():
    # getting input from user
    print('Enter the number of warehouses : ', end='')
    n = int(input())
    print('Enter the number of markets : ', end = '')
    m = int(input())
    
    # getting the costs as input
    print('Enter the costs as', str(n)+'X'+str(m), 'matrix :')
    table = np.array([list(map(int,input().split())) for i in range(n)])
    
    # performing vogel's approximation for initial basic feasible solution
    
if __name__ == '__main__':
    main()