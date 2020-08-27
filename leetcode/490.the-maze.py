#
# @lc app=leetcode id=490 lang=python3
#
# [490] The Maze
#

# @lc code=start
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
# @lc code=end
