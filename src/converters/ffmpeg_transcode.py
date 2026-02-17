import subprocess
import os
from pathlib import Path
from typing import Optional


class FFmpegTranscoder:
    def __init__(self, input_file: str, output_dir: str, input_type: str, output_type: str):
        """
        Initialize FFmpeg converter.
        
        Args:
            input_file: Path to the input audio/video file
            output_dir: Directory where the converted file will be saved
            input_type: Input file format (e.g., 'mp4', 'avi', 'mp3', 'wav')
            output_type: Output file format (e.g., 'mp4', 'avi', 'mp3', 'wav')
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.input_type = input_type.lstrip('.')
        self.output_type = output_type.lstrip('.')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def can_transcode(self) -> bool:
        """
        Check if the input file can be transcoded to the output format.
        
        Returns:
            True if transcoding is possible, False otherwise
        """
        # Define format categories
        video_formats = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'mpg', 'mpeg', 'm4v']
        audio_formats = ['mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'm4a', 'opus', 'alac']
        
        all_supported = video_formats + audio_formats
        
        # Check if formats are supported
        if self.input_type not in all_supported or self.output_type not in all_supported:
            return False
        
        # Determine input and output categories
        input_is_audio = self.input_type in audio_formats
        output_is_video = self.output_type in video_formats
        
        # Invalid: Cannot convert audio-only to video format
        # (would need video content, not just audio)
        if input_is_audio and output_is_video:
            return False
        
        # All other conversions are valid:
        # - Video to Video (transcode)
        # - Video to Audio (extract audio)
        # - Audio to Audio (transcode)
        return True
    
    def transcode(self, overwrite: bool = True, quality: Optional[str] = None) -> str:
        """
        Transcode the input file to the output format using FFmpeg.
        
        Args:
            overwrite: Whether to overwrite existing output file (default: True)
            quality: Optional quality setting for video ('high', 'medium', 'low')
        
        Returns:
            Path to the converted output file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If the conversion is not supported
            RuntimeError: If FFmpeg conversion fails
        """
        # Validate conversion is possible
        if not self.can_transcode():
            raise ValueError(
                f"Cannot convert {self.input_type} to {self.output_type}. "
                f"Audio-only formats cannot be converted to video formats."
            )
        
        # Check if input file exists
        if not os.path.isfile(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        # Generate output filename
        input_filename = Path(self.input_file).stem
        output_file = os.path.join(self.output_dir, f"{input_filename}.{self.output_type}")
        
        # Build FFmpeg command
        cmd = ['ffmpeg']
        
        if overwrite:
            cmd.append('-y')
        else:
            cmd.append('-n')
        
        cmd.extend(['-i', self.input_file])
        
        # Add quality settings for video conversions
        if quality and self.output_type in ['mp4', 'avi', 'mov', 'mkv', 'webm']:
            if quality == 'high':
                cmd.extend(['-crf', '18', '-preset', 'slow'])
            elif quality == 'medium':
                cmd.extend(['-crf', '23', '-preset', 'medium'])
            elif quality == 'low':
                cmd.extend(['-crf', '28', '-preset', 'fast'])
        
        cmd.append(output_file)
        
        # Execute FFmpeg command
        try:
            print(f"Converting {self.input_file} to {output_file}...")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            print(f"Conversion successful: {output_file}")
            return output_file
            
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg conversion failed: {e.stderr}"
            raise RuntimeError(error_msg)
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg not found. Please install FFmpeg: "
                "https://ffmpeg.org/download.html"
            )
