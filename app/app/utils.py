import os
import tempfile
from elevenlabs import generate, set_api_key
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import moviepy.editor as mpe

# Configure API keys
set_api_key(os.getenv("ELEVENLABS_API_KEY"))
stability_api = client.StabilityInference(
    key=os.getenv("STABILITY_API_KEY"),
    engine="stable-diffusion-xl-1024-v1-0"
)

def text_to_audio(text):
    return generate(text=text, voice="Bella", model="eleven_monolingual_v1")

def text_to_image(prompt):
    responses = stability_api.generate(prompt=prompt)
    for resp in responses:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                return artifact.binary
    return None

async def process_audio_to_video(file):
    audio_bytes = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(audio_bytes)
        return create_video([text_to_image("Audio visualization")], tmp_audio.name)

def process_text_to_video(prompt):
    angles = ["front", "side", "overhead"]
    frames = [text_to_image(f"{prompt} {angle} view") for angle in angles]
    return create_video(frames, None)

def create_video(frames, audio_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        clip = mpe.ImageSequenceClip([f for f in frames if f], fps=24)
        if audio_path:
            audio = mpe.AudioFileClip(audio_path)
            clip = clip.set_audio(audio)
        clip.write_videofile(tmp_video.name, codec="libx264")
        return tmp_video.read()
