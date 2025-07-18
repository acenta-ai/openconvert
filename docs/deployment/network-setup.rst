Network Setup
=============

This guide explains how to set up and configure OpenConvert networks for different deployment scenarios.

Quick Local Setup
-----------------

For development and testing, you can quickly set up a local network:

.. code-block:: bash

   # Clone OpenAgents repository
   git clone https://github.com/openagents/openagents.git
   cd openagents

   # Start the network coordinator
   openagents launch-network demos/openconvert/network_config.yaml

   # In separate terminals, start conversion agents
   python demos/openconvert/run_agent.py doc &
   python demos/openconvert/run_agent.py image &
   python demos/openconvert/run_agent.py audio &

   # Test the setup
   openconvert --list-formats

Network Architecture
--------------------

OpenConvert networks consist of:

**Network Coordinator**
  Central discovery service that helps clients find available agents.

**Conversion Agents**
  Specialized services that perform specific file conversions.

**Clients**
  OpenConvert CLI or API clients that request conversions.

.. code-block:: text

   ┌─────────────┐    ┌───────────────────┐    ┌─────────────┐
   │   Client    │───▶│ Network           │◀───│   Agent     │
   │ (CLI/API)   │    │ Coordinator       │    │ (doc-conv)  │
   └─────────────┘    │ (Discovery)       │    └─────────────┘
                      └───────────────────┘    
                               ▲               ┌─────────────┐
                               └───────────────│   Agent     │
                                               │ (img-conv)  │
                                               └─────────────┘

Network Configuration
--------------------

Basic Configuration
~~~~~~~~~~~~~~~~~~~

Create a network configuration file (``network_config.yaml``):

.. code-block:: yaml

   # Basic network configuration
   network:
     name: "openconvert-network"
     coordinator:
       host: "0.0.0.0"
       port: 8765
       max_agents: 50
       
   discovery:
     protocol: "simple"
     heartbeat_interval: 30
     agent_timeout: 120
     
   logging:
     level: "INFO"
     file: "network.log"

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

For production environments:

.. code-block:: yaml

   # Production network configuration
   network:
     name: "openconvert-prod"
     coordinator:
       host: "0.0.0.0"
       port: 8765
       max_agents: 200
       max_connections: 1000
       
   security:
     require_auth: true
     api_key_file: "/etc/openconvert/api_keys.txt"
     tls:
       enabled: true
       cert_file: "/etc/ssl/certs/openconvert.crt"
       key_file: "/etc/ssl/private/openconvert.key"
       
   discovery:
     protocol: "enhanced"
     heartbeat_interval: 30
     agent_timeout: 120
     load_balancing: true
     
   monitoring:
     enabled: true
     metrics_port: 9090
     health_check_endpoint: "/health"
     
   logging:
     level: "INFO"
     file: "/var/log/openconvert/network.log"
     max_size: "100MB"
     retention_days: 30

Agent Configuration
------------------

Document Conversion Agent
~~~~~~~~~~~~~~~~~~~~~~~~~

Create an agent configuration (``doc_agent_config.yaml``):

.. code-block:: yaml

   agent:
     id: "doc-converter-1"
     name: "Document Conversion Agent"
     type: "document"
     
   capabilities:
     formats:
       input: ["text/plain", "text/markdown", "text/csv"]
       output: ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
       
   features:
     supports_prompts: true
     batch_processing: true
     max_file_size: "50MB"
     
   network:
     coordinator_host: "localhost"
     coordinator_port: 8765
     agent_port: 8766
     
   processing:
     max_concurrent: 10
     timeout: 300
     temp_dir: "/tmp/openconvert"

Image Processing Agent
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   agent:
     id: "image-processor-1"
     name: "Image Processing Agent"
     type: "image"
     
   capabilities:
     formats:
       input: ["image/jpeg", "image/png", "image/gif", "image/tiff"]
       output: ["image/jpeg", "image/png", "image/webp", "application/pdf"]
       
   features:
     supports_prompts: true
     batch_processing: true
     max_file_size: "100MB"
     
   processing:
     max_concurrent: 5
     timeout: 180
     quality_settings:
       jpeg_quality: 85
       png_compression: 6
       webp_quality: 80

Starting Agents
~~~~~~~~~~~~~~~

