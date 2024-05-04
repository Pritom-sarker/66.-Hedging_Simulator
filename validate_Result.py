
balance = 100
baseRisk = 2
pf = [0.45,0.375, 0.45 ,0.375 ,0.45 ,0.375 ]
additinonalMuliplier =  [1,1.2 ,1.2,1,0.95,0.9]
fee = 0
dropdown = 0


# order - 1
val = (balance * baseRisk)/100
order1 = (val * additinonalMuliplier[0]) # input(
print("order - 1: ", order1)
print("overall amount we need -> ", order1)
print("If Profit : ", order1 * pf[0]) 
print('--------------')
# order - 2
val = (order1 * (1/pf[1]) ) 
order2 = (val * additinonalMuliplier[1]) # input(
print("order - 2: ", order2)
print("overall amount we need -> ",  order2)
print("If Profit : ", (order2 * pf[1])-order1) 
print('--------------')
 
 # order - 3
val = (order2 * (1/pf[2]) ) - (order1 * pf[0]) 
order3 = (val * additinonalMuliplier[2]) # input(
print("order - 3: ", order3)
print("overall amount we need -> ", (order1 + order3))
print("If Profit : ", (order3 * pf[2])+(order1*pf[0]) - (order2))
print('--------------')

 
 # order - 4
val = ((order3 * (1/pf[3]) ) + (order1 * (1/pf[3]))) - (order2 * pf[1]) 
order4 = (val * additinonalMuliplier[3]) # input(
print("order - 4: ", order4)
print("overall amount we need -> ", (order2 + order4))
print("If Profit : ", ((order4 * pf[3])+(order2*pf[1]) ) - (order1 + order3))
print('--------------')

 
 # order - 5
val = ((order2 * (1/pf[4]) ) + (order4 * (1/pf[4]) )) - ((order1 * pf[0]) + (order3 * pf[2]) )
order5 = (val * additinonalMuliplier[4]) 
print("order - 5 : ", order5)
print("overall amount we need -> ", (order1 + order3+ order5))
print("If Profit : ",  ((order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4) )
print('--------------')


 
 # order - 6
val = ((order1 * (1/pf[5]) ) + (order3 * (1/pf[5]) ) + (order5 * (1/pf[5]) )) - ((order2 * pf[1]) + (order4 * pf[3]) )
order6 = (val * additinonalMuliplier[5]) 
print("order - 6 : ", order6)
print("overall amount we need -> ",  (order2 + order4 + order6))
print("If Profit : ", ((order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5))
print('--------------')

# print('Overall We Put: ', order1 + order2 + order3  +  order4 + order5 + order6)
print('IF its a loss: ',  ((order1 * pf[0])+(order3*pf[2])+(order5*pf[4]) ) - (order2 + order6 +order4) )


