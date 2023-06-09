import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")]) # Add more extensions if needed.
    if file_path is not None:
        file_path_var.set(file_path)
        default_output_path = os.path.join(os.path.dirname(file_path), "trimmed_" + os.path.basename(file_path))
        output_path_var.set(default_output_path)

def save_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4") # Change default extension if needed.
    if output_path is not None:
        output_path_var.set(output_path)

def focus_in(event):
    if output_path_var.get() == default_output_path:
        output_path_var.set('')

def focus_out(event):
    if output_path_var.get() == '':
        output_path_var.set(default_output_path)

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def trim_video():
    status_var.set("Trimming...")
    root.update()
    start_time = time_to_seconds(start_time_var.get())
    end_time = time_to_seconds(end_time_var.get())
    file_path = file_path_var.get()
    output_path = output_path_var.get()
    if output_path == '':
        output_path = default_output_path
    ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=output_path)
    status_var.set("Trim Complete")
    messagebox.showinfo("Info", "Trimming Complete")

# GUI
root = tk.Tk()
root.title('Video Trimmer')

file_path_var = tk.StringVar()
output_path_var = tk.StringVar()
start_time_var = tk.StringVar()
end_time_var = tk.StringVar()
status_var = tk.StringVar()

default_output_path = ''

tk.Label(root, text="Input File Path").grid(row=0, sticky="W")
tk.Entry(root, textvariable=file_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Open", command=open_file).grid(row=0, column=2)

tk.Label(root, text="Output File Path").grid(row=1, sticky="W")
output_entry = tk.Entry(root, textvariable=output_path_var, width=50)
output_entry.grid(row=1, column=1)
output_entry.bind("<FocusIn>", focus_in)
output_entry.bind("<FocusOut>", focus_out)
tk.Button(root, text="Save As", command=save_file).grid(row=1, column=2)

tk.Label(root, text="Start Time (HH:MM:SS)").grid(row=2, sticky="W")
tk.Entry(root, textvariable=start_time_var).grid(row=2, column=1)

tk.Label(root, text="End Time (HH:MM:SS)").grid(row=3, sticky="W")
tk.Entry(root, textvariable=end_time_var).grid(row=3, column=1)

tk.Button(root, text="Trim Video", command=trim_video).grid(row=4, column=1)

tk.Label(root, text="Status").grid(row=5, sticky="W")
tk.Label(root, textvariable=status_var).grid(row=5, column=1)

root.mainloop()
