import tkinter as tk
import math
import time

#Регуляция значения
def Clip(a, min, max):
    if a < min:
        a = min
    if a > max:
        a = max
    return a

#Синус
def Sin(a):
    return math.sin(math.radians(a))

#Косинус
def Cos(a):
    return math.cos(math.radians(a))

#Арктангенс в градусах
def Arctg(a):
    return math.degrees(math.atan(a))

#Получение угла через дельта x и дельта y
def get_ang(delt_x, delt_y):
    
    if delt_x == 0:
        if delt_y < 0:
            ang = 0
        if delt_y > 0:
            ang = 180

    if delt_x < 0:
        ang = 270 - Arctg(-delt_y/delt_x)

    if delt_x > 0:
        ang = 90 - Arctg(-delt_y/delt_x)

    return ang
    

#Окно ввода движений
input_root = tk.Tk()
input_root.geometry("1000x600")
input_root.title("WheelSimul")

#Рисунок поля
input_field = tk.Canvas(input_root, width=600, height=600, bd=0, bg="#8c8c8c", highlightthickness=0)
input_field.place(x=0, y=0)

#Размер сетки
grid = 6

#Рисунок сетки на поле
for i in range(grid):
    tile = 600/grid
    input_field.create_line(0, tile*i, 600, tile*i, width=1, fill="#434343")
    input_field.create_line(tile*i, 0, tile*i, 600, width=1, fill="#434343")

#Предыдущие координаты
prevx = 0
prevy = 0

#Счётчик нажатий
clicknum = 0

#Массив с точками
point_arr = []

#Функция ввода точки
def input_point(event):
    
    global clicknum, prevx, prevy, input_field
    
    x, y = event.x, event.y
    
    clicknum += 1
    if clicknum >= 2:
        input_field.create_line(prevx, prevy, x, y, fill="red", width=3)
    input_field.create_oval(x+7, y+7, x-7, y-7, fill="red")
        
    point_arr.append([x, y])
    print("Точка (" + str(x) + "; " + str(y) + ") введена")

    prevx = x
    prevy = y

input_field.bind("<Button-1>", input_point)

#ЦИКЛ РАЗМЕТКИ ТРАЕКТОРИИ
planned = False
while not planned:
    try:
        input_root.update()
    except tk.TclError:
        planned = True

print(point_arr)

#______________________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________________

#Окно движений
root = tk.Tk()
root.geometry("1000x600")
root.title("WheelSimul")

#Рисунок поля
field = tk.Canvas(root, width=600, height=600, bd=0, bg="#8c8c8c", highlightthickness=0)
field.place(x=0, y=0)

#Размер сетки
grid = 6

#Рисунок сетки на поле
for i in range(grid):
    tile = 600/grid
    field.create_line(0, tile*i, 600, tile*i, width=1, fill="#434343")
    field.create_line(tile*i, 0, tile*i, 600, width=1, fill="#434343")

#Стартовые координаты
rx = 300
ry = 300

#Размеры робота
r_size_x = 30
r_size_y = 30

#Рисунок робота
robot = field.create_rectangle(rx-r_size_x, ry-r_size_y, rx+r_size_x, ry+r_size_y)
robotcenter = [field.create_oval(0, 0, 0, 0)]
robotfront = field.create_line(0, 0, 0, 0)

wheel_nw = field.create_line(0, 0, 0, 0)
wheel_ne = field.create_line(0, 0, 0, 0)
wheel_se = field.create_line(0, 0, 0, 0)
wheel_sw = field.create_line(0, 0, 0, 0)

#Изменение координат и угла поворота робота
delta_x = 0
delta_y = 0
delta_a = 0

#Углы робота
robot_edges = [[0, 0],
               [0, 0],
               [0, 0],
               [0, 0]]

#Рисунок вектора
vector = field.create_line(0, 0, 0, 0)

