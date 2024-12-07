# SlackNotifPy

`slacknotifpy` is a Python CLI tool that sends notifications to a specified Slack channel on job completion. This can be especially useful for tracking automated job results, such as success or failure, directly in Slack.

## Features

- Runs a Python script or shell command and sends a Slack notification upon completion.
- Customizable success and failure messages.
- Simple configuration for Slack tokens and channel IDs.

## Installation

Install `slacknotifpy` from PyPI:

```bash
pip install slacknotifpy
```

## Configuration

To use `slacknotifpy`, you need to configure it with your Slack token and channel ID. These settings will be saved in a `.slacknotif_config` file.

1. Run the following command to set up the configuration:

```bash
slacknotif init
```

2. Follow the prompts to enter:

- Slack Token
- Slack Channel ID
- Custom success and failure messages (optional)

You can find the Slack token and channel ID in your Slack app settings.

### Custom Messages

To update the success and failure messages for a project, use:

```bash
slacknotif config setmessages
```

## Resetting the Configuration

The initialized config file can be reset using the command:

```bash
slacknotif config setconfig
```

and following the prompts.

## Usage

After configuring `slacknotifpy`, you can use it to run scripts and send notifications:

```bash
slacknotif run <script_path> [job_name]
```

- `script_path`: The path to the Python script you want to run.
- `job_name` (optional): A name for the job, used in the Slack message. Defaults to the script filename.

Example:

```bash
slacknotif run my_script.py "Data Processing Job"
```

A shell command can be run instead of a Python script by using the `--cmd` or `-c` flag:


```bash
slacknotif run -c "<SHELL COMMAND>" [job_name]
```

Example:

```bash
slacknotif run -c "ls -l /tmp" "My Shell Comand Job"
```

### Running without a config file

You can run the tool without first running the `init` command by passing in the API token and channel ID (and optionally the custom messages) as arguments. The arguments will override values in the config file if it does exist.

```bash
slacknotif run <script_path> [job_name] [--token TOKEN] [--channel CHANNEL] [--success-msg SUCCESS_MSG] [--failure-msg FAILURE_MSG]
```

Example:

```bash
slacknotif run my_script.py "Data Processing Job" --token "MY-API-TOKEN" --channel "Random"
```

## Example Slack Notification Messages

- Success: "Data Processing Job completed successfully"
- Failure: "Data Processing Job failed"

You can customize these messages using `{job_name}` as a placeholder in the config.

You can also tag users using thier real or display names using `{@John Doe}` or `{@JohnDoe42}`

## Command Reference
- Configure SlackNotifPy: `slacknotif init`
- Re-Configure SlackNotifPy: `slacknotif config setconfig`
- Set Custom Messages: `slacknotif config setmessages`
- Run Script and Notify: `slacknotif run <script_path> [job_name]`
- Run Shell Command and Notify: `slacknotif run -c "<SHELL COMMAND>" [job_name]`
- Run Script and Notify and override config settings: `slacknotif run <script_path> [job_name] [--token TOKEN] [--channel CHANNEL] [--success-msg SUCCESS_MSG] [--failure-msg FAILURE_MSG]`

## License

This project is licensed under the MIT License.
