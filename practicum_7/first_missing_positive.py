class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ans = 1
        c = {}
        for i in range(len(nums)):
            if nums[i] <= 0:
                pass
            else:
                if nums[i] == ans:
                    ans += 1
                elif nums[i] < ans:
                    pass
                elif nums[i] > ans:
                    c[nums[i]] = nums[i]
        while ans in c:
            ans += 1
        print(ans)
        return ans

        #pass


if __name__ == "__main__":
    # Let's solve First Missing Positive problem:
    # https://leetcode.com/problems/first-missing-positive
    sol = Solution()
    nums = [0, 1, 2]
    n = sol.firstMissingPositive(nums)
    nums = [2, 1]
    n = sol.firstMissingPositive(nums)
    nums = [1, 2, 0]
    n = sol.firstMissingPositive(nums)
    nums = [3, 4, -1, 1]
    n = sol.firstMissingPositive(nums)
    nums = [7, 8, 9, 11, 12]
    n = sol.firstMissingPositive(nums)
