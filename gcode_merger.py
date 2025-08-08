import tkinter as tk
from tkinter import filedialog, messagebox

def add_start_gcode():
    file_path = filedialog.askopenfilename(title="Select Start GCode", filetypes=[("GCode files", "*.gcode")])
    if file_path:
        start_gcode_path.set(file_path)

def add_end_gcode():
    file_path = filedialog.askopenfilename(title="Select End GCode", filetypes=[("GCode files", "*.gcode")])
    if file_path:
        end_gcode_path.set(file_path)


def merge_gcodes():
    try:
        lift_by_mm = float(lift_by_mm_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the lift.")
        return

    try:
        with open(start_gcode_path.get(), 'r') as start_file, open(end_gcode_path.get(), 'r') as end_file:
            start_gcode_lines = start_file.readlines()
            end_gcode_lines = end_file.readlines()

        if not start_gcode_lines or not end_gcode_lines:
            messagebox.showerror("Error", "Please select both GCode files.")
            return

        # Find the line to stop printing in the start GCode
        stop_printing_index = None
        
        for i, line in enumerate(start_gcode_lines):
            # print(line)
            if line.startswith('; filament end gcode'):
                stop_printing_index = i
                break

        if stop_printing_index is None:
            messagebox.showerror("Error", "Could not find the stop printing line in the start GCode.")
            return

        # Find the line to start printing in the end GCode
        start_printing_index = None

        for i, line in enumerate(end_gcode_lines):
            # print(line)
            if line.startswith(';Layer: 0') or line.startswith(';LAYER:0'):
                start_printing_index = i
                break

        if start_printing_index is None:
            messagebox.showerror("Error", "Could not find the start printing line in the end GCode.")
            return


        
        # Lift the Z-axis values in the second GCode file
        for i, line in enumerate(end_gcode_lines):
            if line.startswith('G1 Z'):
                parts = line.split(' ')
                for j, part in enumerate(parts):
                    if part.startswith('Z'):
                        z_value = float(part[1:])
                        z_value += lift_by_mm
                        parts[j] = f'Z{z_value:.3f}'
                        end_gcode_lines[i] = ' '.join(parts)
                        break

        # Merge the GCode files
        merged_gcode = start_gcode_lines[:stop_printing_index] + end_gcode_lines[start_printing_index:]

        save_path = filedialog.asksaveasfilename(title="Save Merged GCode", defaultextension=".gcode", filetypes=[("GCode files", "*.gcode")])
        if save_path:
            with open(save_path, 'w') as merged_file:
                merged_file.writelines(merged_gcode)
            messagebox.showinfo("Success", "Merged GCode saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("GCode Merger")

start_gcode_path = tk.StringVar()
end_gcode_path = tk.StringVar()
lift_by_mm_var = tk.StringVar()
start_gcode = tk.StringVar()
end_gcode = tk.StringVar()

tk.Label(root, text="Start GCode:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=start_gcode_path, state="readonly", width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=add_start_gcode).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="End GCode:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=end_gcode_path, state="readonly", width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=add_end_gcode).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Lift by selected number of mm:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=lift_by_mm_var, width=10).grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Merge", command=merge_gcodes).grid(row=3, column=1, pady=10)

root.mainloop()