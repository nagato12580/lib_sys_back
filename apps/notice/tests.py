from django.test import TestCase

# Create your tests here.
def minCost(nums):
    n = len(nums)
    dp = [[float('inf')] * n for _ in range(n)]

    # 初始化只有一个子数组的情况
    for i in range(n):
        dp[i][i] = 0

    # 计算每个位置的最小代价总和
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + max(nums[i:k + 1]) * max(nums[k + 1:j + 1]))

    # 返回以第一个元素为结尾、最后一个元素为起始的最小代价总和
    return dp[0][n - 1]

# 示例输入
nums = [1, 2, 3, 12]

# 调用函数并输出结果
print(minCost(nums))