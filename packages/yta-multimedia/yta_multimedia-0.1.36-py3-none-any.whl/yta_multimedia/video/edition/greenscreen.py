from yta_multimedia.image.greenscreen import remove_greenscreen_from_image
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.utils.ffmpeg_handler import FfmpegHandler, FfmpegPixelFormat
from yta_general_utils.temp import create_custom_temp_filename
from typing import Union
from moviepy import VideoFileClip


def remove_greenscreen_from_video(video_input: Union[VideoFileClip, str], output_filename: str = None):
    """
    Removes the green screen from the 'video_input' video so
    you get a final 'output_filename' video with transparent
    layer.
    """
    video = VideoParser.to_moviepy(video)
    
    # TODO: I think I need to write the frame filenames in a file to be used
    # with the concat flag and ffmpeg library

    # Export all frames
    original_frames_array = []
    for frame in video.iter_frames():
        frame_name = create_custom_temp_filename('tmp_frame_' + str(len(original_frames_array)) + '.png')
        original_frames_array.append(frame_name)
    video.write_images_sequence(create_custom_temp_filename('tmp_frame_%01d.png'), logger = 'bar')

    # Remove green screen of each frame and store it
    processed_frames_array = []
    for index, frame in enumerate(original_frames_array):
        tmp_frame_filename = create_custom_temp_filename('tmp_frame_processed_' + str(index) + '.png')
        processed_frames_array.append(tmp_frame_filename)
        remove_greenscreen_from_image(frame, tmp_frame_filename)

    # Rebuild the video
    if not output_filename:
        output_filename = create_custom_temp_filename('greenscreen_video_removed_background.mov')
    # TODO: What if 'output_filename' is not .mov but it has transparency,
    # maybe we should force '.mov'

    video, _ = FfmpegHandler.concatenate_images(processed_frames_array, frame_rate = 30, pixel_format = FfmpegPixelFormat.YUV420p, output_filename = output_filename)

    return video

    #parameters = ['ffmpeg', '-y', '-i', create_custom_temp_filename('tmp_frame_processed_%01d.png'), '-r', '30', '-pix_fmt', 'yuva420p', output_filename]
    #run(parameters)
        
    # https://stackoverflow.com/a/77608713
    #ImageSequenceClip(processed_frames_array, fps = clip.fps).with_audio(clip.audio).write_videofile(output_filename, codec = 'hap_alpha', ffmpeg_params = ['-c:v', 'hap', '-format', 'hap_alpha', '-vf', 'chromakey=black:0.1:0.1'])
    # https://superuser.com/questions/1779201/combine-pngs-images-with-transparency-into-a-video-and-merge-it-on-a-static-imag
    # ffmpeg -y -i src/tmp/%d.png -c:v libx264 -vf fps=25 -pix_fmt yuva420p land.mov
    
    #clip = ImageSequenceClip(processed_frames_array, fps = clip.fps).with_audio(clip.audio).write_videofile(output_filename, codec = 'libx264', audio_codec = 'aac', temp_audiofile = 'temp-audio.m4a', remove_temp = True)