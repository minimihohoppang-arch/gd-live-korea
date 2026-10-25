
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SEARCH_URL = "https://api.chzzk.naver.com/service/v1/search/lives"
KEYWORD = "Geometry Dash"

def get_chzzk_streams():
    params = urllib.parse.urlencode({"keyword": KEYWORD, "offset": 0, "size": 20})
    request = urllib.request.Request(
        SEARCH_URL + "?" + params,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.load(response)

    results = []
    for item in (data.get("content") or {}).get("data", []):
        live = item.get("live") or item
        channel = live.get("channel") or {}
        channel_id = channel.get("channelId")
        if not channel_id:
            continue

        results.append({
            "platform": "chzzk",
            "title": live.get("liveTitle", ""),
            "streamer": channel.get("channelName", ""),
            "url": "https://chzzk.naver.com/live/" + channel_id,
            "thumbnail": live.get("liveImageUrl", ""),
            "viewers": live.get("concurrentUserCount", 0)
        })
    return results

def main():
    try:
        streams = get_chzzk_streams()
    except Exception as error:
        print("검색 실패:", error)
        raise

    with open("streams.json", "w", encoding="utf-8") as file:
        json.dump(streams, file, ensure_ascii=False, indent=2)

    print(datetime.now(timezone.utc).isoformat(), len(streams), "streams")

if __name__ == "__main__":
    main()
