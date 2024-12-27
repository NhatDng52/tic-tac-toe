from settings import *
from game import Game
 # search hardcore (naive) 
 # luu cac trang thai trung lap lai
 # giam bot cac trang thai trung lap doi xung nhau
"""
    Đối với minimax kết hợp alpha beta prunning , node cha cần xử lý node con ngay khi vừa đệ quy xong, để xét xem cần tỉa cây hay không
    Vì thế phần code của create tree sẽ được sửa về mặt logic và thêm 2 tham số alpha beta khi gọi hàm
    Việc này giúp giảm trạng thái xuống còn 65591 node so với 549946 node như trước kia ( được tính qua biến call mỗi lần create tree được gọi)
    Nhược điểm khi sử dụng abprunning:
        - Vì giải thuật giả sử máy và người chơi đều chơi các nước tối ưu (đánh giá bằng hàm eval)
        - Abprunning dựa vào đó mà cắt các nhánh chứa các state không tối ưu của cả 2
        - Khi người chơi đánh nước không tối ưu, máy sẽ không tìm thấy state đó ( do đã bị cắt mất).
        - Điều này có thể khắc phục bằng cách :
            +   Dùng hàm đánh giá trạng thái ngay lập tức ( đánh giá không dựa hoàn toàn vào kết quả thắng thua như hàm eval mình đã làm)  
            +   Chỉ cắt nhánh của máy chơi ( cho phép người chơi đánh nhiều state không tối ưu, còn máy vẫn chỉ đánh 1 state tối ưu)
"""
class AlphaBetaPrunning():
    def __init__(self):
        self.init_marks = [['none' for _ in range(3)] for _ in range(3)]
        self.root = State(self.init_marks, 0, 0)
        self.curr = self.root
        self.alpha = float ('-inf')
        self.beta = float ('inf')
        self.call = 0
        # self.create_tree(self.root,self.init_marks,(0,0),0,self.alpha,self.beta)

    def create_tree(self, root, marks, index=0, height=0,alpha = float('-inf'),beta =float('inf')):
        self.call+=1
        root.marks = marks
        root.height = height
        root.index = index
        root.turn = 'X' if height % 2 == 1 else 'O'
        root.value = 0
        root.children = []
        prunning = False
        if not root.check_win(): 
            for i in range(3):
                for j in range(3):
                    if root.marks[i][j] == 'none':

                        # can shallow copy vi phep gan bthg o python la deep copy
                        temp_marks = [row.copy() for row in root.marks]
                        temp_marks[i][j] = 'X' if height % 2 == 0 else 'O'
                        child = State(marks=temp_marks, height=height + 1, index=(i,j))
                        temp_alpha = alpha  # shallow cpy vi no la dang float
                        temp_beta = beta
                        self.create_tree(child, temp_marks, (i,j), height + 1,temp_alpha,temp_beta)
                        if(root.height%2 == 0):     # MAX node , update alpha
                            if child.value > alpha and child.value <beta:
                                alpha = child.value
                            elif child.value > beta :
                                prunning = True
                    
                        else:               # MIN node, update beta            
                            if child.value > alpha and child.value < beta:
                                beta = child.value
                            elif child.value < alpha :
                                prunning = True
                        root.children.append(child)


        
                    if prunning:
                        break
                if prunning:
                    break
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
