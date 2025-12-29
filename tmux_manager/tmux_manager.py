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

@mcp.tool()
def tmux_capture_pane(target_pane: str = None, start_line: str = None, end_line: str = None) -> str:
    """
    Captures text content from a tmux pane.
    
    Args:
        target_pane: Optional target pane (e.g., '1', '1.0', '%2'). 
                     Defaults to current pane if omitted.
        start_line: Optional start line offset (e.g., '-100' for last 100 lines).
        end_line: Optional end line offset.
    """
    args = ["capture-pane", "-p"]
    if target_pane:
        args.extend(["-t", target_pane])
    if start_line is not None:
        args.extend(["-S", str(start_line)])
    if end_line is not None:
        args.extend(["-E", str(end_line)])
        
    return run_tmux_command(args)

@mcp.tool()
def tmux_split_window(target_pane: str = None, direction: str = "vertical", command: str = None) -> str:
    """
    Splits a window into two panes.
    
    Args:
        target_pane: Optional target pane to split. Defaults to current.
        direction: 'vertical' (top/bottom) or 'horizontal' (left/right). Default: vertical.
        command: Optional shell command to run in the new pane.
    """
    args = ["split-window"]
    if direction == "horizontal":
        args.append("-h")
    else:
        args.append("-v")
        
    if target_pane:
        args.extend(["-t", target_pane])
        
    if command:
        # If a command is provided, we pass it as a shell command to ensure it stays open if needed,
        # but standard behavior is just to run it.
        # Unlike new_window, split-window accepts command as final args.
        args.append(command)
        
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return "Split window successfully"

@mcp.tool()
def tmux_select_window(target_window: str) -> str:
    """
    Selects (switches to) a specific window.
    
    Args:
        target_window: Target window identifier (e.g., '1', 'mysession:2', 'mywindow').
    """
    return run_tmux_command(["select-window", "-t", target_window])

@mcp.tool()
def tmux_select_pane(target_pane: str) -> str:
    """
    Selects (focuses) a specific pane.
    
    Args:
        target_pane: Target pane identifier (e.g., '0', '%1').
    """
    return run_tmux_command(["select-pane", "-t", target_pane])

@mcp.tool()
def tmux_kill_window(target_window: str) -> str:
    """
    Kills (closes) a specific window.
    
    Args:
        target_window: Target window identifier.
    """
    return run_tmux_command(["kill-window", "-t", target_window])

@mcp.tool()
def tmux_kill_pane(target_pane: str = None) -> str:
    """
    Kills (closes) a specific pane.
    
    Args:
        target_pane: Optional target pane identifier. Defaults to current pane.
    """
    args = ["kill-pane"]
    if target_pane:
        args.extend(["-t", target_pane])
    return run_tmux_command(args)

if __name__ == "__main__":
    mcp.run(show_banner=False)
