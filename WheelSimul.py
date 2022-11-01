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
r_size = 30

#Рисунок робота
robot = field.create_rectangle(startx-r_size, starty-r_size, startx+r_size, starty+r_size)
robotcenter = field.create_oval(0, 0, 0, 0)
robotfront = field.create_line(0, 0, 0, 0)
def draw_robot(cx, cy, tilt):
    global robot, robotcenter, robotfront
    field.delete(robot)
    field.delete(robotcenter)
    field.delete(robotfront)
    alpha = -tilt-45
    robot = field.create_polygon(cx + r_size*Sin(alpha), cy + r_size*Cos(alpha),
                                 cx + r_size*Cos(alpha), cy - r_size*Sin(alpha),
                                 cx - r_size*Sin(alpha), cy - r_size*Cos(alpha),
                                 cx - r_size*Cos(alpha), cy + r_size*Sin(alpha),
                                 fill="", outline="black", width=3)
    robotcenter = field.create_oval(cx + 2, cy + 2,
                                    cx - 2, cy - 2,
                                    fill="black")
    robotfront = field.create_line(cx - r_size*Sin(alpha), cy - r_size*Cos(alpha),
                                   cx - r_size*Cos(alpha), cy + r_size*Sin(alpha),
                                   width=4, fill="green")
    time.sleep(0.0001)

working = True

#Пример движения
k = 1
c = 50
while working:
    c += 1*k
    if c >= 400:
        k = -1
    if c <= 50:
        k = 1
    draw_robot(c, c, c)
    root.update()
