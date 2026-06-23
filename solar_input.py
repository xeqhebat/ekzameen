# coding: utf-8
# license: GPLv3

import math
from solar_objects import Star, Planet, Moon

# Базовая угловая скорость для ПЕРВОЙ (ближайшей) орбиты.
# Скорости остальных орбит вычисляются по третьему закону Кеплера: omega ~ r^(-3/2)
BASE_ORBIT_SPEED = 0.05   # рад/шаг для орбиты
BASE_MOON_SPEED  = 0.12   # рад/шаг для спутников

def read_space_objects_data_from_file(input_filename):
    """ Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов
    """
    objects = []
    stars = []

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts[0].lower() == "star":
                star = Star()
                parse_star_parameters(line, star)
                stars.append(star)
                objects.append(star)

    # Параметры планет и спутников
    configs = [
        {"num_planets": 20, "max_per_orbit": 5, "moons": {5: 1, 10: 1, 20: 1}},
        {"num_planets": 30, "max_per_orbit": 4, "moons": {10: 3, 20: 3}},
        {"num_planets": 30, "max_per_orbit": 3, "moons": {5: 5, 10: 5, 15: 5}},
        {"num_planets": 20, "max_per_orbit": 4, "moons": {10: 3, 20: 3}},
        {"num_planets": 15, "max_per_orbit": 3, "moons": {5: 5, 10: 5, 15: 5}}
    ]

    planet_colors = ["#4fc3f7", "#81c784", "#e57373", "#ffb74d", "#ba68c8", "#4dd0e1", "#aed581"]

    base_orbit_distance = 40   # радиус первой орбиты
    orbit_gap = 25             # шаг между орбитами

    for idx, star in enumerate(stars):
        if idx >= len(configs):
            break
        cfg = configs[idx]
        num_planets = cfg["num_planets"]
        max_per_orbit = cfg["max_per_orbit"]
        moon_cfg = cfg["moons"]

        for i in range(num_planets):
            planet = Planet()
            planet.star = star
            planet.orbit_number = (i // max_per_orbit) + 1
            planet.orbit_radius = base_orbit_distance + (planet.orbit_number - 1) * orbit_gap
            
            # Распределение по орбите
            planet_index_in_orbit = i % max_per_orbit
            planet.angle = (2 * math.pi / max_per_orbit) * planet_index_in_orbit
            
            # Направление
            direction = 1 if (planet.orbit_number % 2 != 0) else -1

            # Кеплеровская скорость: omega = BASE * (r_first / r)^1.5
            kepler_speed = BASE_ORBIT_SPEED * (base_orbit_distance / planet.orbit_radius) ** 1.5
            planet.speed = kepler_speed * direction
            
            planet.color = planet_colors[(planet.orbit_number - 1) % len(planet_colors)]
            planet.R = 4
            
            # Физические координаты планеты
            planet.x = star.x + planet.orbit_radius * math.cos(planet.angle)
            planet.y = star.y + planet.orbit_radius * math.sin(planet.angle)
            
            # Генерация спутников
            human_idx = i + 1
            if human_idx in moon_cfg:
                num_moons = moon_cfg[human_idx]
                for m in range(num_moons):
                    moon = Moon()
                    moon.orbit_radius = 10 + m * 5
                    moon.angle = (2 * math.pi / num_moons) * m
                    moon.speed = BASE_MOON_SPEED * direction  # Направление совпадает с планетой
                    moon.color = "white"
                    moon.R = 1.5
                    
                    moon.x = planet.x + moon.orbit_radius * math.cos(moon.angle)
                    moon.y = planet.y + moon.orbit_radius * math.sin(moon.angle)
                    planet.moons.append(moon)
                    
            objects.append(planet)
            
    return objects

def parse_star_parameters(line, star):
    """Считывает параметры звезды из строки."""
    parts = line.split()
    star.R = int(parts[1])
    star.color = parts[2]
    star.m = float(parts[3])
    star.x = float(parts[4])
    star.y = float(parts[5])
    star.Vx = float(parts[6])
    star.Vy = float(parts[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет базовые координаты космических тел в файл."""
    with open(output_filename, 'w', encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == 'star':
                out_file.write(f"Star {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")