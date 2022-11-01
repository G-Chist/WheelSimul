import tkinter as tk
import math
import time

#Синус
def Sin(a):
    return math.sin(math.radians(a))

#Косинус
def Cos(a):
    return math.cos(math.radians(a))

#Окно
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
startx = 100
starty = 100

#Размеры робота
r_size_x = 30
r_size_y = 30

#Рисунок робота
robot = field.create_rectangle(startx-r_size_x, starty-r_size_y, startx+r_size_x, starty+r_size_y)
robotcenter = [field.create_oval(0, 0, 0, 0)]
robotfront = field.create_line(0, 0, 0, 0)

wheel_nw = field.create_line(0, 0, 0, 0)
wheel_ne = field.create_line(0, 0, 0, 0)
wheel_se = field.create_line(0, 0, 0, 0)
wheel_sw = field.create_line(0, 0, 0, 0)

#Функция движения робота
def draw_robot(cx, cy, tilt, trajectory=False, trajlen=500):
    global robot, robotcenter, robotfront, wheel_nw, wheel_ne, wheel_se, wheel_sw

    field.delete(robot)
    field.delete(robotfront)

    if not trajectory:
        field.delete(robotcenter[-1])

    if len(robotcenter) >= trajlen:
        field.delete(robotcenter[-trajlen])

    field.delete(wheel_nw)
    field.delete(wheel_ne)
    field.delete(wheel_se)
    field.delete(wheel_sw)

    alpha = -tilt-45

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
    time.sleep(0.0001)

working = True

#Пример движения
k = 1
c = 50
while working:
    c += 1*k
    if c >= 500:
        k = -1
    if c <= 50:
        k = 1
    try:
        draw_robot(c, 200+Sin(c)*50, c, trajectory=True, trajlen=100)
        root.update()
    except tk.TclError:
        working = False
