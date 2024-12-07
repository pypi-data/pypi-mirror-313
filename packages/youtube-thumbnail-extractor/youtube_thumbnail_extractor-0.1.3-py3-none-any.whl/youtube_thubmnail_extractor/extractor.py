import os
from moviepy.editor import VideoFileClip
from PIL import Image
import yt_dlp


class YouTubeThumbnailExtractor:
    def __init__(self, output_path="thumbnails"):
        """
        Initialize the extractor with a default output directory.
        """
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    @staticmethod
    def parse_timestamps(timestamps):
        """
        Convert timestamps from HH:MM:SS.sss format to seconds.

        Args:
            timestamps (list of str): List of timestamps in HH:MM:SS.sss format.

        Returns:
            list: List of timestamps in seconds as integers.
        """
        seconds_list = []
        for ts in timestamps:
            try:
                hours, minutes, seconds = map(float, ts.split(":"))
                total_seconds = int(hours * 3600 + minutes * 60 + seconds)
                seconds_list.append(total_seconds)
            except ValueError:
                # Skip invalid timestamp formats silently for production
                continue
        return seconds_list

    def extract_thumbnails(self, video_url, timestamps):
        """
        Extract thumbnails from a YouTube video at specified timestamps.

        Args:
            video_url (str): The URL of the YouTube video.
            timestamps (list of str): The timestamps in HH:MM:SS.sss format.

        Returns:
            list: List of PIL Image objects representing thumbnails.
        """
        # Parse the timestamps to seconds
        timestamps_in_seconds = self.parse_timestamps(timestamps)

        # Set up yt-dlp to stream the video
        ydl_opts = {
            'format': 'best',  # Best video quality
            'outtmpl': '-',  # Avoid downloading the file
            'noplaylist': True,  # Avoid downloading playlists
            'quiet': True,  # Minimize logs
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url_stream = info_dict['url']

        # Load the video stream directly using moviepy
        clip = VideoFileClip(video_url_stream)

        images = []
        for timestamp in timestamps_in_seconds:
            if timestamp > clip.duration:
                continue

            # Capture the frame at the timestamp and convert it to a PIL Image
            frame = clip.get_frame(timestamp)
            pil_image = Image.fromarray(frame)

            images.append(pil_image)

        clip.close()
        return images
