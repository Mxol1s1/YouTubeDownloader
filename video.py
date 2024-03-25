import threading
import queue
import customtkinter as ctk
from pytube import YouTube
import sys
import os

PATH = "Videos"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def download_video_from_youtube(link, frame_ui, completion_callback):

 
    def on_progress(stream, chunk, remaining_bytes):
        total_size = stream.filesize
        bytes_downloaded = total_size - remaining_bytes
        frame_ui.progress_bar.set(bytes_downloaded / total_size)
        frame_ui.update_idletasks()

    yt = YouTube(link)
    yt.register_on_progress_callback(on_progress)
    video = yt.streams.get_highest_resolution()
    video.download(output_path=resource_path(PATH))
    completion_callback()

class DownloadManager(threading.Thread):
    def __init__(self, downloader_frame):
        super().__init__()
        self.downloader_frame = downloader_frame
        self.download_queue = queue.Queue()
        # self.progress_queue = queue.Queue()
        self.running = True
        self.completed_downloads = 0
        self.total_videos =0

    def enqueue_download(self, video_url):
        self.download_queue.put(video_url)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if not self.download_queue.empty():
                link = self.download_queue.get()
                self.downloader_frame.notify_download_complete() #wild card to be modified
                self.downloader_frame.progress_bar.pack(padx=10, pady=9)
                self.downloader_frame.update_idletasks()
                download_video_from_youtube(link, self.downloader_frame,  self.download_completed)
            else:
                # Queue is empty, wait for some time before checking again
                self.downloader_frame.update_download_count_label()
                self.downloader_frame.update_idletasks()
                threading.Event().wait(1)
               
                

    def download_completed(self):
        self.completed_downloads += 1
        self.downloader_frame.notify_download_complete()

class DownloaderFrame(ctk.CTkFrame):
    def __init__(self, app=None):
        super().__init__(app)

        self.input_link = ctk.CTkEntry(self, width=400, placeholder_text="Paste YouTube Link Here")
        self.input_link.pack(padx=10, pady=30)

        self.download_button = ctk.CTkButton(self, text="Download", command=self.enqueue_download)
        self.download_button.pack(padx=10, pady=3)

        self.download_status_label = ctk.CTkLabel(self, text="")
        self.download_status_label.pack(padx=10, pady=6)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)

        self.download_manager = DownloadManager(self)
        self.download_manager.start()
   


    def enqueue_download(self):
        video_url = self.input_link.get()
        if video_url:
            self.download_manager.enqueue_download(video_url)
            self.download_manager.total_videos +=1
            self.input_link.delete(0, "end")
            self.update_download_count_label()

    def update_download_count_label(self):
        queue_size = self.download_manager.download_queue.qsize()
        self.download_status_label.configure(text=f"Videos in Queue: {queue_size}, Completed: {self.download_manager.completed_downloads}/{self.download_manager.total_videos}")


    def notify_download_complete(self):
        self.update_download_count_label()

    def on_exit(self):
        self.download_manager.stop()
        self.download_manager.join()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("YouTube Video Downloader")
    downloader = DownloaderFrame(app=app)
    downloader.pack(fill="both", expand=True)
    app.mainloop()
