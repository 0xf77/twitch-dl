import requests
import random
import string
import sys
import urllib.parse
import re
import os

def randomString(stringLength):
	letters = string.ascii_lowercase
	return ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(stringLength)])


def get_access_token(video_id):

	print("[i] Fetching access token..")

	cookies = {
    'server_session_id': randomString(32),
    'unique_id': randomString(16),
    'api_token': 'twilight.e9310e94d6a6cf6b2d9652c99f476621',
    'twitch.lohp.countryCode': 'IT',
	}

	headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/vnd.twitchtv.v5+json; charset=UTF-8',
    'Host': 'api.twitch.tv',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'br, gzip, deflate',
    'Origin': 'https://www.twitch.tv',
    'Referer': 'https://www.twitch.tv/videos/' + video_id,
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15',
    #Seems that this Client-ID is specific for the not-logged user?
    'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
    'X-Requested-With': 'XMLHttpRequest',
	}


	params = (
    ('oauth_token', 'undefined'),
    ('need_https', 'true'),
    ('platform', 'web'),
    ('player_type', 'site'),
    ('player_backend', 'mediaplayer'),
	)
	response = requests.get('https://api.twitch.tv/api/vods/' + video_id + '/access_token', headers=headers, params=params, cookies=cookies)

	if response.status_code == 200:
		response_obj = {
			'video_id': video_id,
			'auth': response.json()['token'],
			'sig': response.json()['sig']
		}
		print("[i] Got access token!")
		return response_obj
	else:
		print("[e] Got an error requesting the token:")
		print(response.json())
		quit()



def download_video(quality, response_obj):
	print("[i] Generating download url..")
	download_url = "https://usher.ttvnw.net/vod/" + response_obj['video_id'] + ".m3u8" + \
					"?allow_source=true" + \
					"&p=5760802" + \
					"&player_backend=mediaplayer" + \
					"&playlist_include_framerate=true" + \
					"&reassignments_supported=true" + \
					"&sig=" + response_obj['sig']+ \
					"&token=" + urllib.parse.quote(response_obj['auth']) + \
					"&cdm=wv"
	print("[i] Starting ffmpeg..")

	#Use -map p:x for other resolutions (Not implemented yet)
	command = "ffmpeg -i '"+ download_url +"' -acodec copy -vcodec copy out.mp4"
	os.system(command)

def parse_input():
	if len(sys.argv) < 2:
		print("[e] No URL to download")
	else:
		match = re.findall(r'\d+', sys.argv[1])
		if match:
			video_id = match[0]
			print("Downloading video: " + video_id)
			download_video(get_access_token(video_id))
		else:
			print("[e] Can't parse this URL")


if __name__ == "__main__":
	print("\nTwitch-dl * made with ♥ by 0xf77\n")
	parse_input()