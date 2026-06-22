# coding: utf-8
# license: GPLv3

header_font = "Arial-16"
window_width = 1000
window_height = 900
scale_factor = 1.0
show_orbits_global = True

def calculate_scale_factor(max_distance):
    global scale_factor
    scale_factor = 1.0

def scale_x(x):
    return int(x * scale_factor) + window_width // 2

def scale_y(y):
    return int(y * scale_factor) + window_height // 2

def create_star_image(space, star):
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval(x - r, y - r, x + r, y + r, fill=star.color, outline="")

def create_planet_image(space, planet):
    global show_orbits_global
    sx = scale_x(planet.star.x)
    sy = scale_y(planet.star.y)
    r_orbit = planet.orbit_radius
    
    # Исправлена геометрия bounding box (sy + r_orbit)
    state = "normal" if show_orbits_global else "hidden"
    planet.orbit_image = space.create_oval(
        sx - r_orbit, sy - r_orbit,
        sx + r_orbit, sy + r_orbit,
        outline="#252525", width=1, state=state
    )
    
    cx = scale_x(planet.x)
    cy = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval(
        cx - r, cy - r,
        cx + r, cy + r,
        fill=planet.color, outline=""
    )
    
    planet.moon_images = []
    for moon in planet.moons:
        mx = scale_x(moon.x)
        my = scale_y(moon.y)
        mr = moon.R
        m_img = space.create_oval(
            mx - mr, my - mr,
            mx + mr, my + mr,
            fill=moon.color, outline=""
        )
        planet.moon_images.append(m_img)

def update_object_position(space, body):
    if body.type == "star":
        x = scale_x(body.x)
        y = scale_y(body.y)
        r = body.R
        space.coords(body.image, x - r, y - r, x + r, y + r)
    elif body.type == "planet":
        cx = scale_x(body.x)
        cy = scale_y(body.y)
        r = body.R
        space.coords(body.image, cx - r, cy - r, cx + r, cy + r)
        
        # Обновление позиций спутников планеты
        for m_img, moon in zip(body.moon_images, body.moons):
            mx = scale_x(moon.x)
            my = scale_y(moon.y)
            mr = moon.R
            space.coords(m_img, mx - mr, my - mr, mx + mr, my + mr)

def set_orbits_visibility(space, space_objects, visible):
    """Скрывает или отображает линии орбит на холсте."""
    global show_orbits_global
    show_orbits_global = visible
    state = "normal" if visible else "hidden"
    for obj in space_objects:
        if obj.type == "planet" and hasattr(obj, "orbit_image") and obj.orbit_image is not None:
            space.itemconfigure(obj.orbit_image, state=state)