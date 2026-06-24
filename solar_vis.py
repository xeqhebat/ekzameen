# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Только в этом модуле используются экранные координаты объектов.
Все функции принимают физические (модельные) координаты и сами
переводят их в экранные через scale_x / scale_y.
"""

header_font = "Arial-16"

window_width  = 900
window_height = 900

scale_factor = 1.0

show_orbits_global = True


def calculate_scale_factor(max_distance):
    """Устанавливает масштабный коэффициент."""
    global scale_factor
    scale_factor = 1.0


def scale_x(x):
    """Переводит модельную x-координату в экранную.
    Начало координат модели — центр экрана
    """
    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    """Переводит модельную y-координату в экранную."""
    return int(y * scale_factor) + window_height // 2


def create_star_image(space, star):
    """Создаем звездочку"""
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval(
        x - r, y - r, x + r, y + r,
        fill=star.color, outline=""
    )


def create_planet_image(space, planet):
    """Создаем орбиту, планету и спутник"""
    global show_orbits_global

    sx = scale_x(planet.star.x)
    sy = scale_y(planet.star.y)
    r  = planet.orbit_radius

    # Орбита
    orbit_state = "normal" if show_orbits_global else "hidden"
    planet.orbit_image = space.create_oval(
        sx - r, sy - r, sx + r, sy + r,
        outline="#303030", width=1, state=orbit_state
    )

    # Планета
    cx = scale_x(planet.x)
    cy = scale_y(planet.y)
    pr = planet.R
    planet.image = space.create_oval(
        cx - pr, cy - pr, cx + pr, cy + pr,
        fill=planet.color, outline=""
    )

    # Спутник
    planet.moon_images = []
    for moon in planet.moons:
        mx = scale_x(moon.x)
        my = scale_y(moon.y)
        mr = moon.R
        img = space.create_oval(
            mx - mr, my - mr, mx + mr, my + mr,
            fill=moon.color, outline=""
        )
        planet.moon_images.append(img)


def update_object_position(space, body):
    """Перемещает графический объект тела на холсте в соответствии
    с его текущими модельными координатами.
    """
    if body.type == "star":
        x = scale_x(body.x)
        y = scale_y(body.y)
        r = body.R
        space.coords(body.image, x - r, y - r, x + r, y + r)

    elif body.type == "planet":
        cx = scale_x(body.x)
        cy = scale_y(body.y)
        r  = body.R
        space.coords(body.image, cx - r, cy - r, cx + r, cy + r)

        # Обновляем позиции спутников
        for moon_img, moon in zip(body.moon_images, body.moons):
            mx = scale_x(moon.x)
            my = scale_y(moon.y)
            mr = moon.R
            space.coords(moon_img, mx - mr, my - mr, mx + mr, my + mr)


def set_orbits_visibility(space, space_objects, visible):
    """Отображение орбит"""
    global show_orbits_global
    show_orbits_global = visible
    state = "normal" if visible else "hidden"
    for obj in space_objects:
        if (obj.type == "planet"
                and hasattr(obj, "orbit_image")
                and obj.orbit_image is not None):
            space.itemconfigure(obj.orbit_image, state=state)


if __name__ == "__main__":
    print("This module is not for direct call!")
