#!/usr/bin/env python3
"""
OpenConvert Client

Client class for connecting to the OpenConvert OpenAgents network,
discovering conversion agents, and performing file conversions.
"""

import asyncio
import logging
import base64
import tempfile
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import OpenAgents modules
import sys
import os

# Add openagents src to path
current_dir = Path(__file__).resolve().parent
openagents_root = current_dir.parent.parent
sys.path.insert(0, str(openagents_root / "src"))

from openagents.core.client import AgentClient
from openagents.protocols.discovery.openconvert_discovery.adapter import OpenConvertDiscoveryAdapter
from openagents.protocols.communication.simple_messaging.adapter import SimpleMessagingAgentAdapter
from openagents.models.messages import DirectMessage, BaseMessage

logger = logging.getLogger(__name__)


class OpenConvertClient:
    """Client for interacting with the OpenConvert OpenAgents network."""
    
    def __init__(self, agent_id: Optional[str] = None):
        """Initialize the OpenConvert client.
        
        Args:
            agent_id: Optional agent ID. If not provided, a random one will be generated.
        """
        self.agent_id = agent_id or f"openconvert-client-{uuid.uuid4().hex[:8]}"
        self.client = AgentClient(self.agent_id)
        self.discovery_adapter = OpenConvertDiscoveryAdapter()
        self.messaging_adapter = SimpleMessagingAgentAdapter()
        self.conversion_responses = {}
        self.connected = False
        
        logger.info(f"Initialized OpenConvert client with ID: {self.agent_id}")
    
    async def connect(self, host: str = "localhost", port: int = 8765) -> bool:
        """Connect to the OpenConvert network.
        
        Args:
            host: Network host to connect to
            port: Network port to connect to
            
        Returns:
            bool: True if connection successful
        """
        try:
            logger.info(f"Connecting to OpenConvert network at {host}:{port}")
            
            # Connect to the network
            success = await self.client.connect_to_server(
                host=host,
                port=port,
                metadata={
                    "name": "OpenConvert CLI Client",
                    "type": "conversion_client",
                    "capabilities": ["file_conversion_requests"],
                    "version": "1.0.0"
                }
            )
            
            if not success:
                logger.error("Failed to connect to OpenConvert network")
                return False
            
            # Register protocol adapters
            self.client.register_protocol_adapter(self.discovery_adapter)
            self.client.register_protocol_adapter(self.messaging_adapter)
            
            # Set up message handler for conversion responses
            self.messaging_adapter.register_message_handler("conversion_response", self._handle_conversion_response)
            
            self.connected = True
            logger.info("✅ Successfully connected to OpenConvert network")
            
            # Give some time for protocol registration
            await asyncio.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to network: {e}")
            return False
    
    def _handle_conversion_response(self, content: Dict[str, Any], sender_id: str) -> None:
        """Handle conversion response messages.
        
        Args:
            content: Message content
            sender_id: ID of the agent that sent the response
        """
        if content and (content.get("conversion_status") or content.get("action") == "conversion_result"):
            self.conversion_responses[sender_id] = content
            logger.debug(f"Received conversion response from {sender_id}")
    
    async def discover_agents(self, source_format: str, target_format: str) -> List[Dict[str, Any]]:
        """Discover agents capable of performing a specific conversion.
        
        Args:
            source_format: Source MIME type
            target_format: Target MIME type
            
        Returns:
            List of agent information dictionaries
        """
        if not self.connected:
            raise RuntimeError("Client is not connected to network")
        
        logger.info(f"🔍 Discovering agents for {source_format} -> {target_format}")
        
        try:
            # Use the discovery adapter to find suitable agents
            agents = await self.discovery_adapter.discover_conversion_agents(source_format, target_format)
            
            logger.info(f"📋 Found {len(agents)} capable agents:")
            for agent in agents:
                agent_id = agent.get('agent_id', 'Unknown')
                description = agent.get('description', 'No description')
                logger.info(f"  - {agent_id}: {description}")
            
            return agents
            
        except Exception as e:
            logger.error(f"Error during agent discovery: {e}")
            return []
    
    async def convert_file(
        self,
        input_file: Path,
        output_file: Path,
        source_format: str,
        target_format: str,
        prompt: Optional[str] = None,
        timeout: int = 60
    ) -> bool:
        """Convert a single file using the OpenConvert network.
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            source_format: Source MIME type
            target_format: Target MIME type
            prompt: Optional conversion instructions
            timeout: Timeout in seconds for conversion
            
        Returns:
            bool: True if conversion successful
        """
        if not self.connected:
            raise RuntimeError("Client is not connected to network")
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        logger.info(f"🔄 Converting {input_file.name}: {source_format} -> {target_format}")
        
        try:
            # Discover agents capable of this conversion
            agents = await self.discover_agents(source_format, target_format)
            
            if not agents:
                logger.error(f"❌ No agents found for {source_format} -> {target_format} conversion")
                return False
            
            # Use the first available agent
            target_agent = agents[0]
            agent_id = target_agent['agent_id']
            
            logger.info(f"🎯 Using agent: {agent_id}")
            
            # Read and encode the input file
            file_data = input_file.read_bytes()
            file_data_b64 = base64.b64encode(file_data).decode('ascii')
            
            # Prepare conversion request
            request_content = {
                "file_data": file_data_b64,
                "filename": input_file.name,
                "source_format": source_format,
                "target_format": target_format
            }
            
            # Add prompt if provided
            if prompt:
                request_content["prompt"] = prompt
                logger.info(f"💬 Using prompt: {prompt}")
            
            # Clear any previous responses
            if agent_id in self.conversion_responses:
                del self.conversion_responses[agent_id]
            
            # Send conversion request
            logger.info(f"📤 Sending conversion request to {agent_id}")
            await self.messaging_adapter.send_direct_message(agent_id, request_content)
            
            # Wait for response with timeout
            for _ in range(timeout):
                await asyncio.sleep(1)
                
                if agent_id in self.conversion_responses:
                    response = self.conversion_responses[agent_id]
                    
                    # Check if conversion was successful
                    if response.get("conversion_status") == "success" or response.get("success") == True:
                        # Extract converted file data
                        converted_data = response.get("file_data") or response.get("output_data")
                        
                        if not converted_data:
                            logger.error("❌ No converted data in response")
                            return False
                        
                        # Decode and save converted file
                        try:
                            converted_bytes = base64.b64decode(converted_data)
                            
                            # Ensure output directory exists
                            output_file.parent.mkdir(parents=True, exist_ok=True)
                            
                            # Write converted file
                            output_file.write_bytes(converted_bytes)
                            
                            logger.info(f"✅ Conversion successful: {output_file}")
                            return True
                            
                        except Exception as e:
                            logger.error(f"❌ Error saving converted file: {e}")
                            return False
                    
                    elif response.get("conversion_status") == "error" or response.get("success") == False:
                        error_msg = response.get("error", "Unknown error")
                        logger.error(f"❌ Conversion failed: {error_msg}")
                        return False
            
            # Timeout reached
            logger.error(f"❌ Conversion timeout after {timeout} seconds")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error during file conversion: {e}")
            return False
    
    async def convert_files_batch(
        self,
        files: List[Dict[str, Any]],
        timeout: int = 60
    ) -> List[bool]:
        """Convert multiple files in batch.
        
        Args:
            files: List of file conversion specifications, each containing:
                   - input_file: Path to input file
                   - output_file: Path to output file  
                   - source_format: Source MIME type
                   - target_format: Target MIME type
                   - prompt: Optional conversion prompt
            timeout: Timeout per file in seconds
            
        Returns:
            List of success flags for each conversion
        """
        results = []
        
        for i, file_spec in enumerate(files, 1):
            logger.info(f"Processing file {i}/{len(files)}")
            
            try:
                success = await self.convert_file(
                    input_file=file_spec['input_file'],
                    output_file=file_spec['output_file'],
                    source_format=file_spec['source_format'],
                    target_format=file_spec['target_format'],
                    prompt=file_spec.get('prompt'),
                    timeout=timeout
                )
                results.append(success)
                
            except Exception as e:
                logger.error(f"❌ Error processing file {i}: {e}")
                results.append(False)
        
        return results
    
    async def list_available_conversions(self) -> Dict[str, List[str]]:
        """Get a list of all available conversions in the network.
        
        Returns:
            Dictionary mapping source formats to lists of available target formats
        """
        if not self.connected:
            raise RuntimeError("Client is not connected to network")
        
        logger.info("📋 Querying available conversions...")
        
        # This would require a more sophisticated discovery mechanism
        # For now, return a basic set based on known conversion categories
        conversions = {}
        
        # Common conversions to check for
        common_formats = [
            'text/plain', 'text/markdown', 'text/html', 'application/pdf',
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp',
            'audio/mp3', 'audio/wav', 'video/mp4', 'application/zip'
        ]
        
        for source_format in common_formats:
            conversions[source_format] = []
            for target_format in common_formats:
                if source_format != target_format:
                    agents = await self.discover_agents(source_format, target_format)
                    if agents:
                        conversions[source_format].append(target_format)
        
        return conversions
    
    async def disconnect(self) -> None:
        """Disconnect from the OpenConvert network."""
        if self.connected:
            logger.info("🔌 Disconnecting from OpenConvert network")
            await self.client.disconnect()
            self.connected = False
            logger.info("✅ Disconnected successfully")


# Convenience functions for direct usage
async def convert_file(
    input_file: Path,
    output_file: Path,
    source_format: Optional[str] = None,
    target_format: Optional[str] = None,
    prompt: Optional[str] = None,
    host: str = "localhost",
    port: int = 8765
) -> bool:
    """Convenience function to convert a single file.
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
        source_format: Source MIME type (auto-detected if None)
        target_format: Target MIME type (auto-detected if None)
        prompt: Optional conversion instructions
        host: Network host
        port: Network port
        
    Returns:
        bool: True if conversion successful
    """
    client = OpenConvertClient()
    
    try:
        # Auto-detect formats if not provided
        if source_format is None:
            import mimetypes
            source_format, _ = mimetypes.guess_type(str(input_file))
            if source_format is None:
                source_format = 'application/octet-stream'
        
        if target_format is None:
            import mimetypes
            target_format, _ = mimetypes.guess_type(str(output_file))
            if target_format is None:
                target_format = 'application/octet-stream'
        
        # Connect and convert
        await client.connect(host=host, port=port)
        success = await client.convert_file(
            input_file=input_file,
            output_file=output_file,
            source_format=source_format,
            target_format=target_format,
            prompt=prompt
        )
        
        return success
        
    finally:
        await client.disconnect() 