import turtle
import math
import random
import time

def get_shape_coords(a):
    num_points = 5
    sector = 2 * math.pi / num_points
    a_rot = a - math.pi / 2
    phi = (a_rot + sector / 2) % sector - sector / 2
    alpha = abs(phi)
    
    R = 15.0
    r_v = 6.5 
    delta = math.pi / 5
    B = (R - r_v * math.cos(delta)) / (r_v * math.sin(delta))
    
    r = R / (math.cos(alpha) + B * math.sin(alpha))
    
    x = r * math.cos(a)
    y = r * math.sin(a)
    return x, y

def get_evenly_spaced_angles(num_points):
    steps = 2000
    angles = [i * (math.pi * 2) / steps for i in range(steps)]
    
    distances = [0.0]
    for i in range(1, steps):
        x1, y1 = get_shape_coords(angles[i-1])
        x2, y2 = get_shape_coords(angles[i])
        distances.append(distances[-1] + math.hypot(x2 - x1, y2 - y1))
        
    total_length = distances[-1]
    target_spacing = total_length / num_points
    
    a_vals = []
    current_target = 0.0
    
    for i in range(steps - 1):
        while distances[i] <= current_target < distances[i+1]:
            fraction = (current_target - distances[i]) / (distances[i+1] - distances[i])
            a_vals.append(angles[i] + fraction * (angles[i+1] - angles[i]))
            current_target += target_spacing
            if len(a_vals) == num_points:
                return a_vals
    return a_vals

def draw_mini_star(t, c):
    h = t.heading()
    t.color(c)
    t.penup()
    t.backward(3)
    t.left(18) 
    t.pendown()
    t.begin_fill()
    for _ in range(5):
        t.forward(7)
        t.right(144)
    t.end_fill()
    t.penup()
    t.setheading(h)

def draw_inner_shape(t, colors, a_vals):
    t.penup()
    for a in a_vals[::4]:
        bx, by = get_shape_coords(a)
        t.goto(bx * 2.5, by * 2.5)
        core_color = random.choice(['#FFFFFF', '#FFD700', '#FFFACD'])
        t.pensize(1)
        draw_mini_star(t, core_color)

def draw_straight_line(t, sx, sy, ex, ey):
    t.penup()
    t.goto(sx, sy)
    t.pendown()
    for i in range(1, 7):
        st = i / 6
        nx = sx + (ex - sx) * st
        ny = sy + (ey - sy) * st
        t.goto(nx, ny)

screen = turtle.Screen()
screen.bgcolor('#08081a') 
screen.title("Cosmic Starburst")
screen.tracer(1) 

t = turtle.Turtle()
t.speed(0) 
t.hideturtle()

colors = ['#FFFFFF', '#FFD700', '#00FFFF', '#87CEFA', '#FFFACD', '#F0E68C', '#E0FFFF']
num_lines = 120
a_vals = get_evenly_spaced_angles(num_lines)

draw_inner_shape(t, colors, a_vals)

for a in a_vals:
    bx, by = get_shape_coords(a)
    ex, ey = bx * 15, by * 15
    sx, sy = bx * 2.5, by * 2.5
    
    c = random.choice(colors)
    t.color(c)
    t.pensize(random.choice([1, 1, 2])) 
    draw_straight_line(t, sx, sy, ex, ey)
    
    t.pensize(1) 
    draw_mini_star(t, c)

screen.update() 
time.sleep(1)   
screen.tracer(0) 

try:
    while True:
        t.clear()
        draw_inner_shape(t, colors, a_vals)
        
        for a in a_vals:
            bx, by = get_shape_coords(a)
            ex, ey = bx * 15, by * 15
            sx, sy = bx * 2.5, by * 2.5
            
            c = random.choice(colors)
            t.color(c)
            t.pensize(random.choice([1, 1, 2]))
            draw_straight_line(t, sx, sy, ex, ey)
            
            t.pensize(1)
            draw_mini_star(t, c)
            
        screen.update()
        time.sleep(0.6)
        
except turtle.Terminator:
    pass
