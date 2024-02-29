import customtkinter as ctk
from pytube import YouTube
import sys
import os 

PATH ="Videos"


#caution
def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS2
    
    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def download_video_from_youtube(self, link):

    def on_progress(streams, chunk, bytes_remaining):

        total_size = streams.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size)
        self.progress_bar.set(percentage)
        self.update_idletasks()

    yt = YouTube(link)
    yt.register_on_progress_callback(on_progress)
    video = yt.streams.get_highest_resolution()
    self.download_button.configure(text="Downloading...")
    video.download(output_path=resource_path(PATH))


#center the ui to the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) //2
    y = (screen_height - height) //2

    window.geometry(f"{width}x{height}+{x}+{y}")


class DownloaderFrame(ctk.CTkFrame):
    def __init__(self, app = None):
        super().__init__(app)

        #input box
        self.input_link = ctk.CTkEntry(self, width=400, placeholder_text= "Paste YouTube  Link Here")
        self.input_link.pack(padx =10, pady = 30)

        #Download button
        self.download_button = ctk.CTkButton(self, text="Download", command=self.prepare_download)
        self.download_button.pack(padx =10, pady =3)

        #Label text box
        self.download_status_label =ctk.CTkLabel(self, text="")

        #progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.update_idletasks()
      
    
    def prepare_download(self):
        self.download_button.configure(text="Processing...")
        self.download_button.configure(state="disabled")
        self.update_idletasks()
        self.download_status_label.pack(padx =10, pady =6)
        self.progress_bar.pack(padx =10, pady =9)
        self.start_downlaod()
  
    
    def start_downlaod(self):
        video_url = self.input_link.get()
       

        if video_url:
            download_video_from_youtube(self,video_url)
        
        #reset values
        self.download_button.configure(state="normal")
        self.download_button.configure(text="Download")
        self.download_status_label.configure(text =" Video Saved: "+resource_path(PATH))
        self.input_link.delete(0, "end")



if __name__ =="__main__":
    app = ctk.CTk()
    app.title("YouTube Video Downloader")
    center_window(app, 800, 600)
    downloader = DownloaderFrame(app=app)
    downloader.pack(fill="both", expand =True)
    downloader.mainloop()
