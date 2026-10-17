import turtle
import math
import random
import time

def get_shape_coords(a):
    """
    Returns (x, y) for a perfectly sharp, straight-edged 5-pointed star.
    """
    num_points = 5
    sector = 2 * math.pi / num_points
    
    # Offset by pi/2 so the star points upwards
    a_rot = a - math.pi / 2
    
    # Localize angle to the current star point's center
    phi = (a_rot + sector/2) % sector - sector/2
    
    # Absolute local angle from the nearest tip (0 to pi/5)
    alpha = abs(phi)
    
    # Define max radius (tips) and min radius (valleys)
    R = 15.0
    r_v = 6.5 
    
    # Polar equation for a straight line connecting a tip to a valley
    delta = math.pi / 5
    B = (R - r_v * math.cos(delta)) / (r_v * math.sin(delta))
    
    r = R / (math.cos(alpha) + B * math.sin(alpha))
    
    x = r * math.cos(a)
    y = r * math.sin(a)
    return x, y

def get_evenly_spaced_angles(num_points):
    """
    Approximates the curve to find angles that result in evenly 
    spaced points along the star's perimeter based on arc length.
    """
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
    """Draws a tiny sharp star line-by-line."""
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
        # Force inner stars to be bright white/gold to act as a glowing core
        core_color = random.choice(['#FFFFFF', '#FFD700', '#FFFACD'])
        t.pensize(1)
        draw_mini_star(t, core_color)

def draw_straight_line(t, sx, sy, ex, ey):
    """Draws a straight line step-by-step so the animation is still visible."""
    t.penup()
    t.goto(sx, sy)
    t.pendown()
    
    # Break the straight line into 6 small steps for a smooth drawing animation
    for i in range(1, 7):
        st = i / 6
        nx = sx + (ex - sx) * st
        ny = sy + (ey - sy) * st
        t.goto(nx, ny)

screen = turtle.Screen()
# Deep midnight space blue background
screen.bgcolor('#08081a') 
screen.title("Cosmic Starburst - Straight Lines")

screen.tracer(1) 

t = turtle.Turtle()
t.speed(0) 
t.hideturtle()

# Celestial Star Palette: Whites, Golds, Cyans, and Light Blues
colors = ['#FFFFFF', '#FFD700', '#00FFFF', '#87CEFA', '#FFFACD', '#F0E68C', '#E0FFFF']
num_lines = 120

a_vals = get_evenly_spaced_angles(num_lines)

draw_inner_shape(t, colors, a_vals)

for a in a_vals:
    bx, by = get_shape_coords(a)
    
    ex = bx * 15
    ey = by * 15
    
    sx = bx * 2.5
    sy = by * 2.5
    
    c = random.choice(colors)
    t.color(c)
    
    # Randomize line thickness to make them look like dynamic light rays
    t.pensize(random.choice([1, 1, 2])) 
    
    # Draw straight shooting rays instead of curves
    draw_straight_line(t, sx, sy, ex, ey)
    
    # Reset pensize for the star outline
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
            
            ex = bx * 15
            ey = by * 15
            
            sx = bx * 2.5
            sy = by * 2.5
            
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