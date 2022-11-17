from os import path

import ffmpeg


# the command that works:
# bad encoding.  ffmpeg -i /media/basement/CameraArchive/20220630/C0016.MP4 -ss 00:00:20 -to 00:00:37  jordieGrimm_stefanDrillV2ToExtension.mp4
# ffmpeg -i /media/basement/CameraArchive/20220630/C0016.MP4 -ss 00:00:20 -to 00:00:37  -crf 28 -c:v libx264  jordieGrimm_stefanDrillV2ToExtension.mp4

def process_timestamp(timestamp):
    if type(timestamp) == float:
        return timestamp
    elif type(timestamp) == str and ':' in timestamp:
        s = timestamp.split(":")
        if len(s) == 2:  # minutes:seconds.  Theoretically works with partial seconds?
            return float(s[0]) + float(s[1])/60
        elif len(s) == 3: # hours:minutes:seconds.
            return float(s[0])*60 + float(s[1]) + float(s[2])/60


def process_timestamp(timestamp):
    if type(timestamp) == float:
        return timestamp
    elif type(timestamp) == str and ':' in timestamp:
        s = timestamp.split(":")
        if len(s) == 2:  # minutes:seconds.  Theoretically works with partial seconds?
            return float(s[0])*60 + float(s[1])
        elif len(s) == 3: # hours:minutes:seconds.
            return float(s[0])*60*60 + float(s[1])*60 + float(s[2])



original_config = {
    'output_filename': 'test.mp4',  # codec okay?  always force mp4, or just match codec of infiles.  IS SET TO CAMERA FOR NOW
    'deets': [
        ('C0004.MP4', 00.24, 00.28),                                          # 00:27.5
        ('C0005.MP4', 1.12, 1.15),  # 1:16
        ('C0006.MP4', 0.47, 0.51),
        ('C0007.MP4', 0.23, 1.26),
        # ('C0008.MP4', 2.04, 2.10),  # squat and give up
        ('C0008.MP4', 2.58, 3.04),  # weak throw
        ('C0009.MP4', 1.22, 1.25),
        ('C0010.MP4', 2.27, 2.32),
        ('C0012.MP4', 0.27, 0.32),
        ('C0012.MP4', 1.26, 1.30),
        ('C0012.MP4', 2.30, 2.35),  # dancing at 2:05
        ],
    'data_foldername': 'Data'

}

config = {
    'output_filename': 'jordieGrimm_stefanDrillV2ToExtension.mp4',
    'deets': [
        ('C0016.MP4', '00:20', '00:37')
    ],
    'data_foldername': '/media/basement/CameraArchive/20220630'
}



DATA_FOLDER = config['data_foldername']
files_to_clip = config['deets']
output_filename = config['output_filename']


def clip_vid(filename, start_time, end_time):
    # start_frame = start_time
    # end_frame = end_time

    processed_start = process_timestamp(start_time)
    processed_end = process_timestamp(end_time)

    stream = ffmpeg.input(filename, ss=processed_start, to=processed_end)

    return stream


def main():

    trimmed = []
    for filename, start, end in files_to_clip:

        full_filename = path.join(DATA_FOLDER, filename)
        clipped = clip_vid(
            full_filename, start, end
        )
        trimmed.append(clipped)


    # trimmed[0].output(output_filename).overwrite_output().run()

    ffmpeg.concat(*trimmed).output(output_filename).overwrite_output().run()
    return True

if __name__ == '__main__':
    main()
