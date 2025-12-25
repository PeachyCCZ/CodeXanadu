import sys
import os
import vlc
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QFrame, QPushButton, QLabel, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor

# --- Configuration ---
# !!! IMPORTANT: Replace these with the actual paths to your video files !!!
VIDEO_PATH_1 = r"F:\# Videos B\2cstabigailavapreston_1080.mp4"  # e.g., "C:/videos/video1.mp4" or "/home/user/videos/video1.mp4"
VIDEO_PATH_2 = r"F:\# Videos B\JessaRhodes - angel-tits.mp4" # e.g., "C:/videos/video2.mp4" or "/home/user/videos/video2.mp4"

# --- Helper class for Video Frame with Click-to-Seek ---
class VideoFrame(QFrame):
    def __init__(self, player_instance, status_label, video_name="Video"):
        super().__init__()
        self.player = player_instance
        self.status_label = status_label
        self.video_name = video_name
        self.is_playing_flag = False

        # Set a background color so the frame is visible before video loads
        palette = self.palette()
        palette.setColor(QPalette.window, QColor(0, 0, 0)) # Black background
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mousePressEvent(self, event):
        if self.player and self.is_playing_flag: # Check if player is initialized and playing
            if event.button() == Qt.LeftButton:
                click_x = event.pos().x()
                widget_width = self.width()
                if widget_width > 0:
                    seek_to_position = float(click_x) / widget_width
                    self.player.set_position(seek_to_position)
                    current_time_ms = self.player.get_time()
                    total_time_ms = self.player.get_length()
                    if self.status_label:
                        self.status_label.setText(
                            f"{self.video_name}: Seek to {seek_to_position*100:.1f}% "
                            f"({current_time_ms//1000}s / {total_time_ms//1000}s)"
                        )
        super().mousePressEvent(event)

    def set_playing_status(self, is_playing):
        self.is_playing_flag = is_playing


# --- Main Application Window ---
class DualVideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Video Player with Click-to-Seek")
        self.setGeometry(100, 100, 1280, 550) # Window size (x, y, width, height)

        # Check if video files exist
        self.check_video_files()

        # VLC instance
        self.vlc_instance = vlc.Instance("--no-xlib") # Add --no-xlib for some Linux systems if needed

        # Media Players
        self.player1 = self.vlc_instance.media_player_new()
        self.player2 = self.vlc_instance.media_player_new()

        self.media1 = None
        self.media2 = None

        self.init_ui()
        self.load_videos()

        # Timer to update UI elements (like slider, time display) if needed
        # For this click-to-seek example, it's less critical but good for future enhancements
        self.timer = QTimer(self)
        self.timer.setInterval(200) # Update every 200 ms
        self.timer.timeout.connect(self.update_ui_elements)
        # self.timer.start() # Start if you add elements that need periodic updates

    def check_video_files(self):
        if not os.path.isfile(VIDEO_PATH_1):
            print(f"Error: Video file not found at '{VIDEO_PATH_1}'. Please check the path.")
            # You might want to show a QMessageBox here in a real app
            # For simplicity, we'll just print and continue, VLC will show an error.
        if not os.path.isfile(VIDEO_PATH_2):
            print(f"Error: Video file not found at '{VIDEO_PATH_2}'. Please check the path.")


    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Video display area
        video_area_layout = QHBoxLayout()

        self.status_label = QLabel("Status: Ready") # Shared status label

        self.video_frame1 = VideoFrame(self.player1, self.status_label, "Video 1")
        self.video_frame2 = VideoFrame(self.player2, self.status_label, "Video 2")

        video_area_layout.addWidget(self.video_frame1)
        video_area_layout.addWidget(self.video_frame2)
        layout.addLayout(video_area_layout, 1) # Give video area more stretch factor

        # Controls area
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play All")
        self.pause_button = QPushButton("Pause All")
        self.stop_button = QPushButton("Stop All")

        self.play_button.clicked.connect(self.play_all_videos)
        self.pause_button.clicked.connect(self.pause_all_videos)
        self.stop_button.clicked.connect(self.stop_all_videos)

        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        layout.addLayout(controls_layout)
        layout.addWidget(self.status_label)


    def load_videos(self):
        # Video 1
        if os.path.isfile(VIDEO_PATH_1):
            self.media1 = self.vlc_instance.media_new(VIDEO_PATH_1)
            self.player1.set_media(self.media1)
            if sys.platform.startswith('linux'): # for Linux using X Server
                self.player1.set_xwindow(self.video_frame1.winId())
            elif sys.platform == "win32": # for Windows
                self.player1.set_hwnd(self.video_frame1.winId())
            elif sys.platform == "darwin": # for macOS
                self.player1.set_nsobject(int(self.video_frame1.winId()))
        else:
            self.status_label.setText(f"Error: Video 1 not found at '{VIDEO_PATH_1}'")

        # Video 2
        if os.path.isfile(VIDEO_PATH_2):
            self.media2 = self.vlc_instance.media_new(VIDEO_PATH_2)
            self.player2.set_media(self.media2)
            if sys.platform.startswith('linux'):
                self.player2.set_xwindow(self.video_frame2.winId())
            elif sys.platform == "win32":
                self.player2.set_hwnd(self.video_frame2.winId())
            elif sys.platform == "darwin":
                self.player2.set_nsobject(int(self.video_frame2.winId()))
        else:
            self.status_label.setText(f"Error: Video 2 not found at '{VIDEO_PATH_2}'")


    def play_all_videos(self):
        if self.media1:
            self.player1.play()
            self.video_frame1.set_playing_status(True)
        if self.media2:
            self.player2.play()
            self.video_frame2.set_playing_status(True)
        self.status_label.setText("Status: Playing All")
        if not self.timer.isActive():
            self.timer.start()

    def pause_all_videos(self):
        if self.player1.is_playing():
            self.player1.pause()
            self.video_frame1.set_playing_status(False) # Or a 'paused' status
        if self.player2.is_playing():
            self.player2.pause()
            self.video_frame2.set_playing_status(False)
        self.status_label.setText("Status: Paused All")
        self.timer.stop()


    def stop_all_videos(self):
        if self.media1:
            self.player1.stop()
            self.video_frame1.set_playing_status(False)
            
        if self.media2:
            self.player2.stop()
            self.video_frame2.set_playing_status(False)
        self.status_label.setText("Status: Stopped All")
        self.timer.stop()

    def update_ui_elements(self):
        # This is where you would update sliders or time displays if you add them
        # For click-to-seek, the status label is updated directly in mousePressEvent
        pass

    def closeEvent(self, event):
        """Properly clean up VLC resources on window close."""
        self.stop_all_videos() # Stop playback
        if self.player1:
            self.player1.release()
        if self.player2:
            self.player2.release()
        if self.vlc_instance:
            self.vlc_instance.release()
        super().closeEvent(event)


if __name__ == '__main__':
    # --- Crucial: Check if video paths are placeholders ---
    if "path/to/your" in VIDEO_PATH_1 or "path/to/your" in VIDEO_PATH_2:
        print("="*50)
        print("!!! PLEASE UPDATE THE VIDEO_PATH_1 and VIDEO_PATH_2 VARIABLES !!!")
        print("Replace 'path/to/your/first/video.mp4' and 'path/to/your/second/video.mp4'")
        print("with the actual paths to your video files.")
        print("="*50)
        # You could exit here, or let it run and VLC will show an error for missing files.
        # sys.exit(1)


    app = QApplication(sys.argv)
    player_window = DualVideoPlayer()
    player_window.show()
    sys.exit(app.exec_())
