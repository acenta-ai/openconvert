#!/usr/bin/env python3
"""
OpenConvert CLI Demo Script

This script demonstrates how to use the OpenConvert CLI tool.
It assumes you have an OpenConvert network running locally.

To run this demo:
1. Start the OpenConvert network: cd demos/openconvert && openagents launch-network network_config.yaml
2. Start a doc agent: cd demos/openconvert && python run_agent.py doc  
3. Run this demo: python demo.py
"""

import asyncio
import tempfile
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from client import OpenConvertClient

async def demo():
    """Run a simple demonstration of the OpenConvert CLI."""
    print("🧪 OpenConvert CLI Demo")
    print("=" * 50)
    
    # Create a test input file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello, OpenConvert!\n\nThis is a test document.\n\n")
        f.write("Features:\n")
        f.write("- File conversion\n")
        f.write("- Network discovery\n") 
        f.write("- Multi-format support\n")
        input_file = Path(f.name)
    
    print(f"📄 Created test file: {input_file}")
    
    # Set up output file
    output_file = input_file.with_suffix('.md')
    
    try:
        # Create client and connect
        client = OpenConvertClient()
        print(f"🌐 Connecting to OpenConvert network...")
        
        connected = await client.connect(host="localhost", port=8765)
        if not connected:
            print("❌ Failed to connect to network. Make sure the OpenConvert network is running.")
            print("   Start with: cd demos/openconvert && openagents launch-network network_config.yaml")
            return False
        
        print("✅ Connected to network")
        
        # Test agent discovery
        print("🔍 Discovering agents for txt -> md conversion...")
        agents = await client.discover_agents("text/plain", "text/markdown")
        
        if not agents:
            print("❌ No agents found for txt -> md conversion.")
            print("   Start a doc agent with: cd demos/openconvert && python run_agent.py doc")
            return False
        
        print(f"📋 Found {len(agents)} agent(s):")
        for agent in agents:
            print(f"   - {agent.get('agent_id', 'Unknown')}")
        
        # Test file conversion
        print("🔄 Converting file...")
        success = await client.convert_file(
            input_file=input_file,
            output_file=output_file, 
            source_format="text/plain",
            target_format="text/markdown"
        )
        
        if success:
            print("✅ Conversion successful!")
            print(f"📄 Output file: {output_file}")
            
            # Show the converted content
            if output_file.exists():
                content = output_file.read_text()
                print("\n📖 Converted content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
            
            return True
        else:
            print("❌ Conversion failed")
            return False
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
        
    finally:
        # Clean up
        if 'client' in locals():
            await client.disconnect()
        
        # Remove test files
        if input_file.exists():
            input_file.unlink()
        if output_file.exists():
            output_file.unlink()
        
        print("🧹 Cleaned up test files")

def main():
    """Main demo function."""
    try:
        success = asyncio.run(demo())
        if success:
            print("\n🎉 Demo completed successfully!")
            print("\nTry the CLI tool:")
            print("  openconvert -i document.txt -o document.md")
            return 0
        else:
            print("\n❌ Demo failed. Check network setup and try again.")
            return 1
    except KeyboardInterrupt:
        print("\n🛑 Demo cancelled by user")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 