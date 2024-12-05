import os
from pathlib import Path
import subprocess

HOME_DIRECTORY = Path.home()
CURRENT_USER = str(HOME_DIRECTORY.expanduser()).lstrip("/Users/")

PRIMITIVE_BINARY_PATH = Path(HOME_DIRECTORY / ".pyenv" / "shims" / "primitive")

PRIMITIVE_LAUNCH_AGENT_FILEPATH = Path(
    HOME_DIRECTORY / "Library" / "LaunchAgents" / "tech.primitive.agent.plist"
)
PRIMITIVE_LAUNCH_AGENT_LOGS = Path(
    HOME_DIRECTORY / "Library" / "Logs" / "tech.primitive.agent.log"
)
PRIMITIVE_LAUNCH_AGENT_LABEL = "tech.primitive.agent"
PRIMITIVE_LAUNCH_AGENT_WORKING_DIR = Path(
    HOME_DIRECTORY / "Logs" / "tech.primitive.agent.log"
)


def stop_launch_agent():
    try:
        stop_existing_process = f"launchctl stop {PRIMITIVE_LAUNCH_AGENT_LABEL}"
        subprocess.check_output(stop_existing_process.split(" "))
        return True
    except subprocess.CalledProcessError as exception:
        print("stop_launch_agent: ", exception)
        return False


def start_launch_agent():
    try:
        start_new_agent = f"launchctl start {PRIMITIVE_LAUNCH_AGENT_LABEL}"
        subprocess.check_output(start_new_agent.split(" "))
        return True
    except subprocess.CalledProcessError as exception:
        print("start_launch_agent: ", exception)
        return False


def unload_launch_agent():
    try:
        remove_existing_agent = f"launchctl unload -w {PRIMITIVE_LAUNCH_AGENT_FILEPATH}"
        subprocess.check_output(remove_existing_agent.split(" "))
        return True
    except subprocess.CalledProcessError as exception:
        print("remove_launch_agent: ", exception)
        return False


def load_launch_agent():
    try:
        load_new_plist = f"launchctl load -w {PRIMITIVE_LAUNCH_AGENT_FILEPATH}"
        subprocess.check_output(load_new_plist.split(" "))
        return True
    except subprocess.CalledProcessError as exception:
        print("load_launch_agent: ", exception)
        return False


def create_stdout_file():
    if not PRIMITIVE_LAUNCH_AGENT_LOGS.exists():
        PRIMITIVE_LAUNCH_AGENT_LOGS.parent.mkdir(parents=True, exist_ok=True)
        PRIMITIVE_LAUNCH_AGENT_LOGS.touch()


def delete_stdout_file():
    if PRIMITIVE_LAUNCH_AGENT_LOGS.exists():
        PRIMITIVE_LAUNCH_AGENT_LOGS.unlink()


def populate_fresh_launch_agent():
    PRIMITIVE_LAUNCH_AGENT_LOGS.parent.mkdir(parents=True, exist_ok=True)
    PRIMITIVE_LAUNCH_AGENT_LOGS.touch()

    if PRIMITIVE_LAUNCH_AGENT_FILEPATH.exists():
        PRIMITIVE_LAUNCH_AGENT_FILEPATH.unlink()
    PRIMITIVE_LAUNCH_AGENT_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    PRIMITIVE_LAUNCH_AGENT_FILEPATH.touch()

    found_primitive_binary_path = PRIMITIVE_BINARY_PATH
    if not PRIMITIVE_BINARY_PATH.exists():
        result = subprocess.run(["which", "primitive"], capture_output=True)
        if result.returncode == 0:
            found_primitive_binary_path = result.stdout.decode().rstrip("\n")
        else:
            print("primitive binary not found")
            return False

    PRIMITIVE_LAUNCH_AGENT_FILEPATH.write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>KeepAlive</key>
    <true/>
    <key>Label</key>
    <string>{PRIMITIVE_LAUNCH_AGENT_LABEL}</string>
    <key>LimitLoadToSessionType</key>
	<array>
		<string>Aqua</string>
		<string>Background</string>
		<string>LoginWindow</string>
		<string>StandardIO</string>
	</array>
    <key>ProgramArguments</key>
    <array>
        <string>{found_primitive_binary_path}</string>
        <string>agent</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{PRIMITIVE_LAUNCH_AGENT_LOGS}</string>
    <key>StandardOutPath</key>
    <string>{PRIMITIVE_LAUNCH_AGENT_LOGS}</string>
</dict>
</plist>"""  # noqa: E501
    )
    PRIMITIVE_LAUNCH_AGENT_FILEPATH.chmod(0o644)
    verify_launch_agent()


def verify_launch_agent():
    plutil_check = f"plutil -lint {PRIMITIVE_LAUNCH_AGENT_FILEPATH}"
    try:
        subprocess.check_output(plutil_check.split(" "))
        return True
    except subprocess.CalledProcessError as exception:
        print("verify_launch_agent: ", exception)
        return False


def view_launch_agent_logs():
    follow_logs = f"tail -f -n +1 {PRIMITIVE_LAUNCH_AGENT_LOGS}"
    os.system(follow_logs)


def full_launch_agent_install():
    stop_launch_agent()
    unload_launch_agent()
    populate_fresh_launch_agent()
    create_stdout_file()
    load_launch_agent()
    start_launch_agent()


def full_launch_agent_uninstall():
    stop_launch_agent()
    unload_launch_agent()
    if PRIMITIVE_LAUNCH_AGENT_FILEPATH.exists():
        PRIMITIVE_LAUNCH_AGENT_FILEPATH.unlink()
    delete_stdout_file()
