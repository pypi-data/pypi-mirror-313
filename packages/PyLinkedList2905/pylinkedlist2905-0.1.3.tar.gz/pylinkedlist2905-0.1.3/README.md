# Linked List Package

A simple implementation of a singly linked list in Python.

## Features

- Insert elements at the beginning (`insert_left`)
- Insert elements at the end (`insert_right`)
- Insert elements at a specific position (`insert_at`)
- Delete elements from the beginning (`del_left`)
- Delete elements from the end (`del_right`)
- Display the linked list (`show`)
- Merge two linked lists (`merge`)
- Get the length of the linked list (`len`)

## Installation

Install Linked_list with pip

```bash
   pip install Linked_list
```
## Usage 

### insert elements

```python

from linked_list import Linked_list

# Create a new linked list
ll = Linked_list()

# Insert elements at the left (beginning)
ll.insert_left(10)
ll.insert_left(20)

# Insert elements at the right (end)
ll.insert_right(30)

# Insert elements at a specific position
ll.insert_at(1, 25)

# Show the linked list
ll.show()

```
### output
```bash
20-->10-->25-->30-->None
```

### delete elements

```python
# Delete an element from the left (beginning)
ll.del_left()

# Delete an element from the right (end)
ll.del_right()

# Show the linked list after deletions
ll.show()

```

### merge two linked list

```python
# Create another linked list
ll2 = Linked_list()
ll2.insert_left(40)
ll2.insert_right(50)

# Merge the second list into the first list
ll.merge(ll2)

# Show the merged linked list
ll.show()

```
### output
```bash
10-->25-->30-->40-->50-->None
```
### Get the Length of the Linked List

```python
# Get the length of the linked list
print("Length of the list:", ll.len())
```
### output
```bash
Length of the list: 5
```