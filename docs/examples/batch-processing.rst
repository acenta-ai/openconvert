Batch Processing Examples
=========================

This section provides practical examples for batch processing files with OpenConvert.

Document Batch Processing
-------------------------

Convert All Text Files to PDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Simple batch conversion
   openconvert -i documents/ -o pdfs/ --to application/pdf

   # With custom formatting
   openconvert -i documents/ -o pdfs/ --to application/pdf \\
     --prompt "Professional layout with headers"

   # Process specific file pattern
   openconvert -i "*.txt" -o converted/ --to application/pdf

Directory Structure Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # Process entire directory tree
   
   find /path/to/documents -name "*.txt" -type f | while read file; do
       # Create corresponding output path
       output_dir="converted/$(dirname "$file")"
       mkdir -p "$output_dir"
       
       # Convert file
       openconvert -i "$file" -o "$output_dir/$(basename "$file" .txt).pdf"
   done

Parallel Processing
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Process multiple files in parallel
   ls *.txt | xargs -I {} -P 4 openconvert -i {} -o {}.pdf

   # GNU parallel (if available)
   parallel openconvert -i {} -o {.}.pdf ::: *.txt

Python Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   from pathlib import Path
   import concurrent.futures
   from typing import List, Tuple

   def batch_convert_documents(
       input_dir: str, 
       output_dir: str,
       max_workers: int = 4
   ) -> List[Tuple[str, bool]]:
       """Convert all text files in directory to PDF."""
       
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       output_path.mkdir(parents=True, exist_ok=True)
       
       # Find all text files
       text_files = list(input_path.glob("**/*.txt"))
       
       def convert_single(file_path: Path) -> Tuple[str, bool]:
           """Convert a single file."""
           relative_path = file_path.relative_to(input_path)
           output_file = output_path / relative_path.with_suffix('.pdf')
           
           # Create output directory if needed
           output_file.parent.mkdir(parents=True, exist_ok=True)
           
           success = convert_file(
               str(file_path),
               str(output_file),
               prompt="Professional document formatting"
           )
           
           return str(relative_path), success
       
       # Process files in parallel
       results = []
       with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
           future_to_file = {
               executor.submit(convert_single, file_path): file_path 
               for file_path in text_files
           }
           
           for future in concurrent.futures.as_completed(future_to_file):
               try:
                   result = future.result()
                   results.append(result)
                   print(f"{'✅' if result[1] else '❌'} {result[0]}")
               except Exception as e:
                   file_path = future_to_file[future]
                   print(f"❌ {file_path}: {e}")
                   results.append((str(file_path), False))
       
       return results

   # Usage
   results = batch_convert_documents("documents/", "converted_pdfs/")
   successful = sum(1 for _, success in results if success)
   print(f"Converted {successful}/{len(results)} files successfully")

Image Batch Processing
----------------------

Resize and Convert Images
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Convert all JPEG images to WebP with compression
   openconvert -i photos/ -o web_ready/ \\
     --from image/jpeg --to image/webp \\
     --prompt "Compress for web, resize to max 1920px width"

   # Create thumbnails
   openconvert -i photos/ -o thumbnails/ \\
     --from image/jpeg --to image/jpeg \\
     --prompt "Create 300x300 thumbnails"

Photo Library Processing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   from pathlib import Path
   import logging

   def process_photo_library(
       input_dir: str,
       output_dir: str,
       create_thumbnails: bool = True,
       web_format: bool = True
   ):
       """Process entire photo library with multiple output formats."""
       
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       
       # Supported image extensions
       image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
       
       for image_file in input_path.rglob('*'):
           if image_file.suffix.lower() in image_extensions:
               relative_path = image_file.relative_to(input_path)
               
               # Create directory structure
               output_subdir = output_path / relative_path.parent
               output_subdir.mkdir(parents=True, exist_ok=True)
               
               # Web-optimized version
               if web_format:
                   web_file = output_subdir / f"{relative_path.stem}_web.webp"
                   success = convert_file(
                       str(image_file),
                       str(web_file),
                       prompt="Optimize for web: compress and resize to max 1920px"
                   )
                   if success:
                       print(f"✅ Web: {relative_path}")
                   else:
                       print(f"❌ Web: {relative_path}")
               
               # Thumbnail version
               if create_thumbnails:
                   thumb_file = output_subdir / f"{relative_path.stem}_thumb.jpg"
                   success = convert_file(
                       str(image_file),
                       str(thumb_file),
                       prompt="Create 300x300 thumbnail, crop to center"
                   )
                   if success:
                       print(f"✅ Thumb: {relative_path}")
                   else:
                       print(f"❌ Thumb: {relative_path}")

   # Usage
   process_photo_library("raw_photos/", "processed_photos/")

Data Processing
---------------

CSV to Charts
~~~~~~~~~~~~~

.. code-block:: bash

   # Convert all CSV files to chart PDFs
   for csv_file in *.csv; do
       openconvert -i "$csv_file" -o "${csv_file%.csv}_chart.pdf" \\
         --prompt "Create bar charts and line graphs with data analysis"
   done

