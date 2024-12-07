"""
Editor Functions
"""

import sys
import os
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix-like systems
    import tty
    import termios

def _get_key(self):
    """Get a single keypress from the user."""
    if os.name == 'nt':  # Windows
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # Special keys
                    key = msvcrt.getch()
                    if key == b'H':
                        return 'up'
                    elif key == b'P':
                        return 'down'
                elif key == b'\r':
                    return 'enter'
                elif key == b'q':
                    return 'q'
                return key.decode('utf-8')
    else:  # Unix-like systems
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Escape sequence
                # Read the next two characters that make up the arrow key code
                ch = sys.stdin.read(1)
                if ch == '[':
                    ch = sys.stdin.read(1)
                    if ch == 'A':
                        return 'up'
                    elif ch == 'B':
                        return 'down'
            elif ch == '\r':
                return 'enter'
            elif ch == 'q':
                return 'q'
            return ch.decode() if isinstance(ch, bytes) else ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def _clear_lines(n):
    """Clear n lines from the terminal."""
    for _ in range(n):
        sys.stdout.write('\033[F')  # Move cursor up
        sys.stdout.write('\033[K')  # Clear line

def _select_session(sessions, action_name="select"):
    """
    Interactive session selector using arrow keys.
    
    Parameters
    ----------
    sessions : list
        List of session dictionaries from listRemoteDevelopment
    action_name : str
        Name of the action (e.g., "stop" or "delete") for display purposes
        
    Returns
    -------
    str or None
        Selected session ID or None if cancelled
    """
    if not sessions:
        print(f"\n❌ No sessions available to {action_name}")
        return None

    current_selection = None
    last_displayed_lines = 0

    def display_sessions():
        nonlocal last_displayed_lines
        if last_displayed_lines > 0:
            _clear_lines(last_displayed_lines)
        
        print(f"\n📝 Use arrow keys (↑/↓) to {action_name} a session, Enter to confirm, q to quit:\n")
        
        for i, session in enumerate(sessions):
            is_selected = current_selection is not None and i == current_selection
            session_line = (
                f"  {'▶' if is_selected else ' '} "
                f"{session['editorSessionId']}: "
                f"{session['editorUrl']} "
                f"({session['status']['state']})"
            )
            if is_selected:
                print(f"\033[44m{session_line}\033[0m")
            else:
                print(session_line)
        
        last_displayed_lines = len(sessions) + 3

    display_sessions()

    while True:
        key = _get_key(None)
        if key == 'up':
            if current_selection is None:
                current_selection = len(sessions) - 1
            else:
                current_selection = max(0, current_selection - 1)
            display_sessions()
        elif key == 'down':
            if current_selection is None:
                current_selection = 0
            else:
                current_selection = min(len(sessions) - 1, current_selection + 1)
            display_sessions()
        elif key == 'enter':
            if current_selection is not None:
                return sessions[current_selection]['editorSessionId']
        elif key == 'q':
            if last_displayed_lines > 0:
                _clear_lines(last_displayed_lines)
            print("\n❌ Session selection cancelled")
            return None

def _spinner_animation():
    """Generator for a simple spinner animation."""
    while True:
        for char in '|/-\\':
            yield char

def _show_operation_status(operation):
    """Show a loading spinner while an operation is in progress."""
    import threading
    import time

    stop_thread = threading.Event()
    spinner = _spinner_animation()

    def spin():
        while not stop_thread.is_set():
            sys.stdout.write(f"\r⏳ {next(spinner)} {operation}...")
            sys.stdout.flush()
            time.sleep(0.1)

        sys.stdout.write('\r\033[K')
        sys.stdout.write('\n')
        sys.stdout.flush()

    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    return stop_thread, spinner_thread

def create_remote_development(self, channelId, organizationId=None, channelVersion=None, instanceType=None):
    """
    Creates a remote development environment.

    This method initiates a remote development session on the specified channel, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.

    Parameters
    ----------
    channelId : str
        The ID of the channel to use for creating the remote development session.
    channelVersion : str, optional
        The version of the channel to use. If not provided, defaults to the latest version.
    organizationId : str, optional
        The ID of the organization where the session will be created. 
        If not provided, defaults to the user's organization.
    instanceType : str, optional
        The type of instance to use for the remote development session.
        If not provided, defaults to the instance type specified in the channel.

    Returns
    -------
    str
        A message indicating that the session is being created, along with a link to access the session.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.createRemoteDevelopment` to initiate the session.
    - Displays a warning message indicating that the feature is experimental.

    Example Output
    --------------
    ⚠️ Warning: This feature is very experimental. Use with caution! ⚠️
    🚀 Your environment will be available here shortly: 🔗 <editorUrl> 🌐
    """
    if self.check_logout():
        return

    session = self.ana_api.createRemoteDevelopment(
        organizationId=organizationId, 
        channelId=channelId, 
        channelVersion=channelVersion,
        instanceType=instanceType
    )

    print(
        "\n⚠️ Warning: This feature is very experimental. Use with caution! ⚠️\n"
        f"🚀 Your environment will be available here shortly: "
        f"🔗 {session['editorUrl']} 🌐\n"
    )

