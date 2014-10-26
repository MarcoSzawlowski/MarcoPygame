class Players:
    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += 3.6

    def draw(self, win):
        pass

    def xset_vel(self, x):
        self.velocity[0] = x

    def yset_vel(self, y):
        self.velocity[1] = y


