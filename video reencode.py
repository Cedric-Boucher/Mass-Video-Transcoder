import os


folder_configs = [
["CRF 0", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=0:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 2", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=2:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 4", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=4:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 6", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=6:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 8", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=8:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 10", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=10:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 12", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=12:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 14", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=14:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 16", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=16:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 18", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=18:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 20", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=20:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 22", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=22:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 24", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=24:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 26", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=26:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 28", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=28:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 30", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=30:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 32", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=32:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 34", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=34:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 36", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=36:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"'],
["CRF 38", 'ffmpeg -i "{}" -vcodec libx265 -x265-params "crf=38:range=full" -preset slow -pix_fmt yuv444p -c:a flac -max_muxing_queue_size 9999 -y "{} (HEVC).mkv"']]
fold_confs = [[i[0] for i in folder_configs], [i[1] for i in folder_configs]]
batch_file_input = list()

with open("video_reencode.bat", "w") as batchfile:
    for c in range(len(fold_confs[0])):
        for path, dir, file in os.walk(fold_confs[0][c]):
            print(str(len(file))+" files")
            for i in file:
                if (i.endswith(".mp4") or i.endswith(".mkv") or i.endswith(".MP4") or i.endswith(".MOV")) and i.count("(HEVC)") < 1:
                    batch_file_input.append('cd "M:/General/Photos & Videos/Transcode/{}"\n'.format(path))
                    batch_file_input.append(fold_confs[1][c].format(i, i.split(".m")[0]) + "\n")
                    batch_file_input.append('move "{}" "M:/General/Photos & Videos/Transcode/temp vids\n'.format(i))

    batchfile.writelines(batch_file_input)
