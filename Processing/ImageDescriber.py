class ImageDescriber:
    def __init__(self, img, surf):
        self.img = img
        self.surf = surf
        self.kp = None
        self.desc = None

    def detectAndCompute(self):
        self.kp, self.desc = self.surf.detectAndCompute(self.img, None)
        self.desc.shape = (-1, self.surf.descriptorSize())
