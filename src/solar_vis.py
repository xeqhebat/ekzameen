# coding: utf-8
# license: GPLv3

header_font = "Arial-16"
window_width = 1100
window_height = 1100

# Глобальный флаг видимости орбит
_orbits_visible = True

def calculate_scale_factor(max_distance):
    global scale_factor
    scale_factor = 1.0  # Используем экранные координаты напрямую

def scale_x(x):
    return int(x)

def scale_y(y):
    return int(y)

def create_star_image(space, star):
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval(x - r, y - r, x + r, y + r, fill=star.color, outline="")

def create_planet_image(space, planet):
    # Сначала рисуем саму орбиту планеты вокруг звезды
    if planet.orbit_image is None:
        sx = scale_x(planet.star.x)
        sy = scale_y(planet.star.y)
        or_r = planet.orbit_radius
        state = "normal" if _orbits_visible else "hidden"
        planet.orbit_image = space.create_oval(sx - or_r, sy - or_r, sx + or_r, sy - or_r,
                                               outline="#333333", width=1, state=state)

    # Вычисляем текущие экранные координаты планеты
    px = scale_x(planet.x)
    py = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval(px - r, py - r, px + r, py + r, fill=planet.color, outline="")

    # Рисуем все спутники планеты
    import math
    for moon in planet.moons:
        mx = px + moon.orbit_radius * math.cos(moon.angle)
        my = py + moon.orbit_radius * math.sin(moon.angle)
        mr = moon.R
        moon.image = space.create_oval(mx - mr, my - mr, mx + mr, my + mr, fill=moon.color, outline="")

def update_object_position(space, body):
    if body.type == "star":
        x = scale_x(body.x)
        y = scale_y(body.y)
        r = body.R
        space.coords(body.image, x - r, y - r, x + r, y + r)
        
    elif body.type == "planet":
        px = scale_x(body.x)
        py = scale_y(body.y)
        r = body.R
        space.coords(body.image, px - r, py - r, px + r, py + r)
        
        # Обновляем координаты спутников вслед за планетой
        import math
        for moon in body.moons:
            mx = px + moon.orbit_radius * math.cos(moon.angle)
            my = py + moon.orbit_radius * math.sin(moon.angle)
            mr = moon.R
            space.coords(moon.image, mx - mr, my - mr, mx + mr, my + mr)

def set_orbits_visibility(space, space_objects, visible):
    """Переключает видимость всех кругов орбит на холсте."""
    global _orbits_visible
    _orbits_visible = visible
    state = "normal" if visible else "hidden"
    for obj in space_objects:
        if obj.type == "planet" and obj.orbit_image is not None:
            space.itemconfigure(obj.orbit_image, state=state)