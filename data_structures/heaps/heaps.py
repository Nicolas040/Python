#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 09:27:25 2016

@author: nicolas
"""
class NoInfoException(Exception):
    pass

class HeapElement:
    """
    A heap element includes two attributes:
    - A number called key
    - An (optional) object containing possible information the user might
      want the element to carry. Keep in mind that in order to ensure the
      integrity of the object's content, this object should preferably be
      immutable.
    """
    
    def __init__(self, key, *args):
        if type(key) not in [int, float]:
            raise Exception("Key is not a number")
        self.key = key
        if len(args) != 0:
            self._info_ = args
        else:
            self._info_ = None
    
    def add_info(self, info, *args):
        """
        Takes at least one parameter, more if the user so wishes.
        Add all those parameters to the element as additional information.
        """
        if len(args) != 0:
            self._info_ = [info] + args
        else:
            self._info_ = info
    
    def get_info(self):
        """
        Returns the object that store extra information added by user.
        Returns a NoInfoException if there is none
        """
        if not self._info_:
            raise NoInfoException("No added info in element to return")
        return self._info_
    
    def get_key(self):
        "Returns key value of the element"
        return self.key

class WrongElementTypeException(Exception):
    pass

class NoListOfElementsException(Exception):
    pass

class EmptyHeapException(Exception):
    pass

class MinHeap:
    """
    A min-heap is a tree where all elements in the heap the nodes. This tree's properties are:
    - A node's key is higher than or equal to its parent's (except for the root node), and
    - A node's key is lower than or equal to any of its children's.
    """
    
    def __init__(self):
        self._heap_ = []

    def __str__(self):
        result = []
        for element in self._heap_:
            result.append(element.get_key())
        return str(result)

    def add_element(self, element):
        """
        Add 'element' into heap. Check first if element type is right,
        otherwise raise a WrongElementTypeException
        """
        if "HeapElement" not in str(type(element)):
            raise WrongElementTypeException("Element is not of HeapElement type")
        self._heap_.append(element)
        self._toggleUp_(len(self._heap_))
    
    def add_elements(self, list_elements):
        "Add all elements in 'list_elements' into heap"
        if type(list_elements) is not list:
            raise NoListOfElementsException("Argument is not a list")
        for element in list_elements:
            self.add_element(element)
    
    def _swap_(self, index1, index2):
        temp_element = self._heap_[index1 - 1]
        self._heap_[index1 - 1] = self._heap_[index2- 1]
        self._heap_[index2- 1] = temp_element
    
    def _toggleUp_(self, index):
        # Toggle node to its right place if its key is lower than its parent's
        while index > 1 and self._heap_[index - 1].get_key() < self._heap_[index//2 - 1].get_key():
            self._swap_(index, index // 2)
            index = index // 2
    
    def _toggleDown_(self, index):
        # Toggle node to its right place if its key is higher than any of its children's
        while 2*index <= len(self._heap_):
            # Tests comparing the node's key to both its left child and right child if any
            test_left = self._heap_[index - 1].get_key() > self._heap_[2*index - 1].get_key()
            test_right = 2*index < len(self._heap_) and self._heap_[index - 1].get_key() > self._heap_[2*index].get_key()
            # Swap node with its child having the lowest key
            if test_right and self._heap_[2*index].get_key() < self._heap_[2*index - 1].get_key():
                self._swap_(index, 2*index + 1)
                index = 2*index + 1
            elif test_left:
                self._swap_(index, 2*index)
                index = 2*index
            else:
                break
        
    def deleteElement(self, index):
        """
        Delete element in heap in position given by 'index'.
        Replace it with last element in heap and reorganize the heap
        """
        if len(self._heap_) == 1:
            self._heap_ = []
        elif len(self._heap_) == 0:
            raise EmptyHeapException("No element to delete")
        else:
            self._heap_[index - 1] = self._heap_.pop()
            if index > 1 and self._heap_[index - 1].get_key() < self._heap_[index//2 - 1].get_key(): #Toggle the element up if necessary
                self._toggleUp_(index)
            else: # Toggle the element down, does nothing if the element is already in the right place
                self._toggleDown_(index)
        
    def extractMin(self):
        "Extract the element with lowest key from the heap"
        if len(self._heap_) == 0:
            raise EmptyHeapException("No more elements to return")
        result = self._heap_[0]
        self.deleteElement(1)
        return result

class MaxHeap:
    """
    A max-heap is a tree where all elements in the heap the nodes. This tree's properties are:
    - A node's key is lower than or equal to its parent's (except for the root node), and
    - A node's key is higher than or equal to any of its children's.
    """
    
    def __init__(self):
        self._heap_ = []

    def __str__(self):
        result = []
        for element in self._heap_:
            result.append(element.get_key())
        return str(result)

    def add_element(self, element):
        """
        Add 'element' into heap. Check first if element type is right,
        otherwise raise a WrongElementTypeException
        """
        if "HeapElement" not in str(type(element)):
            raise WrongElementTypeException("Element is not of HeapElement type")
        self._heap_.append(element)
        self._toggleUp_(len(self._heap_))
    
    def add_elements(self, list_elements):
        "Add all elements in 'list_elements' into heap"
        if type(list_elements) is not list:
            raise NoListOfElementsException("Argument is not a list")
        for element in list_elements:
            self.add_element(element)
    
    def _swap_(self, index1, index2):
        temp_element = self._heap_[index1 - 1]
        self._heap_[index1 - 1] = self._heap_[index2- 1]
        self._heap_[index2- 1] = temp_element
    
    def _toggleUp_(self, index):
        # Toggle node to its right place if its key is higher than its parent's
        while index > 1 and self._heap_[index - 1].get_key() > self._heap_[index//2 - 1].get_key():
            self._swap_(index, index // 2)
            index = index // 2
    
    def _toggleDown_(self, index):
        # Toggle node to its right place if its key is lower than any of its children's
        while 2*index <= len(self._heap_):
            # Tests comparing the node's key to both its left child and right child if any
            test_left = self._heap_[index - 1].get_key() < self._heap_[2*index - 1].get_key()
            test_right = 2*index < len(self._heap_) and self._heap_[index - 1].get_key() < self._heap_[2*index].get_key()
            # Swap node with its child having the highest key
            if test_right and self._heap_[2*index].get_key() > self._heap_[2*index - 1].get_key():
                self._swap_(index, 2*index + 1)
                index = 2*index + 1
            elif test_left:
                self._swap_(index, 2*index)
                index = 2*index
            else:
                break
        
    def deleteElement(self, index):
        """
        Delete element in heap in position given by 'index'.
        Replace it with last element in heap and reorganize the heap
        """
        if len(self._heap_) == 1:
            self._heap_ = []
        elif len(self._heap_) == 0:
            raise EmptyHeapException("No element to delete")
        else:
            self._heap_[index - 1] = self._heap_.pop()
            if index > 1 and self._heap_[index - 1].get_key() > self._heap_[index//2 - 1].get_key(): #Toggle the element up if necessary
                self._toggleUp_(index)
            else: # Toggle the element down, does nothing if the element is already in the right place
                self._toggleDown_(index)
        
    def extractMax(self):
        "Extract the element with highest key from the heap"
        if len(self._heap_) == 0:
            raise EmptyHeapException("No more elements to return")
        result = self._heap_[0]
        self.deleteElement(1)
        return result
        
                                