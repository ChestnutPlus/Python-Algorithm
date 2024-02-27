# Problem: 混合背包问题
# Contest: AcWing
# URL: https://www.acwing.com/problem/content/7/
# Memory Limit: 64 MB
# Time Limit: 1000 ms

import sys
from collections import deque
from math import inf

RI = lambda: map(int, sys.stdin.buffer.readline().split())
RS = lambda: map(bytes.decode, sys.stdin.buffer.readline().strip().split())
RILST = lambda: list(RI())
DEBUG = lambda *x: sys.stderr.write(f'{str(x)}\n')


class PackMaxMin:
    """    背包问题求最大/最小值，复杂度O(体积*物品(种类)数),
    如果是多重背包，可以优化成O(体积*物品种类数)
    有两种使用方法：
        1. 初始化只传入背包容量vol和极值方法merge(如:max)。外部遍历物品，手动调用p.zero_one_pack等方法。见solve1。
            好处是不用思考怎么创建dp数组，怎么倒序遍历，遍历时的边界问题(如倒序:range(vol,v-1,-1))
        2. 初始化同时传入对应类型的物品集合，然后调用run()，可以直接转移完成。但是需要在外部组合起需要的物品，比较麻烦。
            好处是如果外部本身就组合过了，可以直接算，不用外部暴露逻辑。
    无法处理的问题:
        1. 求方案数(另写一个模板)
        2. 求具体方案(还没想好)
        3. 二维费用背包:一般是f定义成2维，然后倒序枚举j变成倒序枚举j、k即可，但对代码入侵性较强，变化也多，没想好怎么封装，有空可以尝试写一下试试。
    """

    def __init__(self, vol, zero_one=None, multi=None, complete=None, merge=max, sit='just', ini=None):
        """关于ini:
            如果求体积'恰好'j时，ini应该是-inf/inf
            如果求体积'至少/至多'时，ini应该是0
            考虑只有一个物品v=4,但枚举j==5的场景，
                若初始化f[1]=0,f[5]会计算成f[1]+w，是有结果的，实际上认为5可以容纳4，即体积不超过/至多5的数据全部容纳。
                若初始化f[1]=-inf,则f[5]计算也会是-inf，认为非法。则任何位置只能从0先转移一个合法数据。
        """
        self.zero_one = zero_one  # 用于01背包的物品 (v,w):体积，价值
        self.multi = multi  # 用于多重背包的物品 (v,w,c):体积，价值，数量
        self.complete = complete  # 用户完全背包的物品 (v,w):体积，价值
        self.merge = merge  # 取极值的方案数，一般是max
        self.vol = vol  # 背包容量，注意计算复杂度时要用到
        if ini is None:
            if sit == 'just':
                ini = -inf if merge.__name__ == 'max' else inf
            elif sit in ['at_least',
                         'at_most']:  # 注意，至多的情况for循环需要修改为:for j in range(self.vol, -1, -1):f[j] = merge(f[j], f[max(j - v,0)] + w)
                ini = 0
        self.f = [0] + [ini] * vol  # f[j]代表体积至多j时的最优值

    def zero_one_pack(self, v, w):
        """        01背包，逆序处理即可滚动
        v:体积, w:价值
        """
        f, merge = self.f, self.merge
        for j in range(self.vol, v - 1, -1):
            f[j] = merge(f[j], f[j - v] + w)

    def complete_pack(self, v, w):
        """        完全背包，正序处理即可滚动
        v:体积, w:价值
        """
        f, merge = self.f, self.merge
        for j in range(v, self.vol + 1):
            f[j] = merge(f[j], f[j - v] + w)

    def multi_pack_by_zero_one(self, v, w, c):
        """        多重背包转化成01背包，效率最低，但思考方便，一些无脑dp的题可能可以参考到
            注意和分组背包区分:外层枚举c个物品，内层倒序枚举j。因为每个物品都要尝试放，扫一遍j。
            注意有时会和分组背包混淆：如题意描述成，第i种物品有c个，可以任选几个，但同种物品不区分。
            这种情况用多重背包计算就会出现重复方案，实际上考虑分组背包：这组中有c种物品，只能选0/1个。这c种物品分别是1个i，2个i。。c个i。
        v:体积, w:价值, c:本物品个数
        """
        if v * c >= self.vol:  # 如果数量足够到超过目标体积，那么可以当完全背包做，更快
            return self.complete_pack(v, w)
        for _ in range(c):  # 直接展开，尝试c次即可
            self.zero_one_pack(v, w)

    def multi_pack_by_binary(self, v, w, c):
        """        多重背包的二进制优化，可以把复杂度里的*c变成*lg(c)。原理是：
        所有数字都可以用1,2,4,8..等2的幂互相加起来，那么把c分解成这些数字分别尝试逆序转移即可，别忘记最后尝试剩余的部分
        v:体积, w:价值, c:本物品个数
        """
        if v * c >= self.vol:
            return self.complete_pack(v, w)
        f, merge = self.f, self.merge
        k = 1
        while k < c:
            self.zero_one_pack(v * k, w * k)
            c -= k
            k <<= 1

        self.zero_one_pack(v * c, w * c)

    def multi_pack_by_mono_que(self, v, w, c):
        """        多重背包的单调队列优化，可以把复杂度里的*c变成*1。原理需要画图展开消项，比较复杂，还不是很懂。
        v:体积, w:价值, c:本物品个数
        """
        if v * c >= self.vol:
            return self.complete_pack(v, w)
        f, merge = self.f, self.merge
        pre = f[:]
        for k in range(v):
            q = deque()
            for j in range(k, self.vol + 1, v):
                if q and q[0] < j - c * v:
                    q.popleft()
                while q and pre[q[-1]] + (j - q[-1]) // v * w <= pre[j]:
                    q.pop()
                q.append(j)
                f[j] = pre[q[0]] + (j - q[0]) // v * w

    def run(self):
        """直接计算这些背包的转移，除了很模板的题不建议使用"""
        if self.zero_one:
            for v, w in self.zero_one:
                self.zero_one_pack(v, w)
        if self.multi:
            for v, w, c in self.multi:
                self.multi_pack_by_mono_que(v, w, c)
        if self.complete:
            for v, w in self.complete:
                self.complete_pack(v, w)
        return self.f


#   1324    ms
def solve():
    n, vol = RI()
    pp = PackMaxMin(vol, merge=max)
    for _ in range(n):
        v, w, s = RI()
        if s == 1 or s == -1:
            pp.zero_one_pack(v, w)
        elif s == 0:
            pp.complete_pack(v, w)
        else:
            pp.multi_pack_by_mono_que(v, w, s)  # 1324 ms
            # pp.multi_pack_by_binary(v, w, s)  # 1349 ms
            # pp.multi_pack_by_zero_one(v, w, s)  # 1353 ms
    print(max(pp.f))


#     1342   ms
def solve1():
    n, vol = RI()
    zero_one, multi, complete = [], [], []

    for _ in range(n):
        v, w, s = RI()
        if s == 1 or s == -1:
            zero_one.append((v, w))
        elif s == 0:
            complete.append((v, w))
        else:
            multi.append((v, w, s))

    pp = PackMaxMin(vol, zero_one=zero_one, multi=multi, complete=complete, merge=max)
    print(max(pp.run()))


if __name__ == '__main__':
    solve()
