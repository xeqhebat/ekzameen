# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Только в этом модуле используются экранные координаты объектов.
Все функции принимают физические (модельные) координаты и сами
переводят их в экранные через scale_x / scale_y.
"""

import math
from PIL import Image, ImageDraw, ImageTk

header_font = "Arial-16"

window_width  = 950
window_height = 900

scale_factor = 1.0
show_orbits_global = True


background_color = "#000000"  
use_gradient = True          

def create_gradient_background(space, width, height, color1, color2, direction="vertical"):
    """Создает градиентный фон на холсте"""
    
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    
    def hex_to_rgb(hex_color):
        if hex_color.startswith('#'):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        else:
            color_map = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'darkblue': (0, 0, 139),
                'midnightblue': (25, 25, 112),
                'navy': (0, 0, 128),
                'purple': (128, 0, 128),
                'darkred': (139, 0, 0),
                'darkgreen': (0, 100, 0),
                'gray20': (51, 51, 51),
            }
            return color_map.get(hex_color.lower(), (0, 0, 0))
    
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    
    # Рисуем градиент
    if direction == "vertical":
        for y in range(height):
            t = y / height
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for x in range(width):
            t = x / width
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    
    photo = ImageTk.PhotoImage(img)
    
    bg_id = space.create_image(0, 0, image=photo, anchor='nw')
    
    space.bg_image = photo
    
    return bg_id


def set_background(space, width, height):
    """
    Устанавливает фон на холсте (сплошной или градиентный).
    Вызывается при создании окна.
    """
    global background_color, use_gradient
    
    if use_gradient:
        color1 = "#000000"  
        color2 = "#290036"  
        return create_gradient_background(space, width, height, color1, color2, "vertical")
    else:
        # Сплошной цвет
        return space.create_rectangle(0, 0, width, height, fill=background_color, outline="")
    
# Глобальный список для морковок
carrots = []  # Каждая морковка: {image_id: int, x: float, y: float, progress: float, side: int}


def calculate_scale_factor(max_distance):
    """Устанавливаем масштабный коэффициент."""
    global scale_factor
    if max_distance > 10000:
        scale_factor = 0.4 * min(window_height, window_width) / max_distance
    else:
        scale_factor = 1.0


def scale_x(x):
    """Переводит модельную x-координату в экранную.
    Начало координат модели — центр холста.
    """
    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    """Переводит модельную y-координату в экранную."""
    return int(y * scale_factor) + window_height // 2


def create_carrot_image(size=30, color="#FF8C00", outline_color="#CC7000"):
    """
    Создает изображение морковки как единый блок с помощью PIL.
    Возвращает объект Image.
    """
    img = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Центр
    cx = size
    cy = size
    
    height = size
    base_width = size // 2
    
    # Морковка
    left_top = (cx - base_width // 2, cy - height // 2)
    right_top = (cx + base_width // 2, cy - height // 2)
    bottom_tip = (cx, cy + height // 2)
    
    draw.polygon([left_top, right_top, bottom_tip], fill=color, outline=outline_color, width=2)
    
    # Стебли
    stem_length = size // 3
    dark_green = "#006400"
    light_green = "#32CD32"
    
    # Стебель 1 (левый)
    stem1_start = (cx - base_width // 3, cy - height // 2)
    stem1_end = (stem1_start[0], stem1_start[1] - stem_length)
    draw.line([stem1_start, stem1_end], fill=dark_green, width=3)
    
    # Стебель 2 (центральный)
    stem2_start = (cx, cy - height // 2)
    stem2_end = (stem2_start[0], stem2_start[1] - stem_length - 5)
    draw.line([stem2_start, stem2_end], fill=dark_green, width=3)
    
    # Стебель 3 (правый)
    stem3_start = (cx + base_width // 3, cy - height // 2)
    stem3_end = (stem3_start[0], stem3_start[1] - stem_length)
    draw.line([stem3_start, stem3_end], fill=dark_green, width=3)
    
    # Листочки
    # Левый стебель
    draw.line([stem1_end, (stem1_end[0] - 5, stem1_end[1] - 3)], fill=light_green, width=2)
    draw.line([stem1_end, (stem1_end[0] - 3, stem1_end[1] - 6)], fill=light_green, width=2)
    
    # Правый стебель
    draw.line([stem3_end, (stem3_end[0] + 5, stem3_end[1] - 3)], fill=light_green, width=2)
    draw.line([stem3_end, (stem3_end[0] + 3, stem3_end[1] - 6)], fill=light_green, width=2)
    
    # Центральный стебель
    draw.line([stem2_end, (stem2_end[0], stem2_end[1] - 8)], fill=light_green, width=2)
    draw.line([stem2_end, (stem2_end[0] - 4, stem2_end[1] - 4)], fill=light_green, width=2)
    draw.line([stem2_end, (stem2_end[0] + 4, stem2_end[1] - 4)], fill=light_green, width=2)
    
    return img


def rotate_carrot_image(img, angle):
    """Поворачиваем морковку."""
    return img.rotate(angle, expand=True, resample=Image.BICUBIC)


def get_carrot_angle(side):
    """Определяем угол поворота"""
    if side == 0:  
        return 90
    elif side == 1:
        return 0
    elif side == 2: 
        return 270
    else: 
        return 180


def create_carrots(space, num_carrots=30):
    """Создаем морковки"""
    global carrots
    carrots = []
    
    carrot_size = 30
    margin = 14 
    
    base_img = create_carrot_image(carrot_size)
    
    carrots_per_side = num_carrots // 4
    remainder = num_carrots % 4
    
    for side in range(4):
        count = carrots_per_side + (1 if side < remainder else 0)
        for i in range(count):
            progress = (i + 0.5) / count  # 0.5/count, 1.5/count, ...
            
            # Гео морковки
            if side == 0:  # Верхняя сторона
                x = margin + progress * (window_width - 2 * margin)
                y = margin
            elif side == 1:  # Правая сторона
                x = window_width - margin
                y = margin + progress * (window_height - 2 * margin)
            elif side == 2:  # Нижняя сторона
                x = window_width - margin - progress * (window_width - 2 * margin)
                y = window_height - margin
            else:  # Левая сторона
                x = margin
                y = window_height - margin - progress * (window_height - 2 * margin)
            
            # Определяем угол поворота
            angle = get_carrot_angle(side)
            
            # Поворачиваем
            rotated_img = rotate_carrot_image(base_img, angle)
            photo = ImageTk.PhotoImage(rotated_img)
            
            # Создаем
            image_id = space.create_image(x, y, image=photo)
            
            carrots.append({
                'image_id': image_id,
                'photo': photo,  # сохраняем ссылку, чтобы не удалилось
                'x': x,
                'y': y,
                'progress': progress,
                'side': side,
                'angle': angle,
                'size': carrot_size
            })


def update_carrots(space, dt):
    """Обновляет позиции морковок"""
    global carrots

    base_speed = 0.015 * dt
    margin = 14
    
    for carrot in carrots:
        # Обновляем движение
        carrot['progress'] += base_speed
        
        carrot['progress'] %= 1.0
        
        # Находим новые координаты
        side = carrot['side']
        progress = carrot['progress']
        
        if side == 0:
            x = margin + progress * (window_width - 2 * margin)
            y = margin
        elif side == 1: 
            x = window_width - margin
            y = margin + progress * (window_height - 2 * margin)
        elif side == 2: 
            x = window_width - margin - progress * (window_width - 2 * margin)
            y = window_height - margin
        else:
            x = margin
            y = window_height - margin - progress * (window_height - 2 * margin)
        
        # Обновляем координаты морковки
        carrot['x'] = x
        carrot['y'] = y
        
        # Перемещаем морковку
        space.coords(carrot['image_id'], x, y)


def draw_bunny_face(space, x, y, size, color):
    """Рисуем голову зайца"""
    parts = []
    
    # Уши
    ear_width = size // 4
    ear_height = size - 5 
    ear_y = y - ear_height // 1.5
    
    # Левое ухо
    left_ear_x = x - size // 4
    left_ear = space.create_oval(
        left_ear_x - ear_width//2,
        ear_y - ear_height//2,
        left_ear_x + ear_width//2,
        ear_y + ear_height//2,
        fill=color, outline="black", width=2
    )
    parts.append(left_ear)
    
    # Правое ухо
    right_ear_x = x + size // 4
    right_ear = space.create_oval(
        right_ear_x - ear_width//2,
        ear_y - ear_height//2,
        right_ear_x + ear_width//2,
        ear_y + ear_height//2,
        fill=color, outline="black", width=2
    )
    parts.append(right_ear)
    
    # Голова
    head = space.create_oval(
        x - size//2, y - size//2,
        x + size//2, y + size//2,
        fill=color, outline="black", width=2
    )
    parts.append(head)
    
    # Глаза
    eye_radius = max(2, size // 8)
    eye_offset_x = size // 4
    eye_offset_y = size // 8
    
    # Левый глаз
    left_eye = space.create_oval(
        x - eye_offset_x - eye_radius,
        y - eye_offset_y - eye_radius,
        x - eye_offset_x + eye_radius,
        y - eye_offset_y + eye_radius,
        fill="white", outline="black", width=2
    )
    parts.append(left_eye)
    
    # Правый глаз
    right_eye = space.create_oval(
        x + eye_offset_x - eye_radius,
        y - eye_offset_y - eye_radius,
        x + eye_offset_x + eye_radius,
        y - eye_offset_y + eye_radius,
        fill="white", outline="black", width=2
    )
    parts.append(right_eye)
    
    # Зрачки
    pupil_radius = max(1, eye_radius // 3)
    
    # Левый зрачок
    left_pupil = space.create_oval(
        x - eye_offset_x - pupil_radius,
        y - eye_offset_y - pupil_radius,
        x - eye_offset_x + pupil_radius,
        y - eye_offset_y + pupil_radius,
        fill="black", outline=""
    )
    parts.append(left_pupil)
    
    # Правый зрачок
    right_pupil = space.create_oval(
        x + eye_offset_x - pupil_radius,
        y - eye_offset_y - pupil_radius,
        x + eye_offset_x + pupil_radius,
        y - eye_offset_y + pupil_radius,
        fill="black", outline=""
    )
    parts.append(right_pupil)
    
    # 5. Рот
    mouth_width = size // 2
    mouth_height = size // 8
    mouth_y = y + size // 6
    
    mouth = space.create_arc(
        x - mouth_width//2,
        mouth_y - mouth_height//2,
        x + mouth_width//2,
        mouth_y + mouth_height//2,
        start=0, extent=-180,  # дуга вниз (улыбка)
        style="arc", outline="black", width=2
    )
    parts.append(mouth)
    
    return parts


def create_star_image(space, star):
    """Создаем звездочку"""
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    
    # Рисуем зайца
    star.parts = draw_bunny_face(space, x, y, r * 2, star.color)
    if star.parts:
        star.image = star.parts[0]


def create_planet_image(space, planet):
    """Создаем орбиту, планету и спутник"""
    global show_orbits_global

    sx = scale_x(planet.star.x)
    sy = scale_y(planet.star.y)
    
    r_orbit = planet.orbit_radius * scale_factor

    # Орбита
    orbit_state = "normal" if show_orbits_global else "hidden"
    planet.orbit_image = space.create_oval(
        sx - r_orbit, sy - r_orbit, sx + r_orbit, sy + r_orbit,
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
        
        if hasattr(body, 'parts') and body.parts:
            size = r * 2
            ear_width = size // 4
            ear_height = size - 5
            ear_y = y - ear_height // 1.5
            eye_radius = max(2, size // 8)
            eye_offset_x = size // 4
            eye_offset_y = size // 8
            pupil_radius = max(1, eye_radius // 3) 
            mouth_width = size // 2
            mouth_height = size // 8
            mouth_y = y + size // 6
            
            # Координаты для органов зайца
            coords_list = [
                # 1. Левое ухо
                [x - size//4 - ear_width//2, ear_y - ear_height//2,
                 x - size//4 + ear_width//2, ear_y + ear_height//2],
                # 2. Правое ухо
                [x + size//4 - ear_width//2, ear_y - ear_height//2,
                 x + size//4 + ear_width//2, ear_y + ear_height//2],
                # 3. Голова
                [x - size//2, y - size//2, x + size//2, y + size//2],
                # 4. Левый глаз
                [x - eye_offset_x - eye_radius, y - eye_offset_y - eye_radius,
                 x - eye_offset_x + eye_radius, y - eye_offset_y + eye_radius],
                # 5. Правый глаз
                [x + eye_offset_x - eye_radius, y - eye_offset_y - eye_radius,
                 x + eye_offset_x + eye_radius, y - eye_offset_y + eye_radius],
                # 6. Левый зрачок
                [x - eye_offset_x - pupil_radius, y - eye_offset_y - pupil_radius,
                 x - eye_offset_x + pupil_radius, y - eye_offset_y + pupil_radius],
                # 7. Правый зрачок
                [x + eye_offset_x - pupil_radius, y - eye_offset_y - pupil_radius,
                 x + eye_offset_x + pupil_radius, y - eye_offset_y + pupil_radius],
                # 8. Рот
                [x - mouth_width//2, mouth_y - mouth_height//2,
                 x + mouth_width//2, mouth_y + mouth_height//2]
            ]
            
            # Двигаем все части
            for i, part_id in enumerate(body.parts):
                if i < len(coords_list):
                    space.coords(part_id, *coords_list[i])
        else:
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


def update_all_objects(space, space_objects, dt):
    """Обновляем позиции"""
    # Обновляем звезды и планеты
    for obj in space_objects:
        update_object_position(space, obj)
    
    # Обновляем морковки
    update_carrots(space, dt)


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