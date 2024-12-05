import json
import os
from enum import Enum
from hashlib import sha256
from io import BytesIO
from logging import Logger
from pathlib import Path
from time import sleep
from typing import Optional
from urllib import parse

import httpx
from tqdm.auto import tqdm
from whisper_client.extractAudio import toAudioFolder
from whisper_client.file_finder import file_finder, FileType


# global try_count
# try_count = 0


class Scheme(Enum):
    http = "http"
    https = "https"


class Mode(Enum):
    full = "full"
    text = "text"
    segments = "segments"
    words = "words"


class WhisperClient:
    log_level = os.getenv("LOG_LEVEL", "WARNING").upper()

    def __init__(
            self,
            api_key: str,
            *args,
            api_url: str = None,
            audio_folder: Path | str = None,
            video_folder: Path | str = None,
            text_folder: Path | str = None,
            erase_previous: bool = True,
            no_verify: bool = False,
            polling_interval: int = 60,
            timeout: int = 600,
            **kwargs
    ) -> None:

        self.logger = Logger("WhisperClient", level=self.log_level)
        self.logger.info("Starting WhisperClient...")

        self.last_hash = None
        self.last_status = None
        self.last_launched = None

        self.polling_interval = polling_interval
        self.timeout = timeout
        self.no_verify = no_verify

        self.api_key = api_key

        if api_url is None:
            raise ValueError("api_url is required")

        assert self.try_connection(
            api_url=api_url,
            api_key=api_key,
        ), "Could not connect to the API, please check your credentials and the route to the API."

        self.api_url = api_url

        # if (audio_folder or video_folder) and not text_folder:
        #     self.logger.error("ERROR: text_folder is required when using audio_folder or video_folder.")
        #     raise ValueError("text_folder is required when using audio_folder or video_folder.")

        if audio_folder is not None:
            if not isinstance(audio_folder, Path):
                audio_folder = Path(audio_folder)

            if not audio_folder.exists():
                self.logger.error(f"ERROR: audio_folder {audio_folder} does not exist.")
                raise FileNotFoundError(f"audio_folder {audio_folder} does not exist.")

            if not audio_folder.is_dir():
                self.logger.error(f"ERROR: audio_folder {audio_folder} is not a directory.")
                raise NotADirectoryError(f"audio_folder {audio_folder} is not a directory.")

            self.audio_folder = audio_folder

        if video_folder is not None:
            if not isinstance(video_folder, Path):
                video_folder = Path(video_folder)

            if not video_folder.exists():
                self.logger.error(f"ERROR: video_folder {video_folder} does not exist.")
                raise FileNotFoundError(f"video_folder {video_folder} does not exist.")

            if not video_folder.is_dir():
                self.logger.error(f"ERROR: video_folder {video_folder} is not a directory.")
                raise NotADirectoryError(f"video_folder {video_folder} is not a directory.")

            self.video_folder = video_folder

        if text_folder is not None:
            if not isinstance(text_folder, Path):
                text_folder = Path(text_folder)

            if not text_folder.is_dir():
                self.logger.error(f"ERROR: text_folder {text_folder} is not a directory.")
                raise NotADirectoryError(f"text_folder {text_folder} is not a directory.")

            if not text_folder.exists():
                self.logger.warning(f"WARNING: text_folder {text_folder} does not exist, creating it...")
                text_folder.mkdir(parents=True)

        else:
            text_folder = Path("text")
            self.logger.warning(f"WARNING: no text_folder fas been specified, defaulting to {text_folder.resolve()}")

        self.text_folder = text_folder

        self.erase_previous = erase_previous

        self.headers = {
            # "Content-Type": "audio/wav",
            "X-API-Key": parse.quote(self.api_key),
        }

        self.logger.info("WhisperClient started.")

    def __repr__(self) -> str:
        return f"<WhisperClient api_url={self.api_url} api_key={self.api_key}>"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, o: object) -> bool:
        return self.__hash__() == o.__hash__()

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __bool__(self) -> bool:
        return True

    def __enter__(self) -> "WhisperClient":
        return self

    def __del__(self) -> None:
        self.logger.info("Closing WhisperClient...")
        if getattr(self, "conn", None) is None:
            return
        # Else, close the connection
        self.conn.close()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.logger.info("Exiting WhisperClient context...")
        self.__del__()

    @classmethod
    def from_credentials(cls, json_credentials) -> "WhisperClient":
        with open(json_credentials, "r") as f:
            credentials = json.load(f)
        return cls(**credentials)

    def make_request(
            self,
            method: str,
            path: str,
            data: bytes = None,
            headers: dict = None,
            no_verify: bool = None,
            try_count: int = 0,
    ) -> Optional[dict]:
        if headers is None:
            headers = self.headers

        if no_verify is None:
            no_verify = self.no_verify

        if data is not None:
            data = BytesIO(data)
        try:
            response = httpx.request(
                method,
                f"{self.api_url.strip('/')}{path}",
                data=data,
                headers=headers,
                verify=not no_verify,
                timeout=self.timeout,
            )
        except httpx.HTTPError as e:
            try_count += 1
            if try_count > 10:
                self.logger.error(f"ERROR after 10 tries: {e}")
                raise e

            self.logger.error(f"ERROR: {e}, retrying for the {try_count}{'th' if try_count == 1 else 'th'} time...")
            sleep(5)
            return self.make_request(
                method=method,
                path=path,
                data=data,
                headers=headers,
                no_verify=no_verify,
                try_count=try_count,
            )

        try:
            data = response.json()
            assert not "error" in data, f"Error in response (error = {data['error']})"
        except json.JSONDecodeError:
            self.logger.error(f"ERROR decoding JSON: {response.content}")
            return
        except AssertionError as e:
            self.logger.error(f"ERROR in response: {e}\nHINT: check your API key.")
            return

        return data

    def try_connection(
            self,
            api_url: str,
            api_key: str = None,
    ) -> bool:
        self.logger.info(
            f"Trying to connect to {api_url}/healthcheck ...")
        # print(api_url)
        try:
            response = httpx.get(
                f"{api_url}/healthcheck",
                headers={
                    "X-API-Key": parse.quote(api_key),
                },
                verify=not self.no_verify,
            )
        except httpx.HTTPError as e:
            self.logger.error(f"ERROR on healthcheck: {e}")
            return False

        if response.status_code == 401:
            # Special case for invalid API key (401 Unauthorized)
            self.logger.error("ERROR: invalid API key.")
            return False

        return response.status_code == 200

    def get_status(self, hash_audio: str = None, no_verify: bool = False) -> dict:
        if hash_audio is None:
            hash_audio = self.last_hash
        data = self.make_request("GET", f"/status/{hash_audio}", no_verify=no_verify)
        return data

    def get_any_result(self, suffix: str, hash_audio: str = None, no_verify: bool = None) -> \
            Optional[dict | list | str]:
        if hash_audio is None:
            hash_audio = self.last_hash

        data = self.make_request("GET", f"/result/{hash_audio}{suffix}", no_verify=no_verify)

        if data is None or data["status"] != "done":
            print(f"WARNING : No result found for {hash_audio}{suffix}")
            return

        return data["result"]

    def get_result(self, hash_audio: str = None, no_verify: bool = None) -> dict:
        return self.get_any_result("", hash_audio, no_verify=no_verify)

    def get_result_text(self, hash_audio: str = None, no_verify: bool = None) -> str:
        return self.get_any_result("/text", hash_audio, no_verify=no_verify)

    def get_result_segments(self, hash_audio: str = None, no_verify: bool = None) -> list:
        return self.get_any_result("/segments", hash_audio, no_verify=no_verify)

    def get_result_words(self, hash_audio: str = None, no_verify: bool = None) -> list:
        return self.get_any_result("/words", hash_audio, no_verify=no_verify)

    def send_audio(
            self,
            audio: Path | str | bytes,
            hash_audio: str = None,
            no_skip: bool = None,
            no_verify: bool = None,
            verbless: bool = False,
            timeout: float = None,
    ) -> Optional[dict]:
        if timeout is None:
            timeout = self.timeout

        if isinstance(audio, str):
            audio = Path(audio)

        if isinstance(audio, Path):
            if not audio.exists():
                self.logger.error(f"ERROR: audio {audio} does not exist.")
                return

            if not audio.is_file():
                self.logger.error(f"ERROR: audio {audio} is not a file.")
                return

            with open(audio, "rb") as f:
                data = f.read()

        elif isinstance(audio, bytes):
            data = audio

        else:
            self.logger.error(f"ERROR: audio must be either a Path or bytes, not {type(audio)}.")
            return

        if hash_audio is None:
            hash_audio = self.get_hash_audio(data)
            if isinstance(audio, bytes):
                audio = Path(f"{hash_audio}.wav")  # Placeholder name fot the queries

        if no_skip is None:
            no_skip = not self.erase_previous

        if no_verify is None:
            no_verify = self.no_verify

        if not verbless:
            self.logger.info(f"Sending audio {audio}...")

        if not no_skip and self.is_hash_done(hash_audio):
            if verbless:
                print(f"Already done {hash_audio}, skipping")
                return self.get_status(hash_audio, no_verify=no_verify)
            print(f"Result for {audio} already exists")
            # return self.get_result(hash_audio)
            return self.get_status(hash_audio, no_verify=no_verify)

        response = httpx.post(
            self.api_url,
            files={
                "file": (
                    audio.name,
                    data,
                    "audio/wav"
                )
            },
            headers=self.headers,
            verify=not no_verify,
            timeout=timeout,
        )

        try:
            data = response.json()
            assert not "error" in data, f"Error in response (error = {data['error']})"
        except json.JSONDecodeError:
            self.logger.error(f"ERROR decoding JSON: {response.content}")
            return

        except AssertionError as e:
            self.logger.error(f"ERROR in response: {e}\nHINT: check your API key.")
            return

        if hash_audio != data["hash"]:
            self.logger.warning(f"WARNING : Hash mismatch ({hash_audio} != {response['hash']})")

        self.last_hash = data["hash"]
        self.last_status = data["status"]
        self.last_launched = data["launched"]

        if not verbless:
            logger_level = 3
        else:
            logger_level = 1

        self.logger.log(logger_level, f"Sent audio {audio} with hash {hash_audio}")

        if data["launched"]:
            self.logger.log(logger_level, f"Launched {hash_audio}")

        elif data["status"] == "done":
            self.logger.log(logger_level, f"Already done {hash_audio}")

        elif data["status"] == "processing":
            self.logger.log(logger_level, f"Already processing {hash_audio}")

        else:
            raise ValueError(f"Unknown status {data['status']}")

        return data

    def wait_for_result(self, hash_audio: str = None, no_verify: bool = None, interval: int = None) -> dict:
        if interval is None:
            interval = self.polling_interval

        if hash_audio is None:
            hash_audio = self.last_hash

        if no_verify is None:
            no_verify = self.no_verify

        while True:
            status = self.get_status(hash_audio, no_verify=no_verify)
            if status["status"] == "done":
                return status

            sleep(interval)

    def get_result_with_mode(
            self,
            hash_audio: str = None,
            interval: int = None,
            mode: Mode = Mode.full,
            no_verify: bool = None,
            timeout: int = None,
    ) -> dict | list | str:
        if timeout is None:
            timeout = self.timeout

        if hash_audio is None:
            hash_audio = self.last_hash

        if no_verify is None:
            no_verify = self.no_verify

        if not isinstance(mode, Mode):
            try:
                mode = Mode(mode)
            except ValueError:
                raise ValueError(
                    "mode must be either the string 'full', 'text', 'segments' or 'words' or a Mode instance.")

        match mode:
            case Mode.full:
                return self.get_result(hash_audio, no_verify=no_verify)
            case Mode.text:
                return self.get_result_text(hash_audio, no_verify=no_verify)
            case Mode.segments:
                return self.get_result_segments(hash_audio, no_verify=no_verify)
            case Mode.words:
                return self.get_result_words(hash_audio, no_verify=no_verify)
            case _:
                raise ValueError("mode must be either 'full', 'text', 'segments' or 'words'")

    def save_result_with_mode(
            self,
            hash_audio: str = None,
            interval: int = None,
            mode: Mode = Mode.full,
            no_verify: bool = None,
            timeout: int = None,
            path: Path | str = None,
    ) -> dict | list | str:

        if not isinstance(mode, Mode):
            try:
                mode = Mode(mode)
            except ValueError:
                raise ValueError(
                    "mode must be either the string 'full', 'text', 'segments' or 'words' or directly a Mode instance.")

        result = self.get_result_with_mode(
            hash_audio=hash_audio,
            interval=interval,
            mode=mode,
            no_verify=no_verify,
            timeout=timeout,
        )

        if path is None:
            path = self.text_folder / mode.value

        elif isinstance(path, str):
            if path.endswith(".json"):
                path = self.text_folder / mode.value / path
            path = Path(path)

        elif not isinstance(path, Path):
            raise ValueError("`path` must be either a Path instance or a string")

        path.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            path = path / f"{hash_audio}.json"

        if path.exists():
            if self.erase_previous:
                print(f"WARNING : {path} already exists, erasing")
            else:
                print(f"ERROR : {path} already exists and erase_previous is False, skipping")
                return result

        with path.open("w", encoding="utf-8") as f:
            if not isinstance(result, str):
                json.dump(result, f)
            else:
                f.write(result)

        return result

    def manage_audio_folder(
            self,
            folder: Path | str = None,
            mode: list[Mode] | Mode = Mode.full,
            no_verify: bool = None,
            timeout: int = None,
            no_skip: bool = None,
            interval: int = None,
    ) -> None:
        if isinstance(mode, list):
            for m in mode:
                self.manage_audio_folder(
                    folder=folder,
                    mode=m,
                    no_verify=no_verify,
                    timeout=timeout,
                    no_skip=no_skip,
                    interval=interval,
                )
            return

        if isinstance(folder, str):
            folder = Path(folder)

        if folder is None:
            folder = self.audio_folder

        if not folder.exists():
            self.logger.error(f"ERROR : {folder} does not exist")
            return

        if not folder.is_dir():
            self.logger.error(f"ERROR : {folder} is not a directory")
            return


        to_process = list(file_finder(folder, file_type=FileType.audio))

        if not to_process:
            self.logger.warning(f"No file to process in {folder}")
            return

        pbar = tqdm(total=len(to_process))

        hashes_n_paths = {}

        for audio in to_process:
            hashes_n_paths.update({
                self.send_audio(
                    audio,
                    no_skip=no_skip,
                    no_verify=no_verify,
                    timeout=timeout,
                )["hash"]: audio
            })

        while True:
            if not hashes_n_paths:
                break

            to_remove = None
            for hash_audio, audio in hashes_n_paths.items():
                if self.is_hash_done(hash_audio, no_verify=no_verify):
                    path = f"{audio.stem}.json"
                    self.save_result_with_mode(
                        hash_audio=hash_audio,
                        mode=mode,
                        no_verify=no_verify,
                        timeout=timeout,
                        path=path,
                    )
                    to_remove = hash_audio
                    pbar.update(1)
                    break

            else:
                # Sleep if no result has been found
                sleep(interval)
                continue

            if to_remove is not None:
                # Should always be the case
                hashes_n_paths.pop(to_remove)

            else:
                # Should never happen
                self.logger.error("ERROR : to_remove is None, this should never happen as we continue if no result has been found !")

        pbar.close()
        return

    def manage_video_folder(
            self,
            folder: Path | str = None,
            mode: list[Mode] | Mode = Mode.full,
            no_verify: bool = None,
            timeout: int = None,
            no_skip: bool = None,
            interval: int = None,
    ) -> None:
        if isinstance(folder, str):
            folder = Path(folder)

        if folder is None:
            folder = self.video_folder

        if not folder.exists():
            self.logger.error(f"ERROR : {folder} does not exist")
            return

        to_process = list(file_finder(folder, file_type=FileType.video))

        if not to_process:
            print(f"No file to process in {folder}")
            return

        audio_folder = self.video_to_audio_folder(folder)

        self.manage_audio_folder(
            folder=audio_folder,
            mode=mode,
            no_verify=no_verify,
            timeout=timeout,
            no_skip=no_skip,
            interval=interval,
        )

        return

    def video_to_audio_folder(self, folder: Path | str = None) -> Path:
        if isinstance(folder, str):
            folder = Path(folder)

        if not folder.exists():
            print(f"ERROR : {folder} does not exist")
            return

        if not folder.is_dir():
            print(f"ERROR : {folder} is not a directory")
            return

        audio_folder = folder / "extracted_audio"

        toAudioFolder(folder, audio_folder)

        sleep(1)  # Ensures that everything has been written to the disk

        return audio_folder

    def get_hash_audio(self, audio: bytes | BytesIO | Path | str = None) -> str:
        if audio is None:
            if self.last_hash:
                return self.last_hash

            else:
                raise ValueError("No audio passed when no previous hash was computed")

        if isinstance(audio, str):
            audio = Path(audio)

        if isinstance(audio, Path):
            with audio.open("rb") as f:
                audio = f.read()

        if isinstance(audio, BytesIO):
            audio = audio.getvalue()

        return sha256(audio).hexdigest()

    def is_hash_done(
            self,
            hash_audio: str = None,
            no_verify: bool = None,
    ) -> bool:
        if hash_audio is None:
            hash_audio = self.last_hash

        status = self.get_status(hash_audio, no_verify=no_verify)

        return status["status"] == "done"


