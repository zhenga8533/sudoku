class tile:
    def __init__(self, num=0, locked=False):
        self.num = num
        self.locked = locked

    def reset(self):
        self.num = 0
        self.locked = False

    def set(self, num):
        self.num = num

    def lock(self, num):
        self.num = num
        self.locked = True
