DRY_RUN = False # if True, runs without affecting any files

FILEPATH_MATCH_PAIRS: list[tuple[str, dict[str, str], str]] = [
    #(
    #    "C:\\\\Users\\\\onebi\\\\Documents\\\\GitHub\\\\Mass-Video-Transcoder\\\\regex_testing_folder.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=12:crf=63:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Minecraft\\\\Fall 2022.*\\\\Minecraft Fall 2022 [0-9]*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        " retranscoded.webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Beat Saber\\\\.*\\.mp4$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "128K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=50:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Rocket League\\\\.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=63:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Celeste.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Pokemon Emerald.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "32K", "g": "1200", "vf": "scale=out_range=full", "map": "0", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    #(
    #    "K:\\\\Photos Videos\\\\Video game recordings.*\\\\Celeste.*\\.webm$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    "retranscoded.webm"
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
    #    "K:\\\\Photos Videos\\\\Video game recordings\\\\The Entropy Centre\\\\.*\\.webm$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    " retranscoded.webm"
    #),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\Mini Motorways.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Mini Motorways\\\\.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=50:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings.*\\\\Flight Simulator.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings.*\\\\Hollow Knight.*\\.mp4$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Genshin\\\\.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "48K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=63:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Breath of the Wild\\\\.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    (
        "K:\\\\Photos Videos\\\\Video game recordings\\\\Ori and the Will of the Wisps\\\\.*\\.wkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "1200", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=55:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    #( # OP6T videos
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\VID_[0-9]*_[0-9]*.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    #( # OP6T videos
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\OP6T_VID_[0-9]*_[0-9]*.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    ( # OP6T videos
        "K:\\\\Elodie_import\\\\OP6T_VID_[0-9]*_[0-9]*.*\\.mp4$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    ( # older OP6T videos # TODO bring to 1080p first?
        "K:\\\\Elodie_import\\\\VID_[0-9]*_[0-9]*.*\\.mp4$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "96K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=40:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    #( # Linda's Pixel 2 XL videos # TODO bring to 1080p if larger first
    #    "K:\\\\Elodie_import\\\\PXL_[0-9]*_[0-9]*.*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    ( # DSLR videos
        "K:\\\\Elodie_import\\\\MVI_[0-9]*\\.MOV$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=20:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
        ".webm"
    ),
    #( # phone screen recordings
    #    "K:\\\\Unbacked up\\\\Screen Recordings.*\\\\mass transcoder\\\\[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9].*\\.mp4$",
    #    {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "192K", "g": "600", "vf": "scale=out_range=full", "svtav1-params": "preset=5:crf=30:matrix-coefficients=bt709:color-range=1:color-primaries=bt709"},
    #    ".webm"
    #),
    (
        "K:\\\\Unbacked up\\\\Screen Recordings\\\\MakeMKV\\\\.*\\.mkv$",
        {"vcodec": "libsvtav1", "c:a": "libopus", "b:a": "64K", "g": "600", "map": "0", "preset": "4", "crf": "20"},
        ".webm"
    ),
]
# pairs of regular expressions (regex) on the left, ffmpeg command to run on those matching files on the right, followed by file extension (ex: .webm)
# any one file will run the first command that it gets matched to with regex, even if multiples pairs would have matched
# it is expected that your output file specification will not be overwriting your input file specification


PATHS_TO_SEARCH: tuple[str, ...] = (
    "C:\\Users\\onebi\\Documents\\GitHub\\Mass-Video-Transcoder\\regex_testing_folder",
    "K:\\Unbacked up\\Screen Recordings",
    "K:\\Photos Videos\\Video game recordings",
    "K:\\Elodie_import"
)
# only folders (and all their subfolders) in here will be searched for regex matches
