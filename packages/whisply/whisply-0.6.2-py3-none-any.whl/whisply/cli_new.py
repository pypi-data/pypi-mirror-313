import os
import typer

from pathlib import Path
from enum import Enum
from typing import Optional, List
from rich import print


app = typer.Typer(
    help="WHISPLY 💬 Transcribe, translate, annotate and subtitle audio and video files with OpenAI's Whisper ... fast!",
    no_args_is_help=True
    )


class DeviceChoice(str, Enum):
    AUTO = 'auto'
    CPU = 'cpu'
    GPU = 'gpu'
    MPS = 'mps'


def get_device(device: DeviceChoice = DeviceChoice.AUTO, exclude_mps: bool = True) -> str:
    """
    Determine the computation device based on user preference and availability.
    
    Parameters:
    device (DeviceChoice): The computation device that will be checked for availability.
    exclude_mps (bool): Flag to exclude MPS device for certain transcription tasks
        that do not allow MPS backend (e.g., whisperX)
    """
    import torch

    if device == DeviceChoice.AUTO and exclude_mps:
        if torch.cuda.is_available():
            device = 'cuda:0'
        else:
            device = 'cpu'
    elif device == DeviceChoice.AUTO:
        if torch.cuda.is_available():
            device = 'cuda:0'
        elif torch.backends.mps.is_available():
            device = 'mps'
        else:
            device = 'cpu'
    elif device == DeviceChoice.GPU:
        if torch.cuda.is_available():
            device = 'cuda:0'
        else:
            device = 'cpu'
    elif device == DeviceChoice.MPS and not exclude_mps:
        if torch.backends.mps.is_available():
            device = 'mps'
        else:
            device = 'cpu'
    elif device == DeviceChoice.CPU:
        device = 'cpu'
    else:
        device = 'cpu'
    return device


def load_config(config: Optional[Path], **kwargs):
    from whisply import little_helper
    if config:
        config_data = little_helper.load_config(config)
        for key, value in kwargs.items():
            kwargs[key] = config_data.get(key, value)
    return kwargs


def check_model(model: str):
    from whisply import models
    if not models.ensure_model(model):
        msg = f"""[bold]→ Model "{model}" is not available.\n→ Available models: """
        msg += ', '.join(models.WHISPER_MODELS.keys())
        print(f"[bold]{msg}")
        raise typer.Exit(code=1)


@app.command()
def transcribe(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        "-f",
        help="Path to file, folder, URL or .list to process.",
    ),
    output_dir: Path = typer.Option(
        Path("./transcriptions"),
        "--output_dir",
        "-o",
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Folder where transcripts should be saved.",
    ),
    device: DeviceChoice = typer.Option(
        DeviceChoice.AUTO,
        "--device",
        "-d",
        help="Select the computation device: CPU, GPU (NVIDIA), or MPS (Mac M1-M3).",
    ),
    model: str = typer.Option(
        "large-v2",
        "--model",
        "-m",
        help='Whisper model to use (List models via --list_models).',
    ),
    lang: Optional[str] = typer.Option(
        None,
        "--lang",
        "-l",
        help='Language of provided file(s) ("en", "de") (Default: auto-detection).',
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print text chunks during transcription.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to configuration file.",
    ),
):
    """
    Transcribe audio and video files with OpenAI's Whisper.
    """
    from whisply import transcription

    # Load configuration from config.json if provided
    params = load_config(config, files=files, output_dir=output_dir, device=device, model=model, lang=lang, verbose=verbose)
    files, output_dir, device, model, lang, verbose = params.values()

    # Check if provided model is available
    check_model(model)

    # Determine the computation device
    device_str = get_device(device=device)

    # Instantiate TranscriptionHandler
    service = transcription.TranscriptionHandler(
        base_dir=output_dir,
        device=device_str,
        model=model,
        file_language=lang,
        verbose=verbose
    )
    # Process files
    service.process_files(files)


