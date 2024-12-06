import os
import random
import string
import tempfile

SENTINEL = "~/.bpkio/cli_session"


def sentinel_exists():
    session_sentinel = os.path.expanduser(SENTINEL)
    return os.path.exists(session_sentinel)


def remove_sentinel():
    session_sentinel = os.path.expanduser(SENTINEL)
    os.remove(session_sentinel)


def get_session_file():
    session_file = None
    session_sentinel = os.path.expanduser(SENTINEL)
    # open it and extract the path to the session file.
    with open(session_sentinel, "r") as f:
        session_file = f.read()
    return session_file


def make_session_file(session_id):
    # Create the session file
    if not session_id:
        session_id = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, "bpkio_cli", "sessions", session_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Write the path to the sentinel
    session_sentinel = os.path.expanduser(SENTINEL)
    with open(session_sentinel, "w") as f:
        f.write(path)

    return path


def destroy_session_file():
    session_file = get_session_file()
    if session_file:
        os.remove(session_file)
