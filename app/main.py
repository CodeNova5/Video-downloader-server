from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this middleware to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace "*" with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

# Function to download video
def download_video(url):
    import yt_dlp

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Request model
class VideoRequest(BaseModel):
    url: str

@app.post("/download")
async def download(video_request: VideoRequest):
    try:
        download_video(video_request.url)
        return {"message": "Download complete!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

