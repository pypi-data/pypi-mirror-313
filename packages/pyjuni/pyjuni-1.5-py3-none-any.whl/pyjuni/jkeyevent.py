from pynput import keyboard

class JKeyEvent:
    def on_press(self, key):
        if key == keyboard.Key.enter:
            self.keyEnter = True
        if key == keyboard.Key.space:
            self.keySpace = True
        if key == keyboard.Key.up:
            self.keyUp = True
        if key == keyboard.Key.down:
            self.keyDown = True
        if key == keyboard.Key.right:
            self.keyRight = True
        if key == keyboard.Key.left:
           self.keyLeft = True
        if key == keyboard.Key.esc:
           self.keyEsc = True

    def on_release(self, key):
        if key == keyboard.Key.enter:
            self.keyEnter = False
        if key == keyboard.Key.space:
            self.keySpace = False
        if key == keyboard.Key.up:
            self.keyUp = False
        if key == keyboard.Key.down:
            self.keyDown = False
        if key == keyboard.Key.right:
            self.keyRight = False
        if key == keyboard.Key.left:
            self.keyLeft = False
        if key == keyboard.Key.esc:
           self.keyEsc = False

    def __init__(self):
        self.keyEnter = False
        self.keySpace = False   
        self.keyUp = False
        self.keyDown = False
        self.keyLeft = False
        self.keyRight = False
        self.keyEsc = False

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def isKeyEnterPressed(self):
        return self.keyEnter

    def isKeySpacePressed(self):
        return self.keySpace
        
    def isKeyUpPressed(self):
        return self.keyUp

    def isKeyDownPressed(self):
        return self.keyDown

    def isKeyLeftPressed(self):
        return self.keyLeft

    def isKeyRightPressed(self):
        return self.keyRight

    def isKeyEscPressed(self):
        return self.keyEsc
