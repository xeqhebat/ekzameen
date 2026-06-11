# coding: utf-8
# license: GPLv3

import math

def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает положения планет и спутников на основе их орбитального движения."""
    # dt используется как множитель скорости симуляции
    for obj in space_objects:
        if obj.type == "planet":
            # Шаг анимации планеты
            obj.angle += obj.speed * dt
            # Координаты планеты относительно её звезды
            obj.x = obj.star.x + obj.orbit_radius * math.cos(obj.angle)
            obj.y = obj.star.y + obj.orbit_radius * math.sin(obj.angle)
            
            # Шаг анимации её спутников
            for moon in obj.moons:
                moon.angle += moon.speed * dt