---
title: Maze Problems
description: dfs|bfs|dijkstra
---
TL;DR:
- Solution of [The Maze](https://leetcode.com/problems/the-maze/) and [The Maze II](https://leetcode.com/problems/the-maze-ii/)
- Steps to come up with a DFS solution
- Use heapq instead of PriorityQueue for leetcode

TODO:
- [ ] The Maze III

## The maze I
Pretty straightforward solution
- Check if the maze is empty
- Define recursive function
  - Check end condition
  - Exporing branches
  - Search through branch
- Call the recursize and return results

```python
class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        if not maze:
            return False
        visited, n, m = set(), len(maze), len(maze[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        def solve(x, y):
            visited.add((x, y))
            if x == destination[0] and y == destination[1]:
                return True
            for d in directions:
                xx, yy = x, y
                while 0 <= xx + d[0] < n and 0 <= yy + d[1] < m and maze[xx+d[0]][yy+d[1]] == 0:
                    xx += d[0]
                    yy += d[1]
                if (xx, yy) not in visited and solve(xx, yy):
                    return True
            return False
        return solve(*start)
```

## The maze II

### DFS(TLE)
Similar to Maze I, but have to search through all possible paths for optimal steps
- Check if the maze is empty
- Define recursive function
  - Check end condition
  - Exporing branches
  - Search through branch
- Call the recursize and return results
``` python
from collections import defaultdict
class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        if not maze:
            return -1
        dist, n, m = defaultdict(lambda : 0x7fffffff), len(maze), len(maze[0])
        destination, start = tuple(destination), tuple(start)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dist[start] = 0

        def solve(x, y):
            for d in directions:
                xx, yy, st = x + d[0], y + d[1], 0
                if dist[(x, y)] > dist[destination]: return
                while 0 <= xx < n and 0 <= yy < m and maze[xx][yy] == 0:
                    xx += d[0]
                    yy += d[1]
                    st += 1
                if dist[(x, y)] + st < dist[(xx - d[0], yy - d[1])]:
                    dist[(xx - d[0], yy - d[1])] = dist[(x,y)] + st
                    solve(xx - d[0], yy - d[1])
        solve(*start)
        return -1 if dist[destination] == 0x7fffffff else dist[destination]
```
Theoretically DFS and BFS would have the same time complexity of *O(n\*m\*max(m,n))*, because we have to search through every point in the matrix in the worst scenario. 

### BFS with PriorityQueue
For BFS, it usually consists of serveral components
- A *visited* set to store visited nodes
- A *frontier* queue to store intermediate results

When we started a BFS we usually
- Get the current node from frontier, ignore if that node is already visited
- Add current node to visited and check if it satisfies the end condition
- Expolore neighbors from current node
- Add neighbors to the frontier
- Repeat until we have visited all nodes

But this problem can be also seem as a graph problem, where the distance between each possible point can be seem as an edge and we want the minimum distance between the source and destination. 

In that case, we can use [*Dijkstra's algorithm*](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/#:~:text=For%20Dijkstra's%20algorithm%2C%20it%20is,heap%20(or%20priority%20queue).&text=Whenever%20distance%20of%20a%20vertex,instance%20of%20vertex%20in%20priority_queue.) to determine the minimum distance. a priority queue can be used to avoid multiple visits of the same vertex.

```python
import heapq


class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        n, m = len(maze), len(maze[0])
        destination, start = tuple(destination), tuple(start)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        pq = [[0, start[0], start[1]]]
        dist = { (start[0], start[1]): 0}
        while pq:
            dis, x, y = heapq.heappop(pq)
            if destination == (x, y):
                return dis
            for d in directions:
                xx, yy, dd = x, y, 0
                while 0 <= xx + d[0] < n and 0 <= yy+d[1] < m and maze[xx+d[0]][yy+d[1]] == 0:
                    xx += d[0]
                    yy += d[1]
                    dd += 1
                if (xx, yy) not in dist or dis + dd < dist[(xx, yy)]:
                    dist[(xx,yy)] = dis + dd
                    heapq.heappush(pq, (dis + dd, xx, yy))
        return -1
```
In the code, the dist functioned as the *visited* and stores the minimum distance while the priority queue functioned as the *frontier* and effectivly pruned most of the branches due to the nature of problem.
#### Notice
Use **heapq** for leetcode instead of PriorityQueue class. The same code runs for ~360ms using PQ but for ~300ms using heapq. 
The overhead comes from the extra operation from queue class to ensure that the operations are thread safe.


