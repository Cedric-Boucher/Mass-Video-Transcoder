import re
import os
import asyncio
from ffmpeg import Progress, FFmpegError # python-ffmpeg
from ffmpeg.asyncio import FFmpeg
from send2trash import send2trash
import win32_setctime
import datetime
from logger import Logger
import cv2
import config

operations: list[dict[str, str]] = list() # list of complete FFMPEG commands
logger = Logger("regex_based_transcoder.log")
logger.append("\n\n")
logger.append("Program Start")

# convert regex strings to re.Pattern objects
filepath_match_pairs_processed: list[tuple[re.Pattern, dict[str, str], str]] = []
for match_pair in config.FILEPATH_MATCH_PAIRS:
    re_compiled: re.Pattern = re.compile(match_pair[0])
    match_pair_re: tuple[re.Pattern, dict, str] = (re_compiled, match_pair[1], match_pair[2])
    filepath_match_pairs_processed.append(match_pair_re)

def get_video_frame_count(filename) -> int:
    video = cv2.VideoCapture(filename)
    frame_count: int = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    assert (frame_count > 0)
    return frame_count

last_progress_string_length: int = 0
async def run_ffmpeg(ffmpeg: FFmpeg, filepath: str):
    total_frame_count: int = get_video_frame_count(filepath)
    current_video_start_time: datetime.datetime = datetime.datetime.now()
    @ffmpeg.on("progress")
    def print_progress(progress: Progress):
        global last_progress_string_length
        real_timedelta: datetime.timedelta = datetime.datetime.now() - current_video_start_time
        estimated_microseconds_total: float = real_timedelta.total_seconds()*1000000 * total_frame_count / max(progress.frame, 1)
        estimated_finish_datetime: datetime.datetime = current_video_start_time + datetime.timedelta(microseconds = estimated_microseconds_total)
        estimated_remaining_timedelta: datetime.timedelta = estimated_finish_datetime - datetime.datetime.now()
        progress_string: str = (
            "Progress:    "
            + "<<< {fps:4.1f} FPS | "
            + "{frame_num:8d} Frames | "
            + "{size_MB:7.3f} MB | "
            + "{bitrate_Mbps:4.3f} Mb/s | "
            + "{speed_x:4.3f} x Video Speed | "
            + "{video_time:s} Video Time | "
            + "{real_time:s} Real Time | "
            + "{time_remaining:s} Time Remaining >>>"
        )
        # TODO add final bitrate and speed to log?
        progress_string = progress_string.format(
            fps = progress.fps,
            frame_num = progress.frame,
            size_MB = progress.size/1000000,
            bitrate_Mbps = progress.bitrate/1000,
            speed_x = progress.speed,
            video_time = str(progress.time),
            real_time = str(real_timedelta),
            time_remaining = str(estimated_remaining_timedelta)
        )
        print(progress_string + " " * max((last_progress_string_length - len(progress_string)), 0), end="\r")
        last_progress_string_length = len(progress_string)
    await ffmpeg.execute()
    print("\n")

total_size_original = 0
total_size_output = 0

