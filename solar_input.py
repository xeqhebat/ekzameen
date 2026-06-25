# coding: utf-8
# license: GPLv3

import math
from solar_objects import Star, Planet, Moon

BASE_ORBIT_SPEED = 0.05  
BASE_MOON_SPEED  = 0.12   

def read_space_objects_data_from_file(input_filename):
    """Считывает параметры из файла"""
    objects = []
    stars   = []
    planets = []

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
            elif parts[0].lower() == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                planets.append(planet)

    if len(stars) == 5:
        configs = [
            {"num_planets": 20, "max_per_orbit": 5, "moons": {5: 1, 10: 1, 20: 1}},
            {"num_planets": 30, "max_per_orbit": 4, "moons": {10: 3, 20: 3}},
            {"num_planets": 30, "max_per_orbit": 3, "moons": {5: 5, 10: 5, 15: 5}},
            {"num_planets": 20, "max_per_orbit": 4, "moons": {10: 3, 20: 3}},
            {"num_planets": 15, "max_per_orbit": 3, "moons": {5: 5, 10: 5, 15: 5}},
        ]

        planet_colors = ["#4fc3f7", "#81c784", "#e57373", "#ffb74d", "#ba68c8", "#4dd0e1", "#aed581", "#ff8a65"]
        base_orbit_distance = 40
        orbit_gap           = 25

        for idx, star in enumerate(stars):
            if idx >= len(configs): break
            cfg = configs[idx]
            
            for i in range(cfg["num_planets"]):
                planet = Planet()
                planet.star = star
                planet.orbit_number = i // cfg["max_per_orbit"] + 1
                planet.orbit_radius = base_orbit_distance + (planet.orbit_number - 1) * orbit_gap

                position_on_orbit = i % cfg["max_per_orbit"]
                planet.angle = (2 * math.pi / cfg["max_per_orbit"]) * position_on_orbit
                direction = 1 if (planet.orbit_number % 2 != 0) else -1
                planet.speed = (BASE_ORBIT_SPEED * (base_orbit_distance / planet.orbit_radius) ** 1.5) * direction
                planet.color = planet_colors[(planet.orbit_number - 1) % len(planet_colors)]

                planet.x = star.x + planet.orbit_radius * math.cos(planet.angle)
                planet.y = star.y + planet.orbit_radius * math.sin(planet.angle)

                planet_number = i + 1
                if planet_number in cfg["moons"]:
                    num_moons = cfg["moons"][planet_number]
                    for m in range(num_moons):
                        moon = Moon()
                        moon.orbit_radius = 7 + m * 3
                        moon.angle = (2 * math.pi / num_moons) * m
                        moon.speed = BASE_MOON_SPEED * direction
                        moon.x = planet.x + moon.orbit_radius * math.cos(moon.angle)
                        moon.y = planet.y + moon.orbit_radius * math.sin(moon.angle)
                        planet.moons.append(moon)
                objects.append(planet)
    
    else:
        for planet in planets:
            # Планета
            planet.star = stars[0] if stars else None
            if planet.star:
                dx = planet.x - planet.star.x
                dy = planet.y - planet.star.y
                planet.orbit_radius = math.hypot(dx, dy)
                planet.angle = math.atan2(dy, dx)
                
                # Скорост
                if planet.orbit_radius != 0:
                    v_tan = (dx * planet.Vy - dy * planet.Vx) / planet.orbit_radius
                    planet.speed = v_tan / planet.orbit_radius
                else:
                    planet.speed = 0
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

def parse_planet_parameters(line, planet):
    """Считывает параметры планеты из строки."""
    parts = line.split()
    planet.R = int(parts[1])
    planet.color = parts[2]
    planet.m = float(parts[3])
    planet.x = float(parts[4])
    planet.y = float(parts[5])
    planet.Vx = float(parts[6])
    planet.Vy = float(parts[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет текущие параметры объектов в файл."""
    with open(output_filename, "w", encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == "star":
                out_file.write(f"Star {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")
            elif obj.type == "planet":
                out_file.write(f"Planet {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")

if __name__ == "__main__":
    print("This module is not for direct call!")