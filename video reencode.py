import os

video_file_extensions = [".mp4", ".mkv", ".mov", ".webm"]
# not case sensitive

transcoded_marker = " TRANSCODED"
# added at the end of filename before extension

output_extension = ".webm"
# file extension of output transcoded videos

base_command = 'ffmpeg -i "{{input_file}}" -c:v libsvtav1 -c:a libopus -b:a {audio_bitrate}K -g 600 -vf "scale=out_range=full" -svtav1-params "preset={preset}:crf={crf}:matrix-coefficients=bt709:color-range=1:color-primaries=bt709" "{{output_file}}"'
# format parameters: input_file, audio_bitrate, encoding_speed_preset, crf, output_file
# double curly brackets around input and output because it allows us to format the string once without those options set first, then set those later

folder_configs = [
["CRF-0 PRESET-6 AUDIORATE-384K", base_command.format(crf = 0, preset = 6, audio_bitrate = 384)],
["CRF-10 PRESET-6 AUDIORATE-384K", base_command.format(crf = 10, preset = 6, audio_bitrate = 384)],
["CRF-22 PRESET-6 AUDIORATE-384K", base_command.format(crf = 22, preset = 6, audio_bitrate = 384)],
["CRF-44 PRESET-6 AUDIORATE-384K", base_command.format(crf = 44, preset = 6, audio_bitrate = 384)],
["CRF-55 PRESET-6 AUDIORATE-384K", base_command.format(crf = 55, preset = 6, audio_bitrate = 384)],
["CRF-63 PRESET-6 AUDIORATE-384K", base_command.format(crf = 63, preset = 6, audio_bitrate = 384)]
]
folders = [i[0] for i in folder_configs]
commands = [i[1] for i in folder_configs]
batch_file_input = list()

# check if all folders exist. create non-existant folders:
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

files_to_transcode = 0
# look for files to transcode, and create/format their respective commands
for folder_index in range(len(folders)):
    for path, _, file in os.walk(folders[folder_index]):
        for filename in file:
            if (sum([filename.lower().count(extension) for extension in video_file_extensions]) > 0) and filename.count(transcoded_marker) < 1:
                # if this file has a valid file extension and isn't marked as already transcoded
                files_to_transcode += 1
                batch_file_input.append('cd "{}"\n'.format(path))
                period_count = filename.count(".")
                last_start = -1
                for i in range(period_count):
                    extension_start_index = filename.find(".", last_start+1)
                    last_start = extension_start_index
                batch_file_input.append(commands[folder_index].format(input_file = filename, output_file = filename[0:extension_start_index-1]+transcoded_marker+output_extension) + "\n")
                batch_file_input.append('cd ..\n')
                batch_file_input.append('move "{path}/{file}" "{path}/original_videos"\n'.format(path = path, file = filename))

# write batch file with FFMPEG commands:
with open("mass-transcode.bat", "w") as batchfile:
    batchfile.writelines(batch_file_input)

print("files to transcode: {}".format(files_to_transcode))

