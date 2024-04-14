import re
import os
import asyncio
from ffmpeg import Progress, FFmpegError # python-ffmpeg
from ffmpeg.asyncio import FFmpeg
from send2trash import send2trash
from logger import Logger


DRY_RUN = False # if True, runs without affecting any files

filepath_match_pairs: list[tuple[str, dict[str, str], str]] = [
    #(
    #    "C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=12:crf=63:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Minecraft\\\\Fall 2022.*\\\\Minecraft Fall 2022 [0-9]*\\.webm$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        " retranscoded.webm"
    ),
    #(
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Celeste.*\\.mkv$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "256K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    #(
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\The Entropy Centre.*\\.mkv$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "256K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Dirt Rally 2.0.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=6:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    #(
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Mini Motorways.*\\.mkv$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "256K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    #( # OP6T videos
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\VID_[0-9]*_[0-9]*.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=3:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    #( # OP6T videos
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\OP6T_VID_[0-9]*_[0-9]*.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=3:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    #( # phone screen recordings
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9].*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=3:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #)
    # TODO add rule to transcode already transcoded video game recordings to make them much smaller
]
# pairs of regular expressions (regex) on the left, ffmpeg command to run on those matching files on the right, followed by file extension (ex: .webm)
# any one file will run the first command that it gets matched to with regex, even if multiples pairs would have matched
# it is expected that your output file specification will not be overwriting your input file specification

# TODO progress bar :3
# TODO log file (to help see progress if it crashes / computer reboots and to know which files I have to delete)

operations: list[dict[str, str]] = list() # list of complete FFMPEG commands
logger = Logger("regex_based_transcoder.log")
logger.append("\n\n")
logger.append("Program Start")

# convert regex strings to re.Pattern objects
filepath_match_pairs_processed: list[tuple[re.Pattern, dict[str, str], str]] = []
for match_pair in filepath_match_pairs:
    re_compiled: re.Pattern = re.compile(match_pair[0])
    match_pair_re: tuple[re.Pattern, dict, str] = (re_compiled, match_pair[1], match_pair[2])
    filepath_match_pairs_processed.append(match_pair_re)

paths_to_search: tuple[str, ...] = (
    "C:\\Users\\onebi\\Documents\\GitHub\\Mass-Video-Transcoder\\regex_testing_folder",
    "K:\\Unbacked up\\Screen Recordings",
    "K:\\Photos Videos\\Video game recordings"
)
# only folders (and all their subfolders) in here will be searched for regex matches

last_progress_string_length = 0
async def run_ffmpeg(ffmpeg: FFmpeg):
    @ffmpeg.on("progress")
    def print_progress(progress: Progress):
        global last_progress_string_length
        progress_string: str = (
            "Progress:    "
            + "<<< {fps:4.1f} FPS,    "
            + "{frame_num:8d} Frames,    "
            + "{size_MB:7.3f} MB,    "
            + "{bitrate_Mbps:4.3f} Mb/s,    "
            + "{speed_x:4.3f} x Video Speed,    "
            + "{time:s} Video Time >>>\r"
        )
        progress_string = progress_string.format(
            fps = progress.fps,
            frame_num = progress.frame,
            size_MB = progress.size/1000000,
            bitrate_Mbps = progress.bitrate/1000,
            speed_x = progress.speed,
            time = str(progress.time)
        )
        print(" "*last_progress_string_length+"\r", end="")
        print(progress_string, end="")
        last_progress_string_length = len(progress_string)
    await ffmpeg.execute()
    print("\n")

total_size_original = 0
total_size_output = 0

for path_to_search in paths_to_search:
    for folderpath, _, filenames in os.walk(path_to_search):
        filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames]) # convert to absolute filepaths
        for filepath in filepaths:
            for match_pair in filepath_match_pairs_processed:
                # try to match filepath with each regex expression until there's a match (or we've exhausted the list)
                match = match_pair[0].match(filepath)
                if match:
                    logger.append("\n\n--------------------------------------------------", True)
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
                    # add the command to the list of batch file commands
                    ffmpeg = (
                        FFmpeg()
                        .option("y")
                        .input(filepath)
                        .output(output_filepath_in_progress, operation) # type: ignore
                    )
                    logger.append("Found Match on File: \"{}\"".format(filepath), True)
                    logger.append("Running Operation: {}".format(operation), True)
                    logger.append("Outputting to File: \"{}\"".format(output_filepath_in_progress), True)
                    if not DRY_RUN:
                        try:
                            asyncio.run(run_ffmpeg(ffmpeg))
                            size_original: int = os.path.getsize(filepath)
                            size_output: int = os.path.getsize(output_filepath_in_progress)
                            size_fraction: float = size_output / size_original * 100
                            total_size_original += size_original
                            total_size_output += size_output
                            logger.append("Operation Completed!")
                            logger.append("Size reduced from {:.0f}MB to {:.0f}MB -> {:.2f}%, saving {:.0f}MB".format(size_original/1000000, size_output/1000000, size_fraction, (size_original-size_output)/1000000), True)
                            logger.append("Renaming File to: \"{}\"".format(output_filepath))
                            os.rename(output_filepath_in_progress, output_filepath) # remove "_in_progress" once file is done being created
                        except FFmpegError:
                            # transcode had at least one error, aborting
                            print("transcode failed!\n")
                            logger.append("Transcode Failed")
                            # does not try to delete potential broken output file
                            break
                        except FileExistsError:
                            logger.append("Rename Failed: File Already Existed. Deleting Conflicting File")
                            send2trash(output_filepath) # delete existing file before renaming to fix name conflict
                            logger.append("File Deleted, Retrying Rename")
                            os.rename(output_filepath_in_progress, output_filepath)
                            logger.append("Rename Success")


                    #send2trash(filepath) # delete original once transcode has successfully completed

                    print("--------------------------------------------------\n")
                    break # don't compare this file to any more regex
logger.append("Program Finish")
print("files transcoded: {}".format(len(operations)))
if (total_size_original != 0):
    total_size_fraction: float = total_size_output / total_size_original * 100
    print("\nOriginal Size: {:.0f} MB\nOutput Size:   {:.0f} MB\nPercent:       {:.2f}%"
        .format(total_size_original/1000000, total_size_output/1000000, total_size_fraction))
