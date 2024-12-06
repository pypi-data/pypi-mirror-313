# Closed Caption

**Closed Caption** là một thư viện Python mạnh mẽ, giúp bạn tạo và đồng bộ hóa phụ đề từ video một cách tự động. Thư viện hỗ trợ hai chế độ:

- **Có thời gian**: Tự động tạo phụ đề với thời gian đồng bộ từ nội dung âm thanh của video.
- **Không có thời gian**: Tạo phụ đề dạng văn bản mà không kèm thời gian.

## Tính năng nổi bật

- Tự động tạo phụ đề từ nội dung âm thanh của video (speech-to-text).

## Yêu cầu hệ thống

- Python >= 3.7
- FFmpeg (để trích xuất âm thanh từ video)

## Cài đặt

1. **Cài đặt thư viện bằng pip**:

   ```bash
   pip install closed-caption
   ```

2. **Cài đặt FFmpeg**:
   - Trên Linux (Ubuntu):

     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```

   - Trên macOS:

     ```bash
     brew install ffmpeg
     ```

   - Trên Windows:
     - Tải FFmpeg từ [ffmpeg.org](https://ffmpeg.org/) và thêm vào PATH.

## Sử dụng

### Tạo phụ đề từ video

#### 1. Tạo phụ đề có thời gian

Tạo file phụ đề `.srt` với thời gian đồng bộ:

```bash
closed_caption video.mp4 output.srt
```

#### 2. Tạo phụ đề không có thời gian

Tạo file phụ đề `.srt` không chứa thông tin thời gian:

```bash
closed_caption video.mp4 output.srt --no-timing
```

### Sử dụng thư viện trong Python

#### Tạo phụ đề có thời gian

```python
from closed_caption import create_srt_with_timing

video_path = "video.mp4"
output_srt_path = "output.srt"
create_srt_with_timing(video_path, output_srt_path)
```

#### Tạo phụ đề không có thời gian

```python
from closed_caption import create_srt_no_timing

video_path = "video.mp4"
output_srt_path = "output_no_timing.srt"
create_srt_no_timing(video_path, output_srt_path)
```

## Đóng góp

Chúng tôi hoan nghênh mọi đóng góp để cải thiện thư viện. Hãy làm theo các bước sau:

1. Fork repo này.
2. Tạo branch mới từ `main`:

   ```bash
   git checkout -b feature/my-feature
   ```

3. Commit thay đổi của bạn:

   ```bash
   git commit -m "Thêm tính năng mới: My Feature"
   ```

4. Push branch lên fork của bạn:

   ```bash
   git push origin feature/my-feature
   ```

5. Mở Pull Request (PR) và mô tả thay đổi của bạn.

### Hướng dẫn kiểm tra

1. Chạy test:

   ```bash
   python -m unittest discover -s tests
   ```

2. Đóng gói thư viện:

   ```bash
   python setup.py sdist bdist_wheel
   ```

3. Cài đặt thư viện cục bộ:

   ```bash
   pip install .
   ```

4. Chạy thử CLI:

   ```bash
   closed_caption <path-video> <output-path-srt>
   ```

## License

Dự án này được phát hành theo giấy phép MIT. Xem chi tiết tại [LICENSE](./LICENSE).

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ tại:

- **Email**: <ngochai285nd@gmail.com>
- **GitHub Issues**: [Issues](https://github.com/haiphamcoder/closed-caption/issues)

---

Cảm ơn bạn đã sử dụng **Closed Caption**!
