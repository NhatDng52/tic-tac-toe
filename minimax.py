from settings import *
from game import Game
 # search hardcore (naive) 
 # luu cac trang thai trung lap lai
 # giam bot cac trang thai trung lap doi xung nhau

class MinimaxSearch():
    def __init__(self):
        self.init_marks = [['none' for _ in range(3)] for _ in range(3)]
        self.root = State(self.init_marks, 0, 0)
        self.curr = self.root
        self.call=0
        self.create_tree(self.root,self.init_marks,(0,0),0)
       
    def create_tree(self, root, marks, index=0, height=0):
        self.call+=1
        root.marks = marks
        root.height = height
        root.index = index
        root.turn = 'X' if height % 2 == 1 else 'O'
        root.value = 0
        root.children = []
        if not root.check_win(): 
            for i in range(3):
                for j in range(3):
                    if root.marks[i][j] == 'none':
                        # can shallow copy vi phep gan bthg o python la deep copy
                        temp_marks = [row.copy() for row in root.marks]
                        temp_marks[i][j] = 'X' if height % 2 == 0 else 'O'
                        child = State(marks=temp_marks, height=height + 1, index=(i,j))
                        self.create_tree(child, temp_marks, (i,j), height + 1)
                        root.children.append(child)

        root.eval()
    def play(self,game) :
        if game.marks != self.curr.marks:
            for child in self.curr.children :
    
                    if child.marks == game.marks:
                        self.curr = child

        if game.marks == self.curr.marks:
            for child in self.curr.children :
                if child.value == self.curr.value:
                    pos = (((child.index[0]+1)*100)-25,((child.index[1]+1)*100)-25)
                    game.handle_button(pos)
                    self.curr = child
                    break;
      
            





class State():
    # class luu tru cac state 
    def __init__(self,marks, height, index):
        self.marks = marks
        self.height = height
        self.turn = 'X' if height%2 ==1 else 'O'
        self.index = index
        self.value = 0
        self.children = []
    def eval(self):
        """"
                3   2   3
                2   4   2
                3   2   3

                các giá trị sẽ được tính bằng 
                tổng các dấu mà người chơi ở lượt đó đã đánh nhân với trọng só ô
                nếu các dấu đó làm người chơi hay máy thắng, nó sẽ được nhân thêm trọng số 
                để phân biệt với các tổ hợp có trọng số cao hơn trong các trạng thái
                ngoài ra trọng số thắng ở lượt khác nhau cũng khác nhau
                nhằm để giúp máy tìm ra và ưu tiên thắng với ít lượt nhất, không phải lâu mau sao cũng được

        """
        if(not self.children): # không có con , là node lá
            for i in range(0,3):
                for j in range(0,3):
                    if self.marks[i][j] == self.turn:
                        if (i,j) == (1,1):
                            self.value += 4
                        elif (i + j )%2 == 0  :   
                            self.value += 3
                        else :
                            self.value += 2  
            if(self.check_win()):
                self.value *= 2**(9-self.height+1) 
            for i in range(0,3):
                for j in range(0,3):
                    if self.marks[i][j] != self.turn and self.marks[i][j] != 'none':
                        if (i,j) == (1,1):
                            self.value -= 4
                        elif (i + j )%2 == 0  :   
                            self.value -= 3
                        else :
                            self.value -= 2
            self.value = abs(self.value)* (-1)**(self.height%2+1 )
        else :  # node nội
            if self.height%2 == 0:  
                self.value = max(child.value for child in self.children)
            else: 
                self.value = min(child.value for child in self.children)
    def check_win(self):
        win = True;
          #check hang ngang 
        for y in range(0,3):
            for x in range(0,3):
                win = win and (self.marks[x][y]==self.turn)
            if win == True :
                return True
            else :
                win = True # set lai true de check cai khac

         #check hang doc
        for x in range(0,3):
            for y in range(0,3):
                win = win and (self.marks[x][y]==self.turn)
            if win == True :
                return True
            else :
                win = True # set lai true de check cai khac
         #check hang cheo 
          #cheo 1
        for i in range (0,3):
            win = win and (self.marks[i][i]==self.turn)
        if win == True :
                return True
        else :
                win = True # set lai true de check cai khac
            #cheo 2
        for i in range (0,3):
            win = win and (self.marks[i][2-i]==self.turn)
        if win == True :
                return True
        else :
                win = True # set lai true de check cai khac
        self.winner = 'none'
        return False
