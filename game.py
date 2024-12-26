from settings import *

#data

class Game():
    def __init__(self):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.display_surface.set_alpha(255)  # Set display surface to fully opaque
        self.surface.fill(WHITE)  # Fill the surface with white color
        self.surface.set_alpha(100)  # Set opacity of the surface (0 is fully transparent, 255 is fully opaque)
        self.marks =  [['none' for _ in range(3)] for _ in range(3)]
        self.turn = 'X'
        self.winner = 'none'
    def run(self):
        self.display_surface.blit(self.surface,(0+PADDING,0+PADDING)) # draw surface len display surface ( cai o ham main), o vi tri 0+....0+...
    
    def mark(self,pos,player):
        if pos[0] > 3 and pos[1] <0:
            raise IndexError(" Index out of range when player mark") 
        up_x = pos[0] * 100 + 25 + 20
        up_y = pos[1] * 100 + 25 + 20
        down_x = up_x + 60
        down_y = up_y + 60
        print(f"up_x = {up_x}, down_x = {down_x}, up_y = {up_x}, down_y = {down_y}")
        # to hop 4 thang nay ta co topleft toright bottomleft bottomright
        if player == 'X':
            pygame.draw.line(self.surface, BLACK,
                                 (up_x,up_y),
                                 (down_x,down_y), 10)
            pygame.draw.line(self.surface, BLACK,
                                 (up_x,down_y),
                                 (down_x,up_y), 10) 
        elif player == 'O':
            pygame.draw.circle(self.surface, RED,
                                   ((down_x+up_x)/2,(down_y+up_y)/2 ),
                                   60/1.4, 10)
    def check_rule(self,pos):
       
        x = (pos[0])
        y = (pos[1])
        if (x > 2 or x < 0):
             return False
        if (y > 2 or y < 0):
             return False
        if(self.marks[x][y] == 'none'):
            return True
        else :
            return False
    def check_win(self):
        win = True;
        self.winner = self.turn
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
        
    def handle_button(self,pos):
        x = (pos[0]+25)//100 -1
        y = (pos[1]+25)//100 -1
        if(self.check_rule((x,y))):
            self.mark((x,y),self.turn)
            self.marks[x][y] = self.turn
            if(self.check_win()):
                print (f" co nguoi thang r do la {self.turn}")
            #chuyen luot cho ng khac
            self.turn ='X' if self.turn =='O' else 'O'
            return True
        return False