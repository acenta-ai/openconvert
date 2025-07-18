Advanced Usage
==============

This guide covers advanced OpenConvert features and techniques for power users.

Advanced Command-Line Usage
---------------------------

Complex Conversion Scenarios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Multi-step conversions with different prompts:**

.. code-block:: bash

   # Create draft version
   openconvert -i report.txt -o draft.pdf --prompt "Quick draft layout"

   # Create final version with enhanced formatting
   openconvert -i report.txt -o final.pdf \\
     --prompt "Executive presentation with charts, tables, and professional layout"

   # Create presentation version
   openconvert -i report.txt -o slides.pdf \\
     --prompt "Convert to presentation slides with bullet points"

**Conditional conversions with shell scripting:**

.. code-block:: bash

   #!/bin/bash
   # Smart conversion script

   input_file="$1"
   
   # Check file size
   file_size=$(stat -f%z "$input_file" 2>/dev/null || stat -c%s "$input_file")
   
   if [ "$file_size" -gt 10485760 ]; then  # 10MB
       echo "Large file detected, using compression prompt"
       prompt="Optimize for size, compress images and reduce quality if needed"
   else
       echo "Normal file size, using quality prompt"
       prompt="High quality conversion with best formatting"
   fi
   
   # Convert with appropriate prompt
   openconvert -i "$input_file" -o "${input_file%.*}.pdf" --prompt "$prompt"

**Format chain processing:**

.. code-block:: bash

   # Process through multiple formats for different outputs
   input="data.csv"
   
   # Create chart
   openconvert -i "$input" -o "charts.png" --prompt "Create bar and line charts"
   
   # Create formatted table
   openconvert -i "$input" -o "table.pdf" --prompt "Professional data table"
   
   # Create Excel with formulas
   openconvert -i "$input" -o "analysis.xlsx" --prompt "Add formulas and pivot tables"

Advanced Python Integration
---------------------------

Custom Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert.client import OpenConvertClient
   import asyncio
   from pathlib import Path

   class CustomOpenConvertClient:
       """Extended client with additional features."""
       
       def __init__(self, hosts=None, retry_count=3, timeout=30):
           """Initialize with multiple hosts and retry logic."""
           self.hosts = hosts or [("localhost", 8765)]
           self.retry_count = retry_count
           self.timeout = timeout
           self.current_host_index = 0
           self.client = None
           
       async def connect_with_failover(self):
           """Connect with automatic failover to backup hosts."""
           for attempt in range(self.retry_count):
               for i, (host, port) in enumerate(self.hosts):
                   try:
                       self.client = OpenConvertClient()
                       await asyncio.wait_for(
                           self.client.connect(host, port), 
                           timeout=self.timeout
                       )
                       self.current_host_index = i
                       print(f"Connected to {host}:{port}")
                       return True
                   except Exception as e:
                       print(f"Failed to connect to {host}:{port}: {e}")
                       continue
               
               if attempt < self.retry_count - 1:
                   await asyncio.sleep(2 ** attempt)  # Exponential backoff
           
           raise ConnectionError("Failed to connect to any host")
       
       async def convert_with_retry(self, input_file, output_file, **kwargs):
           """Convert with automatic retry and failover."""
           for attempt in range(self.retry_count):
               try:
                   if not self.client:
                       await self.connect_with_failover()
                   
                   result = await self.client.convert_file(
                       input_file=Path(input_file),
                       output_file=Path(output_file),
                       **kwargs
                   )
                   return result
                   
               except Exception as e:
                   print(f"Conversion attempt {attempt + 1} failed: {e}")
                   if attempt < self.retry_count - 1:
                       # Try next host on failure
                       self.current_host_index = (self.current_host_index + 1) % len(self.hosts)
                       self.client = None
                       await asyncio.sleep(1)
                   else:
                       raise

   # Usage
   async def main():
       client = CustomOpenConvertClient(
           hosts=[("primary.example.com", 8765), ("backup.example.com", 8765)],
           retry_count=3
       )
       
       result = await client.convert_with_retry(
           "document.txt", 
           "document.pdf",
           prompt="High-quality conversion"
       )
       print(f"Conversion result: {result}")

   asyncio.run(main())

