# coding: utf-8
# license: GPLv3

import math

def recalculate_space_objects_positions(space_objects, dt):
    """Выполняет кинематический расчёт положений тел по круговым орбитам
    для полного исключения случайных столкновений.
    """
    for obj in space_objects:
        if obj.type == "planet":
            # Шаг движения планеты вокруг звезды
            obj.angle += obj.speed * dt
            obj.x = obj.star.x + obj.orbit_radius * math.cos(obj.angle)
            obj.y = obj.star.y + obj.orbit_radius * math.sin(obj.angle)
            
            # Шаг движения спутников вокруг этой планеты
            for moon in obj.moons:
                moon.angle += moon.speed * dt
                moon.x = obj.x + moon.orbit_radius * math.cos(moon.angle)
                moon.y = obj.y + moon.orbit_radius * math.sin(moon.angle)