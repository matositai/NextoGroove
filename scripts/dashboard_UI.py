import tkinter as tk
from tkinter import ttk

class MonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NextoGroove Monitor")

        self.bool_labels = ["Kick", "SNR", "Hats", "Toms", "Cymb"]
        self.bool_vars = [tk.BooleanVar(value=False) for _ in self.bool_labels]
        self.float_vars = [tk.DoubleVar(value=0.0) for _ in range(5)]
        self.density_vars = [tk.DoubleVar(value=0.0) for _ in range(5)]

        self.build_ui()

    def build_ui(self):
        # Frame for Boolean checkboxes
        bool_frame = ttk.LabelFrame(self.root, text="Recognized Instruments Category")
        bool_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        for label, var in zip(self.bool_labels, self.bool_vars):
            chk = ttk.Checkbutton(bool_frame, text=label, variable=var)
            chk.pack(anchor="w", pady=7)
            # Frame for Density sliders
            density_frame = ttk.LabelFrame(self.root, text="Recognised density")
            density_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

            for i, var in enumerate(self.density_vars):
                row_frame = ttk.Frame(density_frame)
                row_frame.grid(row=i, column=0, pady=5, sticky="w")

                lbl = ttk.Label(row_frame, text=self.bool_labels[i], width=8, anchor="w")
                lbl.pack(side="left", padx=(0, 8))

                slider = ttk.Scale(
                    row_frame, from_=0.0, to=1.0, orient='horizontal',
                    variable=var,
                    command=lambda val, i=i: self.update_value_label(i)
                )
                slider.pack(side="left", fill="x", expand=True)

                value_lbl = ttk.Label(row_frame, textvariable=var, width=6)
                value_lbl.pack(side="left", padx=(8, 0))

        # Frame for Float sliders
        float_frame = ttk.LabelFrame(self.root, text="Opposite Instruments confidence")
        float_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        for i, var in enumerate(self.float_vars):
            row_frame = ttk.Frame(float_frame)
            row_frame.grid(row=i, column=0, pady=5, sticky="w")

            lbl = ttk.Label(row_frame, text=self.bool_labels[i], width=8, anchor="w")
            lbl.pack(side="left", padx=(0,8))

            slider = ttk.Scale(
                row_frame, from_=0.0, to=1.0, orient='horizontal',
                variable=var,
                command=lambda val, i=i: self.update_value_label(i)
            )
            slider.pack(side="left", fill="x", expand=True)

            value_lbl = ttk.Label(row_frame, textvariable=var, width=6)
            value_lbl.pack(side="left", padx=(8,0))



    def update_value_label(self, index):
        pass  # Placeholder for any update logic if needed

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorUI(root)
    root.mainloop()
