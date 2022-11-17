from os import path, mkdir

import ffmpeg


RESULTS_FOLDER = 'out/'
if not path.exists(RESULTS_FOLDER):
    mkdir(RESULTS_FOLDER)


def process_timestamp(timestamp):
    if type(timestamp) == float:
        return timestamp
    elif type(timestamp) == str and ':' in timestamp:
        s = timestamp.split(":")
        if len(s) == 2:  # minutes:seconds.
            return float(s[0])*60 + float(s[1])
        elif len(s) == 3:  # hours:minutes:seconds.
            return float(s[0])*60*60 + float(s[1])*60 + float(s[2])


config = {
    'output_filename': '20221103_GrimmPikeFlip.mp4',
    'deets': [
        ('C0061.MP4', '1:15', '1:20'),
        ('C0061.MP4', '2:10', '2:16'),
    ],
    'data_foldername': '/media/allen/garage/Basement/CameraArchiveDB/20221108_RX100Dump/PRIVATE/M4ROOT/CLIP'
}


config = {
    'output_filename': '20221103_GrimmFrontTuck.mp4',
    'deets': [
        ('C0060.MP4', '0:52', '0:58'),
        ('C0060.MP4', '0:53.485', '0:54.8', 0.125),
    ],
    'data_foldername': '/media/allen/garage/Basement/CameraArchiveDB/20221108_RX100Dump/PRIVATE/M4ROOT/CLIP'
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
    for row in files_to_clip:
        speed = None
        if len(row) == 3:
            filename, start, end = row
        elif len(row) == 4:
            filename, start, end, speed = row

        full_filename = path.join(DATA_FOLDER, filename)
        clipped = clip_vid(
            full_filename, start, end
        )
        if speed is not None:
            # in case I also want audio: https://superuser.com/a/1072826/119690
            clipped = clipped.setpts(f'PTS/{speed}')
        trimmed.append(clipped)

    full_output_filename = path.join(RESULTS_FOLDER, output_filename)
    ffmpeg.concat(*trimmed).output(full_output_filename, crf=28).run(overwrite_output=True)
    return True


if __name__ == '__main__':
    main()
