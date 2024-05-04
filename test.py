sl = 1.05839
openPrice = 1.05680
tp = 1.05519
tpReduce = 0.2


candBody = abs(sl-openPrice)/2

tpShouldBe = openPrice - (candBody * (1-tpReduce))

print(tpShouldBe)