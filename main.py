from grid import Grid
from game import Game
from minimax import MinimaxSearch
from settings import *
class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
        pygame.display.set_caption('Cờ ca rô')
        self.display_surface.fill(BLACK)
        self.game = Game()
        self.grid = Grid()
        self.agent = MinimaxSearch()
        self.agent_played = True #  biến để đồng bộ cho phép máy chơi 1 lần sau đó lắng nghe người dùng 
    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Lang nghe event quit ( dau X goc phai tren)
                    pygame.quit()                   # dong cua so
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if(self.game.handle_button(pygame.mouse.get_pos())): # cần true false vì 1 số trường hợp người chơi bấm ngoài rìa màn hình k hợp lệ khiến agent tự chơi
                        print(" player played")
                        self.agent_played = False
                if not self.agent_played:
                    print("agent start to play")
                    self.agent.play(self.game)
                    self.agent_played = True
            self.game.run()                          # thoat het chuong trinh py
            self.grid.run()
            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()