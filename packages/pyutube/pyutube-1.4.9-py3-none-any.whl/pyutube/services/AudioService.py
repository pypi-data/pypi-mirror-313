import os
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners
from pytubefix import YouTube
from moviepy.audio.io.ffmpeg_audiowriter import ffmpeg_audiowrite
from moviepy.audio.io.AudioFileClip import AudioFileClip


class AudioService:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    @yaspin(
        text=colored("Downloading the audio...", "green"),
        color="green",
        spinner=Spinners.dots13
    )
    def get_audio_streams(video: YouTube) -> YouTube:
        """
        Function to get audio streams from a video.

        Args:
            video: The video for which audio streams are to be obtained.

        Returns:
            The first audio stream found in the video.
        """
        return video.streams.filter(only_audio=True).order_by('mime_type').first()

    @staticmethod
    def convert_m4a_to_mp3(path, input_file, output_file, codec="libmp3lame", bitrate="192k"):
        """
        Converts an audio file from M4A to MP3 format using ffmpeg_audiowrite.

        Parameters:
        - path: Path to the directory containing the input and output files.
        - input_file: Path to the input M4A file.
        - output_file: Path to the output MP3 file.
        - codec: Audio codec to use for conversion (default is libmp3lame for MP3).
        - bitrate: Bitrate for the output file (default is 192k).
        """

        # Ensure the output directory exists
        output_directory = os.path.join(path, "output")
        os.makedirs(output_directory, exist_ok=True)

        # Load the M4A file as an AudioFileClip
        input_file_path = os.path.join(path, input_file)
        output_file_path = os.path.join(output_directory, os.path.basename(output_file))
        with AudioFileClip(input_file_path) as clip:
            # Extract parameters from the clip
            fps = clip.fps
            nbytes = 2  # Assuming 16-bit audio
            buffersize = 2000

            # Write the output MP3 file
            ffmpeg_audiowrite(
                clip=clip,
                filename=output_file_path,
                fps=fps,
                nbytes=nbytes,
                buffersize=buffersize,
                codec=codec,
                bitrate=bitrate,
                write_logfile=False,
                logger=None
            )

        # Delete the input file
        if os.path.exists(input_file_path):
            os.remove(input_file_path)

        # Move the MP3 file to the parent directory
        final_output_path = os.path.join(path, os.path.basename(output_file))
        os.rename(output_file_path, final_output_path)

        # Remove the output directory
        if os.path.exists(output_directory):
            os.rmdir(output_directory)
