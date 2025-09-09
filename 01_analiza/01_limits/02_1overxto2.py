import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Setup figure
fig, ax = plt.subplots(figsize=(8,5))
ax.set_title("Visualization of limit f(x) = 1/x²")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_xlim(-10, 10)
ax.set_ylim(-1, 50)
ax.grid(True)

# X values excluding zero
x_left = np.linspace(-10, -0.01, 500)
x_right = np.linspace(0.01, 10, 500)

# Plot static function
ax.plot(x_left, 1/x_left**2, color='blue', label='x → 0⁻')
ax.plot(x_right, 1/x_right**2, color='red', label='x → 0⁺')

# Asymptotes
ax.axhline(0, color='black', linestyle='--', linewidth=0.7, label='y=0 asymptote')
ax.axvline(0, color='black', linestyle='--', linewidth=0.7, label='x=0 asymptote')

# Points approaching zero
point_left, = ax.plot([], [], 'bo', label='Approaching 0 from left')
point_right, = ax.plot([], [], 'ro', label='Approaching 0 from right')

ax.legend()

# Animation frames
frames_left = np.linspace(-1, -0.01, 100)
frames_right = np.linspace(0.01, 1, 100)

def animate(i):
    point_left.set_data([frames_left[i]], [1/frames_left[i]**2])
    point_right.set_data([frames_right[i]], [1/frames_right[i]**2])
    return point_left, point_right

# Animation
anim = FuncAnimation(fig, animate, frames=100, interval=50, blit=False)

# Show plot
plt.show(block=True)
