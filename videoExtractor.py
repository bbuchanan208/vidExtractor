from shutil import copy2, move, rmtree
import os


def list_all_important_files_alphabetically(file_list):
    file_list.sort()
    return_list = []
    for each in file_list:
        if str(each[:-4]).isdigit():
            return_list.append(each)
    return return_list


def get_video_path(input_dir, file):
    return input_dir + "/" + file + '/Kinect_Output'


def copy_ffmpeg_to_kinect_output(destination):
    copy2('/Users/benjaminbuchanan/Desktop/REU/PythonProjects/audioDetection/ffmpeg', destination)


def exe_ffmpeg_1(kinect_output_directory_path):
    os.chdir(kinect_output_directory_path)
    os.system('./ffmpeg -f f32le -ar 16k -ac 1 -i raw_audio.wav audio.mp3')


def exe_ffmpeg_2(kinect_output_directory_path):
    os.chdir(kinect_output_directory_path + '/Color')
    os.system('./ffmpeg -r 30 -i "ColorFrame_%d.bmp" -i audio.mp3 -c:v libx264 -c:a aac -pix_fmt yuv420p -crf 23 -r 30 -y video.mp4')


def build_audio_file(kinect_output_directory_path):
    copy_ffmpeg_to_kinect_output(kinect_output_directory_path)
    exe_ffmpeg_1(kinect_output_directory_path)


def move_audio_and_ffmpeg_to_color_folder(kinect_output_directory_path):
    move(kinect_output_directory_path + '/ffmpeg', kinect_output_directory_path + '/Color/')
    move(kinect_output_directory_path + '/audio.mp3', kinect_output_directory_path + '/Color/')


def partial_build_video_file(kinect_output_directory_path):
    move_audio_and_ffmpeg_to_color_folder(kinect_output_directory_path)
    exe_ffmpeg_2(kinect_output_directory_path)


def complete_build_video(kinect_output_directory_path):
    build_audio_file(kinect_output_directory_path)
    partial_build_video_file(kinect_output_directory_path)


def move_video_file(orig_fld_loc, kinect_output_directory_path, zero_ref_index):
    os.chdir(orig_fld_loc)
    os.mkdir(str(zero_ref_index + 1))
    move(kinect_output_directory_path + '/Color/video.mp4', orig_fld_loc + '/' + str(zero_ref_index + 1))


def build_all_videos(original_folder_loc):
    folders = list_all_important_files_alphabetically(os.listdir(original_folder_loc))
    for zero_ref_index in range(0, len(folders)):
        kinect_output_path = get_video_path(original_folder_loc, folders[zero_ref_index])
        complete_build_video(kinect_output_path)
        move_video_file(original_folder_loc, kinect_output_path, zero_ref_index)
        rmtree(kinect_output_path[:-14])

input_directory = '/Users/benjaminbuchanan/Desktop/stff'
build_all_videos(input_directory)