#Функция рисования робота
def draw_robot(cx, cy, tilt=0, trajectory=False, trajlen=500):
    global robot, robotcenter, robotfront, wheel_nw, wheel_ne, wheel_se, wheel_sw, delta_x, delta_y, delta_a, rx, ry, robot_edges, vector

    alpha = -tilt-45

    robot_edges = [[cx + r_size_x*Sin(alpha), cy + r_size_y*Cos(alpha)],
                   [cx + r_size_x*Cos(alpha), cy - r_size_y*Sin(alpha)],
                   [cx - r_size_x*Sin(alpha), cy - r_size_y*Cos(alpha)],
                   [cx - r_size_x*Cos(alpha), cy + r_size_y*Sin(alpha)]]

    robot_edges_clipped = []
    for i in robot_edges:
        robot_edges_clipped.append([Clip(i[0], 0, 600), Clip(i[1], 0, 600)])

    if not trajectory:
        field.delete(robotcenter[-1])

    if len(robotcenter) >= trajlen:
        field.delete(robotcenter[-trajlen])

    field.delete(robot)
    field.delete(robotfront)
    field.delete(wheel_nw)
    field.delete(wheel_ne)
    field.delete(wheel_se)
    field.delete(wheel_sw)
    field.delete(vector)

    robot = field.create_polygon(cx + r_size_x*Sin(alpha), cy + r_size_y*Cos(alpha),
                                 cx + r_size_x*Cos(alpha), cy - r_size_y*Sin(alpha),
                                 cx - r_size_x*Sin(alpha), cy - r_size_y*Cos(alpha),
                                 cx - r_size_x*Cos(alpha), cy + r_size_y*Sin(alpha),
                                 fill="", outline="black", width=3)

    robotcenter.append(field.create_oval(cx + 2, cy + 2,
                                    cx - 2, cy - 2,
                                    fill="red", outline="red"))

    robotfront = field.create_line(cx - r_size_x*Sin(alpha), cy - r_size_y*Cos(alpha),
                                   cx - r_size_x*Cos(alpha), cy + r_size_y*Sin(alpha),
                                   width=4, fill="green")

    wheel_nw = field.create_oval(cx + r_size_x * Cos(alpha) - 4, cy - r_size_y * Sin(alpha) - 4,
                                 cx + r_size_x * Cos(alpha) + 4, cy - r_size_y * Sin(alpha) + 4,
                                 fill="black")

    wheel_ne = field.create_oval(cx - r_size_x * Sin(alpha) - 4, cy - r_size_y * Cos(alpha) - 4,
                                 cx - r_size_x * Sin(alpha) + 4, cy - r_size_y * Cos(alpha) + 4,
                                 fill="black")

    wheel_se = field.create_oval(cx - r_size_x * Cos(alpha) - 4, cy + r_size_y * Sin(alpha) - 4,
                                 cx - r_size_x * Cos(alpha) + 4, cy + r_size_y * Sin(alpha) + 4,
                                 fill="black")

    wheel_sw = field.create_oval(cx + r_size_x * Sin(alpha) - 4, cy + r_size_y * Cos(alpha) - 4,
                                 cx + r_size_x * Sin(alpha) + 4, cy + r_size_y * Cos(alpha) + 4,
                                 fill="black")

    dx = cx - rx
    dy = cy - ry

    vector = field.create_line(rx, ry,
                               rx + dx * 60, ry + dy * 60,
                               fill="blue", arrow=tk.LAST)

    rx = cx
    ry = cy

    time.sleep(0.0001)

#Функция движения робота
def apply_vector(object, strength, angle):
    global robot, robotcenter, robotfront, wheel_nw, wheel_ne, wheel_se, wheel_sw, delta_x, delta_y, delta_a, rx, ry, robot_edges, vector

    strength = strength * 2

    beta = -angle % 360

    if object == robotcenter:
        delta_a = 0
        delta_x = -strength*Sin(beta)
        delta_y = -strength*Cos(beta)

#ОСНОВНОЙ ЦИКЛ

working = True

start_time = time.time()
delta_time = 0

#Движение робота
while working:
    try:
        k = 1

        curr_time = time.time()
        delta_time = curr_time - start_time

        apply_vector(robotcenter, 1, -170)

        draw_robot(rx+delta_x, ry+delta_y, trajectory=True, trajlen=400)

        delta_x = 0
        delta_y = 0

        root.update()

    except tk.TclError:
        working = False