Database Export Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   import pandas as pd
   from pathlib import Path

   def process_database_exports(export_dir: str, report_dir: str):
       """Convert database CSV exports to formatted reports."""
       
       export_path = Path(export_dir)
       report_path = Path(report_dir)
       report_path.mkdir(parents=True, exist_ok=True)
       
       # Define report templates for different data types
       templates = {
           'sales': "Create executive sales report with charts showing trends, top products, and regional performance",
           'users': "Create user analytics report with demographics charts and activity graphs", 
           'inventory': "Create inventory report with stock levels, reorder alerts, and category breakdown",
           'default': "Create professional data report with appropriate charts and analysis"
       }
       
       for csv_file in export_path.glob("*.csv"):
           # Determine report type from filename
           report_type = 'default'
           for key in templates:
               if key in csv_file.name.lower():
                   report_type = key
                   break
           
           # Generate report
           output_file = report_path / f"{csv_file.stem}_report.pdf"
           
           success = convert_file(
               str(csv_file),
               str(output_file),
               prompt=templates[report_type]
           )
           
           if success:
               print(f"✅ Generated {report_type} report: {output_file.name}")
           else:
               print(f"❌ Failed to generate report for: {csv_file.name}")

   # Usage
   process_database_exports("exports/", "reports/")

Advanced Batch Patterns
-----------------------

Conditional Processing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   from pathlib import Path
   import os

   def smart_batch_convert(input_dir: str, output_dir: str):
       """Convert files only if output doesn't exist or is older."""
       
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       
       for input_file in input_path.rglob("*.txt"):
           relative_path = input_file.relative_to(input_path)
           output_file = output_path / relative_path.with_suffix('.pdf')
           
           # Skip if output exists and is newer
           if (output_file.exists() and 
               output_file.stat().st_mtime > input_file.stat().st_mtime):
               print(f"⏭️  Skipping {relative_path} (up to date)")
               continue
           
           # Create output directory
           output_file.parent.mkdir(parents=True, exist_ok=True)
           
           # Convert file
           success = convert_file(str(input_file), str(output_file))
           if success:
               print(f"✅ Converted {relative_path}")
           else:
               print(f"❌ Failed {relative_path}")

Error Recovery and Retry
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   import time
   import logging
   from typing import List, Dict

   def robust_batch_convert(
       file_list: List[str],
       output_dir: str,
       max_retries: int = 3,
       retry_delay: int = 5
   ) -> Dict[str, str]:
       """Batch convert with error recovery and retry logic."""
       
       results = {}
       failed_files = []
       
       for input_file in file_list:
           output_file = f"{output_dir}/{Path(input_file).stem}.pdf"
           
           for attempt in range(max_retries + 1):
               try:
                   success = convert_file(input_file, output_file)
                   
                   if success:
                       results[input_file] = "success"
                       print(f"✅ {input_file} (attempt {attempt + 1})")
                       break
                   else:
                       if attempt < max_retries:
                           print(f"🔄 Retrying {input_file} in {retry_delay}s...")
                           time.sleep(retry_delay)
                       else:
                           results[input_file] = "failed_conversion"
                           failed_files.append(input_file)
                           print(f"❌ {input_file} failed after {max_retries + 1} attempts")
                           
               except Exception as e:
                   if attempt < max_retries:
                       print(f"🔄 Error with {input_file}, retrying: {e}")
                       time.sleep(retry_delay)
                   else:
                       results[input_file] = f"error: {e}"
                       failed_files.append(input_file)
                       print(f"❌ {input_file} error: {e}")
       
       # Save failed files list for manual processing
       if failed_files:
           with open(f"{output_dir}/failed_conversions.txt", "w") as f:
               f.write("\\n".join(failed_files))
       
       return results

Progress Tracking
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from openconvert import convert_file
   from pathlib import Path
   import time
   from tqdm import tqdm  # pip install tqdm

   def batch_convert_with_progress(input_dir: str, output_dir: str):
       """Batch convert with progress bar and time estimation."""
       
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       output_path.mkdir(parents=True, exist_ok=True)
       
       # Get list of files to process
       files_to_process = list(input_path.glob("*.txt"))
       
       successful = 0
       failed = 0
       start_time = time.time()
       
       # Process with progress bar
       with tqdm(files_to_process, desc="Converting files") as pbar:
           for input_file in pbar:
               output_file = output_path / f"{input_file.stem}.pdf"
               
               file_start = time.time()
               success = convert_file(str(input_file), str(output_file))
               file_time = time.time() - file_start
               
               if success:
                   successful += 1
                   status = "✅"
               else:
                   failed += 1
                   status = "❌"
               
               # Update progress bar
               pbar.set_postfix({
                   'Success': successful,
                   'Failed': failed,
                   'Time': f"{file_time:.1f}s"
               })
       
       # Final statistics
       total_time = time.time() - start_time
       print(f"\\nBatch conversion completed:")
       print(f"  Successful: {successful}")
       print(f"  Failed: {failed}")
       print(f"  Total time: {total_time:.1f}s")
       print(f"  Average per file: {total_time/len(files_to_process):.1f}s")