def delete_remote_development(self, editorSessionId=None, organizationId=None):
    """
    Deletes a remote development session.

    This method removes a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.
    If no editorSessionId is provided, it will show a list of active sessions and prompt for selection.

    Parameters
    ----------
    editorSessionId : str, optional
        The ID of the editor session to be deleted. If not provided, will prompt for selection.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session deletion.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.deleteRemoteDevelopment` to perform the deletion.
    - Use arrow keys (↑/↓) to select a session, Enter to confirm, q to quit
    """
    if self.check_logout():
        return

    if editorSessionId is None:
        sessions = self.ana_api.listRemoteDevelopment(organizationId=None)
        editorSessionId = _select_session(sessions, action_name="delete")
        if editorSessionId is None:
            return

    spinner_stop_event, spinner_thread = _show_operation_status(f"Deleting Development Session {editorSessionId}")
    try:
        session = self.ana_api.deleteRemoteDevelopment(
            organizationId=organizationId,
            editorSessionId=editorSessionId
        )
    finally:
        spinner_stop_event.set()
        spinner_thread.join()
    print(f"\n🗑️  Successfully deleted Development Session {editorSessionId}\n")


def list_remote_development(self, organizationId=None): 
    """Shows all the active development sessions in the organization.
    
    Parameters
    ----------
    organizationId : str
        The ID of the organization to list the active development sessions.
    
    Returns
    -------
    list[dict]
        If organizationId is not provided, returns all active sessions in organizations that user has access to.
        If organizationId is provided, returns active sessions in that specific organization.
    """
    if self.check_logout():
        return

    sessions = self.ana_api.listRemoteDevelopment(organizationId=organizationId)

    if not sessions:
        print("✨ No active development sessions found. Use `create_remote_development` to start a new session.")
        return sessions
    
    if organizationId is None:
        print("\n🚧 Active Development Sessions:\n")
    else:
        print(f"\n🚧 Active Development Sessions in Organization {organizationId}:\n")

    for session in sessions:
        print(
            f"  🆔 {session['editorSessionId']}: "
            f"🏢 {session['organization'][:15]} "
            f"🔗 {session['editorUrl']} "
            f"📦 {session['channel']} "
            f"📟 {session['instanceType']} "
            f"📊 Status: {session['status']['state']}"
        )

def stop_remote_development(self, editorSessionId=None, organizationId=None):
    """
    Stops a remote development session.

    This method stops a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.
    If no editorSessionId is provided, it will show a list of active sessions and prompt for selection.

    Parameters
    ----------
    editorSessionId : str, optional
        The ID of the editor session to be stopped. If not provided, will prompt for selection.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session stop operation.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.stopRemoteDevelopment` to stop the session.
    - Use arrow keys (↑/↓) to select a session, Enter to confirm, q to quit
    - Only shows sessions that are currently running or resuming
    """
    if self.check_logout():
        return

    if editorSessionId is None:
        sessions = self.ana_api.listRemoteDevelopment(organizationId=None)
        active_sessions = [s for s in sessions if s['status']['state'] in ('RUNNING', 'RESUMING')]
        if not active_sessions and sessions:
            print("✨ No active sessions available to stop.")
            return
        editorSessionId = _select_session(active_sessions, action_name="stop")
        if editorSessionId is None:
            return

    spinner_stop_event, spinner_thread = _show_operation_status(f"Stopping Development Session {editorSessionId}")
    try:
        session = self.ana_api.stopRemoteDevelopment(
            organizationId=organizationId,
            editorSessionId=editorSessionId
        )
    finally:
        spinner_stop_event.set()
        spinner_thread.join()
    print(f"\n🛑 Successfully stopped Development Session {editorSessionId}\n")

def start_remote_development(self, editorSessionId=None, organizationId=None):
    """
    Starts a remote development session.

    This method starts a specific editor session, optionally within a given organization.
    If no organizationId is provided, it defaults to the organization associated with the current user.
    If no editorSessionId is provided, it will show a list of stopped sessions and prompt for selection.

    Parameters
    ----------
    editorSessionId : str, optional
        The ID of the editor session to be started. If not provided, will prompt for selection.
    organizationId : str, optional
        The ID of the organization where the editor session is running.
        If not provided, defaults to the user's organization.

    Returns
    -------
    dict
        A dictionary representing the result of the session start operation.

    Notes
    -----
    - This function checks if the user is logged out before proceeding.
    - Calls `ana_api.startRemoteDevelopment` to start the session.
    - Use arrow keys (↑/↓) to select a session, Enter to confirm, q to quit
    - Only shows sessions that are currently stopped
    """
    if self.check_logout():
        return

    if editorSessionId is None:
        sessions = self.ana_api.listRemoteDevelopment(organizationId=None)
        stopped_sessions = [s for s in sessions if s['status']['state'] == 'STOPPED']
        if not stopped_sessions and sessions:
            print("✨ No stopped sessions available to start.")
            return
        editorSessionId = _select_session(stopped_sessions, action_name="start")
        if editorSessionId is None:
            return

    spinner_stop_event, spinner_thread = _show_operation_status(f"Starting Development Session {editorSessionId}")
    try:
        session = self.ana_api.startRemoteDevelopment(
            organizationId=organizationId,
            editorSessionId=editorSessionId
        )
    finally:
        spinner_stop_event.set()
        spinner_thread.join()
    print(
        f"\n🚀 Successfully started Development Session {editorSessionId}\n"
        f"🔗 Your environment will be available here shortly: {session['editorUrl']} 🌐\n"
    )
