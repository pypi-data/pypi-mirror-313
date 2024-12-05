import json
import sys
from pathlib import Path
import argparse
from enum import Enum
from typing import Optional

from whisper_client.main import WhisperClient, Mode, Scheme

parser = argparse.ArgumentParser()

parser.add_argument("-k", "--api-key", type=str, help="API key for the whisper API")

parser.add_argument("-u", "--api-url", type=str, default=None, help="API url for the whisper API")

parser.add_argument("-i", "--input", type=str, default=None, help="Input file to send to the API")
parser.add_argument("-o", "--output", type=str, default=None, help="Output file to save the result")

parser.add_argument("-f", "--folder", action="store_true", help="Folder mode")
parser.add_argument("--video", action="store_true", help="Video mode")

parser.add_argument("--stdout", action="store_true", help="Print the result to stdout")
parser.add_argument("--stderr", action="store_true", help="Print the result to stderr")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

parser.add_argument("-m", "--mode", type=str, default="full",
                    help="Mode for the API, can be 'full', 'text', 'segments' and/or 'words' (comma separated)")

parser.add_argument("-c", "--config", type=str, default=None,
                    help="Config file for the whisper API, by default it is .whisperrc in the current directory "
                         "or in the home directory")
parser.add_argument("--overwrite-config", action="store_true",
                    help="Overwrite config file with the current arguments (if the --config argument isn't provided,"
                         " this will overwrite the default config file which is .whisperrc in the current directory"
                         " or in the home directory")

parser.add_argument("--no-verify", action="store_true", help="Do not verify the SSL certificate")
parser.add_argument("--no-skip", action="store_true", help="Do not skip already downloaded files")
parser.add_argument("--interval", type=int, default=100, help="Interval between two status checks")
parser.add_argument("--version", action="store_true", help="Print the version of the client")


class Type(Enum):
    VIDEO = "video"
    AUDIO = "audio"


class FileMode(Enum):
    FILE = "file"
    FOLDER = "folder"


def cli(parser: argparse.ArgumentParser = parser) -> None:
    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"whisper-client {__version__}")
        sys.exit(0)

    hash_audio = None

    config = None

    if args.config is not None:
        config = Path(args.config)
        assert config.exists(), f"ERROR : {config} does not exist"

    else:
        config = Path.cwd() / ".whisperrc"
        if not config.exists():
            config = Path.home() / ".whisperrc"
            if not config.exists():
                config = None

    if config is not None:
        with config.open(mode="r", encoding="utf-8") as f:
            config_data = json.load(f)

        for k, v in config_data.items():
            if v is not None and (
                    not hasattr(args, k)  # the attribute does not exist
                    or not getattr(args, k)  # the attribute is None or False or 0 or ""
                    or getattr(args, k) == parser.get_default(k)  # the attribute is the default value
            ):
                setattr(args, k, v)

    if args.verbose:
        print(args)

    if args.api_key is None:
        print("ERROR : no API key provided")
        sys.exit(1)

    if args.api_url is None:
        print("ERROR : no API url provided")
        sys.exit(1)

    if args.mode is not None:
        try:
            if "," in args.mode:
                args.mode = [Mode(m) for m in args.mode.split(",")]
            else:
                args.mode = Mode(args.mode)
        except ValueError:
            print("ERROR : invalid API mode provided")
            sys.exit(1)

    if args.input is None:
        print("ERROR : no input provided")
        sys.exit(1)

    args.input = args.input.strip()

    if all((not args.output, not args.stdout, not args.stderr)) and not args.folder:
        print("ERROR : no output provided")
        sys.exit(1)

    dict_kwargs = {
        "api_key": args.api_key,
        "api_url": args.api_url,
        "verbose": args.verbose,
        "stdout": args.stdout,
        "stderr": args.stderr,
        "no_verify": args.no_verify,
        "no_skip": args.no_skip,
        "mode": args.mode,
    }

    if args.overwrite_config:
        config_data.update(dict_kwargs)
        with config.open(mode="w", encoding="utf-8") as f:
            json.dump(config_data, f)

        del config_data

    audio_folder, video_folder, text_folder = None, None, None

    if args.folder:
        if args.video:
            video_folder = Path(args.input)
        else:
            audio_folder = Path(args.input)

        text_folder = Path(args.output)

    wc = WhisperClient(
        api_key=args.api_key,
        api_url=args.api_url,
        audio_folder=audio_folder,
        video_folder=video_folder,
        text_folder=text_folder,
    )

    res = manage_input(
        wc,
        args.input,
        args.folder,
        args.video,
        args.mode,
        args.no_skip,
        args.no_verify,
        args.interval,
    )

    # hash_audio = wc.get_hash_audio()  ## Getting it from the global variable instead (not the prettiest thing though)

    if args.output is not None:
        manage_output(res, args.output, args.mode, args.folder, hash_audio)

    if args.stdout:
        print(res)

    if args.stderr:
        print(res, file=sys.stderr)


def manage_input(
        wc: WhisperClient,
        input: str,
        folder: bool,
        video: bool,
        modes: Mode | list[Mode] | str | list[str],
        no_skip: bool,
        no_verify: bool,
        interval: int
) -> Optional[list]:
    if folder:
        if video:
            wc.manage_video_folder(
                folder=input,
                mode=modes,
                no_skip=no_skip,
                no_verify=no_verify,
                interval=interval
            )
        else:
            wc.manage_audio_folder(
                folder=input,
                mode=modes,
                no_skip=no_skip,
                no_verify=no_verify,
                interval=interval
            )
    else:
        audiofile = Path(input)
        assert audiofile.exists(), f"ERROR : {audiofile} does not exist"
        hash_audio = wc.get_hash_audio(audiofile)

        if not no_skip and wc.is_hash_done(hash_audio):
            print(f"Result for {audiofile} already exists, skipping")
        else:
            hash_audio = wc.send_audio(audiofile)["hash"]
            wc.wait_for_result()

        if isinstance(modes, list):
            return [
                wc.get_result_with_mode(mode=mode, hash_audio=hash_audio)
                for mode in modes
            ]
        else:
            return wc.get_result_with_mode(mode=modes, hash_audio=hash_audio)


def manage_output(
        res: list | dict | str,
        output: str | Path,
        modes: Mode | list[Mode] | str | list[str],
        folder: bool,
        hash_audio: str = None
) -> None:
    if folder:
        return

    if isinstance(output, str):
        output = Path(output)

    if isinstance(res, list):
        assert len(res) == len(modes), f"ERROR : {len(res)} results for {len(modes)} modes"
        assert output.is_dir(), f"ERROR : {output} is not a directory (folder mode)"
        for r, m in zip(res, modes):
            manage_output(r, output, m, folder)

    output = output if not output.is_dir() else output / f"{hash_audio}_{modes}.json"

    if isinstance(res, dict):
        with output.open(mode="w", encoding="utf-8") as f:
            json.dump(res, f)

    elif isinstance(res, str):
        with output.open(mode="w", encoding="utf-8") as f:
            f.write(res)

    else:
        raise TypeError(f"ERROR : invalid type for res : {type(res)}")


if __name__ == "__main__":
    cli(parser)
