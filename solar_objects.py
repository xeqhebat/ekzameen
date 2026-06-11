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
        self.R = 15
        self.color = "red"
        self.image = None
        # Параметры из билета №5
        self.max_per_orbit = 3
        self.base_orbit = 40
        self.orbit_gap = 25
        self.planets_count = 0 

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
        
        # Орбитальные параметры
        self.star = None          # Ссылка на родительскую звезду
        self.orbit_number = 1     # Номер орбиты (1-based)
        self.orbit_radius = 0     # Радиус орбиты в метрах/модельных координатах
        self.angle = 0.0          # Текущий угол в радианах
        self.speed = 0.01         # Скорость изменения угла за шаг
        self.moons = []           # Список спутников планеты
        self.orbit_image = None   # ID графического объекта орбиты

class Moon:
    """Тип данных, описывающий спутник планеты."""
    def __init__(self):
        self.type = "moon"
        self.R = 2
        self.color = "#b0bec5"
        self.orbit_radius = 10    # Радиус орбиты вокруг планеты
        self.angle = 0.0
        self.speed = 0.04
        self.image = None