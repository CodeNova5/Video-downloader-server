from flask import Flask, request, send_file, after_this_request
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)

# Enable CORS for requests from your Vercel site
CORS(app, resources={r"/*": {"origins": ""}})

@app.route('/download', methods=['GET'])
def download_video_or_audio():
    video_url = request.args.get('url')
    filename = request.args.get('filename', 'output')
    download_type = request.args.get('type', 'video')

    if not video_url:
        return {"error": "Missing 'url' parameter"}, 400

    if download_type == 'audio':
        output_filename = f"{filename}.mp3"
        base_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
    elif download_type == 'video':
        output_filename = f"{filename}.mp4"
        base_opts = {
            'format': 'best',
            'outtmpl': output_filename,
        }
    else:
        return {"error": "Invalid 'type' parameter. Use 'audio' or 'video'."}, 400

    try:
        # First attempt: without cookies
        try:
            with yt_dlp.YoutubeDL(base_opts) as ydl:
                ydl.download([video_url])
        except Exception as first_error:
            app.logger.warning(f"First attempt failed: {first_error}. Retrying with cookies...")

            # Retry with cookies.txt if available
            base_opts['cookiefile'] = 'cookies.txt'
            with yt_dlp.YoutubeDL(base_opts) as ydl:
                ydl.download([video_url])

        @after_this_request
        def remove_file(response):
            try:
                os.remove(output_filename)
            except Exception as e:
                app.logger.error(f"Error deleting file: {e}")
            return response

        return send_file(output_filename, as_attachment=True)

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
