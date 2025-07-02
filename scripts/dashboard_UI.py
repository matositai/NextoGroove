import tkinter as tk
from tkinter import ttk

class MonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NextoGroove Monitor")

        # Updated names for checkboxes (bool values)
        self.bool_labels = ["Kick", "SNR", "Hats", "Toms", "Cymb"]
        self.bool_vars = [tk.BooleanVar(value=False) for _ in self.bool_labels]
        self.float_vars = [tk.DoubleVar(value=0.0) for _ in range(5)]

        self.build_ui()

    def build_ui(self):

        # Frame for Boolean checkboxes
        bool_frame = ttk.LabelFrame(self.root, text="Recognized Instruments Category")
        bool_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        for label, var in zip(self.bool_labels, self.bool_vars):
            chk = ttk.Checkbutton(bool_frame, text=label, variable=var)
            chk.pack(anchor="w", pady=4)

        # Frame for Float sliders
        float_frame = ttk.LabelFrame(self.root, text="Opposite Instruments confidence")
        float_frame.grid(row=0, column=1, padx=10, pady=10)

        for i, var in enumerate(self.float_vars):
            col = ttk.Frame(float_frame)
            col.grid(row=0, column=i, padx=5)
            lbl = ttk.Label(col, text=self.bool_labels[i])  # Match slider label with boolean name
            lbl.pack()
            slider = ttk.Scale(
                col, from_=1.0, to=0.0, orient='vertical',
                variable=var,
                command=lambda val, i=i: self.update_value_label(i)
            )
            slider.pack()
            value_lbl = ttk.Label(col, textvariable=var, width=6)
            value_lbl.pack()

    def update_value_label(self, index):
        pass  # Optional for future features like triggering events on change

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorUI(root)
    root.mainloop()
