#!/usr/bin/env python3
import os
import subprocess
import shlex
from fastmcp import FastMCP

mcp = FastMCP("Tmux Manager")

def is_in_tmux() -> bool:
    return os.environ.get("TMUX") is not None

def run_tmux_command(args: list[str]) -> str:
    if not is_in_tmux():
        return "Error: Not running inside a tmux session."
    
    try:
        result = subprocess.run(
            ["tmux"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Tmux Error: {e.stderr.strip()}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def tmux_list_windows() -> str:
    """
    Lists all windows in the current tmux session.
    Returns a formatted list of window IDs, names, and active commands.
    """
    # format: index:name:layout:active_flag
    return run_tmux_command(["list-windows"])

@mcp.tool()
def tmux_new_window(command: str, name: str = None, keep_open: bool = True) -> str:
    """
    Opens a new tmux window and runs the specified command.
    
    Args:
        command: The shell command to execute.
        name: Optional name for the new window.
        keep_open: If True (default), keeps the window open after command finishes 
                   (by appending '; echo "Press Enter to close..."; read'). 
                   If False, window closes immediately when command exits.
    """
    args = ["new-window"]
    if name:
        args.extend(["-n", name])
    
    final_command = command
    if keep_open:
        # Escape the inner command properly for the shell wrapper
        # We want: sh -c 'COMMAND; echo...; read'
        final_command = f'{command}; echo "\n--------------------------------------------------"; echo "Command finished. Press Enter to close window..."; read'
    
    args.append(final_command)
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Started command in new window{' ' + name if name else ''}: {command}"

@mcp.tool()
def tmux_rename_window(new_name: str, target_window: str = None) -> str:
    """
    Renames a tmux window.
    
    Args:
        new_name: The new name for the window.
        target_window: Optional target window (e.g., '1', 'mysession:1', 'current'). 
                       Defaults to current window if omitted.
    """
    args = ["rename-window"]
    if target_window:
        args.extend(["-t", target_window])
    args.append(new_name)
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Renamed window to '{new_name}'"

@mcp.tool()
def tmux_send_keys(keys: str, target_pane: str = None) -> str:
    """
    Sends keys to a specific tmux pane.
    
    Args:
        keys: The string of keys to send (e.g., 'ls Enter', 'C-c').
        target_pane: Optional target pane (e.g., '1', '1.0'). 
                     Defaults to current pane if omitted.
    """
    args = ["send-keys"]
    if target_pane:
        args.extend(["-t", target_pane])
    
    # Split keys by space to handle multiple keys/modifiers like "C-c Enter"
    # But preserve quoted strings if possible? Simple split is standard for tmux send-keys
    args.extend(shlex.split(keys))
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Sent keys to pane {target_pane or 'current'}"

@mcp.tool()
def tmux_get_active_session_info() -> str:
    """Returns information about the current active tmux session."""
    return run_tmux_command(["display-message", "-p", "Session: #S, Window: #I (#W), Pane: #P"])

if __name__ == "__main__":
    mcp.run(show_banner=False)
