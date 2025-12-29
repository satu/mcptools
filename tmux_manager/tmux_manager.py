#!/usr/bin/env python3
import os
import subprocess
import shlex
import atexit
from fastmcp import FastMCP

mcp = FastMCP("Tmux Manager")

MCP_SESSION_NAME = "mcptools-session"
CREATED_SESSION = False

def is_in_tmux() -> bool:
    """Checks if we are running inside a tmux session."""
    return os.environ.get("TMUX") is not None

def cleanup_session():
    """Cleanup the tmux session if we created it."""
    global CREATED_SESSION
    if CREATED_SESSION:
        try:
            subprocess.run(
                ["tmux", "kill-session", "-t", MCP_SESSION_NAME],
                capture_output=True,
                check=False
            )
        except Exception:
            pass

atexit.register(cleanup_session)

def ensure_session():
    """Ensure the MCP tmux session exists if we are not in tmux."""
    global CREATED_SESSION
    
    # Check if session exists
    check = subprocess.run(
        ["tmux", "has-session", "-t", MCP_SESSION_NAME],
        capture_output=True
    )
    
    if check.returncode != 0:
        # Create it
        try:
            subprocess.run(
                ["tmux", "new-session", "-d", "-s", MCP_SESSION_NAME],
                check=True,
                capture_output=True
            )
            CREATED_SESSION = True
        except subprocess.CalledProcessError as e:
            # It might have been created concurrently or failed
            pass

def resolve_target(target: str = None) -> str:
    """
    Resolves a target string (window/pane) to a valid tmux target.
    If outside tmux, ensures it is qualified with the session name.
    
    Returns:
        The target string to use with -t, or None if no -t is needed (inside tmux with default target).
    """
    if is_in_tmux():
        return target
    
    ensure_session()
    
    if target:
        # If user explicitly gave a target
        if ":" in target:
            return target
        # Prepend session name
        return f"{MCP_SESSION_NAME}:{target}"
    else:
        # Default to the session's active context
        # Using colon ensures we target the session's active window/pane, not the session object itself
        # (though some commands accept session object, others need window/pane)
        return f"{MCP_SESSION_NAME}:"

def run_tmux_command(args: list[str]) -> str:
    """
    Executes a tmux command.
    Automatically handles session creation if outside tmux.
    """
    if not is_in_tmux():
        ensure_session()
    
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
    args = ["list-windows"]
    target = resolve_target()
    if target:
        args.extend(["-t", target])
        
    return run_tmux_command(args)

@mcp.tool()
def tmux_new_window(command: str, name: str = None, keep_open: bool = True) -> str:
    """
    Opens a new tmux window and runs the specified command.
    """
    args = ["new-window"]
    
    # Target resolution for new-window:
    # If we are outside, we MUST target our session.
    target = resolve_target()
    if target:
        args.extend(["-t", target])
        
    if name:
        args.extend(["-n", name])
    
    final_command = command
    if keep_open:
        final_command = f'{command}; echo "\n--------------------------------------------------"; echo "Command finished. Press Enter to close window..."; read'
    
    args.append(final_command)
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Started command in new window{' ' + name if name else ''}: {command}"

@mcp.tool()
def tmux_rename_window(new_name: str, target_window: str = None) -> str:
    """Renames a tmux window."""
    args = ["rename-window"]
    real_target = resolve_target(target_window)
    if real_target:
        args.extend(["-t", real_target])
        
    args.append(new_name)
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Renamed window to '{new_name}'"

@mcp.tool()
def tmux_send_keys(keys: str, target_pane: str = None) -> str:
    """Sends keys to a specific tmux pane."""
    args = ["send-keys"]
    real_target = resolve_target(target_pane)
    if real_target:
        args.extend(["-t", real_target])
    
    args.extend(shlex.split(keys))
    
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return f"Sent keys to pane {target_pane or 'current'}"

@mcp.tool()
def tmux_get_active_session_info() -> str:
    """Returns information about the current active tmux session."""
    args = ["display-message", "-p"]
    target = resolve_target()
    if target:
        args.extend(["-t", target])
        
    args.append("Session: #S, Window: #I (#W), Pane: #P")
    return run_tmux_command(args)

@mcp.tool()
def tmux_capture_pane(target_pane: str = None, start_line: str = None, end_line: str = None) -> str:
    """Captures text content from a tmux pane."""
    args = ["capture-pane", "-p"]
    real_target = resolve_target(target_pane)
    if real_target:
        args.extend(["-t", real_target])
        
    if start_line is not None:
        args.extend(["-S", str(start_line)])
    if end_line is not None:
        args.extend(["-E", str(end_line)])
        
    return run_tmux_command(args)

@mcp.tool()
def tmux_split_window(target_pane: str = None, direction: str = "vertical", command: str = None) -> str:
    """Splits a window into two panes."""
    args = ["split-window"]
    if direction == "horizontal":
        args.append("-h")
    else:
        args.append("-v")
        
    real_target = resolve_target(target_pane)
    if real_target:
        args.extend(["-t", real_target])
        
    if command:
        args.append(command)
        
    output = run_tmux_command(args)
    if "Error" in output:
        return output
    return "Split window successfully"

@mcp.tool()
def tmux_select_window(target_window: str) -> str:
    """Selects (switches to) a specific window."""
    real_target = resolve_target(target_window)
    # resolve_target might return session name if target_window was somehow None, but here it's required.
    # But wait, if target_window is "1", resolve_target("1") -> "session:1". Correct.
    return run_tmux_command(["select-window", "-t", real_target])

@mcp.tool()
def tmux_select_pane(target_pane: str) -> str:
    """Selects (focuses) a specific pane."""
    real_target = resolve_target(target_pane)
    return run_tmux_command(["select-pane", "-t", real_target])

@mcp.tool()
def tmux_kill_window(target_window: str) -> str:
    """Kills (closes) a specific window."""
    real_target = resolve_target(target_window)
    return run_tmux_command(["kill-window", "-t", real_target])

@mcp.tool()
def tmux_kill_pane(target_pane: str = None) -> str:
    """Kills (closes) a specific pane."""
    args = ["kill-pane"]
    real_target = resolve_target(target_pane)
    if real_target:
        args.extend(["-t", real_target])
    return run_tmux_command(args)

if __name__ == "__main__":
    mcp.run(show_banner=False)