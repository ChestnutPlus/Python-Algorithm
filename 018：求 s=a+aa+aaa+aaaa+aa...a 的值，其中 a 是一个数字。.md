例如 2+22+222+2222+22222(此时共有 5 个数相加)，几个数相加由键盘控制。
【思路】：答案给的解法很多种，但是我还是认为我写的方法最简单。
2+22+222+2222+22222
可以理解为：
20000 + 2*2000 + 3*200 + 4*20 + 5*2
也就是：
1*2*10^4 + 2*2*10^3 + 3*2*10^2 + 4*2*10^1 + 5*2*10^0
所以简单迭代就可以出结果

a = 2
t = 5
num = 0
for i in range(1,t+1):
num+=i*a*(10**(t-i))
print(num)
