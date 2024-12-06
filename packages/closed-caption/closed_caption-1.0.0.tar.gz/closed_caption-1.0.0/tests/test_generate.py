import unittest
import os
from closed_caption.generate import create_srt_with_timing, create_srt_no_timing

class TestClosedCaption(unittest.TestCase):
    def test_create_srt_with_timing(self):
        # Test chức năng tạo phụ đề có thời gian
        video_path = "test_video.mp4"
        output_path = "test_output_with_timing.srt"
        create_srt_with_timing(video_path, output_path)
        self.assertTrue(os.path.exists(output_path))

    def test_create_srt_no_timing(self):
        # Test chức năng tạo phụ đề không có thời gian
        video_path = "test_video.mp4"
        output_path = "test_output_no_timing.srt"
        create_srt_no_timing(video_path, output_path)
        self.assertTrue(os.path.exists(output_path))

if __name__ == "__main__":
    unittest.main()
