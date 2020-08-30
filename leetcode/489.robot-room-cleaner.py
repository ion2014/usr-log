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
    def changeToFacing(self, targetFacing):
        while self.facing != targetFacing:
            self.robot.turnRight()
            self.facing = (self.facing + 1) % 4

    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        self.robot = robot
        self.facing = 0
        self.visited = set()
        self.dir = [
            (0, -1, 0, 2), (1, 0, 1, 3), (2, 1, 0, 0), (3, 0, -1, 1), 
            (0, -1, 0, 2), (1, 0, 1, 3), (2, 1, 0, 0), (3, 0, -1, 1)
        ]
        self.solve(0, 0)

    def solve(self, X, Y):
        self.robot.clean()
        self.visited.add((X, Y))

        # Explore
        for d in self.dir[self.facing: self.facing + 4]:
            if (X + d[1], Y + d[2]) not in self.visited:
                self.changeToFacing(d[0])
                if self.robot.move():
                    self.solve(X + d[1], Y + d[2])
                    self.changeToFacing(d[3])
                    self.robot.move()

# @lc code=end