Start agents with their configurations:

.. code-block:: bash

   # Start document agent
   python demos/openconvert/run_agent.py doc --config doc_agent_config.yaml

   # Start image agent  
   python demos/openconvert/run_agent.py image --config image_agent_config.yaml

   # Start multiple instances for load balancing
   for i in {1..3}; do
       python demos/openconvert/run_agent.py doc --id "doc-agent-$i" &
   done

Deployment Scenarios
--------------------

Single Machine Development
~~~~~~~~~~~~~~~~~~~~~~~~~~

Perfect for development and testing:

.. code-block:: bash

   # Terminal 1: Start network
   cd openagents
   openagents launch-network demos/openconvert/network_config.yaml

   # Terminal 2: Start agents
   python demos/openconvert/run_agent.py doc &
   python demos/openconvert/run_agent.py image &

   # Terminal 3: Test conversions
   echo "Hello World" > test.txt
   openconvert -i test.txt -o test.pdf

Small Team Setup
~~~~~~~~~~~~~~~~

Network coordinator on a shared server, agents on multiple machines:

.. code-block:: bash

   # On server (coordinator)
   openagents launch-network --host 0.0.0.0 --port 8765 network_config.yaml

   # On workstation 1 (document processing)
   python run_agent.py doc --coordinator-host server.local

   # On workstation 2 (image processing)  
   python run_agent.py image --coordinator-host server.local

   # On workstation 3 (audio/video processing)
   python run_agent.py audio --coordinator-host server.local
   python run_agent.py video --coordinator-host server.local

Production Cluster
~~~~~~~~~~~~~~~~~~

High-availability setup with multiple coordinators and agent pools:

.. code-block:: bash

   # Load balancer configuration (nginx/haproxy)
   upstream openconvert_coordinators {
       server coord1.example.com:8765;
       server coord2.example.com:8765;
       server coord3.example.com:8765;
   }

   # Agent deployment with process manager
   # /etc/systemd/system/openconvert-doc-agent@.service
   [Unit]
   Description=OpenConvert Document Agent %i
   After=network.target

   [Service]
   Type=simple
   User=openconvert
   WorkingDirectory=/opt/openconvert
   ExecStart=/opt/openconvert/venv/bin/python run_agent.py doc --id doc-agent-%i
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target

Cloud Deployment
~~~~~~~~~~~~~~~~

Using containerized agents with orchestration:

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'
   
   services:
     coordinator:
       image: openagents/coordinator:latest
       ports:
         - "8765:8765"
       environment:
         - NETWORK_CONFIG=/config/network.yaml
       volumes:
         - ./config:/config
         
     doc-agent:
       image: openagents/doc-agent:latest
       scale: 3
       environment:
         - COORDINATOR_HOST=coordinator
         - COORDINATOR_PORT=8765
       depends_on:
         - coordinator
         
     image-agent:
       image: openagents/image-agent:latest
       scale: 2
       environment:
         - COORDINATOR_HOST=coordinator
         - COORDINATOR_PORT=8765
       depends_on:
         - coordinator

Kubernetes deployment:

.. code-block:: yaml

   # k8s-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: openconvert-coordinator
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: openconvert-coordinator
     template:
       metadata:
         labels:
           app: openconvert-coordinator
       spec:
         containers:
         - name: coordinator
           image: openagents/coordinator:latest
           ports:
           - containerPort: 8765
           env:
           - name: NETWORK_CONFIG
             value: "/config/network.yaml"
   
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: openconvert-doc-agents
   spec:
     replicas: 5
     selector:
       matchLabels:
         app: openconvert-doc-agent
     template:
       metadata:
         labels:
           app: openconvert-doc-agent
       spec:
         containers:
         - name: doc-agent
           image: openagents/doc-agent:latest
           env:
           - name: COORDINATOR_HOST
             value: "openconvert-coordinator-service"

Security Configuration
----------------------

Authentication
~~~~~~~~~~~~~~

Configure API key authentication:

.. code-block:: yaml

   # In network configuration
   security:
     require_auth: true
     auth_method: "api_key"
     api_key_file: "/etc/openconvert/keys.txt"

Create API keys file:

.. code-block:: text

   # /etc/openconvert/keys.txt
   client1:abc123def456ghi789
   client2:xyz789uvw456rst123
   admin:super_secret_admin_key

