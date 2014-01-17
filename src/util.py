__author__ = 'ZhangJingtian'

class Stack(object):
    def __init__(self, set=None):
        super(Stack, self).__init__()
        self.stack = []
        self.top   = -1

        if set != None:
            self.stack += set
            self.top = self.top + len(set)

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def pop(self):
        if self.isEmpty():
            return None
        else:
            data = self.stack[-1]
            self.top = self.top - 1
            del self.stack[-1]
            return data

    def push(self, data):
        self.stack.append(data)
        self.top = self.top + 1

    def size(self):
        return len(self.stack)




























