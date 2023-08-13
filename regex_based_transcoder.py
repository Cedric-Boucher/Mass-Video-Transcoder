import re
import os

filepath_match_pairs: list[tuple[re.Pattern, str]] = [
    ("C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$", 'ffmpeg -i "{input_file}" -c:v libsvtav1 -c:a libopus -b:a 128K -g 600 -vf "scale=out_range=full" -svtav1-params "preset=7:crf=22:matrix-coefficients=bt709:color-range=1:color-primaries=bt709" -y "{output_file}.webm"'),
    ("K:\\\\Photos Videos\\\\Screen Recordings.*\\.mkv$", 'ffmpeg -i "{input_file}" -c:v libsvtav1 -c:a libopus -b:a 128K -g 600 -vf "scale=out_range=full" -svtav1-params "preset=7:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709" -y "{output_file}.webm"')
]

operations: list[str] = list() # list of complete FFMPEG commands
batch_file_input: list[str] = list()

i = -1
for match_pair in filepath_match_pairs:
    i += 1
    match_pair = list(match_pair) # to make it mutable
    match_pair[0] = re.compile(match_pair[0])
    filepath_match_pairs[i] = match_pair

paths_to_search: list[str] = ["C:\\Users\\onebi\\Documents\\GitHub\\Mass-Video-Transcoder\\regex_testing_folder",
                              "K:\\Photos Videos\\Screen Recordings"]

for path_to_search in paths_to_search:
    for folderpath, _, filenames in os.walk(path_to_search):
        filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames])
        for filepath in filepaths:
            for match_pair in filepath_match_pairs:
                match = match_pair[0].match(filepath)
                if match:
                    output_folderpath, output_filename = os.path.split(filepath)
                    period_count = output_filename.count(".")
                    extension_start_index = -1
                    for i in range(period_count):
                        extension_start_index = output_filename.find(".", extension_start_index+1)
                    output_filename = output_filename[0:extension_start_index]
                    output_filepath = os.path.abspath(output_folderpath+"/"+output_filename)
                    operation = match_pair[1].format(input_file = filepath, output_file = output_filepath)
                    operations.append(operation)
                    print(operation)
                    batch_file_input.append("{}\n".format(operation))
                    batch_file_input.append('del "{filepath}"\n'.format(filepath = filepath))
                    break

batch_file_input.append("pause\n")
# write batch file with FFMPEG commands:
with open("mass-transcode.bat", "w") as batchfile:
    batchfile.writelines(batch_file_input)

print("files to transcode: {}".format(len(operations)))

