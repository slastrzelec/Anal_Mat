import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class FunctionAnimationApp:
    def __init__(self, master):
        self.master = master
        master.title("Function Animation — AnalizaMatematyczna 🚀")
        master.geometry("1000x650")

        # Controls
        control = tk.Frame(master)
        control.pack(side='top', fill='x', padx=8, pady=6)

        tk.Label(control, text="f(x) =").pack(side='left')
        self.entry_func = tk.Entry(control, width=40)
        self.entry_func.pack(side='left', padx=6)
        self.entry_func.insert(0, "sin(x)/x")

        tk.Label(control, text="x max").pack(side='left', padx=4)
        self.entry_xmax = tk.Entry(control, width=8)
        self.entry_xmax.pack(side='left')
        self.entry_xmax.insert(0, "100")

        tk.Label(control, text="points").pack(side='left', padx=4)
        self.entry_n = tk.Entry(control, width=6)
        self.entry_n.pack(side='left')
        self.entry_n.insert(0, "2000")

        tk.Button(control, text="Draw", command=self.plot).pack(side='left', padx=6)
        tk.Button(control, text="Animate", command=self.animate_func).pack(side='left', padx=6)

        # Figure
        self.fig = Figure(figsize=(8,5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Sympy setup
        self.x = sp.symbols('x')
        self.transformations = standard_transformations + (implicit_multiplication_application,)
        self.local_dict = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
            'Abs': sp.Abs, 'abs': sp.Abs, 'pi': sp.pi, 'E': sp.E,
            'x': self.x, 'pow': sp.Pow
        }

        self.anim = None

    def parse_function(self):
        func_text = self.entry_func.get().strip()
        func_text = func_text.replace("^", "**")
        try:
            expr = parse_expr(func_text, local_dict=self.local_dict, transformations=self.transformations)
        except Exception as e:
            messagebox.showerror("Parse Error", f"Cannot parse function:\n{e}")
            return None
        try:
            f = sp.lambdify(self.x, expr, "numpy")
        except Exception as e:
            messagebox.showerror("Function Error", f"Cannot convert to numerical function:\n{e}")
            return None
        return f

    def plot(self):
        f = self.parse_function()
        if f is None:
            return
        try:
            xmax = float(self.entry_xmax.get())
            npts = int(self.entry_n.get())
        except Exception as e:
            messagebox.showerror("Parameter Error", str(e))
            return

        x_vals = np.linspace(0.01, xmax, npts)
        y_vals = f(x_vals)

        self.ax.clear()
        self.ax.plot(x_vals, y_vals, color='blue', label=f'f(x) = {self.entry_func.get()}')
        self.ax.axhline(0, color='black', linestyle='--', linewidth=0.7, label='y=0 asymptote')
        self.ax.set_xlim(0, xmax)
        self.ax.set_title("Function Plot")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def animate_func(self):
        f = self.parse_function()
        if f is None:
            return
        try:
            xmax = float(self.entry_xmax.get())
            npts = int(self.entry_n.get())
        except Exception as e:
            messagebox.showerror("Parameter Error", str(e))
            return

        x_vals = np.linspace(0.01, xmax, npts)
        y_vals = f(x_vals)

        self.ax.clear()
        self.ax.plot(x_vals, y_vals, color='lightgray', label=f'f(x) = {self.entry_func.get()}')
        self.ax.axhline(0, color='black', linestyle='--', linewidth=0.7)
        self.ax.set_xlim(0, xmax)
        self.ax.set_ylim(np.min(y_vals)-0.1, np.max(y_vals)+0.1)
        self.ax.grid(True)

        point, = self.ax.plot([], [], 'ro', label='moving point')
        self.ax.legend()
        self.canvas.draw()

        frames = x_vals

        def animate(i):
            xi = frames[i]
            yi = f(xi)
            point.set_data([xi], [yi])
            return point,

        if self.anim:
            self.anim.event_source.stop()
        self.anim = FuncAnimation(self.fig, animate, frames=len(frames), interval=20, blit=False)
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = FunctionAnimationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
