#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:16:13 2019

@author: bingqingxie
"""
import collections      
from collections import OrderedDict 

#defined a new data structure to store the start and ending point 
# of the sentence in linkedlist, to find previous or next sentence

class Node(object):
    def __init__(self, data = list, next = None, prev = None):
        self.data = data
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.data)
    

class LinkedList(object):
    
    def __init__(self, head = None):
        self.head = head
        
        
    def append(self, data):
        """
        Insert a new element at the end of the list.
        Takes O(n) time.
        """
        if not self.head:
            self.head = Node(data=data)
            return
        curr = self.head
        while curr.next:
            curr = curr.next
            
        curr.next = Node(data=data, prev=curr)        
        
    #功能：查找链表的节点data与data相同的节点
    def find(self,data):
        
        if data is None:
            return None
        
        curr_node = self.head
        
        while curr_node is not None:
            if curr_node.data == data:
                return curr_node
            
            curr_node = curr_node.next
            
        return None

#define function to convert map object to linkedlist

def convert_map_to_linkedlist(sent_map):
    # convert map to order dictionary to kepp the order
    orderli = collections.OrderedDict(sent_map)
    
    # instantiate the linkedlist
    linked = LinkedList()
    # pass each sentence index into linkedlist
    for l in orderli.items():
        linked.append(list(l))
    
    return linked  

# find the new start point if index is in front of current start point of sentence
def find_new_start(linked, start, end, idx):
    
    search_node = []
    search_node.append(start)
    search_node.append(end)
    node = linked.find(search_node)
    
    while idx < node.prev.data[0]:
        node = node.prev

    return node.prev.data[0]

def find_new_end(linked, start, end, idx):
    
    search_node = []
    search_node.append(start)
    search_node.append(end)
    node = linked.find(search_node)
    
    while node.next is not None and idx > node.next.data[1]:
        node = node.next
    
    if node.next is None:
        return node.data[1]
    
    return node.next.data[1]


