from helper.qlearning import QLearning
from helper.graphic import Plot
from helper.file_operation import FileOperation
from settings.screen import Screen
from settings.colors import Colors
import pygame

class Game:
    pygame.init()

    ## CONTROLLER ##
    APP_RUNNING = True
    DRAWING = False
    DRAWING_WALL = False
    DRAWING_WALL_ADD_OR_REMOVE = False
    DRAWING_START = False
    DRAWING_TARGET = False
    DRAWING_ONETIME = False
    MOUSE_PREV_POS = (0, 0)
    LEARNING = False
    TEMP_PATH = []
    SHORTEST_PATH = []
    IS_LEARNED = 0
    FOUND_PATH_COUNT = 0
    SHOWLEARNEDPATH = False
    FILE_WRITER = FileOperation()
    BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
    BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
    BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
    BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
    BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
    BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
    TEXT_FONT = pygame.font.SysFont("calibri", 30)
    #####################

    ## BUTTONS ##
    TEXT_WALL = TEXT_FONT.render("Engel", True, (255, 255, 255))
    TEXT_START = TEXT_FONT.render("Başlangıç", True, (255, 255, 255))
    TEXT_TARGET = TEXT_FONT.render("Hedef", True, (255, 255, 255))
    TEXT_PLAY = TEXT_FONT.render("Başlat", True, (255, 255, 255))
    TEXT_STOP = TEXT_FONT.render("Durdur", True, (255, 255, 255))
    TEXT_PLOT = TEXT_FONT.render("Grafik", True, (255, 255, 255))
    TEXT_RESTART = TEXT_FONT.render("Sıfırla", True, (255, 255, 255))
    WALL = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP, TEXT_START.get_width() + 10, 40)
    START = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP + 50, TEXT_START.get_width() + 10, 40)
    TARGET = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP + 100, TEXT_START.get_width() + 10, 40)
    PLAY = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP + 150, TEXT_START.get_width() + 10, 40)
    PLOT = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP + 200, TEXT_START.get_width() + 10, 40)
    RESTART = pygame.Rect(Screen.MENU_X + Screen.GRID_GAP + 20, Screen.GRID_GAP + 250, TEXT_START.get_width() + 10, 40)
    #####################

    qlearning = None

    def __init__(self, row, column):
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT),pygame.HWSURFACE)
        pygame.display.set_caption("Q-LEARNING")
        self.screen.fill((255, 255, 255))
        pygame.display.update()
        self.qlearning = QLearning(row=row, column=column, moveScore=-0.1, wallScore=-50, targetScore=100, outsideScore=-100)
        self.calculate_grid_size()
        self.refresh_screen()
        self.plt = Plot("Kazanç, Adım sayısı Grafiği")



    def calculate_grid_size(self):
        if self.qlearning.row >= self.qlearning.column:
            Screen.GRID_SIZE = (
                    (Screen.HEIGHT - (Screen.GRID_LINE_BORDER * (self.qlearning.row + 1))- (Screen.GRID_GAP * 2))
                    / self.qlearning.row)
        else:
            Screen.GRID_SIZE = (
                    (Screen.HEIGHT - (Screen.GRID_LINE_BORDER * (self.qlearning.column + 1)) - (Screen.GRID_GAP * 2))
                    / self.qlearning.column)

    @staticmethod
    def getMousePosInMatrix(arg):
        if arg[0] > Screen.GRID_GAP and arg[1] > Screen.GRID_GAP:
            x = (arg[0] - Screen.GRID_GAP) / (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER)
            y = (arg[1] - Screen.GRID_GAP) / (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER)
        else:
            x = -1
            y = -1
        return [int(y), int(x)]

    def refresh_screen(self):
        self.screen.fill(Colors.COLOR_BACKGROUND)
        pygame.draw.rect(self.screen, color=Colors.COLOR_SIDEMENU,
                                      rect=[Screen.HEIGHT, 0, Screen.MENU_WIDTH, Screen.HEIGHT])
        if self.LEARNING:
            pygame.draw.rect(self.screen, Colors.BTN_COLOR_ACTIVE, self.PLAY)
            self.screen.blit(self.TEXT_STOP, (self.PLAY.x + 5, self.PLAY.y + 5))
        else:
            pygame.draw.rect(self.screen, Colors.BTN_COLOR_PASSIVE, self.PLAY)
            self.screen.blit(self.TEXT_PLAY, (self.PLAY.x + 5, self.PLAY.y + 5))

        pygame.draw.rect(self.screen, self.BTN_COLOR_WALL, self.WALL)
        self.screen.blit(self.TEXT_WALL, (self.WALL.x + 5, self.WALL.y + 5))
        pygame.draw.rect(self.screen, self.BTN_COLOR_START, self.START)
        self.screen.blit(self.TEXT_START, (self.START.x + 5, self.START.y + 5))
        pygame.draw.rect(self.screen, self.BTN_COLOR_TARGET, self.TARGET)
        self.screen.blit(self.TEXT_TARGET, (self.TARGET.x + 5, self.TARGET.y + 5))
        pygame.draw.rect(self.screen, self.BTN_COLOR_PLOT, self.PLOT)
        self.screen.blit(self.TEXT_PLOT, (self.PLOT.x + 5, self.PLOT.y + 5))
        pygame.draw.rect(self.screen, self.BTN_COLOR_RESTART, self.RESTART)
        self.screen.blit(self.TEXT_RESTART, (self.RESTART.x + 5, self.RESTART.y + 5))

        for x in range(self.qlearning.row):
            for y in range(self.qlearning.column):
                pygame.draw.rect(self.screen, color=Colors.COLOR_LINE,
                                              rect=[
                                                (y * (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER)) + Screen.GRID_GAP,
                                                (x * (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER)) + Screen.GRID_GAP,
                                                Screen.GRID_SIZE + (Screen.GRID_LINE_BORDER * 2),
                                                Screen.GRID_SIZE + (Screen.GRID_LINE_BORDER * 2)],
                                                width=Screen.GRID_LINE_BORDER)

                if self.qlearning.matrix[x][y] == 1:
                    pygame.draw.rect(self.screen, color=Colors.COLOR_WALL,
                                                  rect=[
                                                    (y * (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                                    + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                                    (x * (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                                    + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                                    Screen.GRID_SIZE,
                                                    Screen.GRID_SIZE])

        rate = [0,0, 155 / (len(self.TEMP_PATH) - 1)]
 
        tempPath = self.SHORTEST_PATH if self.SHOWLEARNEDPATH else self.TEMP_PATH
        for x in range(len(tempPath)-1):
            pygame.draw.rect(self.screen, color=(0, 0, 100 + rate[2] * x),
                                          rect=[
                                            (tempPath[x][1]*(Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                            + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                            (tempPath[x][0]*(Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                            + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                            Screen.GRID_SIZE,
                                            Screen.GRID_SIZE])

        if self.qlearning.startPos != [-1, -1]:
            pygame.draw.rect(self.screen, color=Colors.COlOR_START,
                                          rect=[
                                            (self.qlearning.startPos[1] *
                                            (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                            + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                            (self.qlearning.startPos[0] *
                                            (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                            + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                            Screen.GRID_SIZE,
                                            Screen.GRID_SIZE])

        if self.qlearning.targetPos != [-1, -1]:
            pygame.draw.rect(self.screen, color=Colors.COLOR_TARGET,
                             rect=[
                                 (self.qlearning.targetPos[1] *
                                  (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                 + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                 (self.qlearning.targetPos[0] *
                                  (Screen.GRID_SIZE + Screen.GRID_LINE_BORDER))
                                 + Screen.GRID_GAP + Screen.GRID_LINE_BORDER,
                                 Screen.GRID_SIZE,
                                 Screen.GRID_SIZE])

        pygame.display.update()

    def mainLoop(self):

        ## MAIN LOOP
        while self.APP_RUNNING:
            self.refresh_screen()

            ## LEARNING - Sadece hedefe ulaştığında çizim
            while self.LEARNING:
                status, self.TEMP_PATH, cost = self.qlearning.move()
                if status != 0: # Hedefe ulaşmadıysa veya duvara çarpmadıysa
                    if status == 2:
                        if self.TEMP_PATH == self.SHORTEST_PATH:
                            if self.IS_LEARNED == 50:
                                self.LEARNING = False
                                self.SHOWLEARNEDPATH = True
                                self.FILE_WRITER.OutputFile(self.qlearning.matrix,
                                                            self.qlearning.startPos,
                                                            self.qlearning.targetPos,
                                                            self.SHORTEST_PATH)
                                self.refresh_screen()
                                self.plt.show()
                            else:
                                self.IS_LEARNED += 1
                        else:
                            self.SHORTEST_PATH = self.TEMP_PATH.copy()
                            self.IS_LEARNED = 0

                        self.plt.add_dot("Kazanç/Maliyet", cost)
                        self.plt.add_dot("Adım Sayısı", len(self.TEMP_PATH))
                    break

            for e in pygame.event.get():

                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1:
                        self.DRAWING = False
                        Colors.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                        Colors.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                        self.refresh_screen()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mousePrevPos = self.getMousePosInMatrix(pygame.mouse.get_pos())

                    if e.button == 1:
                        if 0 <= mousePrevPos[0] < self.qlearning.row and 0 <= mousePrevPos[1] < self.qlearning.column:
                            self.DRAWING_ONETIME = True
                            self.DRAWING = True
                        if self.WALL.collidepoint(e.pos):
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_ACTIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            self.DRAWING_WALL = True
                            self.DRAWING_START = False
                            self.DRAWING_TARGET = False
                            self.refresh_screen()

                        elif self.START.collidepoint(e.pos):
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_ACTIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            self.DRAWING_WALL = False
                            self.DRAWING_START = True
                            self.DRAWING_TARGET = False
                            self.refresh_screen()

                        elif self.TARGET.collidepoint(e.pos):
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_ACTIVE
                            self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            self.DRAWING_WALL = False
                            self.DRAWING_START = False
                            self.DRAWING_TARGET = True
                            self.refresh_screen()

                        elif self.PLAY.collidepoint(e.pos)\
                                and self.qlearning.startPos != [-1,-1] \
                                and self.qlearning.targetPos != [-1,-1]:
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            if self.LEARNING:
                                self.LEARNING = False
                                self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            else:
                                self.LEARNING = True
                                self.BTN_COLOR_PLAY = Colors.BTN_COLOR_ACTIVE

                        elif self.PLOT.collidepoint(e.pos):
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_ACTIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            self.DRAWING_WALL = False
                            self.DRAWING_START = False
                            self.DRAWING_TARGET = False
                            self.refresh_screen()
                            self.plt.show()
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.refresh_screen()

                        elif self.RESTART.collidepoint(e.pos):
                            self.BTN_COLOR_WALL = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_START = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_TARGET = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLAY = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_PLOT = Colors.BTN_COLOR_PASSIVE
                            self.BTN_COLOR_RESTART = Colors.BTN_COLOR_PASSIVE
                            self.DRAWING_WALL = False
                            self.DRAWING_START = False
                            self.DRAWING_TARGET = False
                            self.TEMP_PATH.clear()
                            self.SHORTEST_PATH.clear()
                            self.SHOWLEARNEDPATH = False
                            self.plt.clear()
                            self.qlearning.create_matrix()
                            self.refresh_screen()

                if self.DRAWING and self.LEARNING != True:
                    temp = self.getMousePosInMatrix(pygame.mouse.get_pos())
                    if self.DRAWING_WALL:
                        if self.DRAWING_ONETIME:
                            if self.qlearning.matrix[temp[0]][temp[1]] == 0:
                                self.qlearning.matrix[temp[0]][temp[1]] = 1
                                self.qlearning.update_r_table(temp, "wall", True)
                                self.DRAWING_WALL_ADD_OR_REMOVE = True
                            else:
                                self.qlearning.matrix[temp[0]][temp[1]] = 0
                                self.qlearning.update_r_table(temp, "wall", False)
                                self.DRAWING_WALL_ADD_OR_REMOVE = False
                            self.DRAWING_ONETIME = False
                            self.MOUSE_PREV_POS = temp
                            self.refresh_screen()
                        if 0 <= temp[0] < self.qlearning.row and 0 <= temp[1] < self.qlearning.column and self.MOUSE_PREV_POS != temp:
                            if self.DRAWING_WALL_ADD_OR_REMOVE:
                                self.qlearning.matrix[temp[0]][temp[1]] = 1
                                self.qlearning.update_r_table(temp, "wall", True)
                            else:
                                self.qlearning.matrix[temp[0]][temp[1]] = 0
                                self.qlearning.update_r_table(temp, "wall", False)
                            self.MOUSE_PREV_POS = temp
                            self.refresh_screen()
                    elif self.DRAWING_START:
                        if self.DRAWING_ONETIME:
                            if self.qlearning.startPos[0] == temp[0] and self.qlearning.startPos[1] == temp[1]:
                                self.qlearning.start_position(-1, -1)
                            else:
                                if self.qlearning.matrix[temp[0]][temp[1]] == 0:
                                    if self.qlearning.targetPos[0] != temp[0] or self.qlearning.targetPos[1] != temp[1]:
                                        self.qlearning.start_position(temp[0], temp[1])
                            self.DRAWING_ONETIME = False
                            self.refresh_screen()
                    elif self.DRAWING_TARGET:
                        if self.DRAWING_ONETIME:
                            if self.qlearning.targetPos[0] == temp[0] and self.qlearning.targetPos[1] == temp[1]:
                                self.qlearning.target_position(-1, -1)
                                self.qlearning.update_r_table(temp, "target", False)
                            else:
                                if self.qlearning.matrix[temp[0]][temp[1]] == 0:
                                    if self.qlearning.startPos[0] != temp[0] or self.qlearning.startPos[1] != temp[1]:
                                        self.qlearning.target_position(temp[0], temp[1])
                                        self.qlearning.update_r_table(temp, "target", True)
                            self.DRAWING_ONETIME = False
                            self.refresh_screen()

                # QUIT
                if e.type == pygame.QUIT:
                    self.APP_RUNNING = False
                    break