Configuration-Based Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import yaml
   from openconvert import convert_file
   from pathlib import Path

   def config_based_batch_convert(config_file: str):
       """Batch convert based on YAML configuration."""
       
       with open(config_file, 'r') as f:
           config = yaml.safe_load(f)
       
       for job in config.get('conversion_jobs', []):
           input_pattern = job['input_pattern']
           output_dir = job['output_dir']
           target_format = job.get('target_format', 'application/pdf')
           prompt = job.get('prompt', '')
           
           # Create output directory
           Path(output_dir).mkdir(parents=True, exist_ok=True)
           
           # Process files matching pattern
           for input_file in Path('.').glob(input_pattern):
               output_file = Path(output_dir) / f"{input_file.stem}.pdf"
               
               success = convert_file(
                   str(input_file),
                   str(output_file),
                   to_format=target_format,
                   prompt=prompt
               )
               
               print(f"{'✅' if success else '❌'} {input_file} -> {output_file}")

Example configuration file (``batch_config.yaml``):

.. code-block:: yaml

   conversion_jobs:
     - name: "Documentation to PDF"
       input_pattern: "docs/*.md"
       output_dir: "pdfs/docs"
       target_format: "application/pdf"
       prompt: "Professional documentation format with TOC"
       
     - name: "Reports to PDF"
       input_pattern: "reports/*.txt"
       output_dir: "pdfs/reports"
       target_format: "application/pdf"
       prompt: "Executive report format with charts"
       
     - name: "Images to WebP"
       input_pattern: "images/*.jpg"
       output_dir: "web_images"
       target_format: "image/webp"
       prompt: "Optimize for web, maintain quality"

Usage:

.. code-block:: bash

   python batch_processor.py batch_config.yaml

Monitoring and Logging
----------------------

Production Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import json
   from datetime import datetime
   from openconvert import convert_file
   from pathlib import Path

   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('batch_conversion.log'),
           logging.StreamHandler()
       ]
   )

   def production_batch_convert(input_dir: str, output_dir: str):
       """Production-ready batch conversion with comprehensive logging."""
       
       job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
       logging.info(f"Starting batch job {job_id}")
       
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       
       # Job statistics
       stats = {
           'job_id': job_id,
           'start_time': datetime.now().isoformat(),
           'total_files': 0,
           'successful': 0,
           'failed': 0,
           'errors': []
       }
       
       try:
           files_to_process = list(input_path.glob("*.txt"))
           stats['total_files'] = len(files_to_process)
           
           logging.info(f"Found {len(files_to_process)} files to process")
           
           for input_file in files_to_process:
               output_file = output_path / f"{input_file.stem}.pdf"
               
               try:
                   success = convert_file(str(input_file), str(output_file))
                   
                   if success:
                       stats['successful'] += 1
                       logging.info(f"✅ Converted: {input_file.name}")
                   else:
                       stats['failed'] += 1
                       error_msg = f"Conversion failed: {input_file.name}"
                       stats['errors'].append(error_msg)
                       logging.error(error_msg)
                       
               except Exception as e:
                   stats['failed'] += 1
                   error_msg = f"Exception processing {input_file.name}: {e}"
                   stats['errors'].append(error_msg)
                   logging.error(error_msg)
           
           stats['end_time'] = datetime.now().isoformat()
           stats['success_rate'] = stats['successful'] / stats['total_files'] * 100
           
           # Save job report
           report_file = output_path / f"batch_report_{job_id}.json"
           with open(report_file, 'w') as f:
               json.dump(stats, f, indent=2)
           
           logging.info(f"Batch job completed: {stats['successful']}/{stats['total_files']} successful ({stats['success_rate']:.1f}%)")
           
       except Exception as e:
           logging.error(f"Batch job failed: {e}")
           raise

   # Usage
   production_batch_convert("input_documents/", "output_pdfs/")

Best Practices
--------------

1. **Start Small**: Test with a few files before processing large batches
2. **Monitor Resources**: Watch CPU, memory, and disk usage during batch operations
3. **Use Parallel Processing**: But don't overwhelm the network with too many concurrent requests
4. **Implement Retry Logic**: Network operations can fail temporarily
5. **Log Everything**: Essential for debugging and monitoring progress
6. **Validate Results**: Check that output files were created successfully
7. **Handle Errors Gracefully**: Don't let one failed file stop the entire batch
8. **Progress Tracking**: Use progress bars for long-running operations
9. **Configuration Files**: Use config files for complex batch operations
10. **Cleanup**: Remove temporary files and handle disk space

See Also
--------

- :doc:`../user-guide/python-api` - Python API reference
- :doc:`../user-guide/cli-reference` - Command-line options
- :doc:`python-integration` - More Python integration examples 