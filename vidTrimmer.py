import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from customtkinter import AppearanceModeTracker
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


class VideoProcessor:
    """
    This class handles video processing tasks such as loading video files,
    getting video duration, and trimming videos.
    """
    def __init__(self, file_path):
        """ Initializes the VideoProcessor with a file path and tries to load the video. """
        self.file_path = file_path
        self.clip = None
        try:
            self.clip = VideoFileClip(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video file: {e}")
            self.clip = None

    def get_video_duration(self):
        """ Returns the duration of the video file in seconds. If the video file is not loaded, returns 0. """
        if self.clip:
            return self.clip.duration
        else:
            return 0

    def convert_seconds(self, seconds):
        """ Converts seconds into a formatted string (HH:MM:SS). """
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}"

    def time_to_seconds(self, time_str):
        """ Converts a time string (HH:MM:SS) to seconds. """
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def trim_video(self, start_time, end_time, output_path):
        """
        Trims the video between start_time and end_time, saving the output to output_path.
        Handles exceptions that may occur during this process.
        """
        try:
            ffmpeg_extract_subclip(self.file_path, start_time, end_time, targetname=output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save video file: {e}")



class VideoTrimmerApp:
    """
    This class creates a GUI application for trimming videos.
    It allows the user to select a video file, specify start and end times, and save the trimmed video.
    """
    def __init__(self, root):
        """
        Initializes the VideoTrimmerApp with the root tkinter window.
        Sets up the GUI elements and variables.
        """
        self.root = root
        self.file_path_var = ctk.StringVar()
        self.output_path_var = ctk.StringVar()
        self.start_time_var = ctk.StringVar()
        self.end_time_var = ctk.StringVar()
        self.status_var = ctk.StringVar()
        self.video_processor = None
        self.setup_gui()
   
    def setup_gui(self):
        """
        Sets up the graphical user interface for the application.
        Includes layout, buttons, labels, and input fields.
        """
        self.root.geometry("800x500")
        self.root.title('Video Trimmer')

        ctk.set_default_color_theme("blue")  # default color theme
        ctk.set_appearance_mode("System")  # default appearance mode

        # Configure grid
        self.root.grid_columnconfigure((1, 2, 3), weight=1)
        self.root.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        # Side bar
        self.sidebar = ctk.CTkFrame(self.root, width=120, corner_radius=5)
        self.sidebar.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_title.grid(row=0, column=0, pady=(5))

        # Main title
        self.main_title = ctk.CTkLabel(self.root, text="Trim a video", font=ctk.CTkFont(size=20, weight="bold"))
        self.main_title.grid(row=0, column=1, columnspan=2, pady=(10, 10))


        # Side bar theme
        self.theme_setting_label = ctk.CTkLabel(self.sidebar, text="Theme")
        self.theme_setting_label.grid(row=1, column=0, padx=5, pady=(25, 0))
        self.theme_setting_chooser = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=set_dark_light)
        self.theme_setting_chooser.grid(row=2, column=0)
        self.theme_setting_chooser.set("System") # Set initial value to "system" on the GUI option menu

        # Side bar UI size
        self.ui_size_label = ctk.CTkLabel(self.sidebar, text="UI Size (Broken)")
        self.ui_size_label.grid(row=5, column=0, padx=5, pady=(5, 5))
        self.ui_size_chooser = ctk.CTkOptionMenu(self.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=placeholder)
        self.ui_size_chooser.grid(row=6, column=0)
        self.ui_size_chooser.set("100%") # Set initial value to "100%" on the GUI option menu

        self.emptyline = ctk.CTkLabel(self.sidebar, text="")
        self.emptyline.grid(row=7, column=0)

        self.default_output_path = ''

        # Input
        self.input_label = ctk.CTkLabel(self.root, text="Input File Path")
        self.input_label.grid(row=1, column=1, pady=(20, 0), sticky="nsew") 
        self.input_entry = ctk.CTkEntry(self.root, textvariable=self.file_path_var)
        self.input_entry.grid(row=1, column=2, pady=(35, 0))
        self.input_button= ctk.CTkButton(self.root, text="Open", command=self.open_file)
        self.input_button.grid(row=2, column=1)

        # Output
        self.output_label = ctk.CTkLabel(self.root, text="Output File Path")
        self.output_label.grid(row=3, column=1, pady=(20, 0), sticky="nsew")
        self.output_entry = ctk.CTkEntry(self.root, textvariable=self.output_path_var, placeholder_text=self.default_output_path)
        self.output_entry.bind("<FocusIn>", self.focus_in)
        self.output_entry.bind("<FocusOut>", self.focus_out)
        self.output_entry.grid(row=3, column=2, pady=(35, 0))
        self.output_button = ctk.CTkButton(self.root, text="Save As", command=self.save_file)
        self.output_button.grid(row=4, column=1, pady=(0, 20))

        # Start time
        self.start_time_label = ctk.CTkLabel(self.root, text="Start Time (HH:MM:SS)")
        self.start_time_label.grid(row=5, column=1, pady=(20, 0), sticky="nsew")
        self.start_time_input = ctk.CTkEntry(self.root, textvariable=self.start_time_var)
        self.start_time_input.grid(row=5, column=2, pady=(20, 0), sticky="nsew")
        # Slider for start time
        self.start_time_slider = ctk.CTkSlider(self.root, from_=0, to=100, command=self.update_start_time_from_slider)
        self.start_time_slider.grid(row=5, column=3, columnspan=1, padx=10, pady=10)

        # End time
        self.end_time_label = ctk.CTkLabel(self.root, text="End Time (HH:MM:SS)")
        self.end_time_label.grid(row=6, column=1, pady=(20, 0), sticky="nsew")
        self.end_time_input = ctk.CTkEntry(self.root, textvariable=self.end_time_var)
        self.end_time_input.grid(row=6, column=2, pady=(20, 0), sticky="nsew")
        # Slider for end time
        self.end_time_slider = ctk.CTkSlider(self.root, from_=0, to=100, command=self.update_end_time_from_slider)
        self.end_time_slider.grid(row=6, column=3, columnspan=1, padx=10, pady=10)

        # label to display total original clip duration
        self.original_duration_text = ctk.StringVar()
        self.original_duration_label = ctk.CTkLabel(self.root, textvariable=self.original_duration_text)
        self.original_duration_label.grid(row=7, column=3, columnspan=1, pady=(20, 0), sticky="nsew")
        
        # Label to display new clip duration 
        self.new_duration_text = ctk.StringVar()
        self.new_duration_label = ctk.CTkLabel(self.root, textvariable=self.new_duration_text)
        self.new_duration_label.grid(row=7, column=2, pady=(20, 0), sticky="nsew")
        
        self.trim_button = ctk.CTkButton(self.root, text="Trim Video", command=self.trim_video_wrapper)
        self.trim_button.grid(row=7, column=1, pady=(20, 0))

        self.status_text = ctk.CTkLabel(self.root, text="")
        self.status_text.grid(row=8, column=1, pady=(20, 0), sticky="nsew")
        self.status_label = ctk.CTkLabel(self.root, textvariable=self.status_var)
        self.status_label.grid(row=8, column=2)
        print(self.status_var)

    def open_file(self):
        """
        Opens a file dialog to select a video file.
        Updates the video processor with the selected file.
        """
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
            if file_path:
                self.file_path_var.set(file_path)
                self.video_processor = VideoProcessor(file_path)
                # Generate a default output file name
                directory, original_name = os.path.split(file_path)
                name, ext = os.path.splitext(original_name)
                default_output_name = f"trimmed-{name}{ext}"
                default_output_path = os.path.join(directory, default_output_name)
                self.output_path_var.set(default_output_path)

            # Update the duration label and set placeholders for start and end time
            duration = self.video_processor.get_video_duration()
            formatted_duration = self.video_processor.convert_seconds(duration)
            self.original_duration_text.set(f"Original clip duration: {formatted_duration}")
            self.new_duration_text.set(f"New Duration: ")
            
            # Set placeholder for start time as 00:00:00
            self.start_time_var.set("00:00:00")

            # Set placeholder for end time as the duration of the video
            self.end_time_var.set(formatted_duration)
           
            # Update sliders' maximum value
            duration_in_seconds = self.video_processor.get_video_duration()
            self.start_time_slider.configure(to=duration_in_seconds)
            self.end_time_slider.configure(to=duration_in_seconds)
            # Reset sliders' values
            self.start_time_slider.set(0)
            self.end_time_slider.set(100)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def save_file(self):
        """
        Opens a file dialog to specify the output file path for the trimmed video.
        """
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", initialfile=self.output_path_var.get())
        if output_path:
            self.output_path_var.set(output_path)

    def focus_in(self, event):
        if self.output_path_var.get() == self.default_output_path:
            self.output_path_var.set('')

    def focus_out(self, event):
        if self.output_path_var.get() == '':
            self.output_path_var.set(self.default_output_path)

    def trim_video_wrapper(self):
        """
        Wrapper for the trim_video process.
        Validates start and end times and calls the video processor to trim the video.
        """
        if self.video_processor is not None and self.video_processor.clip:
            start_time = self.video_processor.time_to_seconds(self.start_time_var.get())
            end_time = self.video_processor.time_to_seconds(self.end_time_var.get())
            if start_time < end_time <= self.video_processor.get_video_duration():
                output_path = self.output_path_var.get()
                self.video_processor.trim_video(start_time, end_time, output_path)
                self.status_var.set("Done!")
            else:
                messagebox.showerror("Error", "Invalid start or end time")
        else:
            messagebox.showerror("Error", "No video file selected or file is invalid")

    def update_start_time_from_slider(self, value):
        """ Update start time input field based on slider value. """
        formatted_time = self.video_processor.convert_seconds(int(value))
        self.start_time_var.set(formatted_time)
        self.update_new_clip_duration()  # Update the new clip duration

    def update_end_time_from_slider(self, value):
        """ Update end time input field based on slider value. """
        formatted_time = self.video_processor.convert_seconds(int(value))
        self.end_time_var.set(formatted_time)
        self.update_new_clip_duration()  # Update the new clip duration)
        
    def update_new_clip_duration(self):
        """ Calculates the new clip duration based on the start and end times and updates the label. """
        start_time = self.video_processor.time_to_seconds(self.start_time_var.get())
        end_time = self.video_processor.time_to_seconds(self.end_time_var.get())
        new_duration = end_time - start_time
        if new_duration >= 0:
            formatted_duration = self.video_processor.convert_seconds(new_duration)
            self.new_duration_text.set(f"New Duration: {formatted_duration}")
        else:
            self.new_duration_text.set("Invalid duration")


def placeholder(text):
    print(text)

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


# Main application setup and execution
root = ctk.CTk()
app = VideoTrimmerApp(root)
root.mainloop()