#!/usr/bin/env python3
"""
OpenConvert Agents Launcher (Python version)
Launches all or specific OpenConvert service agents in the background

Usage:
    python launch_agents.py start [category] [--host HOST] [--port PORT]
    python launch_agents.py stop [category]
    python launch_agents.py status
    python launch_agents.py restart [category] [--host HOST] [--port PORT]
    python launch_agents.py logs [category]

Categories: archive, audio, code, doc, image, model, video
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
SERVICE_SCRIPT = PROJECT_ROOT / "service" / "run_agent.py"
PID_DIR = SCRIPT_DIR / "pids"
LOG_DIR = SCRIPT_DIR / "logs"

# Network configuration - using the updated default network address
DEFAULT_HOST = "network.openconvert.ai"
DEFAULT_PORT = 8765

# All supported categories
ALL_CATEGORIES = ["archive", "audio", "code", "doc", "image", "model", "video"]

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(color: str, message: str):
    """Print colored output."""
    print(f"{color}{message}{Colors.NC}")

def ensure_directories():
    """Create necessary directories."""
    PID_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

def get_pid_file(category: str) -> Path:
    """Get PID file path for a category."""
    return PID_DIR / f"{category}_agent.pid"

def get_log_file(category: str) -> Path:
    """Get log file path for a category."""
    return LOG_DIR / f"{category}_agent.log"

def is_agent_running(category: str) -> bool:
    """Check if agent is running."""
    pid_file = get_pid_file(category)
    
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            # Check if process is still running
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            # PID file exists but process is dead
            pid_file.unlink(missing_ok=True)
            return False
    return False

def start_agent(category: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> bool:
    """Start a single agent."""
    if is_agent_running(category):
        print_color(Colors.YELLOW, f"⚠️  {category} agent is already running")
        return False
    
    print_color(Colors.BLUE, f"🚀 Starting {category} agent on {host}:{port}...")
    
    pid_file = get_pid_file(category)
    log_file = get_log_file(category)
    
    # Start agent in background
    try:
        cmd = [
            sys.executable,
            str(SERVICE_SCRIPT),
            category,
            "--host", host,
            "--port", str(port)
        ]
        
        with log_file.open('w') as log:
            process = subprocess.Popen(
                cmd,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True  # Detach from parent
            )
        
        # Save PID to file
        pid_file.write_text(str(process.pid))
        
        # Wait a moment and check if it's still running
        time.sleep(2)
        if process.poll() is None:
            print_color(Colors.GREEN, f"✅ {category} agent started (PID: {process.pid})")
            return True
        else:
            print_color(Colors.RED, f"❌ Failed to start {category} agent")
            pid_file.unlink(missing_ok=True)
            return False
    
    except Exception as e:
        print_color(Colors.RED, f"❌ Error starting {category} agent: {e}")
        pid_file.unlink(missing_ok=True)
        return False

def stop_agent(category: str) -> bool:
    """Stop a single agent."""
    if not is_agent_running(category):
        print_color(Colors.YELLOW, f"⚠️  {category} agent is not running")
        return False
    
    pid_file = get_pid_file(category)
    pid = int(pid_file.read_text().strip())
    
    print_color(Colors.BLUE, f"🛑 Stopping {category} agent (PID: {pid})...")
    
    try:
        # Send SIGTERM first
        os.kill(pid, signal.SIGTERM)
        
        # Wait up to 5 seconds for graceful shutdown
        for i in range(5):
            try:
                os.kill(pid, 0)  # Check if still running
                time.sleep(1)
            except OSError:
                break
        
        # Force kill if still running
        try:
            os.kill(pid, 0)
            print_color(Colors.YELLOW, f"Force killing {category} agent...")
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        
        pid_file.unlink(missing_ok=True)
        print_color(Colors.GREEN, f"✅ {category} agent stopped")
        return True
        
    except OSError:
        print_color(Colors.RED, f"❌ Failed to stop {category} agent")
        pid_file.unlink(missing_ok=True)
        return False

def show_status(category: str):
    """Show agent status."""
    if is_agent_running(category):
        pid = int(get_pid_file(category).read_text().strip())
        print_color(Colors.GREEN, f"✅ {category} agent: RUNNING (PID: {pid})")
    else:
        print_color(Colors.RED, f"❌ {category} agent: STOPPED")

def start_all(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> int:
    """Start all agents."""
    print_color(Colors.BLUE, f"🚀 Starting all OpenConvert agents on {host}:{port}...")
    success_count = 0
    
    for category in ALL_CATEGORIES:
        if start_agent(category, host, port):
            success_count += 1
    
    print_color(Colors.GREEN, f"✅ Started {success_count}/{len(ALL_CATEGORIES)} agents")
    return success_count

def stop_all() -> int:
    """Stop all agents."""
    print_color(Colors.BLUE, "🛑 Stopping all OpenConvert agents...")
    success_count = 0
    
    for category in ALL_CATEGORIES:
        if stop_agent(category):
            success_count += 1
    
    print_color(Colors.GREEN, f"✅ Stopped {success_count} agents")
    return success_count

def show_all_status():
    """Show status of all agents."""
    print_color(Colors.BLUE, "📊 OpenConvert Agents Status:")
    print(f"Host: {DEFAULT_HOST}:{DEFAULT_PORT}")
    print(f"PID Directory: {PID_DIR}")
    print(f"Log Directory: {LOG_DIR}")
    print()
    
    for category in ALL_CATEGORIES:
        show_status(category)

def restart_agents(category: Optional[str] = None, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """Restart agents."""
    if category:
        print_color(Colors.BLUE, f"🔄 Restarting {category} agent...")
        stop_agent(category)
        time.sleep(1)
        start_agent(category, host, port)
    else:
        print_color(Colors.BLUE, "🔄 Restarting all agents...")
        stop_all()
        time.sleep(2)
        start_all(host, port)

def show_logs(category: Optional[str] = None):
    """Show logs for category or list all log files."""
    if category:
        log_file = get_log_file(category)
        if log_file.exists():
            print_color(Colors.BLUE, f"📄 Showing logs for {category} agent:")
            try:
                # Use tail -f equivalent
                subprocess.run(['tail', '-f', str(log_file)])
            except KeyboardInterrupt:
                pass
        else:
            print_color(Colors.RED, f"❌ Log file not found: {log_file}")
    else:
        print_color(Colors.BLUE, "📄 Available log files:")
        log_files = list(LOG_DIR.glob("*.log"))
        if log_files:
            for log_file in log_files:
                print(f"  {log_file.name}")
        else:
            print_color(Colors.YELLOW, "No log files found")

def validate_category(category: Optional[str]):
    """Validate category if provided."""
    if category and category not in ALL_CATEGORIES:
        print_color(Colors.RED, f"❌ Invalid category: {category}")
        print(f"Valid categories: {', '.join(ALL_CATEGORIES)}")
        sys.exit(1)

def main():
    """Main function."""
    ensure_directories()
    
    parser = argparse.ArgumentParser(
        description="OpenConvert Agents Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python {Path(__file__).name} start                    # Start all agents with default network
  python {Path(__file__).name} start image              # Start only image agent
  python {Path(__file__).name} start doc --host localhost --port 8765  # Start doc agent on localhost:8765
  python {Path(__file__).name} stop                     # Stop all agents
  python {Path(__file__).name} stop image               # Stop only image agent
  python {Path(__file__).name} status                   # Show status of all agents
  python {Path(__file__).name} logs doc                 # Show logs for doc agent

Categories: {', '.join(ALL_CATEGORIES)}
Default network: {DEFAULT_HOST}:{DEFAULT_PORT}
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start agents')
    start_parser.add_argument('category', nargs='?', choices=ALL_CATEGORIES, help='Specific category to start')
    start_parser.add_argument('--host', default=DEFAULT_HOST, help=f'Network host (default: {DEFAULT_HOST})')
    start_parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'Network port (default: {DEFAULT_PORT})')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop agents')
    stop_parser.add_argument('category', nargs='?', choices=ALL_CATEGORIES, help='Specific category to stop')
    
    # Status command
    subparsers.add_parser('status', help='Show status of all agents')
    
    # Restart command
    restart_parser = subparsers.add_parser('restart', help='Restart agents')
    restart_parser.add_argument('category', nargs='?', choices=ALL_CATEGORIES, help='Specific category to restart')
    restart_parser.add_argument('--host', default=DEFAULT_HOST, help=f'Network host (default: {DEFAULT_HOST})')
    restart_parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'Network port (default: {DEFAULT_PORT})')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Show logs')
    logs_parser.add_argument('category', nargs='?', choices=ALL_CATEGORIES, help='Specific category to show logs for')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'start':
        if args.category:
            start_agent(args.category, args.host, args.port)
        else:
            start_all(args.host, args.port)
    
    elif args.command == 'stop':
        if args.category:
            stop_agent(args.category)
        else:
            stop_all()
    
    elif args.command == 'status':
        show_all_status()
    
    elif args.command == 'restart':
        restart_agents(args.category, args.host, args.port)
    
    elif args.command == 'logs':
        show_logs(args.category)

if __name__ == "__main__":
    main() 