class Agent:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.visited_list = []
        self.list = []
        self.numbers_list = []
        for i in range(0,self.size_y):
            for j in range(0,self.size_x):
                list.append(0)
            self.visited_list.append(list)

        for i in range(0,self.size_y):
            for j in range(0,self.size_x):
                list.append(0)
            self.numbers_list.append(list)
        self.foundGold = False

    def move(self, state):

        while(self.foundGold == False):
            dir = self.step(self, state)
            self.move_out(self,dir)

    def move_out(self,direct):
        if direct == 'n':
            self.boty = max(self.boty-1,0)
        if direct == 'w':
            self.botx = min(self.botx+1,3)
        if direct == 's':
            self.boty = min(self.boty+1,3)
        if direct == 'e':
            self.botx = max(self.botx-1,0)


    def step(self, state):
        print("HELLO WORLD")
        return "move_up"
