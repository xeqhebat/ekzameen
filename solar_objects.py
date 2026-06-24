# coding: utf-8
# license: GPLv3


class Star:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """
    def __init__(self):
        self.type  = "star"
        self.m     = 0        # Масса звезды
        self.x     = 0        # Координата по оси x
        self.y     = 0        # Координата по оси y
        self.Vx    = 0        # Скорость по оси x
        self.Vy    = 0        # Скорость по оси y
        self.Fx    = 0        # Сила по оси x
        self.Fy    = 0        # Сила по оси y
        self.R     = 5        # Радиус звезды
        self.color = "red"    # Цвет звезды
        self.image = None     # Графический ID звезды


class Planet:
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет.
    """
    def __init__(self):
        self.type  = "planet"
        self.m     = 0        # Масса планеты
        self.x     = 0        # Координата по оси x
        self.y     = 0        # Координата по оси y
        self.Vx    = 0        # Скорость по оси x
        self.Vy    = 0        # Скорость по оси y
        self.Fx    = 0        # Сила по оси x
        self.Fy    = 0        # Сила по оси y
        self.R     = 4        # Радиус планеты в пикселах
        self.color = "green"  # Цвет планеты
        self.image = None     # Графический ID кружка планеты

        # Параметры кинематической орбиты
        self.star         = None  # Ссылка на родительскую звезду
        self.orbit_number = 0     # Номер орбиты
        self.orbit_radius = 0     # Радиус орбиты
        self.angle        = 0.0   # Текущий угол
        self.speed        = 0.0   # Угловая скорость
        self.orbit_image  = None  # Графический ID орбиты
        self.moons        = []    # Список спутников
        self.moon_images  = []    # Графические ID спутников


class Moon:
    """Тип данных, описывающий спутник планеты."""
    def __init__(self):
        self.type         = "moon"
        self.x            = 0      # Координата по оси x
        self.y            = 0      # Координата по оси y
        self.R            = 1.5    # Радиус спутника
        self.color        = "white"
        self.orbit_radius = 0      # Радиус орбиты вокруг планеты
        self.angle        = 0.0    # Текущий угол
        self.speed        = 0.0    # Угловая скорость
