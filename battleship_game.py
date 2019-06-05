import pygame
import sys, time, math
from battleship_network import Network

#Grid variables
Grid_Height = 40
Grid_Width = 40
Grid_Margin = 10

#define colors
BLACK = 0, 0, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
WHITE = 255,255,255
GRAY = 128, 128, 128

#location for asset to be printed
x = (600 * 0.20)
y = (600 * 0.10)

class Player():
    width = height = 600

    #defines the self object with the variables
    def __init__(self, color=GRAY):
        self.gridShips = []
        self.gridHits = []
        self.color = color
        
        #initializes the grid columns and rows
        for row in range(10):
            self.gridHits.append([])
            for column in range(10):
                self.gridHits[row].append(0)
                
        for row in range(10):
            self.gridShips.append([])
            for column in range(10):
                self.gridShips[row].append(0)

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def setShips(self, gridOfShips): 
        self.gridShips = gridOfShips
       
    def target(self, gridOfHits):
        self.gridHits = gridOfHits

#Game object that contains the network connection
#Defines the player object contained in the game as well
class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player()
        self.canvas = Canvas(self.width, self.height, "Battleship")
        self.stage = "set"
        self.win_flag = None

    #runs the self object, with timing from the clock
    def run(self):
        clock = pygame.time.Clock()
        
        mouse = pygame.mouse.get_pos()
            
        grid = []
        grid2 = []
        
        #initializes the grids with values
        for row in range(10):
            grid.append([])
            for column in range(10):
                grid[row].append(0)
                
        for row in range(10):
            grid2.append([])
            for column in range(10):
                grid2[row].append(0)
                    
        run = True
        ship_count = 0
        attempt = False
        while run:

            #main loop that takes care of the event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                #exits the game
                elif event.type == pygame.K_ESCAPE:
                    run = False

                #detects the mouse down event, so we can shoot and such
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    #performs math to convert pygame grid values to integer grid values
                    column = int(math.floor(pos[0]/50))
                    row = int(math.floor(pos[1]/50))
                    
                    #prevents the arrays from going out of bounds due to player misinput
                    if(self.stage == "set" and (ship_count > 9 or column > 9 or row > 9)):
                        print("Outside out bounds")
                    if(self.stage == "hit" and ((column < 10 and column < 21) or row > 9)):
                        print("Hit - Outside out bounds")
                    elif(self.stage == "set"):
                        print("Click ",pos, "Grid cords: ",row,column)
                        if(column < 10 and row < 10):
                            if grid[row][column] != 1:
                                ship_count = ship_count + 1
                                grid[row][column] = 1    #need to do math with 500 / use player object
                    #target == 1, hit == 2, miss == 3
                    elif(self.stage == "hit"):
                        print("Target ",pos, "Grid cords: ",row,column)
                        if grid2[row][column-11] == 0:
                            grid2[row][column-11] = 1 
                            attempt = True
        
                    
            # Send Network Stuff to set the stage to play
            if ship_count == 10 and self.stage == "set":
                self.player.setShips(grid)
                reply = self.parse_data(self.send_data("set"))
            
            # Send Network Stuff to shoot and play the game
            if self.stage == "hit" and attempt == True:
                self.player.target(grid2)
                response = self.parse_data(self.send_data("hit"))
                attempt = False; 
            
            #draws the background
            self.canvas.draw_background()
            
            #draws the grids and the background
            for row in range(10):
                for column in range(10):
                    color = GRAY
                    if grid[row][column] == 1:
                        color = WHITE
                    pygame.draw.rect(self.canvas.get_canvas(),color,[(Grid_Margin + Grid_Width) * column + Grid_Margin,(Grid_Margin + Grid_Height) * row + Grid_Margin,Grid_Width,Grid_Height])

                    #draw borders around the grids
                    pygame.draw.line(self.canvas.get_canvas(),WHITE,[0,510],[500,510],10)
                    pygame.draw.line(self.canvas.get_canvas(),WHITE,[510,0],[510,510],10)
                    
                    
            for row in range(10):
                for column in range(10):
                
                    #Set color schemes for the grids. Red is ihit, black is miss, white is nothing
                    color = GRAY
                    if self.player.gridHits[row][column] == 2:
                        color = RED
                    elif self.player.gridHits[row][column] == 3:
                        color = BLACK
                    elif self.player.gridHits[row][column] == 1:
                        color = WHITE
                        
                    pygame.draw.rect(self.canvas.get_canvas(),color,[(Grid_Margin + Grid_Width) * (column + 11) + Grid_Margin,(Grid_Margin + Grid_Height) * row + Grid_Margin,Grid_Width,Grid_Height])

                    pygame.draw.line(self.canvas.get_canvas(),RED,[540,510],[1050,510],10)
                    pygame.draw.line(self.canvas.get_canvas(),RED,[530,0],[530,510],10)
                    
            
            if(self.win_flag == True):
                self.canvas.draw_text("YOU WIN", 100, 80, 80)
            elif(self.win_flag == False):
                self.canvas.draw_text("YOU LOSE", 100, 80, 80)
            
            self.canvas.update() #updates display
            
            clock.tick(60)

        pygame.quit()

    #Sends the data to everyone
    def send_data(self, stage):
        """
        Send position to server
        :return: None
        """
        reply = ""
        if(stage == "set"):
            for row in range(10):
                    for column in range(10):
                        if self.player.gridShips[row][column] == 1:
                            data = "SET|" + str(self.net.id) + ":" + str(row) + "," + str(column) 
                            reply += self.net.send(data)
            print(self.net.id)
            print(reply)
            while self.stage != "hit":
                time.sleep(1)
                if "BOTH" in reply:
                    self.stage = "hit"
                else:
                    data = "ASK|" + str(self.net.id) + ":" + "ASK"
                    reply = self.net.send(data)
                
            
        #If we get a hit, we parse out the data and updated with a fail or a hit
        elif(stage == "hit"):
            for row in range(10):
                    for column in range(10):
                        if self.player.gridHits[row][column] == 1:
                            data = "HIT|" + str(self.net.id) + ":" + str(row) + "," + str(column) 
                            reply = self.net.send(data)
                            print(reply)
                            if "Success" in reply:
                                self.player.gridHits[row][column] = 2
                                print("HIT")
                            elif "Fail" in reply:
                                self.player.gridHits[row][column] = 3
                                print("MISS")
                            elif "WON" in reply:
                                if((("2 WON" in reply) and (self.net.id == "1")) or (("1 WON" in reply) and (self.net.id == "0"))):
                                    self.player.gridHits[row][column] = 2
                                    print("YOU WIN")
                                    self.win_flag = True
                                else:
                                    print("YOU LOSE")
                                    self.win_flag = False
                              
                            
        return reply

    #splits up the data into usuable tokens
    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

#Canvas class is what the game draws on, and what the game acts on
class Canvas:

    def __init__(self, w, h, name="Battleship"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        #shipImg = pygame.image.load("BattleShip.png")
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    #draws the text on the pygame canvas object
    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, RED)

        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(BLUE)