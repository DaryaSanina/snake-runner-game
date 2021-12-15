from pygame.sprite import Sprite


class RoadPart(Sprite):
    def __init__(self, x, y, side, *group):
        super(RoadPart, self).__init__(*group)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.rect.height = side
    # TODO
    pass


class Snake(Sprite):
    def __init__(self, velocity, *group):
        super(Snake, self).__init__(*group)
        self.velocity = velocity
    # TODO


class Monster(Sprite):
    def __init__(self, *group):
        super(Monster, self).__init__(*group)
    # TODO
    pass


class Apple(Sprite):
    def __init__(self, *group):
        super(Apple, self).__init__(*group)
    # TODO
    pass
