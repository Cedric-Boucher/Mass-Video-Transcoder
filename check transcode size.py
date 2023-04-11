import os


minimum_size_diff = 0.70 # times original filesize
folder_configs = [
["CRF 0", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 0 -y "{} (HEVC).mkv"'],
["CRF 2", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 2 -y "{} (HEVC).mkv"'],
["CRF 4", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 4 -y "{} (HEVC).mkv"'],
["CRF 6", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 6 -y "{} (HEVC).mkv"'],
["CRF 8", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 8 -y "{} (HEVC).mkv"'],
["CRF 10", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 10 -y "{} (HEVC).mkv"'],
["CRF 12", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 12 -y "{} (HEVC).mkv"'],
["CRF 14", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 14 -y "{} (HEVC).mkv"'],
["CRF 16", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 16 -y "{} (HEVC).mkv"'],
["CRF 18", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 18 -y "{} (HEVC).mkv"'],
["CRF 20", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 20 -y "{} (HEVC).mkv"'],
["CRF 22", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 22 -y "{} (HEVC).mkv"'],
["CRF 24", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 24 -y "{} (HEVC).mkv"'],
["CRF 26", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 26 -y "{} (HEVC).mkv"'],
["CRF 28", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 28 -y "{} (HEVC).mkv"'],
["CRF 30", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 30 -y "{} (HEVC).mkv"'],
["CRF 32", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 32 -y "{} (HEVC).mkv"'],
["CRF 34", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 34 -y "{} (HEVC).mkv"'],
["CRF 36", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 36 -y "{} (HEVC).mkv"'],
["CRF 38", 'ffmpeg -i "{}" -vcodec libx265 -preset slower -crf 38 -y "{} (HEVC).mkv"']]
fold_confs = [[i[0] for i in folder_configs], [i[1] for i in folder_configs]]

for c in range(len(fold_confs[0])):
    for path, dir, file in os.walk(fold_confs[0][c]):
        for i in file:
            if (i.endswith(".mp4") or i.endswith(".mkv")) and i.count("(HEVC)") >= 1:
                filesize = os.stat("M:/General/Photos & Videos/Transcode/{}/{}".format(path, i))[6]
                old_files = [i[2] for i in os.walk("M:/General/Photos & Videos/Transcode/temp vids")][0]
                test = [f for f in old_files if str(f).count(str(i.replace(" (HEVC).mkv", ""))) >= 1]
                try:
                    original_filesize = os.stat("temp vids/{}".format(test[0]))[6]
                    print(str(int(filesize/original_filesize*10000)/100)+"% size of original file")

                    if filesize/original_filesize > minimum_size_diff:
                        batch_file_input = list()
                        with open("video_reencode.bat", "w") as batchfile:
                            batch_file_input.append('cd "M:/General/Photos & Videos/Transcode/temp vids"\n')
                            num = int(path.rsplit(" ", 1)[-1])+2
                            p = str(path.rsplit(" ", 1)[0])
                            if num > 38:
                                num = 38
                            batch_file_input.append('move "{}" "M:/General/Photos & Videos/Transcode/{}{}"\n'.format(test[0], p, " "+str(num)))
                            batch_file_input.append('cd "M:/General/Photos & Videos/Transcode/{}"\n'.format(path))
                            batch_file_input.append('del "{}"\n'.format(i))

                            batchfile.writelines(batch_file_input)
                except IndexError:
                    print("file not found in temp vids, skipping")
