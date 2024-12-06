import argparse
from .generate import create_srt_with_timing, create_srt_no_timing

def main():
    parser = argparse.ArgumentParser(description="Tạo phụ đề từ video.")
    parser.add_argument("video", help="Đường dẫn tới tệp video")
    parser.add_argument("output", help="Đường dẫn tệp phụ đề đầu ra (.srt)")
    parser.add_argument("--no-timing", action="store_true", help="Tạo phụ đề không có thời gian")

    args = parser.parse_args()

    if args.no_timing:
        create_srt_no_timing(args.video, args.output)
    else:
        create_srt_with_timing(args.video, args.output)
