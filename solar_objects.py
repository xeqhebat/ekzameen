# coding: utf-8
# license: GPLv3

class Star:
    """Тип данных, описывающий звезду."""
    def __init__(self):
        self.type = "star"
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0
        self.R = 5
        self.color = "red"
        self.image = None

class Planet:
    """Тип данных, описывающий планету."""
    def __init__(self):
        self.type = "planet"
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0
        self.R = 5
        self.color = "green"
        self.image = None
        
        # Параметры
        self.star = None          # Ссылка на родительскую звезду
        self.orbit_number = 0     # Номер орбиты
        self.orbit_radius = 0     # Радиус орбиты
        self.angle = 0.0          # Текущий полярный угол
        self.speed = 0.0          # Угловая скорость движения
        self.orbit_image = None   # Графический ID орбиты
        self.moons = []           # Список спутников
        self.moon_images = []     # Графические ID спутников

class Moon:
    """Тип данных, описывающий спутник планеты."""
    def __init__(self):
        self.type = "moon"
        self.x = 0
        self.y = 0
        self.R = 2
        self.color = "white"
        self.orbit_radius = 0     # Радиус обращения
        self.angle = 0.0          # Текущий угол спутника
        self.speed = 0.0          # Угловая скорость спутника