import argparse
from pathlib import Path
from typing import Tuple

import numpy as np
from pydub import AudioSegment
from pydub.audio_segment import CouldntDecodeError
from safetensors.numpy import save_file
from tqdm import tqdm


# Load audio and convert to numpy array
def load_audio(audio_path: Path) -> Tuple[np.ndarray, int]:
    audio = AudioSegment.from_file(audio_path)
    # Change sample rate to 16000
    audio = audio.set_frame_rate(16000)
    audio_array = np.array(audio.get_array_of_samples())
    audio_sample_rate = audio.frame_rate
    return audio_array, audio_sample_rate


def save_audio_tensor(audio_tensor: np.ndarray, audio_sample_rate: int, save_path: Path):
    mean = np.mean(audio_tensor)
    std = np.std(audio_tensor)
    message_to_return = None
    if std == 0:
        message_to_return = f"std is 0 for {save_path}"
    normalized_audio = (audio_tensor - mean) / std
    normalized_audio = normalized_audio.astype(np.float32)
    struct = {
        "audio_tensor": normalized_audio,
        "audio_sample_rate": np.array(audio_sample_rate),
        "audio_mean": mean,
        "audio_std": std,
    }
    save_file(struct, save_path)
    return message_to_return


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--audio_path", type=str, required=True)
    argparse.add_argument("--save_path", type=str, required=True)
    args = argparse.parse_args()

    # check if audio_path is a folder and exist
    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio path {audio_path} does not exist")
    if not audio_path.is_dir():
        raise ValueError("Audio path must be a dir")

    save_path = Path(args.save_path)
    if not save_path.exists():
        save_path.mkdir(parents=True, exist_ok=True)

    error_files = []
    for audio_file in tqdm(audio_path.glob("**/*.webm")):
        # the struct prefix should be same
        relative_path = audio_file.relative_to(audio_path)
        # change extension to .safetensors
        new_path = relative_path.with_suffix(".safetensors")
        if (save_path / new_path).exists():
            continue
        else:
            try:
                audio_a, audio_sr = load_audio(audio_file)
            except CouldntDecodeError as e:
                print(f"Could not decode {audio_file}")
                error_files.append(audio_file)
                continue
            message = save_audio_tensor(audio_a, audio_sr, save_path / new_path)
            if message is not None:
                error_files.append(message)

    # save error files to a txt file oneline a file
    with open(save_path / "error_files.txt", "w") as f:
        f.write("\n".join([str(file_name) for file_name in error_files]))
