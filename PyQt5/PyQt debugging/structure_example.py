class Connect:

    def __init__(self, window):# same as in custmoize
        self.window = window

    def reset_window(self):
        self.window = 0

class Customize:

    def __init__(self, window):
        self.window = window # setting the varaible as the main draw screen

    def reset_window(self): # example function for anything 
        self.window = 0

class Send: # same as in Customize

    def __init__(self, window):
        self.window = window

    def reset_window(self):
        self.window = 0


class App:

    def __init__(self):
        self.window = 4 # the main object surface the appp varaible
        self.connect = Connect(self.window) # the class for connection, it passes the main app argument
        self.customize = Customize(self.window) # the class for customization, it passes the main app argument
        self.send = Send(self.window) # the class for sending the results, it passes the main app argument