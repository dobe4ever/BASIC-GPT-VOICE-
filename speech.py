from elevenlabs import generate
import os


def elevenlabs_gen(ai_response):
    # Optimize text message for speech
    paragraphs = split_text(text=ai_response)
    # Convert text to audio
    generate_audio(paragraphs)

    return open(os.path.abspath(f"downloads/audio-response.mp3"), "rb")


def split_text(text):
    # Split the text into chunks of 2400 characters each
    chunks = [text[i:i+2400] for i in range(0, len(text), 2400)]

    paragraphs = []

    for chunk in chunks:
        start = 0
        while start < len(chunk):
            # Find the closest period before the 230th character
            end = chunk.rfind('.', start, start + 230)

            if end == -1: 
                # If there is no period within the first 230 characters,
                # just cut off at the maximum length.
                end = min(start + 230, len(chunk))

            paragraph = chunk[start:end].strip()

            if paragraph: 
                paragraphs.append(paragraph)

            start = end + 1

    return paragraphs


def generate_audio(paragraphs):
    audio_files = []

    for paragraph in paragraphs:
        print(paragraph, "\n\n")

        # Generate audio for each paragraph
        audio = generate(
            text=paragraph,
            voice='Bella',
            # api_key="",
        )
        audio_files.append(audio)

    # Combine all audios into one and save it
    combined_audio = b"".join(audio_files)

    with open(os.path.abspath(
        f"downloads/audio-response.mp3"), "wb") as f:
            f.write(combined_audio)


def restart():
    import subprocess
    SystemExit()
    subprocess.run(["kill", "1"])