if __name__ == "__main__":
    # print(Path.cwd())
    # if Path.cwd().name == "whisper_client":
    #     if Path.parent == "whisper_client":
    #         root = Path.cwd().parent
    #     else:
    #         root = Path.cwd()
    # else:
    #     raise Exception("You must run this script from the whisperClient folder or it's origin folder")
    #
    # data = root / "data"
    # res = root / "results"
    # # wc = WhisperClient.from_credentials(root / "credentials_tunnel.json")
    # wc = WhisperClient.from_credentials("/home/marceau/PycharmProjects/whisper-client/credentials.json")
    #
    # wc.send_audio("7206340881052372229.wav")
    #
    # wc.wait_for_result()
    #
    # with open(res / f"{wc.last_hash}.json", "w", encoding="utf-8") as f:
    #     json.dump(wc.get_result(), f)
    #
    # with open(res / f"{wc.last_hash}.txt", "w", encoding="utf-8") as f:
    #     f.write(wc.get_result_text())
    #
    # with open(res / f"{wc.last_hash}_segments.json", "w", encoding="utf-8") as f:
    #     json.dump(wc.get_result_segments(), f)
    #
    # with open(res / f"{wc.last_hash}_words.json", "w", encoding="utf-8") as f:
    #     json.dump(wc.get_result_words(), f)
    #
    # print(wc.last_hash)

    wc = WhisperClient.from_credentials("/home/marceau/PycharmProjects/whisper-client/credentials.json")

    res = wc.manage_video_folder(
        folder="../../dgs",
        mode=Mode.text,
        no_skip=True,
    )

    print(res)