for path_to_search in config.PATHS_TO_SEARCH:
    for folderpath, _, filenames in os.walk(path_to_search):
        filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames]) # convert to absolute filepaths
        for filepath in filepaths:
            for match_pair in filepath_match_pairs_processed:
                # try to match filepath with each regex expression until there's a match (or we've exhausted the list)
                match = match_pair[0].match(filepath)
                if match:
                    logger.append("\n\n--------------------------------------------------", True)
                    # get full output filepath and remove file extension from filename as it is determined by transcode
                    output_folderpath: str
                    output_filename: str
                    output_folderpath, output_filename = os.path.split(filepath)
                    period_count: int = output_filename.count(".")
                    extension_start_index = -1
                    for i in range(period_count):
                        extension_start_index: int = output_filename.find(".", extension_start_index+1)
                    output_filename: str = output_filename[0:extension_start_index]
                    output_filepath: str = os.path.abspath(output_folderpath+"/"+output_filename)

                    # create the command by inserting the filepaths
                    operation: dict[str, str] = match_pair[1]
                    operations.append(operation)
                    extension: str = match_pair[2]
                    output_filepath_in_progress: str = output_filepath
                    output_filepath_in_progress += "_in_progress"
                    output_filepath += extension
                    output_filepath_in_progress += extension
                    # add the command to the list of batch file commands
                    ffmpeg: FFmpeg = (
                        FFmpeg()
                        .option("y")
                        .input(filepath)
                        .output(output_filepath_in_progress, operation) # type: ignore
                    )
                    logger.append("Found Match on File: \"{}\"".format(filepath), True)
                    logger.append("Running Operation: {}".format(operation), True)
                    logger.append("Outputting to File: \"{}\"".format(output_filepath_in_progress), True)
                    if not config.DRY_RUN:
                        try:
                            asyncio.run(run_ffmpeg(ffmpeg, filepath))
                            size_original: int = os.path.getsize(filepath)
                            size_output: int = os.path.getsize(output_filepath_in_progress)
                            size_fraction: float = size_output / size_original * 100
                            total_size_original += size_original
                            total_size_output += size_output
                            logger.append("Operation Completed!")
                            logger.append("Size reduced from {:.0f}MB to {:.0f}MB -> {:.2f}%, saving {:.0f}MB".format(size_original/1000000, size_output/1000000, size_fraction, (size_original-size_output)/1000000), True)
                            logger.append("Renaming File to: \"{}\"".format(output_filepath))
                            os.rename(output_filepath_in_progress, output_filepath) # remove "_in_progress" once file is done being created
                        except FFmpegError as e:
                            # transcode had at least one error, aborting
                            print("transcode failed... {}: {}\n".format(type(e).__name__, str(e)))
                            logger.append("Transcode Failed - {}: {}".format(type(e).__name__, str(e)))
                            send2trash(output_filepath) # delete failed output
                            logger.append("Deleted Failed Output File")
                            break
                        except FileExistsError:
                            logger.append("Rename Failed: File Already Existed. Deleting Conflicting File")
                            send2trash(output_filepath) # delete existing file before renaming to fix name conflict
                            logger.append("File Deleted, Retrying Rename")
                            os.rename(output_filepath_in_progress, output_filepath)
                            logger.append("Rename Success")
                        except PermissionError:
                            logger.append("Rename Failed: File Was In Use / Did Not Have Permission To Rename")
                            break
                        # change the output file's creation and modification time to match original file
                        creation_time_original: float = os.path.getctime(filepath)
                        modification_time_original: float = os.path.getmtime(filepath)
                        accessed_time: float = os.path.getatime(output_filepath)
                        # set modification time, can be done easily with `os`
                        logger.append("setting modification time to {}".format(datetime.datetime.fromtimestamp(modification_time_original).strftime("%Y-%m-%d %H:%M:%S")))
                        try:
                            os.utime(output_filepath, (accessed_time, modification_time_original))
                        except Exception as e:
                            logger.append("ERROR, failed to update output file modification time: {}, {}".format(type(e).__name__, str(e)))
                        # set creation time, cannot be done with `os` for some reason
                        logger.append("setting creation time to {}".format(datetime.datetime.fromtimestamp(creation_time_original).strftime("%Y-%m-%d %H:%M:%S")))
                        try:
                            win32_setctime.setctime(output_filepath, creation_time_original)
                        except Exception as e:
                            logger.append("ERROR, failed to update output file creation time: {}, {}".format(type(e).__name__, str(e)))

                    #send2trash(filepath) # delete original once transcode has successfully completed

                    print("--------------------------------------------------\n")
                    break # don't compare this file to any more regex

logger.append("Program Finish")
print("files transcoded: {}".format(len(operations)))
if (total_size_original != 0):
    total_size_fraction: float = total_size_output / total_size_original * 100
    print("\nOriginal Size: {:.0f} MB\nOutput Size:   {:.0f} MB\nPercent:       {:.2f}%"
        .format(total_size_original/1000000, total_size_output/1000000, total_size_fraction))
