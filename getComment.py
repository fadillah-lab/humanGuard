from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mengatur API youtube
api_service_name = "youtube"
api_version = "v3"
YOUTUBE_API_KEY = 'AIzaSyDehe6eX_W81H5CYCPyTteUp7jC98JrJTU'

def get_youtube_comments(video_id, api_key):
    base_url = 'https://www.googleapis.com/youtube/v3/commentThreads' #url untuk mengambil data comment dari API youtube
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': api_key,
        'maxResults' : 5 #jumlah comment yang akan ditampilkan
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None  #untuk menangani error (bila ada), belum dibuat nanti aja ya

@app.route('/get_comments', methods=['GET'])
def get_comments():
    # Ambil parameter video_id dari URL
    video_id = 'r7uapAIwvao'

    if not video_id:
        return jsonify({'error': 'Parameter video_id diperlukan'}), 400

    # Dapatkan data komentar dari YouTube menggunakan kunci API
    comments_data = get_youtube_comments(video_id, YOUTUBE_API_KEY)

    if comments_data is not None:
        # Pilih hanya data yang dibutuhkan dari respons YouTube
        parsed_comments = []
        for item in comments_data.get('items', []):
            snippet = item.get('snippet', {})
            parsed_comments.append({
                'user': snippet.get('topLevelComment', {}).get('snippet', {}).get('authorDisplayName', 'Unknown'),
                'comment': snippet.get('topLevelComment', {}).get('snippet', {}).get('textDisplay', 'No comment'),
                'user_profile': snippet.get('top_level_comment', {}).get('snippet', {}).get('authorProfileImageUrl', 'No profile image')
            })

        #pemisah antar baris comment, tapi masih ngaco nih
        comments_list = [{'user': comment['user'],'comment': comment['comment']} for comment in parsed_comments]

        return jsonify({'video_id': video_id, 'comments': comments_list})
    else:
        return jsonify({'error': 'Gagal mengambil data komentar dari YouTube'}), 500

if __name__ == '_main_':
    app.run(debug=True)

# from flask import Flask 

# from .routes import main

# def create_app(config_file='settings.py'):
#     app = Flask(__name__)

#     app.config.from_pyfile(config_file)

#     app.register_blueprint(main)

#     return app
    
