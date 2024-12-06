import whisper
from pysrt import SubRipFile, SubRipItem, SubRipTime

def create_srt_with_timing(video_path, output_srt_path, model_name="base"):
    """
    Tạo tệp phụ đề .srt từ video với thời gian đồng bộ.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(video_path)

    subs = SubRipFile()
    for segment in result['segments']:
        start_time = convert_seconds_to_srt_time(segment['start'])
        end_time = convert_seconds_to_srt_time(segment['end'])
        text = segment['text'].strip()

        subs.append(SubRipItem(index=len(subs)+1, start=start_time, end=end_time, text=text))

    subs.save(output_srt_path, encoding="utf-8")
    print(f"Tệp phụ đề đã được tạo (có thời gian): {output_srt_path}")

def create_srt_no_timing(video_path, output_srt_path, model_name="base"):
    """
    Tạo tệp phụ đề .srt từ video không kèm thời gian.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(video_path)

    subs = SubRipFile()
    for index, segment in enumerate(result['segments'], start=1):
        text = segment['text'].strip()
        subs.append(SubRipItem(index=index, start=SubRipTime(), end=SubRipTime(), text=text))

    subs.save(output_srt_path, encoding="utf-8")
    print(f"Tệp phụ đề đã được tạo (không có thời gian): {output_srt_path}")

def convert_seconds_to_srt_time(seconds):
    """
    Chuyển đổi giây sang định dạng thời gian SRT.
    """
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
