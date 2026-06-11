# coding: utf-8
# license: GPLv3

import math
from solar_objects import Star, Planet, Moon

BASE_PLANET_SPEED = 0.012
BASE_MOON_SPEED = 0.045

def read_space_objects_data_from_file(input_filename):
    """Считывает данные о звёздах из файла и автоматически генерирует 
    связанные планеты и спутники согласно Билету №5.
    """
    objects = []
    stars = []

    with open(input_filename, "r", encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            
            parts = line.split()
            object_type = parts[0].lower()
            
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                stars.append(star)
                objects.append(star)

    # Применяем конфигурацию Билета №5 для загруженных звёзд
    # Нам нужно настроить до 5 звёзд
    configs = [
        {"num_planets": 20, "max_per_orbit": 5, "base_orbit": 45, "orbit_gap": 28, "moons": {5: 1, 10: 1, 20: 1}},
        {"num_planets": 30, "max_per_orbit": 4, "base_orbit": 40, "orbit_gap": 26, "moons": {10: 3, 20: 3}},
        {"num_planets": 30, "max_per_orbit": 3, "base_orbit": 40, "orbit_gap": 26, "moons": {5: 5, 10: 5, 15: 5}},
        {"num_planets": 20, "max_per_orbit": 4, "base_orbit": 40, "orbit_gap": 26, "moons": {10: 3, 20: 3}},
        {"num_planets": 15, "max_per_orbit": 3, "base_orbit": 38, "orbit_gap": 25, "moons": {5: 5, 10: 5, 15: 5}}
    ]

    planet_colors = ["#4fc3f7", "#81c784", "#e57373", "#ffb74d", "#ba68c8", "#4dd0e1", "#aed581", "#ff8a65"]

    for idx, star in enumerate(stars):
        if idx >= len(configs):
            break
        cfg = configs[idx]
        star.max_per_orbit = cfg["max_per_orbit"]
        star.base_orbit = cfg["base_orbit"]
        star.orbit_gap = cfg["orbit_gap"]
        
        for p_idx in range(cfg["num_planets"]):
            planet = Planet()
            planet.star = star
            
            # Вычисление орбиты
            planet.orbit_number = (p_idx // star.max_per_orbit) + 1
            planet.orbit_radius = star.base_orbit + (planet.orbit_number - 1) * star.orbit_gap
            
            # Равномерное распределение на одной орбите
            pos_on_orbit = p_idx % star.max_per_orbit
            planet.angle = (2 * math.pi / star.max_per_orbit) * pos_on_orbit
            
            # Направление вращения: чётные = по часовой (+1), нечётные = против (-1)
            direction = 1 if planet.orbit_number % 2 == 0 else -1
            planet.speed = BASE_PLANET_SPEED * direction
            
            planet.color = planet_colors[(planet.orbit_number - 1) % len(planet_colors)]
            planet.R = 4
            
            # Генерация спутников (1-based индексация планет)
            p_num = p_idx + 1
            if p_num in cfg["moons"]:
                num_moons = cfg["moons"][p_num]
                for m_idx in range(num_moons):
                    moon = Moon()
                    moon.orbit_radius = 10 + m_idx * 7
                    moon.angle = (2 * math.pi / num_moons) * m_idx
                    moon.speed = BASE_MOON_SPEED * direction  # Направление как у планеты
                    planet.moons.append(moon)
            
            objects.append(planet)

    return objects

def parse_star_parameters(line, star):
    """Парсит строку вида: Star <R> <color> <m> <x> <y> <Vx> <Vy>"""
    parts = line.split()
    star.R = int(parts[1])
    star.color = parts[2]
    star.m = float(parts[3])
    star.x = float(parts[4])
    star.y = float(parts[5])
    star.Vx = float(parts[6])
    star.Vy = float(parts[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет базовые координаты объектов в файл."""
    with open(output_filename, 'w', encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == 'star':
                out_file.write(f"Star {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")