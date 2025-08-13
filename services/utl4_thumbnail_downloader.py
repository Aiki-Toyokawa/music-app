# utl4_thumbnail_downloader.py  — code2 改良版（高速 + 640x480取りこぼし防止）
import os
from typing import Optional, Dict, Any, List, Tuple
import requests

# 既知の解像度順（大→小）
JPG_ORDER = ["maxresdefault", "sddefault", "hqdefault", "mqdefault", "default"]
ENABLE_WEBP_FALLBACK = True
BIGGER_THAN_DEFAULT_RATIO = 1.2

def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (compatible; ThumbnailFetcher/1.1)"})
    return s

def _urls_from_info(info_dict: dict) -> List[Tuple[str, Optional[int], Optional[int]]]:
    thumbs = info_dict.get("thumbnails") or []
    items: List[Tuple[str, Optional[int], Optional[int]]] = []
    for t in thumbs:
        if isinstance(t, dict) and t.get("url"):
            items.append((t["url"], t.get("width"), t.get("height")))
    items.sort(key=lambda x: ((x[2] or 0), (x[1] or 0)), reverse=True)
    return items

def _jpg_candidates(video_id: str) -> List[str]:
    base = f"https://img.youtube.com/vi/{video_id}"
    return [f"{base}/{name}.jpg" for name in JPG_ORDER]

def _webp_candidates(video_id: str) -> List[str]:
    base = f"https://i.ytimg.com/vi_webp/{video_id}"
    return [f"{base}/{name}.webp" for name in JPG_ORDER]

def _head_len(sess: requests.Session, url: str, timeout: int = 6) -> Optional[int]:
    try:
        r = sess.head(url, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            cl = r.headers.get("Content-Length")
            return int(cl) if cl and cl.isdigit() else None
    except requests.RequestException:
        pass
    return None

def _get_bytes(sess: requests.Session, url: str, timeout: int = 10) -> Optional[bytes]:
    try:
        r = sess.get(url, timeout=timeout, stream=False)
        if r.status_code == 200 and r.content:
            return r.content
    except requests.RequestException:
        pass
    return None

def _try_upgrade_to_sd_or_maxres(
    sess: requests.Session,
    vid: str,
    baseline_len: Optional[int],
) -> Optional[str]:
    """
    いま持っているサムネ（例: hq 480x360）が baseline の場合、
    できるだけ軽く sd(640x480)/maxres を試して、明らかに大きければその URL を返す。
    HEAD の Content-Length が取れない場合は、最小1回だけ GET で確かめる。
    """
    # 候補は sd → maxres の順（sd で十分なことが多い）
    jpg_sd = f"https://img.youtube.com/vi/{vid}/sddefault.jpg"
    jpg_max = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"

    # 1) HEAD で確認
    for url in (jpg_sd, jpg_max):
        clen = _head_len(sess, url)
        if baseline_len and clen and clen >= int(baseline_len * BIGGER_THAN_DEFAULT_RATIO):
            return url

    # 2) HEAD で判断できなければ、最小1回だけ GET を許容（sd を先に）
    data = _get_bytes(sess, jpg_sd)
    if data and baseline_len and len(data) >= int(baseline_len * BIGGER_THAN_DEFAULT_RATIO):
        # 良化が明確
        return jpg_sd

    # maxres は未生成が多いので GET は原則しない（コスト/失敗率の観点）
    return None

def download_thumbnail(info_or_url, each_video_folder_path: str) -> Optional[str]:
    os.makedirs(each_video_folder_path, exist_ok=True)
    sess = _session()

    # (A) URL 文字列ならそのまま 1 回 GET
    if isinstance(info_or_url, str):
        data = _get_bytes(sess, info_or_url)
        if not data:
            print("サムネイル画像を取得できませんでした。")
            return None
        ext = ".webp" if info_or_url.lower().endswith(".webp") else (".png" if info_or_url.lower().endswith(".png") else ".jpg")
        out = os.path.join(each_video_folder_path, f"thumbnail{ext}")
        with open(out, "wb") as f:
            f.write(data)
        print(f"サムネイル画像のダウンロード完了: {out}\nfrom: {info_or_url}")
        return out

    # (B) info_dict ベース
    info_dict: Dict[str, Any] = info_or_url or {}
    vid = info_dict.get("id")
    if not vid:
        print("サムネイル取得: video id が不明です。")
        return None

    # 1) info_dict['thumbnails'] に寸法あり → まず最大URLを GET
    from_info = _urls_from_info(info_dict)
    if from_info:
        top_url, top_w, top_h = from_info[0]
        data = _get_bytes(sess, top_url)
        if data:
            # 2) もし info_dict 最大が <640x480 っぽい/寸法不明なら、sd/maxres を軽くプローブしてアップグレード
            should_probe = (not top_w or not top_h or (top_w < 640 and top_h < 480))
            if should_probe:
                upgraded = _try_upgrade_to_sd_or_maxres(sess, vid, baseline_len=len(data))
                if upgraded:
                    up_data = _get_bytes(sess, upgraded)
                    if up_data:
                        top_url, data = upgraded, up_data
            ext = ".webp" if top_url.lower().endswith(".webp") else (".png" if top_url.lower().endswith(".png") else ".jpg")
            out = os.path.join(each_video_folder_path, f"thumbnail{ext}")
            with open(out, "wb") as f:
                f.write(data)
            print(f"サムネイル画像のダウンロード完了: {out}\nfrom: {top_url} (info_dict with upgrade check)")
            return out
        # 取れなければ既知URLにフォールバック

    # 3) 既知URL（JPG）側で、default を baseline に HEAD 比較 → 最終 GET は1回だけ
    jpgs = _jpg_candidates(vid)
    default_len = _head_len(sess, jpgs[-1])  # .../default.jpg

    picked: Optional[str] = None
    for url in jpgs[:-1]:  # default 以外
        clen = _head_len(sess, url)
        if default_len and clen and clen >= int(default_len * BIGGER_THAN_DEFAULT_RATIO):
            picked = url
            break

    # JPGで決まらなければ必要時のみ WEBP
    if not picked and ENABLE_WEBP_FALLBACK:
        webps = _webp_candidates(vid)
        if default_len is None:
            default_len = _head_len(sess, webps[-1])
        for url in webps[:-1]:
            clen = _head_len(sess, url)
            if default_len and clen and clen >= int(default_len * BIGGER_THAN_DEFAULT_RATIO):
                picked = url
                break

    # どれも判定できない→ default.jpg
    if not picked:
        picked = jpgs[-1]

    data = _get_bytes(sess, picked)
    if not data:
        print("サムネイル画像を取得できませんでした。")
        return None

    ext = os.path.splitext(picked)[1] or ".jpg"
    out = os.path.join(each_video_folder_path, f"thumbnail{ext}")
    with open(out, "wb") as f:
        f.write(data)
    print(f"サムネイル画像のダウンロード完了: {out}\nfrom: {picked}")
    return out
