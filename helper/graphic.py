import matplotlib.pyplot as plt

class Plot:
    graphicElement = []

    def __init__(self,title):
        plt.title(title)
        self.clear()

    def show(self):
        for i in self.graphicElement:
            plt.plot(i[1], i[2], label=i[0], linewidth = 1)
        plt.legend()
        plt.show()

    def add_dot(self, name, y):
        control = False
        for i in self.graphicElement:
            if i[0] == name:
                control = True
                i[1].append(len(i[1])+1)
                i[2].append(y)
        if not control:
            self.graphicElement.append([name,[1],[y]])

    def clear(self):
        self.graphicElement.clear()

