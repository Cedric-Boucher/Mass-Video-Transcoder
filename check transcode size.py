import os


minimum_size_diff = 0.70
# transcoded files must be at least this much smaller (multiplier)

transcoded_marker = " TRANSCODED"
# marker before file extension for transcoded files

cwd_path = os.path.abspath(os.getcwd())

required_folders = ["original_videos", "originals_of_accepted_transcode", "originals_of_rejected_transcode", "accepted_transcodes"]

# create any required folders that are missing
for folder in required_folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

original_files_list = os.listdir(cwd_path+"/"+"original_videos")

batch_file_input = list()

for path, _, file in os.walk(cwd_path):
    for filename in file:
        if filename.count(transcoded_marker) >= 1:
            filesize = os.stat(path+"\\"+filename)[6]
            period_count = filename.count(".")
            extension_start_index = -1
            for i in range(period_count):
                extension_start_index = filename.find(".", extension_start_index+1)
            marker_position = filename[:extension_start_index].find(transcoded_marker)            
            original_filename_guess = filename[:marker_position] # derived from transcoded filename, no extension
            original_filename = ""
            for original_file in original_files_list:
                if original_file.startswith(original_filename_guess): # find the actual filename of the original file
                    original_filename = original_file
                    break
            if original_filename == "":
                continue
            original_filesize = os.stat(cwd_path+"\\"+"original_videos"+"\\"+original_filename)[6]
            if (filesize/original_filesize) < minimum_size_diff: # transcode size accepted
                batch_file_input.append('move "{source_path}\{file}" "{destination_path}"\n'.format(source_path = cwd_path+"\\"+"original_videos", file = original_filename, destination_path = cwd_path+"\\"+"originals_of_accepted_transcode"))
            else: # transcode size rejected
                batch_file_input.append('move "{source_path}\{file}" "{destination_path}"\n'.format(source_path = cwd_path+"\\"+"original_videos", file = original_filename, destination_path = cwd_path+"\\"+"originals_of_rejected_transcode"))
            batch_file_input.append('move "{source_path}/{file}" "{destination_path}"\n'.format(source_path = path+"\\", file = filename, destination_path = cwd_path+"\\"+"accepted_transcodes"))

batch_file_input.append("pause\n")
# write batch file with move commands:
with open("transcode_size_checker.bat", "w") as batchfile:
    batchfile.writelines(batch_file_input)

print("move commands: {}".format(len(batch_file_input)-1))

