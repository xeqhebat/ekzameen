# coding: utf-8
# license: GPLv3

import math
from solar_objects import Star, Planet, Moon


BASE_ORBIT_SPEED = 0.05  
BASE_MOON_SPEED  = 0.12   


def read_space_objects_data_from_file(input_filename):
    """Считывает параметры звёзд из файла и автоматически генерирует
    систему планет и спутников согласно условиям Билета №5.

    Формат строки звезды в файле:
    Star <радиус_px> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    objects = []
    stars   = []

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

    # Конфигурация звёзд
    configs = [
        {"num_planets": 20, "max_per_orbit": 5,
         "moons": {5: 1, 10: 1, 20: 1}},          # Звезда 1 (yellow)
        {"num_planets": 30, "max_per_orbit": 4,
         "moons": {10: 3, 20: 3}},                  # Звезда 2 (orange)
        {"num_planets": 30, "max_per_orbit": 3,
         "moons": {5: 5, 10: 5, 15: 5}},            # Звезда 3 (cyan)
        {"num_planets": 20, "max_per_orbit": 4,
         "moons": {10: 3, 20: 3}},                  # Звезда 4 (magenta)
        {"num_planets": 15, "max_per_orbit": 3,
         "moons": {5: 5, 10: 5, 15: 5}},            # Звезда 5 (lime)
    ]

    planet_colors = [
        "#4fc3f7", "#81c784", "#e57373", "#ffb74d",
        "#ba68c8", "#4dd0e1", "#aed581", "#ff8a65",
    ]

    base_orbit_distance = 40
    orbit_gap           = 25

    for idx, star in enumerate(stars):
        if idx >= len(configs):
            break
        cfg            = configs[idx]
        num_planets    = cfg["num_planets"]
        max_per_orbit  = cfg["max_per_orbit"]
        moon_cfg       = cfg["moons"]

        for i in range(num_planets):
            planet = Planet()
            planet.star = star
            planet.orbit_number = i // max_per_orbit + 1
            planet.orbit_radius = (base_orbit_distance
                                   + (planet.orbit_number - 1) * orbit_gap)

            position_on_orbit = i % max_per_orbit
            planet.angle = (2 * math.pi / max_per_orbit) * position_on_orbit

            direction = 1 if (planet.orbit_number % 2 != 0) else -1

            # Скорость по закону Кеплера: omega = BASE * (r0 / r)^1.5
            kepler_speed = (BASE_ORBIT_SPEED
                            * (base_orbit_distance / planet.orbit_radius) ** 1.5)
            planet.speed = kepler_speed * direction

            planet.color = planet_colors[(planet.orbit_number - 1) % len(planet_colors)]

            # Начальные координаты планеты
            planet.x = star.x + planet.orbit_radius * math.cos(planet.angle)
            planet.y = star.y + planet.orbit_radius * math.sin(planet.angle)

            # Спутники
            planet_number = i + 1
            if planet_number in moon_cfg:
                num_moons = moon_cfg[planet_number]
                for m in range(num_moons):
                    moon = Moon()
                    moon.orbit_radius = 7 + m * 3      # 7, 10, 13, 16, 19 px
                    moon.angle = (2 * math.pi / num_moons) * m
                    moon.speed = BASE_MOON_SPEED * direction  # то же направление
                    moon.x = planet.x + moon.orbit_radius * math.cos(moon.angle)
                    moon.y = planet.y + moon.orbit_radius * math.sin(moon.angle)
                    planet.moons.append(moon)

            objects.append(planet)

    return objects


def parse_star_parameters(line, star):
    """Считывает параметры звезды из строки.
    Формат строки:
    Star <радиус_px> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    parts    = line.split()
    star.R   = int(parts[1])
    star.color = parts[2]
    star.m   = float(parts[3])
    star.x   = float(parts[4])
    star.y   = float(parts[5])
    star.Vx  = float(parts[6])
    star.Vy  = float(parts[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет текущие параметры звёзд в файл.
    Строки звёзд имеют формат:
    Star <радиус_px> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    with open(output_filename, "w", encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == "star":
                out_file.write(
                    f"Star {obj.R} {obj.color} {obj.m} "
                    f"{obj.x} {obj.y} {obj.Vx} {obj.Vy}\n"
                )


if __name__ == "__main__":
    print("This module is not for direct call!")
