#!/bin/bash

# OpenConvert Agents Launcher
# Launches all or specific OpenConvert service agents in the background
# 
# Usage:
#   ./launch_agents.sh start [category]    - Start all agents or specific category
#   ./launch_agents.sh stop [category]     - Stop all agents or specific category  
#   ./launch_agents.sh status              - Show status of all agents
#   ./launch_agents.sh restart [category]  - Restart all agents or specific category
#
# Categories: archive, audio, code, doc, image, model, video

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SERVICE_SCRIPT="$PROJECT_ROOT/service/run_agent.py"
PID_DIR="$SCRIPT_DIR/pids"
LOG_DIR="$SCRIPT_DIR/logs"

# Network configuration - using the updated default network address
DEFAULT_HOST="network.openconvert.ai"
DEFAULT_PORT="8765"

# All supported categories
ALL_CATEGORIES=("archive" "audio" "code" "doc" "image" "model" "video")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create necessary directories
mkdir -p "$PID_DIR" "$LOG_DIR"

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if agent is running
is_agent_running() {
    local category=$1
    local pid_file="$PID_DIR/${category}_agent.pid"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # Running
        else
            # PID file exists but process is dead
            rm -f "$pid_file"
            return 1  # Not running
        fi
    fi
    return 1  # Not running
}

# Function to start a single agent
start_agent() {
    local category=$1
    local host=${2:-$DEFAULT_HOST}
    local port=${3:-$DEFAULT_PORT}
    
    if is_agent_running "$category"; then
        print_color $YELLOW "⚠️  $category agent is already running"
        return 1
    fi
    
    print_color $BLUE "🚀 Starting $category agent on $host:$port..."
    
    local pid_file="$PID_DIR/${category}_agent.pid"
    local log_file="$LOG_DIR/${category}_agent.log"
    
    # Start agent in background and capture PID
    nohup python3 "$SERVICE_SCRIPT" "$category" --host "$host" --port "$port" \
        > "$log_file" 2>&1 &
    local pid=$!
    
    # Save PID to file
    echo $pid > "$pid_file"
    
    # Wait a moment and check if it's still running
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        print_color $GREEN "✅ $category agent started (PID: $pid)"
        return 0
    else
        print_color $RED "❌ Failed to start $category agent"
        rm -f "$pid_file"
        return 1
    fi
}

# Function to stop a single agent
stop_agent() {
    local category=$1
    local pid_file="$PID_DIR/${category}_agent.pid"
    
    if ! is_agent_running "$category"; then
        print_color $YELLOW "⚠️  $category agent is not running"
        return 1
    fi
    
    local pid=$(cat "$pid_file")
    print_color $BLUE "🛑 Stopping $category agent (PID: $pid)..."
    
    # Send SIGTERM first, then SIGKILL if needed
    if kill "$pid" 2>/dev/null; then
        # Wait up to 5 seconds for graceful shutdown
        for i in {1..5}; do
            if ! kill -0 "$pid" 2>/dev/null; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            print_color $YELLOW "Force killing $category agent..."
            kill -9 "$pid" 2>/dev/null || true
        fi
        
        rm -f "$pid_file"
        print_color $GREEN "✅ $category agent stopped"
        return 0
    else
        print_color $RED "❌ Failed to stop $category agent"
        rm -f "$pid_file"
        return 1
    fi
}

# Function to show agent status
show_status() {
    local category=$1
    
    if is_agent_running "$category"; then
        local pid=$(cat "$PID_DIR/${category}_agent.pid")
        print_color $GREEN "✅ $category agent: RUNNING (PID: $pid)"
    else
        print_color $RED "❌ $category agent: STOPPED"
    fi
}

# Function to start all agents
start_all() {
    local host=${1:-$DEFAULT_HOST}
    local port=${2:-$DEFAULT_PORT}
    
    print_color $BLUE "🚀 Starting all OpenConvert agents on $host:$port..."
    local success_count=0
    
    for category in "${ALL_CATEGORIES[@]}"; do
        if start_agent "$category" "$host" "$port"; then
            ((success_count++))
        fi
    done
    
    print_color $GREEN "✅ Started $success_count/${#ALL_CATEGORIES[@]} agents"
}