Client configuration:

.. code-block:: bash

   # Use API key with client
   export OPENCONVERT_API_KEY=abc123def456ghi789
   openconvert -i file.txt -o file.pdf

TLS/SSL Setup
~~~~~~~~~~~~~

Enable encrypted communication:

.. code-block:: yaml

   # Network configuration
   security:
     tls:
       enabled: true
       cert_file: "/etc/ssl/certs/openconvert.crt"
       key_file: "/etc/ssl/private/openconvert.key"
       ca_file: "/etc/ssl/certs/ca.crt"
       verify_clients: true

Generate certificates:

.. code-block:: bash

   # Generate CA key and certificate
   openssl genrsa -out ca.key 4096
   openssl req -new -x509 -days 365 -key ca.key -out ca.crt

   # Generate server key and certificate
   openssl genrsa -out server.key 4096
   openssl req -new -key server.key -out server.csr
   openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -out server.crt

Monitoring and Maintenance
--------------------------

Health Monitoring
~~~~~~~~~~~~~~~~~

Configure health checks:

.. code-block:: yaml

   monitoring:
     enabled: true
     health_check:
       endpoint: "/health"
       interval: 30
       timeout: 10
     metrics:
       enabled: true
       port: 9090
       format: "prometheus"

Monitor with external tools:

.. code-block:: bash

   # Check coordinator health
   curl http://coordinator:8765/health

   # Check metrics
   curl http://coordinator:9090/metrics

   # Monitor with Prometheus
   # Add to prometheus.yml:
   scrape_configs:
     - job_name: 'openconvert'
       static_configs:
         - targets: ['coordinator:9090']

Log Management
~~~~~~~~~~~~~~

Configure comprehensive logging:

.. code-block:: yaml

   logging:
     level: "INFO"
     format: "json"
     outputs:
       - type: "file"
         path: "/var/log/openconvert/network.log"
         max_size: "100MB"
         max_files: 10
       - type: "syslog"
         facility: "daemon"
       - type: "elasticsearch"
         host: "logs.example.com"
         index: "openconvert"

Performance Tuning
~~~~~~~~~~~~~~~~~~

Optimize for your workload:

.. code-block:: yaml

   performance:
     coordinator:
       max_connections: 1000
       connection_pool_size: 100
       request_timeout: 30
       
     agents:
       max_concurrent_jobs: 10
       job_timeout: 300
       memory_limit: "2GB"
       
   caching:
     enabled: true
     ttl: 3600
     max_entries: 10000

Backup and Recovery
~~~~~~~~~~~~~~~~~~~

Backup configuration and logs:

.. code-block:: bash

   #!/bin/bash
   # backup.sh
   
   BACKUP_DIR="/backup/openconvert/$(date +%Y%m%d)"
   mkdir -p "$BACKUP_DIR"
   
   # Backup configurations
   cp -r /etc/openconvert/ "$BACKUP_DIR/config/"
   
   # Backup logs (last 7 days)
   find /var/log/openconvert/ -mtime -7 -type f -exec cp {} "$BACKUP_DIR/logs/" \\;
   
   # Backup agent states
   curl http://coordinator:8765/export > "$BACKUP_DIR/agent_states.json"

Troubleshooting
---------------

Common Network Issues
~~~~~~~~~~~~~~~~~~~~

**Coordinator won't start:**

.. code-block:: bash

   # Check port availability
   netstat -an | grep 8765
   
   # Check configuration
   openagents validate-config network_config.yaml
   
   # Check logs
   tail -f /var/log/openconvert/network.log

**Agents can't connect:**

.. code-block:: bash

   # Test connectivity
   telnet coordinator-host 8765
   
   # Check firewall
   iptables -L | grep 8765
   
   # Verify agent configuration
   python run_agent.py doc --dry-run

**Performance issues:**

.. code-block:: bash

   # Monitor resource usage
   htop
   iotop
   
   # Check network latency
   ping coordinator-host
   
   # Monitor agent queues
   curl http://coordinator:8765/stats

See Also
--------

- :doc:`agent-configuration` - Detailed agent setup
- :doc:`docker-deployment` - Container deployment
- :doc:`../user-guide/troubleshooting` - General troubleshooting 