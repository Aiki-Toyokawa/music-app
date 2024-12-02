# utl1_info_json_creator.py

import os
import json
from datetime import datetime, timedelta

# ----------------------------------------------------
# YouTube動画の情報を抽出し、JSONファイルに保存します。
# Parameters:
#     info_dict (str): 情報を抽出するYouTube動画のURL。
#     json_filename (str): 出力するJSONファイルのパス。
# Returns:
#     dict: 抽出された情報データ。
# ----------------------------------------------------

def create_info_json(info_dict, each_video_folder_path):
    if not info_dict:
        print("有効な情報辞書が提供されていません。")
        return None

    # 必要な情報を抽出し、指定された形式に合わせる
    description_text = info_dict.get('description', '不明')
    description_list = description_text.splitlines() if description_text != '不明' else ['不明']

    # 動画品質と音声品質の初期化
    video_quality = '不明'
    audio_quality = '不明'
    video_width = '不明'
    video_height = '不明'
    this_video_quality = '不明'

    # 利用可能な最高品質の動画と音声の情報を取得
    formats = info_dict.get('formats', [])
    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height')]
    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('abr')]

    if video_formats:
        # 最高品質の動画を取得
        best_video = max(video_formats, key=lambda f: f.get('height', 0))
        video_quality = f"{best_video.get('height')}p"
        video_width = best_video.get('width', '不明')
        video_height = best_video.get('height', '不明')

        # 現在の動画品質を取得
        current_format_id = info_dict.get('format_id', '')
        current_video_format = next((f for f in video_formats if f.get('format_id') == current_format_id), None)
        if current_video_format and current_video_format.get('height'):
            this_video_quality = f"{current_video_format.get('height')}p"
        else:
            this_video_quality = video_quality  # 指定がなければ最高品質を使用

    if audio_formats:
        best_audio = max(audio_formats, key=lambda f: f.get('abr', 0))
        audio_quality = f"{best_audio.get('abr')}kbps"

    raw_data = {
        "title": info_dict.get('title', '不明'),
        "target_url": info_dict.get('webpage_url', '不明'),
        "thumbnail_url": info_dict.get('thumbnail', '不明'),
        "uploader": info_dict.get('uploader', '不明'),
        "uploader_id": info_dict.get('uploader_id', '不明'),
        "uploader_url": info_dict.get('uploader_url', '不明'),
        "channel": info_dict.get('channel', '不明'),
        "channel_id": info_dict.get('channel_id', '不明'),
        "channel_url": info_dict.get('channel_url', '不明'),
        "duration": str(timedelta(seconds=info_dict.get('duration', 0))),
        "serial_duration": info_dict.get('duration', 0),
        "upload_date": info_dict.get('upload_date', '不明'),
        "release_date": info_dict.get('release_date', '不明'),
        "video_id": info_dict.get('id', '不明'),
        "site_name": info_dict.get('extractor', '不明'),
        "this_video_quality": this_video_quality,
        "video_quality": video_quality,
        "audio_quality": audio_quality,
        "video_width": video_width,
        "video_height": video_height,
        "age_limit": info_dict.get('age_limit', 0),
        "categories": info_dict.get('categories', []),
        "video_tags": info_dict.get('tags', []),
        "description": description_list,
    }

    # ユーザーデータを設定
    user_data = {
        "user_edited_title": raw_data['title'],  # 必要に応じて編集可能
        "user_download_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "user_notes": "",
        "user_tags": [],
    }

    # 全体のデータをまとめる
    output_data = {
        "user_data": user_data,
        "raw_data": raw_data,
    }

    # JSONファイルに書き込む
    info_json_file_path = os.path.join(each_video_folder_path, 'info.json')

    try:
        print(f"動画情報をjsonファイルに書き込みます...\npath: {info_json_file_path}")
        with open(info_json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)
        print(f"動画情報の書き込み完了: {info_json_file_path}")
    except IOError as e:
        print(f"ファイルの書き込み中にエラーが発生しました: {e}")
        return None

    return info_json_file_path