# Function to stop all agents
stop_all() {
    print_color $BLUE "🛑 Stopping all OpenConvert agents..."
    local success_count=0
    
    for category in "${ALL_CATEGORIES[@]}"; do
        if stop_agent "$category"; then
            ((success_count++))
        fi
    done
    
    print_color $GREEN "✅ Stopped $success_count agents"
}

# Function to show status of all agents
show_all_status() {
    print_color $BLUE "📊 OpenConvert Agents Status:"
    echo "Host: $DEFAULT_HOST:$DEFAULT_PORT"
    echo "PID Directory: $PID_DIR"
    echo "Log Directory: $LOG_DIR"
    echo ""
    
    for category in "${ALL_CATEGORIES[@]}"; do
        show_status "$category"
    done
}

# Function to restart agents
restart_agents() {
    local category=$1
    local host=${2:-$DEFAULT_HOST}
    local port=${3:-$DEFAULT_PORT}
    
    if [[ -n "$category" ]]; then
        print_color $BLUE "🔄 Restarting $category agent..."
        stop_agent "$category" || true
        sleep 1
        start_agent "$category" "$host" "$port"
    else
        print_color $BLUE "🔄 Restarting all agents..."
        stop_all
        sleep 2
        start_all "$host" "$port"
    fi
}

# Function to show usage
show_usage() {
    echo "OpenConvert Agents Launcher"
    echo ""
    echo "Usage:"
    echo "  $0 start [category] [host] [port]    - Start all agents or specific category"
    echo "  $0 stop [category]                   - Stop all agents or specific category"  
    echo "  $0 status                            - Show status of all agents"
    echo "  $0 restart [category] [host] [port]  - Restart all agents or specific category"
    echo "  $0 logs [category]                   - Show logs for category (or all if not specified)"
    echo ""
    echo "Categories: ${ALL_CATEGORIES[*]}"
    echo ""
    echo "Default network: $DEFAULT_HOST:$DEFAULT_PORT"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all agents with default network"
    echo "  $0 start image              # Start only image agent" 
    echo "  $0 start doc localhost 8765 # Start doc agent on localhost:8765"
    echo "  $0 stop                     # Stop all agents"
    echo "  $0 stop image               # Stop only image agent"
    echo "  $0 status                   # Show status of all agents"
    echo "  $0 logs doc                 # Show logs for doc agent"
}

# Function to show logs
show_logs() {
    local category=$1
    
    if [[ -n "$category" ]]; then
        local log_file="$LOG_DIR/${category}_agent.log"
        if [[ -f "$log_file" ]]; then
            print_color $BLUE "📄 Showing logs for $category agent:"
            tail -f "$log_file"
        else
            print_color $RED "❌ Log file not found: $log_file"
        fi
    else
        print_color $BLUE "📄 Available log files:"
        ls -la "$LOG_DIR"/*.log 2>/dev/null || print_color $YELLOW "No log files found"
    fi
}

# Validate category if provided
validate_category() {
    local category=$1
    if [[ -n "$category" ]]; then
        if [[ ! " ${ALL_CATEGORIES[*]} " =~ " $category " ]]; then
            print_color $RED "❌ Invalid category: $category"
            echo "Valid categories: ${ALL_CATEGORIES[*]}"
            exit 1
        fi
    fi
}

# Main command processing
case "${1:-}" in
    "start")
        validate_category "$2"
        if [[ -n "$2" ]]; then
            start_agent "$2" "$3" "$4"
        else
            start_all "$2" "$3"
        fi
        ;;
    "stop")
        validate_category "$2"
        if [[ -n "$2" ]]; then
            stop_agent "$2"
        else
            stop_all
        fi
        ;;
    "status")
        show_all_status
        ;;
    "restart")
        validate_category "$2"
        restart_agents "$2" "$3" "$4"
        ;;
    "logs")
        validate_category "$2"
        show_logs "$2"
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        print_color $RED "❌ Invalid command: ${1:-}"
        echo ""
        show_usage
        exit 1
        ;;
esac 