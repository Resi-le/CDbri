import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import datetime
import ctypes
import winreg
import sys
import re

# Enable High DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Python 3.13+ Compatibility (audioop missing)
if sys.version_info >= (3, 13):
    try:
        import audioop
    except ImportError:
        try:
            import pyaudioop as audioop
            sys.modules["audioop"] = audioop
        except ImportError:
            pass

# Check required libraries
try:
    from pydub import AudioSegment
except ImportError as e:
    err_msg = str(e)
    root = tk.Tk()
    root.withdraw()
    
    if "audioop" in err_msg or "pyaudioop" in err_msg:
        messagebox.showerror(
            "Python 3.13+ Issue Detected",
            "Core module 'audioop' is missing.\n"
            "Please reinstall via terminal:\n"
            "pip install pyaudioop-lts\n\n"
            f"Error: {err_msg}"
        )
    else:
         messagebox.showerror(
            "Library Missing",
            "The 'pydub' library is required.\n\n"
            "Please install it by running:\n"
            "pip install pydub"
         )
    sys.exit(1)

class AudioCDCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CDbri")
        self.root.geometry("500x720")
        self.root.resizable(False, False)
        
        # Determine script directory (Handling Nuitka/PyInstaller/Script modes)
        if getattr(sys, 'frozen', False):
            self.script_dir = os.path.dirname(sys.executable)
        elif "__compiled__" in globals():
            self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            try:
                self.script_dir = os.path.dirname(os.path.abspath(__file__))
            except NameError:
                self.script_dir = os.getcwd()
                
        icon_path = os.path.join(self.script_dir, "icon.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.file_list = []
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.colors = {
            "Light": {
                "bg": "#f0f0f0",
                "fg": "black",
                "btn_bg": "#e1e1e1",
                "btn_active": "#d0d0d0",
                "input_bg": "#ffffff",
                "input_fg": "black",
                "list_bg": "#ffffff",
                "list_fg": "black",
                "accent": "#0078d7",
                "sub_text": "#666666",
                "scroll_trough": "#f0f0f0",
                "scroll_thumb": "#cdcdcd",
                "scroll_arrow": "#606060",
                "progress_bg": "#e6e6e6"
            },
            "Dark": {
                "bg": "#2b2b2b",
                "fg": "#e0e0e0",
                "btn_bg": "#3c3c3c",
                "btn_active": "#505050",
                "input_bg": "#1e1e1e",
                "input_fg": "#ffffff",
                "list_bg": "#1e1e1e",
                "list_fg": "#e0e0e0",
                "accent": "#4cc2ff",
                "sub_text": "#aaaaaa",
                "scroll_trough": "#2b2b2b",
                "scroll_thumb": "#505050",
                "scroll_arrow": "#a0a0a0",
                "progress_bg": "#1e1e1e"
            }
        }

        self._create_ui()
        self.apply_theme()

    def get_system_theme(self):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, regtype = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "Light" if value == 1 else "Dark"
        except Exception:
            return "Light"

    def _set_titlebar_color(self, mode):
        try:
            self.root.update()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1 if mode == "Dark" else 0)
            
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_USE_IMMERSIVE_DARK_MODE, 
                ctypes.byref(value), 
                ctypes.sizeof(value)
            )
        except Exception:
            pass 

    def apply_theme(self):
        mode = self.get_system_theme()
        self._set_titlebar_color(mode)
        
        c = self.colors[mode]
        base_font = ("Calibri", 10)
        
        self.root.configure(bg=c["bg"])
        self.style.configure(".", background=c["bg"], foreground=c["fg"], font=base_font)
        self.style.configure("TLabel", background=c["bg"], foreground=c["fg"])
        
        self.style.configure("TButton", padding=5, relief="raised", background=c["btn_bg"], foreground=c["fg"], borderwidth=1)
        self.style.map("TButton", 
            background=[('active', c["btn_active"]), ('pressed', c["btn_bg"])],
            foreground=[('active', c["fg"])]
        )
        
        self.style.configure("TLabelframe", padding=15, relief="solid", borderwidth=1, background=c["bg"])
        self.style.configure("TLabelframe.Label", font=("Calibri", 10, "bold"), foreground=c["fg"], background=c["bg"])
        
        self.style.configure("TEntry", fieldbackground=c["input_bg"], foreground=c["input_fg"], insertcolor=c["fg"])
        
        self.style.configure("Accent.TButton", font=("Calibri", 11, "bold"), padding=8, foreground=c["fg"])
        
        self.style.configure("Vertical.TScrollbar",
            gripcount=0,
            background=c["scroll_thumb"],
            troughcolor=c["scroll_trough"],
            bordercolor=c["bg"],
            arrowcolor=c["scroll_arrow"],
            lightcolor=c["scroll_thumb"],
            darkcolor=c["scroll_thumb"]
        )
        self.style.map("Vertical.TScrollbar", background=[('active', c["btn_active"])])

        self.style.configure("Horizontal.TProgressbar",
            background=c["accent"],
            troughcolor=c["progress_bg"],
            bordercolor=c["bg"],
            lightcolor=c["accent"],
            darkcolor=c["accent"]
        )
        
        if hasattr(self, 'listbox'):
            self.listbox.configure(
                bg=c["list_bg"],
                fg=c["list_fg"],
                selectbackground=c["accent"],
                selectforeground="white" if mode == "Light" else "black"
            )
            
        if hasattr(self, 'path_info'):
            self.path_info.configure(foreground=c["sub_text"])

    def _create_ui(self):
        PAD_X = 20
        PAD_Y = 10

        top_frame = ttk.Frame(self.root, padding=(PAD_X, 15))
        top_frame.pack(fill=tk.X)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        ttk.Button(top_frame, text="Add Audio", command=self.add_files).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(top_frame, text="Remove Selected", command=self.remove_file).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(top_frame, text="Clear List", command=self.clear_files).grid(row=0, column=2, padx=5, sticky="ew")

        settings_frame = ttk.LabelFrame(self.root, text="CD information")
        settings_frame.pack(fill=tk.X, padx=PAD_X, pady=5)
        settings_frame.columnconfigure(1, weight=1)

        ttk.Label(settings_frame, text="CD Name").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.title_entry = ttk.Entry(settings_frame)
        self.title_entry.insert(0, "Audio CD")
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 5))

        ttk.Label(settings_frame, text="Artist").grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.performer_entry = ttk.Entry(settings_frame)
        self.performer_entry.insert(0, "Various Artists")
        self.performer_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 5))

        ttk.Label(settings_frame, text="Folder Name").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.folder_entry = ttk.Entry(settings_frame)
        self.folder_entry.insert(0, "New_CD")
        self.folder_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 5))
        
        save_path_preview = os.path.join(self.script_dir, "Export")
        self.path_info = ttk.Label(settings_frame, text=f"※ Saves to: {save_path_preview}\\[Folder Name]", font=("Calibri", 8))
        self.path_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(5, 0))

        list_container = ttk.Frame(self.root)
        list_container.pack(fill=tk.BOTH, expand=True, padx=PAD_X, pady=PAD_Y)

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_container, 
            selectmode=tk.EXTENDED, 
            yscrollcommand=scrollbar.set,
            bd=1, 
            relief="sunken",
            highlightthickness=0,
            font=("Calibri", 10)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        order_frame = ttk.Frame(self.root)
        order_frame.pack(fill=tk.X, padx=PAD_X, pady=5)
        order_frame.columnconfigure(0, weight=1)
        order_frame.columnconfigure(1, weight=1)
        
        ttk.Button(order_frame, text="▲ Move Up", command=self.move_up).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(order_frame, text="▼ Move Down", command=self.move_down).grid(row=0, column=1, padx=5, sticky="ew")

        action_frame = ttk.Frame(self.root, padding=(0, 20))
        action_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(action_frame, text="READY", font=("Calibri", 9))
        self.status_label.pack(side=tk.TOP, pady=5)

        self.progress = ttk.Progressbar(action_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(side=tk.TOP, pady=(0, 15), padx=PAD_X, fill=tk.X)

        create_btn = ttk.Button(action_frame, text="GO", style="Accent.TButton", command=self.start_creation_thread)
        create_btn.pack(side=tk.TOP, pady=(0, 10), ipadx=30, ipady=5)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio",
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a"), ("All Files", "*.*")]
        )
        for f in files:
            self.file_list.append(f)
            filename = os.path.basename(f)
            self.listbox.insert(tk.END, f"{len(self.file_list)}. {filename}")

    def remove_file(self):
        selection = self.listbox.curselection()
        if not selection: return
        for index in reversed(selection):
            self.file_list.pop(index)
            self.listbox.delete(index)
        self.refresh_list_numbers()

    def clear_files(self):
        self.file_list = []
        self.listbox.delete(0, tk.END)

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection: return
        
        new_selection = []
        for i in selection:
            if i == 0: 
                new_selection.append(i)
                continue
            text = self.file_list.pop(i)
            self.file_list.insert(i-1, text)
            new_selection.append(i-1)
            
        self.refresh_list()
        
        for i in new_selection:
            self.listbox.selection_set(i)
        if new_selection:
            self.listbox.see(new_selection[0])
        
    def move_down(self):
        selection = self.listbox.curselection()
        if not selection: return
        
        new_selection = []
        for i in reversed(selection):
            if i == len(self.file_list) - 1: 
                new_selection.append(i)
                continue
            text = self.file_list.pop(i)
            self.file_list.insert(i+1, text)
            new_selection.append(i+1)
            
        self.refresh_list()
        
        for i in new_selection:
            self.listbox.selection_set(i)
        if new_selection:
            self.listbox.see(new_selection[-1])

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for idx, f in enumerate(self.file_list):
            filename = os.path.basename(f)
            self.listbox.insert(tk.END, f"{idx+1}. {filename}")

    def refresh_list_numbers(self):
        self.refresh_list()

    def sanitize_filename(self, name):
        # Remove characters invalid in Windows filenames
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def start_creation_thread(self):
        if not self.file_list:
            messagebox.showwarning("Warning!", "No audio added.")
            return
        
        cd_title = self.title_entry.get().strip() or "My Audio CD"
        performer = self.performer_entry.get().strip() or "Various Artists"
        folder_name = self.folder_entry.get().strip() or f"Music_CD_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        export_root = os.path.join(self.script_dir, "Export")

        t = threading.Thread(target=self.create_cd_files, args=(export_root, folder_name, cd_title, performer))
        t.start()

    def create_cd_files(self, export_root, folder_name, cd_title, performer):
        try:
            if not os.path.exists(export_root): os.makedirs(export_root)
            output_dir = os.path.join(export_root, folder_name)
            if not os.path.exists(output_dir): os.makedirs(output_dir)

            total_files = len(self.file_list)
            
            # Sanitize CD title for filename usage
            file_base_name = self.sanitize_filename(cd_title)
            bin_filename = f"{file_base_name}.bin"
            
            cue_content = []
            cue_content.append(f'TITLE "{cd_title}"')
            cue_content.append(f'PERFORMER "{performer}"')
            cue_content.append(f'FILE "{bin_filename}" BINARY')

            combined_audio = AudioSegment.empty()
            current_time_ms = 0
            CD_SAMPLE_RATE = 44100
            CD_SAMPLE_WIDTH = 2
            CD_CHANNELS = 2

            for i, file_path in enumerate(self.file_list):
                track_num = i + 1
                self.root.after(0, self.update_status, f"Processing Track {track_num}... ({os.path.basename(file_path)})")
                
                try:
                    audio = AudioSegment.from_file(file_path)
                    audio = audio.set_frame_rate(CD_SAMPLE_RATE)
                    audio = audio.set_sample_width(CD_SAMPLE_WIDTH)
                    audio = audio.set_channels(CD_CHANNELS)

                    # Insert 2s silence for CD gap (except for the first track usually, 
                    # but here we prepend if index>0 to separate tracks properly)
                    if i > 0:
                        silence = AudioSegment.silent(duration=2000, frame_rate=CD_SAMPLE_RATE)
                        silence = silence.set_sample_width(CD_SAMPLE_WIDTH).set_channels(CD_CHANNELS)
                        combined_audio += silence
                        current_time_ms += 2000
                    
                    # Calculate CUE timestamps (75 frames/sec)
                    total_seconds = current_time_ms / 1000.0
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    frames = int((total_seconds - int(total_seconds)) * 75)
                    time_str = f"{minutes:02d}:{seconds:02d}:{frames:02d}"
                    
                    cue_content.append(f'  TRACK {track_num:02d} AUDIO')
                    cue_content.append(f'    TITLE "{os.path.splitext(os.path.basename(file_path))[0]}"') 
                    cue_content.append(f'    INDEX 01 {time_str}')
                    
                    combined_audio += audio
                    current_time_ms += len(audio)

                except Exception as e:
                    messagebox.showerror("Error!", f"An error occurred while processing the file...\n{file_path}\n\n{str(e)}")
                    self.root.after(0, self.reset_ui)
                    return

                progress_val = ((i + 1) / total_files) * 50 
                self.root.after(0, self.update_progress, progress_val)

            self.root.after(0, self.update_status, "Saving BIN...")
            output_bin = os.path.join(output_dir, bin_filename)
            output_cue = os.path.join(output_dir, f"{file_base_name}.cue")

            combined_audio.export(output_bin, format="raw")
            self.root.after(0, self.update_progress, 90)

            with open(output_cue, "w", encoding="utf-8") as f:
                f.write("\n".join(cue_content))
            
            self.root.after(0, self.update_progress, 100)
            self.root.after(0, self.update_status, "DONE!")
            messagebox.showinfo("Success", f"Task succeed!\n\nFolder Location is \n{output_dir}")

        except Exception as e:
            messagebox.showerror("Fatal Error!", f"Task failed... {str(e)}")
        finally:
            self.root.after(0, self.reset_ui)

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_progress(self, val):
        self.progress["value"] = val

    def reset_ui(self):
        self.progress["value"] = 0
        self.status_label.config(text="READY")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioCDCreatorApp(root)
    root.mainloop()
