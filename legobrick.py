class Lego(object):
    def __init__(self):
        self.active = False
        self.colour = None
        self.coords = ()
        pass

    def get_colour(self):
        return self.colour
    
    def get_xy(self):
        return self.coords[0], self.coords[1]
    
    def activate(self):
        self.active = True
        pass

    def deactivate(self):
        self.active = False
        pass

    def update(self, colour, coords):
        self.activate()
        self.colour = colour
        x,y = coords[0], coords[1]
        self.coords = (x,y)
        pass

##test comment