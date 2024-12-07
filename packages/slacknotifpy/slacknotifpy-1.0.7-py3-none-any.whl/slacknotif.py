#!/usr/bin/env python3

import argparse
import json
import locale
import os
import re
import stat
import subprocess
import sys
from typing import Optional

from slack_bolt import App


def get_config_path() -> str:
    """Get the path to the config file.

    Returns:
        str: Path to the config file.
    """
    cwd = os.getcwd()
    print(f"Looking for config in the current working directory: {cwd}")
    return os.path.join(cwd, ".slacknotif_config")


def init_config() -> None:
    """Initialize the SlackNotifPy configuration in the current working directory."""
    config_path = get_config_path()
    if os.path.exists(config_path):
        print(f"Config file already exists at {config_path}.")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != "y":
            print("Initialization cancelled.")
            sys.exit(0)

    set_config(config_path)


def set_message_flow() -> tuple[str, str]:
    """Set custom messages for success and failure notifications.

    Returns:
        tuple[str, str]: Success message and failure message.
    """
    print(
        "\nYou can use {job_name} in your messages as a placeholder.\nYou can tag a user with their real name or display name with {@John Doe} or {@JohnDoe42}"
    )
    print("Example: '{job_name} did the thing! Congrats {@John Doe}!'")
    success_msg = input(
        "Enter custom success message (press Enter to use default): "
    ).strip()
    failure_msg = input(
        "Enter custom failure message (press Enter to use default): "
    ).strip()
    return success_msg, failure_msg


def set_config(config_path: str) -> None:
    """Set the Slack token, channel ID, and custom messages.

    Args:
        config_path (str): Path to the config file.
    """
    print("Setting up SlackNotifPy...")
    print("Please enter your Slack token and channel ID.")
    print("You can find your Slack token and channel ID in your Slack app settings.")
    token = input("Enter your Slack token: ").strip()
    channel_id = input("Enter your Slack Channel ID: ").strip()
    success_msg, failure_msg = set_message_flow()

    config = {
        "SLACK_TOKEN": token,
        "CHANNEL_ID": channel_id,
        "SUCCESS_MSG": success_msg,
        "FAILURE_MSG": failure_msg,
    }

    with open(config_path, "w", encoding=locale.getencoding()) as config_file:
        json.dump(config, config_file)

    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)

    print(f"SlackNotif config has been saved to {config_path}")


def load_config(config_path: str) -> tuple[str, str, str, str]:
    """Load the Slack token, channel ID, and custom messages from the config file.

    Args:
        config_path (str): Path to the config file.

    Returns:
        dict: Slack configuration (could be partial if keys are missing).
    """
    if not os.path.exists(config_path):
        print(
            "SlackNotif config not set for this project. Proceeding with defaults or CLI arguments."
        )
        return {}

    with open(config_path, "r", encoding=locale.getencoding()) as config_file:
        return json.load(config_file)


def resolve_user_mentions(app: App, message: str) -> str:
    """Resolve {@username} mentions to Slack user IDs in a message.

    Args:
        app (App): Slack Bolt app for API interaction.
        message (str): The message containing {@username} placeholders.

    Returns:
        str: The message with resolved user mentions.
    """
    user_mentions = re.findall(r"{@([^}]+)}", message)
    if not user_mentions:
        return message

    try:
        users_response = app.client.users_list()
        if not users_response["ok"]:
            print("Error retrieving user list from Slack.")
            return message
        slack_users = {}
        for user in users_response["members"]:
            if user.get("deleted", False):
                continue
            slack_id = user["id"]
            display_name = user.get("profile", {}).get("display_name_normalized", "")
            real_name = user.get("profile", {}).get("real_name_normalized", "")
            if display_name:
                slack_users[display_name] = slack_id
            if real_name:
                slack_users[real_name] = slack_id
    except Exception as e:
        print(f"Error querying users.list: {e}")
        return message

    for username in user_mentions:
        slack_id = slack_users.get(username, None)
        mention = f"<@{slack_id}>" if slack_id else "<user not found>"
        message = message.replace(f"{{@{username}}}", mention)

    return message


def format_message(message_template: str, job_name: str) -> str:
    """Format the message with the job name.

    Args:
        message_template (str): Message template with placeholders.
        job_name (str): Name of the job.

    Returns:
        str: Formatted message.
    """
    if not message_template:
        return None
    try:
        return message_template.format(job_name=job_name)
    except KeyError:
        print("Warning: Invalid message template. Using default message.")
        return None


def get_default_job_name(script_path: str) -> str:
    """Get the default job name from the script path.

    Args:
        script_path (str): Path to the job script.

    Returns:
        str: Default job name.
    """
    return os.path.splitext(os.path.basename(script_path))[0]


