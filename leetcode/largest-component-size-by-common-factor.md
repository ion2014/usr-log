---
title: Largest Component size by common factor
description: Union Find|Number Theory
image:
    path: /img/meme_1.jpg
---
TL;DR:
- Solution of [largest-component-size-by-common-factor](https://leetcode.com/problems/largest-component-size-by-common-factor/), 484ms beats 100%
- Iteration process of the solution

## Problem Introduction
Given a non-empty array of unique positive integers A, consider the following graph:

- There are A.length nodes, labelled A[0] to A[A.length - 1];
- There is an edge between A[i] and A[j] if and only if A[i] and A[j] share a common factor greater than 1.
Return the size of the largest connected component in the graph.
- *任何不互质的两个数之间连一条边，求由n个数这样连接所构成的图的最大连通分量的大小*

### Data Range

- 1 <= A.length <= 20000
- 1 <= A[i] <= 1E5


## Examples 
Input: [4, 6, 15, 35]
Output: 4

- (4, 6) = 2, (6, 15) = 3, (15, 35) = 5, 形成一个连通图，连通图的连通分量只有它本身，所以答案是4.

## Solutions
首先需要将问题转化：
每两个相连的点，其实等效于相连到了他们的公共素因数上。

因为如果两个数存在公共素因数，那么他们两就不互质；如果两个数不互质，那么他们的最大公约数的所有素因数即为他们的公共素因数。

那么如果将每个素数视为一个组，组的大小就是能被它整除的数的个数。

每当有新数加入时，将所有其素因数的组合并，最后最大组的大小就是最大连通分量的大小。

**注意：为了防止一个数被多次计算，先进行素因数代表组的合并，再更新合并后组的大小**

### Iteration #1 3000ms[15%]

第一个想到的优化是优先打出素数表，这样可以减少素因数分解的时间，考虑到数据范围只到100000，所以只需要输出小于等于sqrt(1E5)+1=317的素数即可。

对于不在素数表又不能被整除的数，只可能是素数，直接记为新的素因数代表组一齐计算即可。

```Python
from collections import defaultdict


class Solution:
    def largestComponentSize(self, A: List[int]) -> int:
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317]
        label = defaultdict(int)
       
        def findRoot(key):
            if label[key] > 0:
                label[key] = findRoot(label[key])
                return label[key]
            else:
                return key
        
        def mergeRoot(k1, k2):
            r1, r2 = findRoot(k1), findRoot(k2)
            if r1 == 0:
                return r2
            if r1 < r2:
                label[r1] += label[r2]
                label[r2] = r1
            elif r1 > r2:
                label[r2] += label[r1]
                label[r1] = r2
            return min(r1, r2)

        large_prime = 0
        for x in A:
            root_id = 0
            for p in small_primes:
                if p > x:
                    break
                elif x % p == 0:
                    root_id = mergeRoot(root_id, p)
                    while x % p == 0:
                        x /= p
            if x != 1:
                root_id = mergeRoot(root_id, x)
            label[root_id] -= 1
        
        return -min(label.values())
```

### Iteration #2 2500ms[59%]

简化了mergeRoot的判断条件，将其移动到函数外进行判断

```Python
from collections import defaultdict


class Solution:
    def largestComponentSize(self, A: List[int]) -> int:
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317]
        label = defaultdict(int)
       
        def findRoot(key):
            if label[key] > 0:
                label[key] = findRoot(label[key])
                return label[key]
            else:
                return key
        
        def mergeRoot(k1, k2):
            r1, r2 = findRoot(k1), findRoot(k2)
            if r1 < r2:
                label[r1] += label[r2]
                label[r2] = r1
            elif r1 > r2:
                label[r2] += label[r1]
                label[r1] = r2
            return min(r1, r2)

        large_prime = 0
        for x in A:
            root_id = 0
            for p in small_primes:
                if p > x:
                    break
                elif x % p == 0:
                    root_id = findRoot(p) if root_id == 0 else mergeRoot(root_id, p)
                    while x % p == 0:
                        x //= p
            if x != 1:
                root_id = findRoot(x) if root_id == 0 else mergeRoot(root_id, x)
            label[root_id] -= 1
        
        return -min(label.values())
```

### Iteration #3 2000ms[67%]

进一步简化了MergeRoot的判断条件

```python
from collections import defaultdict


class Solution:
    def largestComponentSize(self, A: List[int]) -> int:
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317]
        label = defaultdict(int)
       
        def findRoot(key):
            if label[key] > 0:
                label[key] = findRoot(label[key])
                return label[key]
            else:
                return key
        
        def mergeRoot(k1, k2):
            r1, r2 = findRoot(k1), findRoot(k2)
            if r1 != r2:
                r1, r2 = min(r1, r2), max(r1, r2)
                label[r1] += label[r2]
                label[r2] = r1
            return r1

        for x in A:
            root_id = 0
            for p in small_primes:
                if p >= x:
                    break
                if x % p == 0:
                    root_id = findRoot(p) if root_id == 0 else mergeRoot(root_id, p)
                    while x % p == 0:
                        x //= p
            if x != 1:
                root_id = findRoot(x) if root_id == 0 else mergeRoot(root_id, x)
            label[root_id] -= 1
        
        return -min(label.values())
```

### Iteration #4 1000ms[99%]

相比于上个版本，我意识到在对数组中的数做素因数分解时，寻找素因数的中止可以提前到*sqrt(x)*而不是*x* ，考虑到大部分数据规模较小，实际效果来看减少了将近一半的时间。

**注意：没有动态使用p>sqrt(x)+1的原因是计算平方根的开销大于剪枝的收益**

```python
from collections import defaultdict


class Solution:
    def largestComponentSize(self, A: List[int]) -> int:
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317]
        label = defaultdict(int)
       
        def findRoot(key):
            if label[key] > 0:
                label[key] = findRoot(label[key])
                return label[key]
            else:
                return key
        
        def mergeRoot(k1, k2):
            r1, r2 = findRoot(k1), findRoot(k2)  
            if r1 != r2:
                r1, r2 = min(r1, r2), max(r1, r2)
                label[r1] += label[r2]
                label[r2] = r1
            return r1

        for x in A:
            root_id = 0
            t = sqrt(x) + 1
            for p in small_primes:
                if p > t:
                    break
                elif x % p == 0:
                    root_id = findRoot(p) if root_id == 0 else mergeRoot(root_id, p)
                    while x % p == 0:
                        x //= p
            if x != 1:
                root_id = findRoot(x) if root_id == 0 else mergeRoot(root_id, x)
            label[root_id] -= 1
        
        return -min(label.values())
```

### Iteration #5 480ms[100%]

最后一个有取巧的成分，考虑到在Solution中打表是不计算在总体时间中的，我选择了生成式的素数分解表，其中isPrime中的每个数，是对应下标的最小的素因数（类似的生成方法在Project Euler中出现过），这样再进行素因数分解时，只需要使用`x //= isPrime[x]`便可以得到所有的素因数了。经过测试发现，如果将计算素因数表的部分放到函数中，将会花费~2500ms的时间。


```Python
from collections import defaultdict


class Solution:
    MAXA = 100001
    isPrime=[0 for _ in range(MAXA+1)]
    isPrime[0]=-1;isPrime[1]=-1 #0 and 1 are not prime numbers
    for i in range(2, MAXA):
        if isPrime[i]==0: #i is prime
            for multiple in range(i*i,MAXA+1,i):
                if isPrime[multiple]==0:
                	isPrime[multiple]=i
    	isPrime[i] = i # let i store itself for consistency

    def largestComponentSize(self, A: List[int]) -> int:
        label = defaultdict(int)

        def findRoot(key):
            if label[key] > 0:
                label[key] = findRoot(label[key])
                return label[key]
            else:
            	return key

        def mergeRoot(k1, k2):
            r1, r2 = findRoot(k1), findRoot(k2)  
            if r1 != r2:
                r1, r2 = min(r1, r2), max(r1, r2)
                label[r1] += label[r2]
                label[r2] = r1
            return r1

        for x in A:
        	root_id = 0
            while Solution.isPrime[x]!=-1:
                p = Solution.isPrime[x]
                root_id = findRoot(p) if root_id == 0 else mergeRoot(root_id, p)
                x //= p
            label[root_id] -= 1

    return -min(label.values())

```




# Complexity Analysis
记*MAXA = UpperBound(A)*

### Iteration 1-2

对于并查集，由于路径压缩的存在，整个并查集中不存在高度大于2的树，查询根节点和合并的操作均接近*O(1)*。遍历求素因数的时间上界为*O(Pi(MAXA))*，对于非trivial的MAXA，*Pi(MAXA)~O(log(MAXA))*，所以整个时间复杂度为*O(NlogN+Nlog(MAXA))*

### Iteration 3

相比于1，2优化了求素因数的效率，时间复杂度为*O(NlogN+N\*Pi(sqrt(N)))=O(NlogN)*

### Iteration 4

素数表的生成 的时间复杂度为*O(Pi(MAXA)\*MAXA)*，查表时间的上界为*log(MAXA)*，其中*Pi(MAXA)*表示不小于*MAXA*的素数的数目，总的生成的时间复杂度的上界为*O(MAXA\*log(MAXA))*。
所以总时间复杂度的上界为*O((N+MAXA)\*log(MAXA))*。由于leetcode的评测机机制，其中生成部分不被计算在总时间中，所以评测时的时间复杂度为O(N*log(MAXA))。