Intelligent Format Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import mimetypes
   from pathlib import Path
   from openconvert import convert_file

   class SmartConverter:
       """Intelligent converter that selects optimal formats and prompts."""
       
       def __init__(self):
           self.format_mappings = {
               'text/plain': {
                   'best_outputs': ['application/pdf', 'text/html'],
                   'prompts': {
                       'application/pdf': 'Professional document formatting',
                       'text/html': 'Clean web-readable format'
                   }
               },
               'image/jpeg': {
                   'best_outputs': ['image/webp', 'image/png'],
                   'prompts': {
                       'image/webp': 'Optimize for web with quality preservation',
                       'image/png': 'Lossless conversion'
                   }
               },
               'text/csv': {
                   'best_outputs': ['application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
                   'prompts': {
                       'application/pdf': 'Create formatted report with charts',
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Structured spreadsheet with formulas'
                   }
               }
           }
       
       def detect_input_format(self, file_path):
           """Detect input file format."""
           mime_type, _ = mimetypes.guess_type(file_path)
           return mime_type
       
       def suggest_output_format(self, input_format, purpose='general'):
           """Suggest optimal output format based on input and purpose."""
           mapping = self.format_mappings.get(input_format, {})
           best_outputs = mapping.get('best_outputs', ['application/pdf'])
           
           # Purpose-specific logic
           if purpose == 'web':
               web_formats = ['image/webp', 'text/html', 'application/pdf']
               for fmt in web_formats:
                   if fmt in best_outputs:
                       return fmt
           elif purpose == 'print':
               if 'application/pdf' in best_outputs:
                   return 'application/pdf'
           
           return best_outputs[0] if best_outputs else 'application/pdf'
       
       def get_smart_prompt(self, input_format, output_format, file_size=None):
           """Generate intelligent prompt based on formats and file properties."""
           mapping = self.format_mappings.get(input_format, {})
           base_prompt = mapping.get('prompts', {}).get(output_format, '')
           
           # Enhance prompt based on file size
           if file_size:
               if file_size > 10 * 1024 * 1024:  # 10MB
                   base_prompt += ". Optimize for file size."
               elif file_size < 1024:  # 1KB
                   base_prompt += ". Maintain maximum quality."
           
           return base_prompt
       
       def smart_convert(self, input_file, output_file=None, purpose='general'):
           """Perform intelligent conversion with optimal settings."""
           input_path = Path(input_file)
           
           # Detect input format
           input_format = self.detect_input_format(str(input_path))
           if not input_format:
               raise ValueError(f"Cannot detect format for {input_file}")
           
           # Determine output format and file
           if output_file:
               output_path = Path(output_file)
               output_format = self.detect_input_format(str(output_path))
           else:
               output_format = self.suggest_output_format(input_format, purpose)
               ext = mimetypes.guess_extension(output_format) or '.pdf'
               output_path = input_path.with_suffix(ext)
           
           # Get file size
           file_size = input_path.stat().st_size
           
           # Generate smart prompt
           prompt = self.get_smart_prompt(input_format, output_format, file_size)
           
           print(f"Converting {input_file}")
           print(f"  Input format: {input_format}")
           print(f"  Output format: {output_format}")
           print(f"  Output file: {output_path}")
           print(f"  Prompt: {prompt}")
           
           # Perform conversion
           return convert_file(
               str(input_path),
               str(output_path),
               from_format=input_format,
               to_format=output_format,
               prompt=prompt
           )

   # Usage
   converter = SmartConverter()
   
   # Automatic optimization for web
   converter.smart_convert("photo.jpg", purpose="web")
   
   # Automatic optimization for print
   converter.smart_convert("document.txt", purpose="print")
   
   # Manual output specification
   converter.smart_convert("data.csv", "report.pdf")

Advanced Prompt Engineering
---------------------------

Context-Aware Prompts
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   import re
   from datetime import datetime
   from pathlib import Path

   class PromptBuilder:
       """Build intelligent, context-aware prompts."""
       
       def __init__(self):
           self.templates = {
               'document': {
                   'academic': "Format as academic paper with: title page, abstract, sections with numbered headings, bibliography, proper margins, Times New Roman font",
                   'business': "Professional business document with: company header, executive summary, clear sections, bullet points, charts where appropriate",
                   'casual': "Clean, readable format with: clear headings, good spacing, easy-to-read font",
                   'presentation': "Convert to presentation format with: slide titles, bullet points, large readable text, minimal text per slide"
               },
               'image': {
                   'thumbnail': "Create {size} thumbnail: crop to center, maintain aspect ratio, optimize for fast loading",
                   'web_optimized': "Optimize for web: compress to {quality}% quality, convert to {format}, reduce file size",
                   'print_ready': "Prepare for print: high DPI, CMYK color space if possible, preserve quality",
                   'social_media': "Optimize for social media: crop to {aspect_ratio}, enhance colors, compress appropriately"
               },
               'data': {
                   'report': "Create professional data report with: formatted tables, charts for trends, summary statistics, conclusions",
                   'dashboard': "Build executive dashboard with: key metrics highlighted, visual charts, clear labels, trend indicators",
                   'analysis': "Perform data analysis with: statistical summaries, correlation analysis, trend identification, insights"
               }
           }
       
       def analyze_content(self, file_path):
           """Analyze file content to determine appropriate prompt."""
           path = Path(file_path)
           
           # Analyze filename for clues
           filename = path.stem.lower()
           
           context = {
               'type': 'general',
               'domain': 'general',
               'urgency': 'normal',
               'audience': 'general'
           }
           
           # Detect document type from filename
           if any(word in filename for word in ['report', 'summary', 'analysis']):
               context['type'] = 'report'
           elif any(word in filename for word in ['presentation', 'slides', 'deck']):
               context['type'] = 'presentation'
           elif any(word in filename for word in ['academic', 'paper', 'thesis', 'research']):
               context['type'] = 'academic'
           elif any(word in filename for word in ['business', 'proposal', 'contract']):
               context['type'] = 'business'
           
           # Detect domain
           if any(word in filename for word in ['financial', 'finance', 'budget', 'accounting']):
               context['domain'] = 'finance'
           elif any(word in filename for word in ['technical', 'engineering', 'spec', 'design']):
               context['domain'] = 'technical'
           elif any(word in filename for word in ['marketing', 'sales', 'campaign']):
               context['domain'] = 'marketing'
           
           # Detect urgency
           if any(word in filename for word in ['urgent', 'priority', 'asap']):
               context['urgency'] = 'high'
           elif any(word in filename for word in ['draft', 'preliminary', 'temp']):
               context['urgency'] = 'low'
           
           return context
       
       def build_prompt(self, file_path, output_format, context_override=None):
           """Build context-aware prompt."""
           context = context_override or self.analyze_content(file_path)
           
           # Base prompt from template
           file_type = 'document' if 'text' in output_format or 'pdf' in output_format else 'image'
           template_type = context.get('type', 'general')
           
           base_prompt = self.templates.get(file_type, {}).get(template_type, "Professional formatting")
           
           # Add domain-specific enhancements
           domain_enhancements = {
               'finance': "Include financial formatting: currency symbols, percentage formatting, aligned numbers",
               'technical': "Use technical formatting: code blocks, diagrams, precise terminology",
               'marketing': "Use engaging formatting: attractive layout, emphasis on key points, visual appeal"
           }
           
           domain = context.get('domain')
           if domain in domain_enhancements:
               base_prompt += f". {domain_enhancements[domain]}"
           
           # Add urgency considerations
           if context.get('urgency') == 'high':
               base_prompt += ". Prioritize clarity and quick readability."
           elif context.get('urgency') == 'low':
               base_prompt += ". Focus on detailed formatting and visual appeal."
           
           return base_prompt
       
       def build_batch_prompts(self, file_list, output_format):
           """Build prompts for batch processing with consistency."""
           prompts = {}
           
           # Analyze all files to find common context
           contexts = [self.analyze_content(f) for f in file_list]
           
           # Find most common type and domain
           types = [c.get('type') for c in contexts]
           domains = [c.get('domain') for c in contexts]
           
           common_type = max(set(types), key=types.count) if types else 'general'
           common_domain = max(set(domains), key=domains.count) if domains else 'general'
           
           base_context = {'type': common_type, 'domain': common_domain}
           
           for file_path in file_list:
               # Use common context for consistency, but allow for file-specific tweaks
               file_context = self.analyze_content(file_path)
               
               # Override with common context for consistency
               merged_context = {**file_context, **base_context}
               
               prompts[file_path] = self.build_prompt(file_path, output_format, merged_context)
           
           return prompts

   # Usage
   prompt_builder = PromptBuilder()

   # Single file with automatic context detection
   prompt = prompt_builder.build_prompt("financial_report_Q3.txt", "application/pdf")
   print(f"Generated prompt: {prompt}")

   # Batch processing with consistent prompts
   files = ["report1.txt", "report2.txt", "report3.txt"]
   prompts = prompt_builder.build_batch_prompts(files, "application/pdf")

   for file_path, prompt in prompts.items():
       convert_file(file_path, f"{file_path}.pdf", prompt=prompt)

Dynamic Prompt Adjustment
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from openconvert import convert_file

   class AdaptiveConverter:
       """Converter that learns from conversion results and adjusts prompts."""
       
       def __init__(self, feedback_file="conversion_feedback.json"):
           self.feedback_file = feedback_file
           self.feedback_data = self.load_feedback()
           
       def load_feedback(self):
           """Load previous conversion feedback."""
           try:
               with open(self.feedback_file, 'r') as f:
                   return json.load(f)
           except FileNotFoundError:
               return {}
       
       def save_feedback(self):
           """Save feedback data."""
           with open(self.feedback_file, 'w') as f:
               json.dump(self.feedback_data, f, indent=2)
       
       def get_success_rate(self, prompt_pattern):
           """Get success rate for similar prompts."""
           matching_conversions = [
               conv for conv in self.feedback_data.values()
               if prompt_pattern.lower() in conv.get('prompt', '').lower()
           ]
           
           if not matching_conversions:
               return 0.5  # Default success rate
           
           successful = sum(1 for conv in matching_conversions if conv.get('success', False))
           return successful / len(matching_conversions)
       
       def optimize_prompt(self, base_prompt, input_format, output_format):
           """Optimize prompt based on historical success rates."""
           
           # Try variations of the prompt
           variations = [
               base_prompt,
               f"{base_prompt}. Use high quality settings.",
               f"{base_prompt}. Optimize for readability.",
               f"{base_prompt}. Ensure professional appearance.",
               f"Professional formatting: {base_prompt.lower()}"
           ]
           
           # Score each variation
           scored_variations = []
           for variation in variations:
               score = self.get_success_rate(variation)
               scored_variations.append((variation, score))
           
           # Return best variation
           best_prompt, best_score = max(scored_variations, key=lambda x: x[1])
           
           print(f"Selected prompt (score: {best_score:.2f}): {best_prompt}")
           return best_prompt
       
       def convert_with_learning(self, input_file, output_file, base_prompt, **kwargs):
           """Convert and learn from the result."""
           
           # Optimize prompt
           optimized_prompt = self.optimize_prompt(
               base_prompt, 
               kwargs.get('from_format'), 
               kwargs.get('to_format')
           )
           
           # Perform conversion
           success = convert_file(
               input_file, 
               output_file, 
               prompt=optimized_prompt,
               **kwargs
           )
           
           # Record feedback
           conversion_id = f"{input_file}_{output_file}_{hash(optimized_prompt)}"
           self.feedback_data[conversion_id] = {
               'input_file': input_file,
               'output_file': output_file,
               'prompt': optimized_prompt,
               'success': success,
               'input_format': kwargs.get('from_format'),
               'output_format': kwargs.get('to_format'),
               'timestamp': datetime.now().isoformat()
           }
           
           self.save_feedback()
           
           return success

   # Usage
   adaptive_converter = AdaptiveConverter()

   # Convert with learning
   success = adaptive_converter.convert_with_learning(
       "document.txt",
       "document.pdf", 
       "Create professional document",
       from_format="text/plain",
       to_format="application/pdf"
   )

Performance Optimization
-----------------------

Parallel Processing Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import concurrent.futures
   from pathlib import Path
   from openconvert import convert_file
   from openconvert.client import OpenConvertClient

   class HighPerformanceConverter:
       """High-performance converter with multiple optimization strategies."""
       
       def __init__(self, max_workers=4, max_concurrent_agents=2):
           self.max_workers = max_workers
           self.max_concurrent_agents = max_concurrent_agents
           
       async def convert_with_agent_pool(self, conversion_tasks):
           """Convert using multiple agent connections."""
           
           # Create agent pool
           agent_pool = []
           for i in range(self.max_concurrent_agents):
               client = OpenConvertClient(agent_id=f"batch-client-{i}")
               await client.connect()
               agent_pool.append(client)
           
           try:
               # Distribute tasks across agents
               semaphore = asyncio.Semaphore(self.max_concurrent_agents)
               
               async def convert_with_semaphore(task, agent):
                   async with semaphore:
                       return await agent.convert_file(**task)
               
               # Create tasks
               tasks = []
               for i, conversion_task in enumerate(conversion_tasks):
                   agent = agent_pool[i % len(agent_pool)]
                   task = convert_with_semaphore(conversion_task, agent)
                   tasks.append(task)
               
               # Execute all tasks
               results = await asyncio.gather(*tasks, return_exceptions=True)
               return results
               
           finally:
               # Cleanup agent connections
               for agent in agent_pool:
                   await agent.disconnect()
       
       def convert_cpu_bound_parallel(self, file_pairs):
           """Use process pool for CPU-bound pre/post-processing."""
           
           def process_file_pair(pair):
               input_file, output_file, prompt = pair
               return convert_file(input_file, output_file, prompt=prompt)
           
           with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
               future_to_pair = {
                   executor.submit(process_file_pair, pair): pair 
                   for pair in file_pairs
               }
               
               results = []
               for future in concurrent.futures.as_completed(future_to_pair):
                   pair = future_to_pair[future]
                   try:
                       result = future.result()
                       results.append((pair, result))
                   except Exception as e:
                       results.append((pair, f"Error: {e}"))
               
               return results
       
       def convert_io_bound_parallel(self, file_pairs):
           """Use thread pool for I/O-bound operations."""
           
           def convert_single(pair):
               input_file, output_file, prompt = pair
               return convert_file(input_file, output_file, prompt=prompt)
           
           with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
               futures = [executor.submit(convert_single, pair) for pair in file_pairs]
               results = []
               
               for future in concurrent.futures.as_completed(futures):
                   try:
                       result = future.result()
                       results.append(result)
                   except Exception as e:
                       results.append(f"Error: {e}")
               
               return results

   # Usage
   converter = HighPerformanceConverter(max_workers=8, max_concurrent_agents=4)

   # For many small files (I/O bound)
   file_pairs = [
       ("file1.txt", "file1.pdf", "Quick conversion"),
       ("file2.txt", "file2.pdf", "Quick conversion"),
       # ... many more files
   ]
   
   results = converter.convert_io_bound_parallel(file_pairs)

   # For fewer large files (agent-bound)
   conversion_tasks = [
       {
           'input_file': Path("large1.txt"),
           'output_file': Path("large1.pdf"),
           'prompt': "Detailed formatting"
       },
       {
           'input_file': Path("large2.txt"), 
           'output_file': Path("large2.pdf"),
           'prompt': "Detailed formatting"
       }
   ]
   
   results = asyncio.run(converter.convert_with_agent_pool(conversion_tasks))

Monitoring and Profiling
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import psutil
   import logging
   from contextlib import contextmanager
   from openconvert import convert_file

   class ConversionProfiler:
       """Profile conversion performance and resource usage."""
       
       def __init__(self):
           self.metrics = []
           
       @contextmanager
       def profile_conversion(self, conversion_name):
           """Context manager to profile a conversion."""
           
           # Record start metrics
           start_time = time.time()
           start_memory = psutil.virtual_memory().used
           start_cpu = psutil.cpu_percent(interval=None)
           
           try:
               yield
           finally:
               # Record end metrics
               end_time = time.time()
               end_memory = psutil.virtual_memory().used
               end_cpu = psutil.cpu_percent(interval=None)
               
               metrics = {
                   'name': conversion_name,
                   'duration': end_time - start_time,
                   'memory_used': end_memory - start_memory,
                   'cpu_avg': (start_cpu + end_cpu) / 2,
                   'timestamp': time.time()
               }
               
               self.metrics.append(metrics)
               
               logging.info(f"Conversion '{conversion_name}': "
                          f"{metrics['duration']:.2f}s, "
                          f"Memory: {metrics['memory_used']/1024/1024:.1f}MB, "
                          f"CPU: {metrics['cpu_avg']:.1f}%")
       
       def get_performance_report(self):
           """Generate performance report."""
           if not self.metrics:
               return "No conversions recorded"
           
           total_time = sum(m['duration'] for m in self.metrics)
           avg_time = total_time / len(self.metrics)
           max_memory = max(m['memory_used'] for m in self.metrics)
           avg_cpu = sum(m['cpu_avg'] for m in self.metrics) / len(self.metrics)
           
           report = f"""
   Performance Report:
   ==================
   Total conversions: {len(self.metrics)}
   Total time: {total_time:.2f}s
   Average time per conversion: {avg_time:.2f}s
   Peak memory usage: {max_memory/1024/1024:.1f}MB
   Average CPU usage: {avg_cpu:.1f}%
   
   Individual conversions:
   """
           
           for m in self.metrics:
               report += f"  {m['name']}: {m['duration']:.2f}s\n"
           
           return report

   # Usage
   profiler = ConversionProfiler()

   files_to_convert = [
       ("doc1.txt", "doc1.pdf"),
       ("doc2.txt", "doc2.pdf"),
       ("doc3.txt", "doc3.pdf")
   ]

   for input_file, output_file in files_to_convert:
       with profiler.profile_conversion(f"{input_file} -> {output_file}"):
           convert_file(input_file, output_file)

   print(profiler.get_performance_report())

See Also
--------

- :doc:`python-api` - Python API reference
- :doc:`../examples/batch-processing` - Batch processing examples
- :doc:`../examples/python-integration` - Integration examples
- :doc:`../deployment/network-setup` - Network optimization 