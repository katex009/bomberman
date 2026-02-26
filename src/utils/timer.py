class Timer:
    def __init__(self, duration: float):
        self.duration = duration
        self.time = 0

    def update(self, dt: float) -> bool:
        self.time += dt
        if self.time >= self.duration:
            self.time = 0
            return True
        return False

    def reset(self):
        self.time = 0