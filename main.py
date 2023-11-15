import subprocess
import re
import customtkinter as ctk  # CustomTkinter for modern UI elements
from tkinter import filedialog, ttk  # Tkinter for file dialogs and styling

def run_ffmpeg_command(command, duration):
    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Regex pattern to match the time
    time_pattern = re.compile(r"time=(\d+:\d+:\d+.\d+)")

    # Loop to parse FFmpeg stderr output and update the progress bar
    while True:
        line = process.stderr.readline()
        if line == '' and process.poll() is not None:
            break
        if line:
            match = time_pattern.search(line)
            if match:
                elapsed_time = match.group(1)
                progress = get_progress(elapsed_time, duration)
                progress_bar['value'] = progress
                app.update_idletasks()
    if process.poll() != 0:
        raise subprocess.CalledProcessError(process.returncode, command)

def get_duration(file_path):
    # Get the duration of the video
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=True
    )
    duration = result.stdout.strip()
    return float(duration)

def get_progress(elapsed_time, duration):
    # Convert the HH:MM:SS.FF format into seconds
    h, m, s = elapsed_time.split(':')
    elapsed_seconds = int(h) * 3600 + int(m) * 60 + float(s)
    # Calculate the progress as a percentage
    progress = int((elapsed_seconds / duration) * 100)
    return progress

def merge_audio_tracks():
    input_video = input_path.get()
    output_video = output_path.get()

    if not input_video or not output_video:
        result_label.configure(text="Please select both input and output files.")
        return

    try:
        duration = get_duration(input_video)
        command = [
            "ffmpeg", "-y", "-i", input_video,
            "-filter_complex", "[0:a:0][0:a:1]amerge=inputs=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
            output_video
        ]
        run_ffmpeg_command(command, duration)
        update_result_label("Success! The audio tracks have been merged and saved in the new video file.", 'info')
    except Exception as e:
        update_result_label(f"Error: {str(e)}", 'error')

# Function to update the message label and make it visible
def update_result_label(message, message_type='info'):
    # Configure text and colors based on the type of message
    if message_type == 'info':
        result_label.configure(text=message, fg_color="#D4EDDA", text_color="#155724")
    elif message_type == 'error':
        result_label.configure(text=message, fg_color="#F8D7DA", text_color="#721C24")
    
    # Make the label visible
    result_label.pack(pady=10)

# Main application configuration
ctk.set_appearance_mode("Dark")  # Set the theme of CustomTkinter
ctk.set_default_color_theme("blue")  # Set color theme to blue

# Main window setup
app = ctk.CTk()
app.title("Audio Track Merger")
app.geometry("745x240")  # Define the fixed size of the window
app.resizable(False, False)  # Disable window resizing

# Progress bar styling to match the CustomTkinter button color
button_color = "#4C8CBF"  # Example color for buttons and progress bar
style = ttk.Style(app)
style.theme_use('clam')
style.configure("Horizontal.TProgressbar", troughcolor="#333333", bordercolor="#333333",
                background=button_color, lightcolor=button_color, darkcolor=button_color)

# Layout frames setup
top_frame = ctk.CTkFrame(app)
top_frame.pack(pady=(10, 0), padx=10, fill="x", expand=True)

bottom_frame = ctk.CTkFrame(app)
bottom_frame.pack(pady=(0, 10), padx=10, fill="x", expand=True)

# Top frame components for input and output selection
input_path_label = ctk.CTkLabel(top_frame, text="Select your video file:")
input_path_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
input_path = ctk.CTkEntry(top_frame, width=400, corner_radius=10)
input_path.grid(row=0, column=1, pady=2, padx=10)
input_path_button = ctk.CTkButton(top_frame, text="Browse", corner_radius=10, fg_color=button_color, command=lambda: input_path.insert(ctk.END, filedialog.askopenfilename()))
input_path_button.grid(row=0, column=2, pady=10, padx=10)

output_path_label = ctk.CTkLabel(top_frame, text="Save the new video as:")
output_path_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
output_path = ctk.CTkEntry(top_frame, width=400, corner_radius=10)
output_path.grid(row=1, column=1, pady=2, padx=10)
output_path_button = ctk.CTkButton(top_frame, text="Save As...", corner_radius=10, fg_color=button_color, command=lambda: output_path.insert(ctk.END, filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])))
output_path_button.grid(row=1, column=2, pady=10, padx=10)

# Bottom frame components for merge operation
merge_button = ctk.CTkButton(bottom_frame, text="Merge Audio Tracks", fg_color=button_color, corner_radius=10, command=merge_audio_tracks)
merge_button.pack(pady=10, fill="x", padx=20)

progress_bar = ttk.Progressbar(bottom_frame, length=450, mode="determinate", style="Horizontal.TProgressbar")
progress_bar.pack(pady=10, fill="x", padx=20)

# Status message label, initially hidden
result_label = ctk.CTkLabel(bottom_frame, text="", fg_color="#D4EDDA", text_color="#155724", corner_radius=10)
result_label.pack_forget()

# Start the application
app.mainloop()