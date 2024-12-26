from settings import *

class Grid():
    def __init__(self):
        self.line_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.display_surface.set_alpha(255)  # Set display surface to fully opaque
        self.line_surface.fill(GREY)  # Fill the surface with white color
        self.line_surface.set_colorkey(GREY)
        self.line_surface.set_alpha(100)  # Set opacity of the surface (0 is fully transparent, 255 is fully opaque)
        pygame.display.set_caption('Cờ ca rô')
    def draw_grid(self):
            for line in range (1, 3):
                x = line * SQUARE_SIZE -25
                y = line * SQUARE_SIZE -25
        
                pygame.draw.line(self.line_surface,BLACK, (x,0) ,(x,self.line_surface.get_height()),10)
        
                pygame.draw.line(self.line_surface,BLACK, (0,y) ,(self.line_surface.get_width(),y),10)
    def run(self):
        self.draw_grid()
        self.display_surface.blit(self.line_surface,(75,75)) # draw surface len display surface ( cai o ham main), o vi tri 0+....0+...