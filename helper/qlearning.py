from random import randint, choice,uniform

class QLearning:
    directionMatrix = [[-1, 0 ],  # up
                       [-1, 1 ],  # up-right
                       [ 0, 1 ],  # right
                       [ 1, 1 ],  # down-right
                       [ 1, 0 ],  # down
                       [ 1,-1 ],  # down-left
                       [ 0,-1 ],  # left
                       [-1,-1 ]]  # up-left
    matrix = []                   # Matris
    RTable = []                   # R tablosu
    QTable = []                   # Q tablosu
    startPos = []                 # Başlangıç koordinatı
    targetPos = []                # Hedef koordinatı
    learningRate = 0.8            # Öğrenme oranı
    currentState = []             # Ajanın aktif konumu
    previousState = []            # Ajanın önceki konumu
    action = 0                    # Ajanın yaptığı hareketin yönü
    learnedPath = []              # Öğrenilmiş en kısa yol
    path = []                     # Her denemenin tutulduğu geçici yol değişkeni
    cost = 0                      # Her yol denemesinde edinilen kazanç
    wallRate = 3                # Matristeki engel oranı

    ## CONSTRUCTER ##
    def __init__(self, row, column, moveScore, wallScore, targetScore, outsideScore):
        self.row = row
        self.column = column
        self.moveScore = moveScore
        self.wallScore = wallScore
        self.targetScore = targetScore
        self.outsideScore = outsideScore
        self.create_matrix()

    ## R veya Q Matris isminden koordinat ##
    def coord_from_name(self, name):
        for x in range(self.row):
            for y in range(self.column):
                if (y + (self.column * x)) == name:
                    return [x, y]

    ## Koordinattan R veya Q Matris ismi  ##
    def name_from_coord(self, coord):
        return coord[1] + (self.column * coord[0])

    ## Matrise göre girilen koordinattan aksiyon sonucu elde edilen r tablosu değeri ##
    def r_value_from_matrix(self, state, action):
        statePos = self.coord_from_name(state)
        actionPos = self.directionMatrix[action]
        actionPos = [statePos[0] + actionPos[0], statePos[1] + actionPos[1]]
        if 0 <= actionPos[0] < self.row and 0 <= actionPos[1] < self.column:
            if self.matrix[actionPos[0]][actionPos[1]] == 0:
                return self.moveScore
            elif self.matrix[actionPos[0]][actionPos[1]] == 1:
                return self.wallScore
        else:
            return self.outsideScore

    ## Matris, Q Tablosu, R Tablosu oluşturma ##
    def create_matrix(self):
        self.matrix.clear()
        self.QTable.clear()
        self.RTable.clear()
        self.startPos = [-1,-1]
        self.targetPos = [-1,-1]
        self.currentState = []
        self.previousState = []

        for i in range(self.row):
            temp = []
            for j in range(self.column):
                if randint(0, 9) < self.wallRate:
                    temp.append(1)
                else:
                    temp.append(0)
            self.matrix.append(temp)

        for i in range(self.row * self.column):
            tempQtable = []
            tempRtable = []
            for j in range(8):
                tempQtable.append(0)
                tempRtable.append(0)
            self.QTable.append(tempQtable)
            self.RTable.append(tempRtable)

        for x in range(len(self.RTable)):
            for y in range(8):
                self.RTable[x][y] = self.r_value_from_matrix(x, y)

    ## R tablosu güncelleme ##
    def update_r_table(self, coord, stateType, add = False):
        for i in range(8):
            if self.action_control(coord, i):
                temp = self.action_coord(coord, i)
                tempAction = i + 4 if 0 <= i < 4 else i - 4
                self.RTable[self.name_from_coord(temp)][tempAction] = (self.wallScore if stateType == "wall" else self.targetScore) if add else self.moveScore

    ## Başlangıç poziyonunu belirle ##
    def start_position(self, x, y):
        self.startPos = [x, y]
        self.currentState = self.startPos
        self.previousState = self.currentState

    ## Hedef pozisyonunu belirle ##
    def target_position(self, x, y):
        self.targetPos = [x, y]

    ## Girilen state'ten aksiyon yönüne hareket sonrası bulunulan koordinat ##
    def action_coord(self, state, action):
        return [state[0] + self.directionMatrix[action][0], state[1] + self.directionMatrix[action][1]]

    ## Girilen state'in aksiyon yönünde hareketi mümkün mü? ##
    def action_control(self, state, action):
        actionCoord = self.action_coord(state, action)
        return True if 0 <= actionCoord[0] < self.row and 0 <= actionCoord[1] < self.column else False

    ## Aksiyon seç ##
    def choose_action(self, state):
        # if random.uniform(0, 1) < 0.98:
        temp_Q_row = self.QTable[self.name_from_coord(state)]
        temp_R_row = self.RTable[self.name_from_coord(state)]
        temp_Q_List = []
        for i in range(len(temp_R_row)):
            if temp_R_row[i] != -100:
                temp_Q_List.append(temp_Q_row[i])
        maxValue = max(temp_Q_List)

        temp_Selectable = []
        for i in range(len(temp_Q_row)):
            if temp_R_row[i] != -100 and temp_Q_row[i] == maxValue:
                temp_Selectable.append(i)

        return choice(temp_Selectable)

    ## State'ten Action yönündeki Q tablosu değerini hesaplar. ##
    def calculate_q_value(self, state, action):
        actionCoord = self.action_coord(state, action)
        maxValueOfAction = self.QTable[self.name_from_coord(actionCoord)][self.choose_action(actionCoord)]
        return self.RTable[self.name_from_coord(state)][action] + (self.learningRate * maxValueOfAction)

    ## Matris üzerinde tek kare hareket ve konum kontrolü ##
    def move(self):
        self.path.append(self.currentState)
        self.previousState = self.currentState
        self.action = self.choose_action(self.currentState)
        self.currentState = self.action_coord(self.currentState, self.action)
        self.QTable[self.name_from_coord(self.previousState)][self.action] = self.calculate_q_value(self.previousState, self.action)
        self.cost += self.QTable[self.name_from_coord(self.previousState)][self.action]

        if self.currentState == self.targetPos:
            self.path.append(self.currentState)
            tempPath = self.path.copy()
            tempCost = self.cost
            self.path.clear()
            self.cost = 0
            self.currentState = self.startPos
            self.previousState = self.currentState
            return 2, tempPath, tempCost

        elif self.matrix[self.currentState[0]][self.currentState[1]] == 1:
            self.path.append(self.currentState)
            tempPath = self.path.copy()
            tempCost = self.cost
            self.path.clear()
            self.cost = 0
            self.currentState = self.startPos
            self.previousState = self.currentState
            return 1, tempPath, tempCost

        elif self.matrix[self.currentState[0]][self.currentState[1]] == 0:
            return 0, [], 0
