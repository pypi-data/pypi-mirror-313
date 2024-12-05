# SPDX-FileCopyrightText: 2023-present Marceau-h <pypi@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-V3-or-later
#

from whisper_client.main import WhisperClient, Mode, Scheme
from whisper_client.cli import cli
from whisper_client.__about__ import __version__



__all__ = ["WhisperClient", "Mode", "Scheme", "cli", "__version__"]
