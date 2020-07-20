# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseKGroup(self, head, k):

        # 链表长度，O(n)
        num_len = 0
        p = head
        while p is not None:
            num_len += 1
            p = p.next

        if num_len < k:
            return head

        start = ListNode(-1)
        start.next = head
        cur = start
        while 1:
            p = cur
            tag = 0
            ListNode_li = []
            for i in range(k):
                p = p.next
                if p is not None:
                    ListNode_li.append(p)
                else:
                    # 少于k 个，之后不做处理
                    tag = 1
                    break

            if tag == 1:
                break
            else:
                cur.next = ListNode_li[-1]
                cur = ListNode_li[0]
                ListNode_li[0].next = ListNode_li[-1].next
                for i in range(k - 1, 0, -1):
                    ListNode_li[i].next = ListNode_li[i - 1]

        return start.next


node_object = Solution()

start = ListNode(-1)
tmp = start

for i in range(1, 6):
    tmp.next = ListNode(i)
    tmp = tmp.next

a = node_object.reverseKGroup(start.next, 3)

while a is not None:
    print(a.val)
    a = a.next
