# import sys
# import wave
# import os
#
# def wav_to_header(wav_path, header_path, array_name="sound_data"):
#     with wave.open(wav_path, 'rb') as wav_file:
#         num_channels = wav_file.getnchannels()
#         sample_width = wav_file.getsampwidth()
#         frame_rate = wav_file.getframerate()
#         num_frames = wav_file.getnframes()
#         audio_data = wav_file.readframes(num_frames)
#
#         print(f"Channels: {num_channels}, Sample Width: {sample_width} bytes, "
#               f"Sample Rate: {frame_rate}, Total Frames: {num_frames}")
#
#     return
#     # Format the audio data as a C-style byte array
#     byte_array = ', '.join(f'0x{b:02x}' for b in audio_data)
#
#     header_guard = os.path.splitext(os.path.basename(header_path))[0].upper() + "_H"
#
#     with open(header_path, 'w') as header_file:
#         header_file.write(f"#ifndef {header_guard}\n")
#         header_file.write(f"#define {header_guard}\n\n")
#         header_file.write(f"// Audio data generated from {os.path.basename(wav_path)}\n")
#         header_file.write(f"const unsigned char {array_name}[] = {{\n")
#
#         # Split into lines of 12 bytes
#         for i in range(0, len(audio_data), 12):
#             line = ', '.join(f"0x{b:02x}" for b in audio_data[i:i + 12])
#             header_file.write(f"    {line},\n")
#
#         header_file.write("};\n\n")
#         header_file.write(f"const unsigned int {array_name}_len = {len(audio_data)};\n")
#         header_file.write(f"#endif // {header_guard}\n")
#
#     print(f"Header file written to {header_path}")
#
#
# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print(f"Usage: {sys.argv[0]} <output.h> <input.wav>")
#         sys.exit(1)
#     wav_to_header(sys.argv[1], sys.argv[2])
#

import numpy as np
from scipy.io.wavfile import write
import os

# === Config ===
sample_rate = 22050      # Hz
duration = 10            # seconds
frequency = 1          # Hz (A4 tone)

# === Output folder ===
os.makedirs("output", exist_ok=True)

# === Time array ===
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# === Waveform generators ===
def generate_sine(frequency, t):
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def generate_square(frequency, t):
    return 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))

def generate_sawtooth(frequency, t):
    return 0.5 * 2 * (t * frequency % 1) - 0.5

# === Convert to 16-bit PCM ===
def float_to_pcm(data):
    return np.int16(data * 32767)

# === Generate and save ===
waveforms = {
    "sine": generate_sine,
    "square": generate_square,
    "tooth": generate_sawtooth
}

for name, generator in waveforms.items():
    waveform = generator(frequency, t)
    pcm_data = float_to_pcm(waveform)
    filename = f"output/{name}.wav"
    write(filename, sample_rate, pcm_data)
    print(f"Saved {filename}")
