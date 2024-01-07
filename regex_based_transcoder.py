import re
import os
import asyncio
from ffmpeg import Progress, FFmpegError # python-ffmpeg
from ffmpeg.asyncio import FFmpeg
from send2trash import send2trash


DRY_RUN = False # if True, runs without affecting any files

filepath_match_pairs: list[tuple[re.Pattern, dict, str]] = [
    (
        "C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=12:crf=63:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Celeste.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "256K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=6:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\The Entropy Centre.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "256K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=6:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    )
]
# pairs of regular expressions (regex) on the left, ffmpeg command to run on those matching files on the right, followed by file extension (ex: .webm)
# any one file will run the first command that it gets matched to with regex, even if multiples pairs would have matched
# it is expected that your output file specification will not be overwriting your input file specification

operations: list[str] = list() # list of complete FFMPEG commands

# convert regex strings to re.Pattern objects
i = -1
for match_pair in filepath_match_pairs:
    i += 1
    match_pair = list(match_pair) # convert to list to make it mutable
    match_pair[0] = re.compile(match_pair[0])
    filepath_match_pairs[i] = match_pair # overwrite the tuple that was there since tuples are immutable

paths_to_search: tuple[str] = (
    "C:\\Users\\onebi\\Documents\\GitHub\\Mass-Video-Transcoder\\regex_testing_folder",
    "K:\\Unbacked up\\Screen Recordings"
)
# only folders (and all their subfolders) in here will be searched for regex matches

last_progress_string_length = 0
async def run_ffmpeg(ffmpeg: FFmpeg):
    @ffmpeg.on("progress")
    def print_progress(progress: Progress):
        global last_progress_string_length
        print(" "*last_progress_string_length+"\r"+str(progress)+"\r", end="")
        last_progress_string_length = len(str(progress))
    await ffmpeg.execute()
    print("\n")


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
                    ffmpeg.output(output_filepath_in_progress, operation)
                    if not DRY_RUN:
                        try:
                            asyncio.run(run_ffmpeg(ffmpeg))
                            size_original: int = os.path.getsize(filepath)
                            size_output: int = os.path.getsize(output_filepath_in_progress)
                            print("Original Size: {:.0f} MB\nOutput Size:   {:.0f} MB\n"
                                  .format(size_original/1000000, size_output/1000000))
                            os.rename(output_filepath_in_progress, output_filepath) # remove "_in_progress" once file is done being created
                        except FFmpegError:
                            # transcode had at least one error, aborting
                            print("transcode failed!\n")
                            # does not try to delete potential broken output file
                            break
                        except FileExistsError:
                            send2trash(output_filepath) # delete existing file before renaming to fix name conflict
                            os.rename(output_filepath_in_progress, output_filepath)


                    send2trash(filepath) # delete original once transcode has successfully completed

                    break # don't compare this file to any more regex

print("files transcoded: {}".format(len(operations)))
