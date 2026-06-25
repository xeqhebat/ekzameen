# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename

import solar_vis
from solar_model import recalculate_space_objects_positions
from solar_input import read_space_objects_data_from_file, write_space_objects_data_to_file


perform_execution = False
physical_time     = 0

displayed_time = None
time_step      = None
time_speed     = None
show_orbits    = None

space_objects = []
space         = None
start_button  = None


# Логика

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    if not perform_execution:
        return

    recalculate_space_objects_positions(space_objects, time_step.get())
    
    # Обновляем объекты
    solar_vis.update_all_objects(space, space_objects, time_step.get())

    physical_time += time_step.get()
    displayed_time.set(f"{physical_time:.1f} seconds gone")

    space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Запускает симуляцию"""
    global perform_execution
    if not perform_execution:
        perform_execution = True
        start_button["text"]    = "Pause"
        start_button["command"] = stop_execution
        execution()


def stop_execution():
    """Останавливаем симуляцию"""
    global perform_execution
    perform_execution = False
    start_button["text"]    = "Start"
    start_button["command"] = start_execution


# Файлы

def open_file_dialog():
    """Открываем файл"""
    global space_objects, physical_time

    stop_execution()
    space.delete("all")
    space_objects = []
    physical_time = 0
    displayed_time.set("0.0 seconds gone")

    filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if not filename:
        return

    # Экран
    solar_vis.set_background(space, solar_vis.window_width, solar_vis.window_height)
    
    space_objects = read_space_objects_data_from_file(filename)
    
    if space_objects:
        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
        if max_distance == 0:
            max_distance = 1000
        solar_vis.calculate_scale_factor(max_distance)
    else:
        solar_vis.calculate_scale_factor(1000)
    
    # Рисуем морковки
    solar_vis.create_carrots(space, num_carrots=30)

    # Рисуем орбиты и планеты
    for obj in space_objects:
        if obj.type == "planet":
            solar_vis.create_planet_image(space, obj)

    # Рисуем звёзды
    for obj in space_objects:
        if obj.type == "star":
            solar_vis.create_star_image(space, obj)


def save_file_dialog():
    """Сохраняем файл"""
    filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if filename:
        write_space_objects_data_to_file(filename, space_objects)


def toggle_orbits():
    """Переключаем видимость орбит"""
    solar_vis.set_orbits_visibility(space, space_objects, show_orbits.get())


# Главная функция
def main():
    """Создаёт окно, холст и панель управления, затем запускает главный цикл tkinter."""
    global displayed_time, time_step, time_speed, show_orbits
    global space, start_button, physical_time

    physical_time = 0

    root = tkinter.Tk()
    root.title("Солнечная система — Билет №5")
    root.resizable(False, False)

    # Панель управления
    panel = tkinter.Frame(root, bg="#1a1a1a")
    panel.pack(side=tkinter.TOP, fill=tkinter.X, ipady=4)

    # Кнопка Start/Pause
    start_button = tkinter.Button(panel, text="Start", command=start_execution,
                                   width=8, bg="#2d2d2d", fg="white",
                                   activebackground="#3d3d3d", activeforeground="white")
    start_button.pack(side=tkinter.LEFT, padx=6, pady=5)

    # dt
    tkinter.Label(panel, text="DT:", bg="#1a1a1a", fg="#aaaaaa",
                  font=("Courier", 9)).pack(side=tkinter.LEFT)
    time_step = tkinter.DoubleVar(value=1.0)
    tkinter.Entry(panel, textvariable=time_step, width=5,
                  bg="#2d2d2d", fg="white", insertbackground="white").pack(
        side=tkinter.LEFT, padx=4)

    # Скорость
    time_speed = tkinter.DoubleVar(value=70.0)
    tkinter.Scale(panel, variable=time_speed,
                  orient=tkinter.HORIZONTAL, from_=1, to=100,
                  label="Скорость", length=120,
                  bg="#1a1a1a", fg="white", highlightthickness=0,
                  troughcolor="#333333").pack(side=tkinter.LEFT, padx=4)

    # Загрузка
    tkinter.Button(panel, text="Открыть файл...", command=open_file_dialog,
                   bg="#2d2d2d", fg="white",
                   activebackground="#3d3d3d", activeforeground="white").pack(
        side=tkinter.LEFT, padx=4)

    # Сохранение
    tkinter.Button(panel, text="Сохранить...", command=save_file_dialog,
                   bg="#2d2d2d", fg="white",
                   activebackground="#3d3d3d", activeforeground="white").pack(
        side=tkinter.LEFT, padx=4)

    # Отображение орбит
    show_orbits = tkinter.BooleanVar(value=True)
    tkinter.Checkbutton(panel, text="Отображать орбиты",
                        variable=show_orbits, command=toggle_orbits,
                        bg="#1a1a1a", fg="white",
                        selectcolor="#333333",
                        activebackground="#1a1a1a", activeforeground="white",
                        font=("Courier", 10)).pack(side=tkinter.LEFT, padx=8)

    # Метка времени
    displayed_time = tkinter.StringVar(value="0.0 seconds gone")
    tkinter.Label(panel, textvariable=displayed_time,
                  width=22, bg="#1a1a1a", fg="#cccccc",
                  font=("Courier", 10)).pack(side=tkinter.RIGHT, padx=6)

    # Холст
    space = tkinter.Canvas(root,
                           width=solar_vis.window_width,
                           height=solar_vis.window_height,
                           bg=solar_vis.background_color)  # ← уже используем константу
    space.pack(side=tkinter.BOTTOM)
    
    # Фон
    solar_vis.set_background(space, solar_vis.window_width, solar_vis.window_height)

    root.mainloop()


if __name__ == "__main__":
    main()