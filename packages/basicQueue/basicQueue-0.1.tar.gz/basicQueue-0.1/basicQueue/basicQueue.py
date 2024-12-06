class Queue():
    def __init__(self, max_val):
        self.queue = []
        self.front_pointer = 0
        self.end_pointer = 0
        self.is_Full = False
        self.is_Empty = True
        self.max_val = int(max_val)
        self.end_val = 0

        for i in range(self.max_val):
            self.queue.append(" ")

    def length(self):
        len = 0
        for i in range(self.max_val):
            if self.queue[i] != " ":
                len += 1
        return len

    def enQueue(self, val):
        length = self.length()
        if self.is_Empty:
            self.queue[self.front_pointer] = val
            self.is_Empty = False
            self.end_pointer
            #print(f"FRONT: {self.front_pointer}\nEND: {self.end_pointer}")
            # CHECKS IF THE QUEUE IS FULL
            if (self.end_pointer + 1) == self.max_val:
                self.is_Full = True

        elif not self.is_Full:
            #print(length)
            self.queue[self.front_pointer + length] = val
            self.is_Empty = False
            self.end_pointer = self.front_pointer + length
            # CHECKS IF THE QUEUE IS FULL
            if (self.end_pointer + 1) == self.max_val:
                self.is_Full = True
                print("LIST IS FULL")


        else:
            print("ERROR 001: QUEUE HAS REACHED MAX SIZE")

    def deQueue(self):
        if self.is_Empty == True:
            print("ERROR 002: QUEUE IS EMPTY ")
        else:
            val = self.queue[self.front_pointer]
            self.queue[self.front_pointer] = " "
            self.front_pointer += 1
            if self.front_pointer == (self.end_pointer + 1):
                self.is_Empty = True
                self.front_pointer = 0
                self.end_pointer = 1
            #print(f"    FRONT: {self.front_pointer}\n    END: {self.end_pointer}")
            return val

    def isFull(self):
        return self.is_Full

    def isEmpty(self):
        return self.is_Empty