def notify(
    job: str,
    job_name: Optional[str] = None,
    is_command: bool = False,
    cli_config: dict = None,
) -> None:
    """Send a notification to Slack.

    Args:
        job_script (str): Path to the job script.
        job_name (str): Name of the job.
        is_command (bool): Whether or not the job is an arbitrary shell command.
        cli_config: (dict): Dictionary of values to override the config file.
    """
    if cli_config is None:
        cli_config = {}

    if job_name is None:
        job_name = get_default_job_name(job) if not is_command else "Command Job"

    config_path = get_config_path()
    file_config = load_config(config_path)

    config = {
        "SLACK_TOKEN": cli_config.get("token") or file_config.get("SLACK_TOKEN"),
        "CHANNEL_ID": cli_config.get("channel") or file_config.get("CHANNEL_ID"),
        "SUCCESS_MSG": cli_config.get("success_msg")
        or file_config.get("SUCCESS_MSG", ""),
        "FAILURE_MSG": cli_config.get("failure_msg")
        or file_config.get("FAILURE_MSG", ""),
    }

    if not config["SLACK_TOKEN"] or not config["CHANNEL_ID"]:
        print(
            "Error: Slack token and channel ID are required. Provide them via CLI or config."
        )
        sys.exit(1)

    app = App(token=config.get("SLACK_TOKEN"))
    bot_name = "SlackNotifPy"

    try:
        if is_command:
            subprocess.run(job, shell=True, check=True)
        else:
            subprocess.run(["python", job], check=True)

        success_msg = resolve_user_mentions(app, config.get("SUCCESS_MSG"))
        formatted_success = format_message(success_msg, job_name)
        message = formatted_success or f"{job_name} completed successfully"
    except subprocess.CalledProcessError:
        failure_msg = resolve_user_mentions(app, config.get("FAILURE_MSG"))
        formatted_failure = format_message(failure_msg, job_name)
        message = formatted_failure or f"{job_name} failed"

    try:
        app.client.chat_postMessage(
            channel=config.get("CHANNEL_ID"), text=message, username=bot_name
        )
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")


def set_messages(config_path: str) -> None:
    """Set custom messages for success and failure notifications.

    Args:
        config_path (str): Path to the config file.
    """
    if not os.path.exists(config_path):
        print(
            "Config file doesn't exist. Please set up the basic config first with `slacknotif init`."
        )
        sys.exit(1)

    with open(config_path, "r", encoding=locale.getencoding()) as config_file:
        config = json.load(config_file)

    success_msg, failure_msg = set_message_flow()

    config["SUCCESS_MSG"] = success_msg
    config["FAILURE_MSG"] = failure_msg

    with open(config_path, "w", encoding=locale.getencoding()) as config_file:
        json.dump(config, config_file)

    print("Custom messages have been updated!")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the SlackNotifPy CLI.

    Returns:
        argparse.ArgumentParser: The argument parser for the SlackNotifPy CLI.
    """
    parser = argparse.ArgumentParser(
        description="SlackNotifPy - Send Slack notifications on python job completion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "init", help="Initialize the SlackNotifPy configuration in the CWD"
    )

    run_parser = subparsers.add_parser(
        "run", help="Run a Python script and send a Slack notification"
    )
    run_parser.add_argument(
        "-c", "--cmd", action="store_true", help="Specify if the job is a shell command"
    )
    run_parser.add_argument(
        "job", help="Path to the Python script or shell command to run"
    )
    run_parser.add_argument(
        "job_name",
        nargs="?",
        help="Name of the job (used in notifications), defaults to script filename or 'Command Job'",
    )
    run_parser.add_argument("--token", help="Slack API token (overrides config file)")
    run_parser.add_argument(
        "--channel", help="Slack channel ID (overrides config file)"
    )
    run_parser.add_argument(
        "--success-msg", help="Custom success message (overrides config file)"
    )
    run_parser.add_argument(
        "--failure-msg", help="Custom failure message (overrides config file)"
    )

    config_parser = subparsers.add_parser(
        "config", help="Configure SlackNotifPy settings"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Configuration commands"
    )

    config_subparsers.add_parser(
        "setconfig", help="Set configuration (token, channel, custom messages)"
    )
    config_subparsers.add_parser("setmessages", help="Set custom notification messages")

    return parser


def main() -> None:
    """Main function to run the SlackNotifPy CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        init_config()

    elif args.command == "run":
        if not args.job:
            parser.parse_args(["run", "--help"])
            sys.exit(1)

        cli_config = {
            "token": args.token,
            "channel": args.channel,
            "success_msg": args.success_msg,
            "failure_msg": args.failure_msg,
        }

        notify(
            job=args.job,
            job_name=args.job_name,
            is_command=args.cmd,
            cli_config=cli_config,
        )

    elif args.command == "config":
        if not args.config_command:
            parser.parse_args(["config", "--help"])
            sys.exit(1)

        config_path = get_config_path()

        if args.config_command == "setconfig":
            set_config(config_path)
        elif args.config_command == "setmessages":
            set_messages(config_path)

    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
