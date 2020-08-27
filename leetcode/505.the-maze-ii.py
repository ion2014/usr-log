#
# @lc app=leetcode id=505 lang=python3
#
# [505] The Maze II
#

# @lc code=start
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

# @lc code=end
