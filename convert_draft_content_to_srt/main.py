import json
import sys

from googletrans import Translator


def us_to_srt_timecode(microseconds):
    total_seconds = microseconds / 1_000_000  # Chuyển đổi thành giây
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Tính toán phần giây và phần mili giây
    seconds_int = int(seconds)
    milliseconds = int((seconds - seconds_int) * 1000)

    if milliseconds == 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds_int:02d},{milliseconds:03d}"
    else:
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds_int:02d},{milliseconds:03d}"


def translate(source, destination, content):
    # Tạo một đối tượng Translator
    translator = Translator()
    # Dịch sang tiếng Việt
    translated = translator.translate(content, src=source, dest=destination)
    # In kết quả dịch
    return (translated.text)


# Đọc dữ liệu từ file JSON
with open('draft_content.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
# Tạo danh sách chứa các đoạn phụ đề
subtitles = []

# Lấy thông tin cần thiết
materials = data.get('materials', [])
material_name = materials['videos'][0]['material_name']
tracks = data.get('tracks', [])

# Lấy thông tin về văn bản (texts) trong material
texts = materials['texts']

for i, text_info in enumerate(texts):
    content = text_info['content']
    content = content[content.find('[') + 1:content.find(']')]

    for track in tracks:
        if track.get('type') == 'text':
            segments = track['segments']
            start_time = segments[i]['target_timerange']['start']
            end_time = start_time + segments[i]['target_timerange']['duration']

    # Kiểm tra xem có đủ đối số không
    if len(sys.argv) < 2:
        subtitle = {
            'start': us_to_srt_timecode(start_time),
            'end': us_to_srt_timecode(end_time),
            'text': content
        }
    else:
        # Lấy ngôn ngữ nguồn từ đối số dòng lệnh
        source = sys.argv[1]
        subtitle = {
            'start': us_to_srt_timecode(start_time),
            'end': us_to_srt_timecode(end_time),
            'text': translate(source, 'vi', content)
        }
        print(str(i) + ' - ', content+' --> ', subtitle['text'])

    subtitles.append(subtitle)


# Sắp xếp các đoạn phụ đề theo thời gian bắt đầu
subtitles.sort(key=lambda x: x['start'])

# Tạo tệp .srt
output_srt = material_name[:-3] + "srt"
with open(output_srt, 'w', encoding='utf-8') as srt_file:
    for i, subtitle in enumerate(subtitles, start=1):
        srt_file.write(str(i) + '\n')
        srt_file.write(f"{subtitle['start']} --> {subtitle['end']}\n")
        srt_file.write(subtitle['text'] + '\n\n')

print(f"Dữ liệu đã được trích xuất và lưu vào tệp {output_srt}")
