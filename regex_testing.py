import re
import os

filepath_match_pairs: list[tuple[re.Pattern, str]] = [
    ("C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$", 'ffmpeg -i "{input_file}" -c:v libsvtav1 -c:a libopus -b:a 128K -g 600 -vf "scale=out_range=full" -svtav1-params "preset=7:crf=22:matrix-coefficients=bt709:color-range=1:color-primaries=bt709" -y "{output_file}"'),
    ("C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.txt$", 'no')

]

i = -1
for match_pair in filepath_match_pairs:
    i += 1
    match_pair = list(match_pair) # to make it mutable
    match_pair[0] = re.compile(match_pair[0])
    filepath_match_pairs[i] = match_pair


for folderpath, _, filenames in os.walk("C:/Users/onebi/Documents/GitHub"):
    filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames])
    for filepath in filepaths:
        for match_pair in filepath_match_pairs:
            match = match_pair[0].match(filepath)
            if match:
                print(filepath)
                print(match_pair[1])
                break
