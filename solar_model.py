# coding: utf-8
# license: GPLv3

import math

gravitational_constant = 6.67408E-11


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты всех планет и их спутников."""
    for obj in space_objects:
        if obj.type != "planet":
            continue

        # Движение планет
        obj.angle += obj.speed * dt
        obj.x = obj.star.x + obj.orbit_radius * math.cos(obj.angle)
        obj.y = obj.star.y + obj.orbit_radius * math.sin(obj.angle)

        # Движение спутников
        for moon in obj.moons:
            moon.angle += moon.speed * dt
            moon.x = obj.x + moon.orbit_radius * math.cos(moon.angle)
            moon.y = obj.y + moon.orbit_radius * math.sin(moon.angle)


if __name__ == "__main__":
    print("This module is not for direct call!")
