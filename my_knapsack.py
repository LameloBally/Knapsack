import numpy as np
import pandas as pd
import csv
import timeit
import sys
from functools import lru_cache as cache
sys.setrecursionlimit(10000)

# 아이템의 번호와 weight, profit을 attribute로 가지는 클래스 
class Item:
    def __init__(self, item_ID, weight, profit):
        self.item_ID = item_ID
        self.weight = weight
        self.profit = profit

# knapsack class의 attribute로 capacity와 objective_value로 갖고 엑셀 파일을 읽어서 아이템의 정보를 담은 아이템 리스트를 Data에 담음
# inp
class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.objective_value = 0
        
        # List of item instance 
        self.data = [] 
        # Tableau of matrix based iterative
        self.tableau = np.array([])

    def temp(self): 
        return self.weight

    # csv.reader 함수로 엑셀파일을 읽은 후 각 행의 element를 item의 number, weight, profit으로 담는다  
    def read_data(self, input_file_path):
        # TODO : Implement the read_data (read csv file)
        f = open(input_file_path,'r',encoding='cp949')
        data = csv.reader(f)
        next(data)
        for row in data:
            self.data.append(Item(int(row[0]),int(row[1]),int(row[2])))
        f.close()
        self.tableau = np.zeros((len(self.data)+1,self.capacity+1)) # DP으로 문제를 해결하기 위해 solution을 저장해 놓을 2d arrary를 만든다.


     # (item의 수 + 1) * (capacity +1) Matrix self.tableau를 만들고 n*m matirx라고 하면
     #  m만큼의 capacity가 남았을때, n개의 아이템으로 만들 수 있는 최적의 profit을 반환하는 함수
    def matrix_based_iterative(self):  
        # TODO : Implement the matrix based iterative method and print objective value
        for i in range(len(self.data)+1): #n행 m열의 2d Arrary에 대해서
            for j in range(self.capacity+1):
                if i ==0 or j ==0: #아이템이 없거나, capacity가 없으면 최적의 profit이 0
                    self.tableau[i][j] = 0
                elif self.data[i-1].weight <= j: #선택 유뮤에 따른 profit중 큰 값을 선택한다.
                    self.tableau[i][j] = max(self.data[i-1].profit + self.tableau[i-1][j-self.data[i-1].weight],
                     self.tableau[i-1][j])
                else: #capa가 없으면 선택하지 않는다
                    self.tableau[i][j] = self.tableau[i-1][j]
        self.objective_value = self.tableau[len(self.data),self.capacity]
        print(f"objective value: {self.tableau[len(self.data),self.capacity]}")
        
# weight/profit을 받아 capacity가 y라는 조건하에 i번째 아이템부터의 optimal profit 반환
@cache(maxsize=None)
def recursive(weight:tuple,profit:tuple,i:int,y:int):
    if i == len(weight)-1: # 마지막 아이템 weight이 capa보다 크면0
        if y < weight[-1]:
            return 0
        else:
            return profit[-1] # 작거나 같거나 작으면 그 아이템의 profit을 반환
    else:
        if y < weight[i]: #  남은 capa보다 그 아이템의 weight이 무거우면 선택하지 말아라
            return recursive(weight,profit,i+1,y)
        else: # 안선택 했을때의 profit과 선택했을 때의 profit중 큰 값을 선택
            return max(recursive(weight,profit,i+1,y),recursive(weight,profit,
            i+1,y-weight[i])+profit[i])
            
        
if __name__ == "__main__":
    if len(sys.argv) != 5: # Command창에서 제대로 입력하지 않은 경우
        print("Input file 이름과 capacity, algorithm type, Output file 이름을 제대로 입력하세요")
    
    else: # Command창에서 제대로 입력한 경우
        input_file_path = sys.argv[1] #command창에서 입력한 file name을 input file name으로 이용
        output_file_path = sys.argv[4] #command창에서 입력한 file name을 output file name으로 이용
        solution = Knapsack(int(sys.argv[2])) #command창에서 입력한 정수를 capacity로 이용
        solution.read_data(input_file_path)

        if int(sys.argv[3]) == 2: # Iterative를 이용하면
            start1 = timeit.default_timer()
            solution.matrix_based_iterative()
            stop1 = timeit.default_timer()
            print(f"iterative solution은 {stop1-start1}초 걸렸습니다")
            f = open(output_file_path,'w',newline='')
            data = csv.writer(f)
            data.writerow(['input size',str(len(solution.data))])
            data.writerow(['capacity',str(solution.capacity)])
            data.writerow(['Algorithm type', 'Iterative'])
            data.writerow(['Elapsed time(ms)',str((stop1 - start1)*1000)])
            data.writerow(['objective value',str(solution.objective_value)])
            f.close()
        
        elif int(sys.argv[3]) == 1: # Recursive를 이용하면
            weight = [solution.data[i].weight for i in range(len(solution.data))]
            profit = [solution.data[i].profit for i in range(len(solution.data))]
            start2 = timeit.default_timer()
            a = recursive(tuple(weight),tuple(profit),0,solution.capacity)
            stop2 = timeit.default_timer()
            print(f"objective value: {a}")
            print(f"recursive solution 은 {stop2-start2}초 걸렸습니다")

            f = open(output_file_path,'w',newline='')
            data = csv.writer(f)
            data.writerow(['input size',str(len(solution.data))])
            data.writerow(['capacity',str(solution.capacity)])
            data.writerow(['Algorithm type', 'Recursive'])
            data.writerow(['Elapsed time(ms)',str((stop2 - start2)*1000)])
            data.writerow(['objective value',str(a)])
            f.close()

#---------------------------------------------------------------------------
    
   