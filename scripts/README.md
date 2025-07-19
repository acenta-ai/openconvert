# OpenConvert Agent Launchers

This directory contains scripts to launch and manage OpenConvert service agents in the background.

## Scripts

### 🚀 `launch_agents.sh` (Bash version)
Bash script for launching all OpenConvert agents or specific categories.

### 🐍 `launch_agents.py` (Python version)  
Python script with the same functionality as the bash version.

## Supported Agent Categories

The OpenConvert service supports the following file conversion categories:

- **archive**: zip, rar, 7z, tar, gz
- **audio**: mp3, wav, ogg, flac, aac  
- **code**: json, yaml, xml, html, md, latex
- **doc**: txt, docx, pdf, html, md, rtf, csv, xlsx, epub
- **image**: png, jpg, jpeg, bmp, tiff, gif, ico, svg, webp
- **model**: stl, obj, fbx, ply, glb
- **video**: mp4, avi, mkv, mov, gif, webm

## Usage

### Bash Script

```bash
# Start all agents
./launch_agents.sh start

# Start specific agent
./launch_agents.sh start image

# Start agent with custom network
./launch_agents.sh start doc localhost 8765

# Stop all agents
./launch_agents.sh stop

# Stop specific agent
./launch_agents.sh stop image

# Show status of all agents
./launch_agents.sh status

# Restart all agents
./launch_agents.sh restart

# Restart specific agent
./launch_agents.sh restart doc

# Show logs for specific agent
./launch_agents.sh logs image

# Show available log files
./launch_agents.sh logs

# Show help
./launch_agents.sh help
```

### Python Script

```bash
# Start all agents
python launch_agents.py start

# Start specific agent
python launch_agents.py start image

# Start agent with custom network
python launch_agents.py start doc --host localhost --port 8765

# Stop all agents
python launch_agents.py stop

# Stop specific agent
python launch_agents.py stop image

# Show status of all agents
python launch_agents.py status

# Restart all agents
python launch_agents.py restart

# Restart specific agent
python launch_agents.py restart doc

# Show logs for specific agent
python launch_agents.py logs image

# Show help
python launch_agents.py --help
```

## Network Configuration

**Default Network**: `network.openconvert.ai:8765`

Both scripts use the production OpenConvert network by default. You can override this with:

- **Bash**: `./launch_agents.sh start [category] [host] [port]`
- **Python**: `python launch_agents.py start [category] --host HOST --port PORT`

## File Structure

When you run the launchers, they create the following directory structure:

```
scripts/
├── launch_agents.sh      # Bash launcher script
├── launch_agents.py      # Python launcher script  
├── README.md            # This file
├── pids/                # PID files for running agents
│   ├── archive_agent.pid
│   ├── audio_agent.pid
│   ├── ...
└── logs/                # Log files for agents
    ├── archive_agent.log
    ├── audio_agent.log
    └── ...
```

## Process Management

### Starting Agents
- Each agent runs in the background as a separate process
- PID files are stored in `scripts/pids/`
- Log output is redirected to `scripts/logs/`
- Agents automatically connect to the OpenConvert network

### Stopping Agents
- Scripts first send SIGTERM for graceful shutdown
- If the process doesn't stop within 5 seconds, SIGKILL is used
- PID files are automatically cleaned up

### Status Checking
- Scripts check if processes are actually running, not just PID file existence
- Dead processes are automatically detected and PID files cleaned up

## Requirements

### For service/run_agent.py to work:
- Python 3.7+
- `openagents` package (for network communication)
- `agconvert` package (for actual file conversions, optional for testing)

### For launcher scripts:
- **Bash script**: bash shell, standard Unix tools (kill, nohup, etc.)
- **Python script**: Python 3.7+, no additional packages

## Troubleshooting

### Check Agent Status
```bash
./launch_agents.sh status
# or
python launch_agents.py status
```

### View Agent Logs
```bash
./launch_agents.sh logs [category]
# or  
python launch_agents.py logs [category]
```

### Common Issues

1. **Port already in use**: Check if another service is using port 8765
2. **Permission denied**: Make sure scripts are executable (`chmod +x`)
3. **Python module not found**: Install required packages (`openagents`, `agconvert`)
4. **Network connection failed**: Verify `network.openconvert.ai` is accessible

### Force Stop All Agents
If normal stop doesn't work:

```bash
# Kill all python processes running run_agent.py
pkill -f "run_agent.py"

# Clean up PID files
rm -f scripts/pids/*.pid
```

## Development

The launcher scripts are designed to work with the OpenConvert service architecture:

- Each agent specializes in one file category
- Agents communicate via the OpenAgents protocol
- Discovery and messaging adapters handle network communication
- Background processes enable scalable service deployment

For more information about the OpenConvert service architecture, see `service/README.md`. 