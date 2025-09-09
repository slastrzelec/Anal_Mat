import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

class FunctionPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Function Plotter — AnalizaMatematyczna 🚀")
        master.geometry("1000x650")

        # symbol
        self.x = sp.symbols('x')

        # Controls (góra)
        control = tk.Frame(master)
        control.pack(side='top', fill='x', padx=8, pady=6)

        tk.Label(control, text="f(x) =").pack(side='left')
        self.entry_func = tk.Entry(control, width=40)
        self.entry_func.pack(side='left', padx=6)
        self.entry_func.insert(0, "sin(x)/x")

        sample_list = [
            "sin(x)/x", "sin(x)", "cos(x)", "tan(x)",
            "exp(-x**2)", "log(x)", "x**2", "1/x", "sqrt(x)"
        ]
        self.cb_samples = ttk.Combobox(control, values=sample_list, width=20, state="readonly")
        self.cb_samples.pack(side='left', padx=6)
        self.cb_samples.bind("<<ComboboxSelected>>", self._on_sample)

        tk.Label(control, text="x min").pack(side='left', padx=4)
        self.entry_xmin = tk.Entry(control, width=8)
        self.entry_xmin.pack(side='left')
        self.entry_xmin.insert(0, "-10")

        tk.Label(control, text="x max").pack(side='left', padx=4)
        self.entry_xmax = tk.Entry(control, width=8)
        self.entry_xmax.pack(side='left')
        self.entry_xmax.insert(0, "10")

        tk.Label(control, text="punkty").pack(side='left', padx=4)
        self.entry_n = tk.Entry(control, width=6)
        self.entry_n.pack(side='left')
        self.entry_n.insert(0, "1000")

        self.grid_var = tk.IntVar(value=1)
        tk.Checkbutton(control, text="siatka", variable=self.grid_var).pack(side='left', padx=6)

        self.der_var = tk.IntVar(value=0)
        tk.Checkbutton(control, text="pochodna", variable=self.der_var).pack(side='left', padx=6)

        tk.Button(control, text="Rysuj", command=self.plot).pack(side='left', padx=6)
        tk.Button(control, text="Wyczyść", command=self.clear).pack(side='left', padx=2)

        # Plot area (center)
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Status (dół)
        self.status = tk.Label(master, text="Gotowe ✅", anchor='w')
        self.status.pack(side='bottom', fill='x', padx=6, pady=4)

        # Parser config: bezpieczny parser z ograniczonymi funkcjami
        self.transformations = standard_transformations + (implicit_multiplication_application,)
        self.local_dict = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
            'Abs': sp.Abs, 'abs': sp.Abs, 'pi': sp.pi, 'E': sp.E,
            'x': self.x, 'pow': sp.Pow
        }

    def _on_sample(self, event):
        v = self.cb_samples.get()
        self.entry_func.delete(0, tk.END)
        self.entry_func.insert(0, v)

    def clear(self):
        self.ax.clear()
        self.canvas.draw()
        self.status.config(text="Wykres wyczyszczony 😊")

    def plot(self):
        func_text = self.entry_func.get().strip()
        func_text = func_text.replace("^", "**")  # użytkownicy często wpisują ^ zamiast **

        # parametry
        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            npts = int(self.entry_n.get())
            if xmax <= xmin:
                raise ValueError("x max musi być większe niż x min.")
            if npts <= 10 or npts > 2000000:
                raise ValueError("Liczba punktów powinna być w zakresie 11..2_000_000.")
        except Exception as e:
            messagebox.showerror("Błąd parametrów", str(e))
            return

        # parsowanie wyrażenia (sympy)
        try:
            expr = parse_expr(func_text, local_dict=self.local_dict, transformations=self.transformations)
        except Exception as e:
            messagebox.showerror("Błąd parsowania", f"Nie udało się zinterpretować funkcji:\n{e}")
            return

        # lambdify -> numpy
        try:
            f = sp.lambdify(self.x, expr, "numpy")
        except Exception as e:
            messagebox.showerror("Błąd przygotowania funkcji", str(e))
            return

        X = np.linspace(xmin, xmax, npts)
        try:
            with np.errstate(all='ignore'):
                Y = f(X)
            Y = np.array(Y, dtype=np.complex128)
            # jeśli wartości zespolone mają niewielkie części urojone, bierzemy część rzeczywistą
            if np.iscomplexobj(Y):
                if np.max(np.abs(Y.imag)) < 1e-9:
                    Y = Y.real
                else:
                    # tam gdzie duża część urojona -> nan (nie rysujemy)
                    Y = np.where(np.abs(Y.imag) < 1e-9, Y.real, np.nan)
            else:
                Y = np.array(Y, dtype=np.float64)
        except Exception as e:
            messagebox.showerror("Błąd ewaluacji", f"Problem przy obliczaniu wartości funkcji:\n{e}")
            return

        # rysowanie
        self.ax.clear()
        self.ax.plot(X, Y, label=f"f(x) = {func_text}")
        # pochodna (opcjonalnie)
        if self.der_var.get():
            try:
                dexpr = sp.diff(expr, self.x)
                fd = sp.lambdify(self.x, dexpr, "numpy")
                with np.errstate(all='ignore'):
                    Yd = fd(X)
                Yd = np.array(Yd, dtype=np.float64)
                self.ax.plot(X, Yd, linestyle='--', label="f'(x)")
            except Exception as e:
                messagebox.showwarning("Pochodna", f"Nie udało się policzyć lub narysować pochodnej:\n{e}")

        # estetyka
        self.ax.set_xlim(xmin, xmax)
        self.ax.axhline(0, linewidth=0.6)  # oś x
        self.ax.axvline(0, linewidth=0.6)  # oś y
        if self.grid_var.get():
            self.ax.grid(True)
        self.ax.legend()
        self.ax.set_title(f"f(x) = {func_text}")

        self.canvas.draw()
        self.status.config(text="Wykres narysowany ✅")

def main():
    root = tk.Tk()
    app = FunctionPlotter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
