#
# @lc app=leetcode id=969 lang=python3
#
# [969] Pancake Sorting
#

# @lc code=start
class Solution:
    def pancakeSort(self, A: List[int]) -> List[int]:
        if len(A) <= 1:
            return []
        idx = A.index(len(A))
        if idx == 0:
            return [len(A)] + self.pancakeSort(list(reversed(A[1:])))
        elif idx == len(A) - 1:
            return self.pancakeSort(A[:-1])
        else:
            return [idx + 1, len(A)] + self.pancakeSort(list(reversed(A[idx + 1:])) + A[:idx])   

# @lc code=end

