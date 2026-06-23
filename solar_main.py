# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import solar_vis
from solar_model import recalculate_space_objects_positions
from solar_input import read_space_objects_data_from_file, write_space_objects_data_to_file

perform_execution = False
physical_time = 0
displayed_time = None
time_step = None
space_objects = []
space = None
start_button = None

def execution():
    global physical_time
    if perform_execution:
        recalculate_space_objects_positions(space_objects, time_step.get())
        for body in space_objects:
            solar_vis.update_object_position(space, body)
        physical_time += time_step.get()
        displayed_time.set(f"{physical_time:.1f} seconds gone")
        space.after(101 - int(time_speed.get()), execution)

def start_execution():
    global perform_execution
    if not perform_execution:
        perform_execution = True
        start_button['text'] = "Pause"
        start_button['command'] = stop_execution
        execution()

def stop_execution():
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution

def open_file_dialog():
    global space_objects, perform_execution, physical_time
    stop_execution()
    space.delete("all")
    space_objects = []
    physical_time = 0
    displayed_time.set("0.0 seconds gone")
    
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if not in_filename:
        return
        
    space_objects = read_space_objects_data_from_file(in_filename)
    solar_vis.calculate_scale_factor(1000)

    #Отрисовываем нижний слой (орбиты, планеты, спутники)
    for obj in space_objects:
        if obj.type == 'planet':
            solar_vis.create_planet_image(space, obj)
            
    #Накладываем звёзды
    for obj in space_objects:
        if obj.type == 'star':
            solar_vis.create_star_image(space, obj)

def save_file_dialog():
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if out_filename:
        write_space_objects_data_to_file(out_filename, space_objects)

def toggle_orbits():
    solar_vis.set_orbits_visibility(space, space_objects, show_orbits.get())

def main():
    global displayed_time, time_step, time_speed, space, start_button, show_orbits

    root = tkinter.Tk()
    root.title("Солнечная система — Билет №5")

    #Панель управления
    frame = tkinter.Frame(root, bg="#1a1a1a")
    frame.pack(side=tkinter.TOP, fill=tkinter.X, ipady=4)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=8)
    start_button.pack(side=tkinter.LEFT, padx=5, pady=5)

    tkinter.Label(frame, text="Шаг времени (DT):", bg="#1a1a1a", fg="white").pack(side=tkinter.LEFT, padx=2)
    time_step = tkinter.DoubleVar()
    time_step.set(1.0)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step, width=6)
    time_step_entry.pack(side=tkinter.LEFT, padx=5)

    time_speed = tkinter.DoubleVar()
    time_speed.set(70.0)
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL, from_=1, to=100, label="Скорость", bg="#1a1a1a", fg="white", highlightthickness=0)
    scale.pack(side=tkinter.LEFT, padx=5)

    load_file_button = tkinter.Button(frame, text="Открыть файл...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT, padx=5)

    #Видимость орбит
    show_orbits = tkinter.BooleanVar(value=True)
    orbit_check = tkinter.Checkbutton(
        frame, text="Отображать орбиты", variable=show_orbits, command=toggle_orbits,
        bg="#1a1a1a", fg="white", selectcolor="#333333", activebackground="#1a1a1a", activeforeground="white"
    )
    orbit_check.pack(side=tkinter.LEFT, padx=10)

    displayed_time = tkinter.StringVar()
    displayed_time.set("0.0 seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=20, bg="#1a1a1a", fg="white")
    time_label.pack(side=tkinter.RIGHT, padx=5)

    # Холст
    space = tkinter.Canvas(root, width=solar_vis.window_width, height=solar_vis.window_height, bg="black")
    space.pack(side=tkinter.BOTTOM)

    root.mainloop()

if __name__ == "__main__":
    main()