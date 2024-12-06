import subprocess
import argparse
import os
import sys
import json


import argparse
import json
from pathlib import Path


from pathlib import Path


def file_type(file_path):
    """
    Determines if the file is a video, image, or document based on its extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The type of file - 'video', 'image', 'document', or 'unknown'.
    """
    video_extensions = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"}
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"}
    document_extensions = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
    }

    extension = Path(file_path).suffix.lower()

    if extension in video_extensions:
        return "video"
    elif extension in image_extensions:
        return "image"
    elif extension in document_extensions:
        return "document"
    else:
        return None


def user_dir():
    """Return the directory for user-specific data."""
    return Path.home() / ".config" / "send-tele"


def get_keys_file(name):
    """Return the path to the keys file for the given name."""
    return user_dir() / f"{name}_keys.json"


def list_keys(key_type):
    """List names of all stored keys for the given type."""
    path = get_keys_file(key_type)
    if not path.exists():
        print(f"No keys found for {key_type}")
        return
    keys = json.loads(path.read_text())
    for key in sorted(keys.keys()):
        if key != "// Note":
            print(key)


def get_default(key_type):
    filename = f"default_{key_type}.txt"
    path = user_dir() / filename
    if path.exists():
        return path.read_text().strip()
    else:
        return None


def set_default(key_type, model):
    filename = f"default_{key_type}.txt"
    path = user_dir() / filename
    if model is None and path.exists():
        path.unlink()
    else:
        path.write_text(model)


def get_key(key_type, name):
    """Return the value of a stored key for the given type."""
    path = get_keys_file(key_type)
    if not path.exists():
        raise Exception(f"No keys found for {key_type}")
    keys = json.loads(path.read_text())
    try:
        return keys[name]
    except KeyError:
        raise Exception(f"No key found with name '{name}' in {key_type}")


def set_key(key_type, name, value=None):
    """Save a key in the keys.json file for the given type."""
    default = {"// Note": "This file stores secret API credentials. Do not share!"}
    path = get_keys_file(key_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default))
        path.chmod(0o600)
    try:
        current = json.loads(path.read_text())
    except json.decoder.JSONDecodeError:
        current = default
    if not value:
        value = input("Enter key: ")
    current[name] = value
    path.write_text(json.dumps(current, indent=2) + "\n")


def create_subparser(subparsers, name):
    """Create a subparser for a specific type (bot or chatid)."""
    type_parser = subparsers.add_parser(name, help=f"Manage {name} keys")
    type_subparsers = type_parser.add_subparsers(dest="subcommand", required=False)

    type_parser.set_defaults(func=lambda args: list_keys(name))

    # List keys command
    list_parser = type_subparsers.add_parser(
        "list", help="List names of all stored keys"
    )
    list_parser.set_defaults(func=lambda args: list_keys(name))

    # Set key command
    set_parser = type_subparsers.add_parser(
        "set", help="Save a key in the keys.json file"
    )
    set_parser.add_argument("name", help="Name of the key to set")
    set_parser.add_argument("-v", "--value", help="Value to set (optional)")
    set_parser.set_defaults(func=lambda args: set_key(name, args.name, args.value))


def create_default_subparser(subparsers):
    default_parser = subparsers.add_parser("default", help=f"Manage Default")
    defsubparsers = default_parser.add_subparsers(dest="subcommand", required=False)

    get_parser = defsubparsers.add_parser("get", help="Get defaluts ")
    get_parser.add_argument("name", type=str, help="Get Default bot or chatid")
    get_parser.set_defaults(func=lambda args: get_default(args.name))

    set_parser = defsubparsers.add_parser("set", help="Set defaluts ")
    set_parser.add_argument("name", type=str, help="Set Default bot or chatid")
    set_parser.add_argument("value", type=str, help="Name to used as default")
    set_parser.set_defaults(func=lambda args: set_default(args.name, args.value))


def mainrun():
    parser = argparse.ArgumentParser(
        description="Manage stored API keys for different models"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create bot and chatid subparsers
    create_subparser(subparsers, "bot")
    create_subparser(subparsers, "chatid")

    args = parser.parse_args()
    args.func(args)


def load_config(filename=os.path.join(os.path.dirname(__file__), "config.json")):
    with open(filename, "r") as f:
        config = json.load(f)
    return config["config"]


def send_message(msg, bot_token, chatid):
    command = (
        "curl -s -X POST https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage -F chat_id="
        + chatid
        + " -F"
    )
    command = command.split(" ")
    command = command + ["text={}".format(msg)]
    subprocess.call(command)
    return


def create_parser():
    parser = argparse.ArgumentParser(
        description="Send message/videos/photos/docs using Telegram"
    )
    parser.add_argument("-m", "--message", help="Message Text", nargs="*", default=None)
    parser.add_argument(
        "-a",
        "--attachment",
        help="A valid file can be an image, video, docs",
        default=None,
    )
    parser.add_argument(
        "-b",
        "--bot",
        help="Bot Name. Set this with bot sendtele bot set <botname>",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--chatid",
        help="Bot Name. Set this with bot sendtele bot set <botname>",
        default=None,
    )
    subparsers = parser.add_subparsers(dest="command", required=False)
    # Create bot and chatid subparsers
    create_subparser(subparsers, "bot")
    create_subparser(subparsers, "chatid")
    create_default_subparser(subparsers)

    parser.set_defaults(func=mainsend)

    return parser


def send_media(file_path, media_type, bot_token, chatid):
    if media_type == "image":
        command = f"curl -s -X POST https://api.telegram.org/bot{bot_token}/sendPhoto -F chat_id={chatid} -F photo=@{file_path}"
    elif media_type == "video":
        command = f"curl -s -X POST https://api.telegram.org/bot{bot_token}/sendVideo -F chat_id={chatid} -F video=@{file_path}"
    elif media_type == "document":
        command = f"curl -s -X POST https://api.telegram.org/bot{bot_token}/sendDocument -F chat_id={chatid} -F document=@{file_path} -F content_type=application/pdf"
    else:
        raise ValueError("Invalid media type")

    subprocess.call(command.split(" "))


def main():
    parser = create_parser()
    args = parser.parse_args()

    args.func(args)


def mainsend(args):
    bot = args.bot
    chatid = args.chatid

    if bot is None:
        bot = get_default("bot")
        if bot is None:
            raise RuntimeError("No default bot present")

    if chatid is None:
        chatid = get_default("bot")
        if chatid is None:
            raise RuntimeError("No default chatid present")

    bot_token = get_key("bot", bot)
    chatid_token = get_key("chatid", chatid)

    if not (args.message or args.attachment):
        msg = sys.stdin.read()
        send_message(msg, bot_token, chatid_token)

    if args.attachment:
        attachement_type = file_type(args.attachment)
        if attachement_type is None:
            return
        if os.path.exists(args.attachment):
            send_media(args.attachment, attachement_type, bot_token, chatid_token)

    if args.message:
        msg = " ".join(args.message)
        send_message(msg, bot_token, chatid_token)


if __name__ == "__main__":
    main()
