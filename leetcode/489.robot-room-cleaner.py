#
# @lc app=leetcode id=489 lang=python3
#
# [489] Robot Room Cleaner
#

# @lc code=start
# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# """
# class Robot:
#    def move(self):
#        """
#        Returns true if the cell in front is open and robot moves into the cell.
#        Returns false if the cell in front is blocked and robot stays in the current cell.
#        :rtype bool
#        """

#    def turnLeft(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """

#    def turnRight(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """

#    def clean(self):
#        """
#        Clean the current cell.
#        :rtype void
#        """
class Solution:
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        facing = 0
        visited = set()
        dir = [(0, -1, 0, 2), (1, 0, 1, 3), (2, 1, 0, 0), (3, 0, -1, 1)]
        
        def changeToFacing(targetFacing):
            nonlocal facing
            while facing != targetFacing:
                robot.turnRight()
                facing = (facing + 1) % 4
        
        def solve(X, Y):
            robot.clean()
            visited.add((X, Y))

            # Explore
            for d in dir:
                if (X + d[1], Y + d[2]) not in visited:
                    changeToFacing(d[0])
                    if robot.move():
                        solve(X + d[1], Y + d[2])
                        changeToFacing(d[3])
                        robot.move()  

        solve(0, 0)

# @lc code=end
