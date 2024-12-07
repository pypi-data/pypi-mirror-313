# -*- coding: UTF-8 -*-
class Solution:
    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        """
        给定一个字符串s，请你找出其中不含有重复字符的最长子串的长度。
        P[i,j] [i,j)内不含重复
        """
        if len(s) == 0:
            return 0
        rst = 0
        h = 0
        has = {s[0]}
        for t in range(1, len(s)):
            if s[t] in has:
                for h in range(h, t):
                    has.remove(s[h])
                    if s[h] == s[t]:
                        h += 1
                        break
            has.add(s[t])
            rst = max(rst, len(has))
        return rst

print(Solution.lengthOfLongestSubstring('aa'))
