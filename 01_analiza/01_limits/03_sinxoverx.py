import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# X values
x = np.linspace(0.01, 100, 2000)  # zaczynamy od 0.01, aby uniknąć dzielenia przez zero
y = np.sin(x)/x

# -----------------------
# 1️⃣ Static Plot
# -----------------------
plt.figure(figsize=(10,5))
plt.plot(x, y, color='blue', label='f(x) = sin(x)/x')
plt.axhline(0, color='black', linestyle='--', linewidth=0.7, label='y=0 asymptote')
plt.title("Behavior of f(x) = sin(x)/x for x → +∞")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.show()

# -----------------------
# 2️⃣ Animation
# -----------------------
fig, ax = plt.subplots(figsize=(10,5))
ax.set_xlim(0, 100)
ax.set_ylim(-0.25, 1.1)  # zakres y dopasowany do funkcji
ax.grid(True)
ax.set_title("Animation of f(x) = sin(x)/x for x → +∞")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")

# Plot static function in background
ax.plot(x, y, color='lightgray', label='f(x) = sin(x)/x')
ax.axhline(0, color='black', linestyle='--', linewidth=0.7)
point, = ax.plot([], [], 'ro', label='moving point')
ax.legend()

# Frames for animation
frames = np.linspace(0.01, 100, 500)

def animate(i):
    xi = frames[i]
    yi = np.sin(xi)/xi
    point.set_data([xi], [yi])
    return point,

anim = FuncAnimation(fig, animate, frames=len(frames), interval=20, blit=False)
plt.show(block=True)
