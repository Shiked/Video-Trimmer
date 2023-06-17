import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from customtkinter import AppearanceModeTracker
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


def placeholder(text):
    print(text)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")]) # Add more extensions
    if file_path is not None:
        file_path_var.set(file_path)
        default_output_path = os.path.join(os.path.dirname(file_path), "trimmed_" + os.path.basename(file_path))
        output_path_var.set(default_output_path)
        # Get the duration of the video
        duration = get_video_duration(file_path)
        
        # Convert the duration into HH:MM:SS format
        formatted_duration = convert_seconds(duration)
        
        # Set the text of the duration label
        duration_text.set(formatted_duration)

def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration # in seconds
    return duration
    
# Function to convert the seconds into a format: "HH:MM:SS"
def convert_seconds(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}"
    
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def save_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4") # Change default extension if needed
    if output_path is not None:
        output_path_var.set(output_path)

def focus_in(event):
    """ Clear default output path if it is the default and user focuses on the entry """
    if output_path_var.get() == default_output_path:
        output_path_var.set(' ')

def focus_out(event):
    if output_path_var.get() == ' ':
        output_path_var.set(default_output_path)


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


def set_dark_light(theme_string: str):
    """ possible values: light, dark, system """
    AppearanceModeTracker.set_appearance_mode(theme_string)
     
def get_dark_light() -> str:
    """ get current state of the appearance mode (light or dark) """
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"

def change_dark_light_event(root, new_theme_mode: str):
    ctk.set_appearance_mode(new_theme_mode)


    
# GUI

root = ctk.CTk()
root.geometry("600x500")
root.title('Video Trimmer')

ctk.set_default_color_theme("blue")  # default color theme
ctk.set_appearance_mode("System")  # default appearance mode

# Configure grid
root.grid_columnconfigure((1, 2, 3), weight=1)
root.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)


# Side bar
root.sidebar = ctk.CTkFrame(root, width=120, corner_radius=5)
root.sidebar.grid(row=0, column=0, rowspan=7, sticky="nsew")
root.sidebar.grid_rowconfigure(4, weight=1)
root.sidebar_title = ctk.CTkLabel(root.sidebar, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
root.sidebar_title.grid(row=0, column=0, pady=(5))

# Side bar title
root.main_title = ctk.CTkLabel(root, text="Trim a video", font=ctk.CTkFont(size=20, weight="bold"))
root.main_title.grid(row=0, column=1, pady=(5))

# Side bar theme
root.theme_setting_label = ctk.CTkLabel(root.sidebar, text="Theme")
root.theme_setting_label.grid(row=1, column=0, padx=5, pady=(25, 0))
root.theme_setting_chooser = ctk.CTkOptionMenu(root.sidebar, values=["Light", "Dark", "System"], command=set_dark_light)
root.theme_setting_chooser.grid(row=2, column=0)
root.theme_setting_chooser.set("System") # Set initial value to "system" on the GUI option menu

# Side bar UI size
root.ui_size_label = ctk.CTkLabel(root.sidebar, text="UI Size (Broken)")
root.ui_size_label.grid(row=5, column=0, padx=5, pady=(5, 5))
root.ui_size_chooser = ctk.CTkOptionMenu(root.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=placeholder)
root.ui_size_chooser.grid(row=6, column=0)
root.ui_size_chooser.set("100%") # Set initial value to "100%" on the GUI option menu

root.emptyline = ctk.CTkLabel(root.sidebar, text="")
root.emptyline.grid(row=7, column=0)

# Vars for tk
file_path_var = ctk.StringVar()
output_path_var = ctk.StringVar()
start_time_var = ctk.StringVar()
end_time_var = ctk.StringVar()
status_var = ctk.StringVar()

default_output_path = ''

# Input
ctk.CTkLabel(root, text="Input File Path").grid(row=1, column=1, pady=(20, 0), sticky="nsew")
ctk.CTkEntry(root, textvariable=file_path_var).grid(row=1, column=2, pady=(35, 0))
ctk.CTkButton(root, text="Open", command=open_file).grid(row=2, column=1)

# Output
ctk.CTkLabel(root, text="Output File Path").grid(row=3, column=1, pady=(20, 0), sticky="nsew")
output_entry = ctk.CTkEntry(root, textvariable=output_path_var, placeholder_text=default_output_path)
output_entry.bind("<FocusIn>", focus_in)
output_entry.bind("<FocusOut>", focus_out)
output_entry.grid(row=3, column=2, pady=(35, 0))
ctk.CTkButton(root, text="Save As", command=save_file).grid(row=4, column=1, pady=(0, 20))

# Start time
ctk.CTkLabel(root, text="Start Time (HH:MM:SS)").grid(row=5, column=1, pady=(20, 0), sticky="nsew")
start_time_input = ctk.CTkEntry(root, textvariable=start_time_var)
start_time_input.grid(row=5, column=2, columnspan=1, pady=(20, 0), sticky="nsew")
# start_time_slider = ctk.CTkSlider(root, from )

# End time
ctk.CTkLabel(root, text="End Time (HH:MM:SS)").grid(row=6, column=1, pady=(20, 0), sticky="nsew")
end_time_input = ctk.CTkEntry(root, textvariable=end_time_var)
end_time_input.grid(row=6, column=2, columnspan=1, pady=(20, 0), sticky="nsew")
# end_time_slider = ctk.CTkSlider(root, from_=0, to=100, orient=tk.HORIZONTAL, length=200)

duration_text = ctk.StringVar()

# Create label to display duration
duration_label = ctk.CTkLabel(root, textvariable=duration_text)
duration_label.grid(row=6, column=3, columnspan=1, pady=(20, 0), sticky="nsew")
ctk.CTkButton(root, text="Trim Video", command=trim_video).grid(row=7, column=1, pady=(20, 0),)

ctk.CTkLabel(root, text="Status").grid(row=8, column=1, pady=(20, 0), sticky="nsew")
ctk.CTkLabel(root, textvariable=status_var).grid(row=8, column=2)
print(status_var)

# create main entry and button


root.mainloop()
