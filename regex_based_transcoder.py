import re
import os
from ffmpeg import FFmpeg, Progress, FFmpegError # python-ffmpeg
from send2trash import send2trash


filepath_match_pairs: list[tuple[re.Pattern, dict, str]] = [
    ("C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$", {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=7:crf=40:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"}, ".webm"),
    ("K:\\\\Photos Videos\\\\Screen Recordings.*\\.mkv$", {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=7:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"}, ".webm")
]
# pairs of regular expressions (regex) on the left, ffmpeg command to run on those matching files on the right, followed by file extension (ex: .webm)
# any one file will run the first command that it gets matched to with regex, even if multiples pairs would have matched

operations: list[str] = list() # list of complete FFMPEG commands

# convert regex strings to re.Pattern objects
i = -1
for match_pair in filepath_match_pairs:
    i += 1
    match_pair = list(match_pair) # convert to list to make it mutable
    match_pair[0] = re.compile(match_pair[0])
    filepath_match_pairs[i] = match_pair # overwrite the tuple that was there since tupes are immutable

paths_to_search: tuple[str] = (
    "C:\\Users\\onebi\\Documents\\GitHub\\Mass-Video-Transcoder\\regex_testing_folder",
    "K:\\Photos Videos\\Screen Recordings"
)
# only folders (and all their subfolders) in here will be searched for regex matches


for path_to_search in paths_to_search:
    for folderpath, _, filenames in os.walk(path_to_search):
        filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames]) # convert to absolute filepaths
        for filepath in filepaths:
            for match_pair in filepath_match_pairs:
                # try to match filepath with each regex expression until there's a match (or we've exhausted the list)
                match = match_pair[0].match(filepath)
                if match:
                    # get full output filepath and remove file extension from filename as it is determined by transcode
                    output_folderpath, output_filename = os.path.split(filepath)
                    period_count = output_filename.count(".")
                    extension_start_index = -1
                    for i in range(period_count):
                        extension_start_index = output_filename.find(".", extension_start_index+1)
                    output_filename = output_filename[0:extension_start_index]
                    output_filepath = os.path.abspath(output_folderpath+"/"+output_filename)

                    # create the command by inserting the filepaths
                    operation = match_pair[1]
                    operations.append(operation)
                    extension = match_pair[2]
                    output_filepath_in_progress = output_filepath
                    output_filepath_in_progress += "_in_progress"
                    output_filepath += extension
                    output_filepath_in_progress += extension
                    print("input: {}\noutput: {}\noptions: {}\n".format(filepath, output_filepath, operation))
                    # add the command to the list of batch file commands
                    ffmpeg = FFmpeg()
                    ffmpeg.option("y")
                    ffmpeg.input(filepath)
                    ffmpeg.output(output_filepath, operation)
                    try:
                        ffmpeg.execute()
                    except FFmpegError:
                        # transcode had at least one error, aborting
                        print("transcode failed!\n")
                        break

                    os.rename(output_filepath_in_progress, output_filepath)

                    #send2trash(filepath) # delete original once transcode has successfully completed

                    break # don't compare this file to any more regex

print("files transcoded: {}".format(len(operations)))

