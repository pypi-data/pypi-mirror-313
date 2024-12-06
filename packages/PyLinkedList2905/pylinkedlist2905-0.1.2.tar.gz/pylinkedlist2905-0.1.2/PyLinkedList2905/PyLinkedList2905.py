
class Node:
    def __init__(self,data,next=None):
        self.data = data
        self.next = next
        


class Linked_list:
    def __init__(self):
        self.head = None



    def insert_left(self,data):
        node = Node(data,self.head)
        self.head = node


    def insert_right(self,data):
        if self.head == None:
            self.head = Node(data)
            return
        it = self.head
        while it.next:
            it = it.next
        it.next = Node(data)

    def show(self):
        if not self.head:
            print('Linked list is empty')
        it = self.head
        link = ''
        while it:
            link += str(it.data) +'-->'
            it = it.next
        link+='None'
        print(link)

    def len(self):
        l = 0
        it = self.head
        while it :
            l+=1
            it = it.next
        return l

    def length(self):
        l = 0
        it = self.head
        while it :
            l+=1
            it = it.next
        print(l)
        

    def insert_at(self, position, data):
        if position > self.len() or position < 0:
            print("Out of range of our linked list")
            return
        if position == 0:
            self.insert_left(data)
            return
        it = self.head
        t = 0
        while it:
            if position == t + 1: 
                it.next = Node(data, it.next)
                break
            it = it.next
            t += 1


    def del_left(self):
        if not self.head:
            print('Nothing to delete, linked list is empty')
            return
        if self.len() == 1:
            self.head = None
            return
        self.head = self.head.next

    def del_right(self):
        if not self.head:
            print('Nothing to delete, linked list is empty')
            return
        if self.len() == 1 :
            self.head = None
            return
        it = self.head
        t = 0
        while it.next:
            if t == self.len() -2:
                it.next = None
                break
            it = it.next
            t +=1
    
    def merge(self, merged):
        if not self.head:  
            self.head = merged
            return
        it = self.head
        while it.next:  
            it = it.next
        it.next = merged.head
    
            
        
            