@app.command()
def translate(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        "-f",
        help="Path to file, folder, URL or .list to process.",
    ),
    output_dir: Path = typer.Option(
        Path("./transcriptions"),
        "--output_dir",
        "-o",
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Folder where transcripts should be saved.",
    ),
    model: str = typer.Option(
        "large-v2",
        "--model",
        "-m",
        help='Whisper model to use (List models via --list_models).',
    ),
    lang: Optional[str] = typer.Option(
        None,
        "--lang",
        "-l",
        help='Language of provided file(s) ("en", "de") (Default: auto-detection).',
    ),
    translate: bool = typer.Option(
        True,
        "--translate",
        "-t",
        help="Translate transcription to English.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print text chunks during transcription.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to configuration file.",
    ),
):
    """
    Translate transcriptions to English.
    """
    from whisply import transcription

    # Load configuration from config.json if provided
    params = load_config(config, files=files, output_dir=output_dir, model=model, lang=lang, translate=translate, verbose=verbose)
    files, output_dir, model, lang, translate, verbose = params.values()

    # Check if provided model is available
    check_model(model)

    # Instantiate TranscriptionHandler
    service = transcription.TranscriptionHandler(
        base_dir=output_dir,
        model=model,
        file_language=lang,
        translate=translate,
        verbose=verbose
    )
    # Process files
    service.process_files(files)


@app.command()
def subtitle(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        "-f",
        help="Path to file, folder, URL or .list to process.",
    ),
    output_dir: Path = typer.Option(
        Path("./transcriptions"),
        "--output_dir",
        "-o",
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Folder where subtitles should be saved.",
    ),
    model: str = typer.Option(
        "large-v2",
        "--model",
        "-m",
        help='Whisper model to use (List models via --list_models).',
    ),
    subtitle: bool = typer.Option(
        True,
        "--subtitle",
        "-s",
        help="Create subtitles (Saves .srt, .vtt and .webvtt).",
    ),
    sub_length: int = typer.Option(
        5,
        "--sub_length",
        help="Subtitle segment length in words"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print text chunks during transcription.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to configuration file.",
    ),
):
    """
    Create subtitles for audio and video files.
    """
    from whisply import transcription

    # Load configuration from config.json if provided
    params = load_config(config, files=files, output_dir=output_dir, model=model, subtitle=subtitle, sub_length=sub_length, verbose=verbose)
    files, output_dir, model, subtitle, sub_length, verbose = params.values()

    # Check if provided model is available
    check_model(model)

    # Instantiate TranscriptionHandler
    service = transcription.TranscriptionHandler(
        base_dir=output_dir,
        model=model,
        subtitle=subtitle,
        sub_length=sub_length,
        verbose=verbose
    )
    # Process files
    service.process_files(files)


@app.command()
def annotate(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        "-f",
        help="Path to file, folder, URL or .list to process.",
    ),
    output_dir: Path = typer.Option(
        Path("./transcriptions"),
        "--output_dir",
        "-o",
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Folder where annotations should be saved.",
    ),
    model: str = typer.Option(
        "large-v2",
        "--model",
        "-m",
        help='Whisper model to use (List models via --list_models).',
    ),
    annotate: bool = typer.Option(
        True,
        "--annotate",
        "-a",
        help="Enable speaker annotation (Saves .rttm).",
    ),
    hf_token: Optional[str] = typer.Option(
        None,
        "--hf_token",
        "-hf",
        help="HuggingFace Access token required for speaker annotation.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print text chunks during transcription.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to configuration file.",
    ),
):
    """
    Annotate audio and video files with speaker information.
    """
    from whisply import transcription

    # Load configuration from config.json if provided
    params = load_config(config, files=files, output_dir=output_dir, model=model, annotate=annotate, hf_token=hf_token, verbose=verbose)
    files, output_dir, model, annotate, hf_token, verbose = params.values()

    # Check if provided model is available
    check_model(model)

    # Check for HuggingFace Access Token if speaker annotation is enabled
    if annotate and not hf_token:
        hf_token = os.getenv('HF_TOKEN')
        if not hf_token:
            print('[bold]→ Please provide a HuggingFace access token (--hf_token / -hf) to enable speaker annotation.')
            raise typer.Exit(code=1)

    # Instantiate TranscriptionHandler
    service = transcription.TranscriptionHandler(
        base_dir=output_dir,
        model=model,
        annotate=annotate,
        hf_token=hf_token,
        verbose=verbose
    )
    # Process files
    service.process_files(files)


@app.callback()
def default_options(
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to configuration file.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print verbose output.",
    ),
):
    """
    Default options if no command is provided.
    """
    if config:
        print(f"Loading configuration from: {config}")
    if verbose:
        print("Verbose mode enabled.")
        

def run():
    app()


if __name__ == "__main__":
    run()
