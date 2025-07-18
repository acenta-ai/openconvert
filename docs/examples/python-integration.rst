Python Integration Examples
===========================

This page provides practical examples of integrating OpenConvert into Python applications.

Web Framework Integration
-------------------------

Flask Application
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from flask import Flask, request, send_file, jsonify, render_template
   from openconvert import convert_file
   import tempfile
   import os
   from werkzeug.utils import secure_filename

   app = Flask(__name__)
   app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

   ALLOWED_EXTENSIONS = {'txt', 'md', 'csv', 'jpg', 'png', 'gif'}

   def allowed_file(filename):
       return '.' in filename and \\
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

   @app.route('/')
   def index():
       return render_template('upload.html')

   @app.route('/convert', methods=['POST'])
   def convert_endpoint():
       """API endpoint for file conversion."""
       if 'file' not in request.files:
           return jsonify({'error': 'No file provided'}), 400
       
       file = request.files['file']
       
       if file.filename == '':
           return jsonify({'error': 'No file selected'}), 400
       
       if not allowed_file(file.filename):
           return jsonify({'error': 'File type not allowed'}), 400
       
       target_format = request.form.get('format', 'application/pdf')
       prompt = request.form.get('prompt', '')
       
       with tempfile.TemporaryDirectory() as temp_dir:
           # Save uploaded file
           filename = secure_filename(file.filename)
           input_path = os.path.join(temp_dir, filename)
           file.save(input_path)
           
           # Convert file
           output_filename = f"{os.path.splitext(filename)[0]}.pdf"
           output_path = os.path.join(temp_dir, output_filename)
           
           try:
               success = convert_file(
                   input_path,
                   output_path,
                   to_format=target_format,
                   prompt=prompt if prompt else None
               )
               
               if success:
                   return send_file(
                       output_path, 
                       as_attachment=True,
                       download_name=output_filename
                   )
               else:
                   return jsonify({'error': 'Conversion failed'}), 500
                   
           except Exception as e:
               return jsonify({'error': f'Conversion error: {str(e)}'}), 500

   @app.route('/formats')
   def list_formats():
       """Get available conversion formats."""
       # This would integrate with OpenConvert's format discovery
       formats = {
           'text/plain': ['application/pdf', 'text/html'],
           'image/jpeg': ['image/png', 'image/webp', 'application/pdf'],
           'text/csv': ['application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
       }
       return jsonify(formats)

   if __name__ == '__main__':
       app.run(debug=True)

FastAPI Application
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI, UploadFile, File, Form, HTTPException
   from fastapi.responses import FileResponse
   from openconvert import convert_file
   import tempfile
   import os
   from typing import Optional

   app = FastAPI(title="OpenConvert API", version="1.0.0")

   @app.post("/convert")
   async def convert_file_endpoint(
       file: UploadFile = File(...),
       target_format: str = Form("application/pdf"),
       prompt: Optional[str] = Form(None)
   ):
       """Convert uploaded file to specified format."""
       
       if not file.filename:
           raise HTTPException(status_code=400, detail="No file provided")
       
       with tempfile.TemporaryDirectory() as temp_dir:
           # Save uploaded file
           input_path = os.path.join(temp_dir, file.filename)
           with open(input_path, "wb") as buffer:
               content = await file.read()
               buffer.write(content)
           
           # Convert file
           output_filename = f"{os.path.splitext(file.filename)[0]}.pdf"
           output_path = os.path.join(temp_dir, output_filename)
           
           try:
               success = convert_file(
                   input_path,
                   output_path,
                   to_format=target_format,
                   prompt=prompt
               )
               
               if success:
                   return FileResponse(
                       output_path,
                       filename=output_filename,
                       media_type='application/octet-stream'
                   )
               else:
                   raise HTTPException(status_code=500, detail="Conversion failed")
                   
           except Exception as e:
               raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

   @app.get("/health")
   async def health_check():
       """Health check endpoint."""
       return {"status": "healthy"}

Django Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # views.py
   from django.shortcuts import render
   from django.http import HttpResponse, JsonResponse
   from django.views.decorators.csrf import csrf_exempt
   from django.core.files.storage import default_storage
   from django.core.files.base import ContentFile
   from openconvert import convert_file
   import tempfile
   import os
   import json

   @csrf_exempt
   def convert_view(request):
       if request.method == 'POST':
           if 'file' not in request.FILES:
               return JsonResponse({'error': 'No file provided'}, status=400)
           
           uploaded_file = request.FILES['file']
           target_format = request.POST.get('format', 'application/pdf')
           prompt = request.POST.get('prompt', '')
           
           with tempfile.TemporaryDirectory() as temp_dir:
               # Save uploaded file
               input_path = os.path.join(temp_dir, uploaded_file.name)
               with open(input_path, 'wb+') as destination:
                   for chunk in uploaded_file.chunks():
                       destination.write(chunk)
               
               # Convert file
               output_filename = f"{os.path.splitext(uploaded_file.name)[0]}.pdf"
               output_path = os.path.join(temp_dir, output_filename)
               
               try:
                   success = convert_file(
                       input_path,
                       output_path,
                       to_format=target_format,
                       prompt=prompt if prompt else None
                   )
                   
                   if success:
                       with open(output_path, 'rb') as f:
                           response = HttpResponse(
                               f.read(),
                               content_type='application/octet-stream'
                           )
                           response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                           return response
                   else:
                       return JsonResponse({'error': 'Conversion failed'}, status=500)
                       
               except Exception as e:
                   return JsonResponse({'error': str(e)}, status=500)
       
       return render(request, 'convert.html')

Desktop Application Integration
-------------------------------

Tkinter GUI Application
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tkinter as tk
   from tkinter import filedialog, messagebox, ttk
   from openconvert import convert_file
   import threading
   import os

   class OpenConvertGUI:
       def __init__(self, root):
           self.root = root
           self.root.title("OpenConvert GUI")
           self.root.geometry("600x400")
           
           self.setup_ui()
           
       def setup_ui(self):
           # File selection
           file_frame = ttk.Frame(self.root, padding="10")
           file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
           
           ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W)
           self.file_path = tk.StringVar()
           ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
           ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)
           
           # Output format selection
           format_frame = ttk.Frame(self.root, padding="10")
           format_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
           
           ttk.Label(format_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W)
           self.output_format = tk.StringVar(value="PDF")
           format_combo = ttk.Combobox(
               format_frame, 
               textvariable=self.output_format,
               values=["PDF", "Word Document", "PNG Image", "WebP Image"]
           )
           format_combo.grid(row=0, column=1, padx=5)
           
           # Prompt input
           prompt_frame = ttk.Frame(self.root, padding="10")
           prompt_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
           
           ttk.Label(prompt_frame, text="Conversion Prompt (optional):").grid(row=0, column=0, sticky=tk.W)
           self.prompt_text = tk.Text(prompt_frame, height=6, width=70)
           self.prompt_text.grid(row=1, column=0, columnspan=2, pady=5)
           
           # Convert button
           button_frame = ttk.Frame(self.root, padding="10")
           button_frame.grid(row=3, column=0)
           
           self.convert_button = ttk.Button(
               button_frame, 
               text="Convert File", 
               command=self.convert_file_threaded
           )
           self.convert_button.grid(row=0, column=0, padx=5)
           
           # Progress bar
           self.progress = ttk.Progressbar(button_frame, mode='indeterminate')
           self.progress.grid(row=0, column=1, padx=5)
           
           # Status label
           self.status_label = ttk.Label(self.root, text="Ready")
           self.status_label.grid(row=4, column=0, pady=5)
           
       def browse_file(self):
           filename = filedialog.askopenfilename(
               title="Select file to convert",
               filetypes=[
                   ("Text files", "*.txt"),
                   ("Markdown files", "*.md"),
                   ("CSV files", "*.csv"),
                   ("Image files", "*.jpg *.jpeg *.png *.gif"),
                   ("All files", "*.*")
               ]
           )
           if filename:
               self.file_path.set(filename)
               
       def get_mime_type(self, format_name):
           format_map = {
               "PDF": "application/pdf",
               "Word Document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
               "PNG Image": "image/png",
               "WebP Image": "image/webp"
           }
           return format_map.get(format_name, "application/pdf")
           
       def convert_file_threaded(self):
           """Run conversion in separate thread to avoid freezing UI."""
           thread = threading.Thread(target=self.convert_file_worker)
           thread.daemon = True
           thread.start()
           
       def convert_file_worker(self):
           input_path = self.file_path.get()
           
           if not input_path:
               messagebox.showerror("Error", "Please select an input file")
               return
               
           if not os.path.exists(input_path):
               messagebox.showerror("Error", "Input file does not exist")
               return
           
           # Start progress animation
           self.progress.start()
           self.convert_button.config(state='disabled')
           self.status_label.config(text="Converting...")
           
           try:
               # Generate output path
               base_name = os.path.splitext(input_path)[0]
               output_path = f"{base_name}_converted.pdf"
               
               # Get conversion parameters
               target_format = self.get_mime_type(self.output_format.get())
               prompt = self.prompt_text.get("1.0", tk.END).strip()
               
               # Perform conversion
               success = convert_file(
                   input_path,
                   output_path,
                   to_format=target_format,
                   prompt=prompt if prompt else None
               )
               
               # Update UI on main thread
               self.root.after(0, self.conversion_complete, success, output_path)
               
           except Exception as e:
               self.root.after(0, self.conversion_error, str(e))
               
       def conversion_complete(self, success, output_path):
           self.progress.stop()
           self.convert_button.config(state='normal')
           
           if success:
               self.status_label.config(text=f"Conversion completed: {output_path}")
               messagebox.showinfo("Success", f"File converted successfully!\\nOutput: {output_path}")
           else:
               self.status_label.config(text="Conversion failed")
               messagebox.showerror("Error", "Conversion failed")
               
       def conversion_error(self, error_message):
           self.progress.stop()
           self.convert_button.config(state='normal')
           self.status_label.config(text="Error occurred")
           messagebox.showerror("Error", f"Conversion error: {error_message}")

   if __name__ == "__main__":
       root = tk.Tk()
       app = OpenConvertGUI(root)
       root.mainloop()

Data Science Integration
------------------------

Jupyter Notebook Helper
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   import matplotlib.pyplot as plt
   from openconvert import convert_file
   import tempfile
   import os
   from IPython.display import display, HTML

   class NotebookConverter:
       """Helper class for converting data and plots in Jupyter notebooks."""
       
       def __init__(self):
           self.temp_files = []
           
       def dataframe_to_pdf(self, df, filename="data_report.pdf", prompt=None):
           """Convert DataFrame to PDF report."""
           with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
               df.to_csv(f.name, index=False)
               self.temp_files.append(f.name)
               
               success = convert_file(
                   f.name,
                   filename,
                   to_format="application/pdf",
                   prompt=prompt or "Create formatted data table with headers"
               )
               
               if success:
                   print(f"✅ DataFrame converted to {filename}")
                   return filename
               else:
                   print("❌ Conversion failed")
                   return None
                   
       def plot_to_pdf(self, fig, filename="plot.pdf", prompt=None):
           """Convert matplotlib figure to PDF."""
           with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
               fig.savefig(f.name, dpi=300, bbox_inches='tight')
               self.temp_files.append(f.name)
               
               success = convert_file(
                   f.name,
                   filename,
                   to_format="application/pdf",
                   prompt=prompt or "High quality plot for publication"
               )
               
               if success:
                   print(f"✅ Plot converted to {filename}")
                   return filename
               else:
                   print("❌ Conversion failed")
                   return None
                   
       def create_report(self, dataframes, plots, output_file="analysis_report.pdf"):
           """Create comprehensive report from multiple dataframes and plots."""
           # This would combine multiple elements into a single report
           # Implementation would depend on specific requirements
           pass
           
       def cleanup(self):
           """Clean up temporary files."""
           for temp_file in self.temp_files:
               try:
                   os.unlink(temp_file)
               except:
                   pass
           self.temp_files = []

   # Usage example
   converter = NotebookConverter()

   # Convert DataFrame
   df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
   converter.dataframe_to_pdf(df, "my_data.pdf", "Professional data table")

   # Convert plot
   fig, ax = plt.subplots()
   ax.plot([1, 2, 3], [4, 5, 6])
   converter.plot_to_pdf(fig, "my_plot.pdf", "Scientific publication quality")

   # Cleanup when done
   converter.cleanup()

Automation and Scripting
-------------------------

File Watcher Service
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import os
   from watchdog.observers import Observer
   from watchdog.events import FileSystemEventHandler
   from openconvert import convert_file
   import logging

   class ConversionHandler(FileSystemEventHandler):
       """Handler for automatic file conversion."""
       
       def __init__(self, output_dir, target_format="application/pdf", prompt=None):
           self.output_dir = output_dir
           self.target_format = target_format
           self.prompt = prompt
           
           # Ensure output directory exists
           os.makedirs(output_dir, exist_ok=True)
           
           # Setup logging
           logging.basicConfig(level=logging.INFO)
           self.logger = logging.getLogger(__name__)
           
       def on_created(self, event):
           """Handle new file creation."""
           if event.is_directory:
               return
               
           file_path = event.src_path
           
           # Only process certain file types
           if not self.should_process(file_path):
               return
               
           # Wait a moment for file to be fully written
           time.sleep(1)
           
           self.convert_file(file_path)
           
       def should_process(self, file_path):
           """Check if file should be processed."""
           _, ext = os.path.splitext(file_path)
           return ext.lower() in ['.txt', '.md', '.csv', '.jpg', '.png']
           
       def convert_file(self, input_path):
           """Convert the file."""
           try:
               filename = os.path.basename(input_path)
               name, _ = os.path.splitext(filename)
               output_path = os.path.join(self.output_dir, f"{name}.pdf")
               
               self.logger.info(f"Converting {input_path} to {output_path}")
               
               success = convert_file(
                   input_path,
                   output_path,
                   to_format=self.target_format,
                   prompt=self.prompt
               )
               
               if success:
                   self.logger.info(f"✅ Successfully converted {filename}")
               else:
                   self.logger.error(f"❌ Failed to convert {filename}")
                   
           except Exception as e:
               self.logger.error(f"Error converting {input_path}: {e}")

   def watch_directory(input_dir, output_dir, target_format="application/pdf", prompt=None):
       """Watch directory for new files and convert them automatically."""
       
       event_handler = ConversionHandler(output_dir, target_format, prompt)
       observer = Observer()
       observer.schedule(event_handler, input_dir, recursive=True)
       
       observer.start()
       print(f"Watching {input_dir} for new files...")
       
       try:
           while True:
               time.sleep(1)
       except KeyboardInterrupt:
           observer.stop()
           print("Stopping file watcher...")
           
       observer.join()

   # Usage
   if __name__ == "__main__":
       watch_directory(
           "input_files/",
           "converted_files/",
           prompt="Automatic conversion with professional formatting"
       )

Scheduled Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import schedule
   import time
   import os
   from pathlib import Path
   from openconvert import convert_file
   import logging
   from datetime import datetime

   class ScheduledConverter:
       """Scheduled batch file conversion service."""
       
       def __init__(self, input_dir, output_dir, archive_dir=None):
           self.input_dir = Path(input_dir)
           self.output_dir = Path(output_dir)
           self.archive_dir = Path(archive_dir) if archive_dir else None
           
           # Create directories
           self.output_dir.mkdir(exist_ok=True)
           if self.archive_dir:
               self.archive_dir.mkdir(exist_ok=True)
               
           # Setup logging
           logging.basicConfig(
               level=logging.INFO,
               format='%(asctime)s - %(levelname)s - %(message)s',
               handlers=[
                   logging.FileHandler('conversion_scheduler.log'),
                   logging.StreamHandler()
               ]
           )
           self.logger = logging.getLogger(__name__)
           
       def process_pending_files(self):
           """Process all pending files in input directory."""
           self.logger.info("Starting scheduled conversion batch")
           
           processed_count = 0
           failed_count = 0
           
           for file_path in self.input_dir.glob("*"):
               if file_path.is_file() and self.should_process(file_path):
                   try:
                       if self.convert_single_file(file_path):
                           processed_count += 1
                           
                           # Move to archive if configured
                           if self.archive_dir:
                               archive_path = self.archive_dir / file_path.name
                               file_path.rename(archive_path)
                               
                       else:
                           failed_count += 1
                           
                   except Exception as e:
                       self.logger.error(f"Error processing {file_path}: {e}")
                       failed_count += 1
           
           self.logger.info(f"Batch completed: {processed_count} successful, {failed_count} failed")
           
       def convert_single_file(self, file_path):
           """Convert a single file."""
           output_path = self.output_dir / f"{file_path.stem}.pdf"
           
           self.logger.info(f"Converting {file_path.name}")
           
           success = convert_file(
               str(file_path),
               str(output_path),
               to_format="application/pdf",
               prompt="Scheduled batch conversion with standard formatting"
           )
           
           if success:
               self.logger.info(f"✅ Converted {file_path.name}")
           else:
               self.logger.error(f"❌ Failed to convert {file_path.name}")
               
           return success
           
       def should_process(self, file_path):
           """Check if file should be processed."""
           return file_path.suffix.lower() in ['.txt', '.md', '.csv']
           
       def start_scheduler(self):
           """Start the scheduled processing."""
           # Schedule conversions
           schedule.every().hour.do(self.process_pending_files)
           schedule.every().day.at("09:00").do(self.process_pending_files)
           schedule.every().monday.at("08:00").do(self.weekly_cleanup)
           
           self.logger.info("Scheduler started")
           
           while True:
               schedule.run_pending()
               time.sleep(60)  # Check every minute
               
       def weekly_cleanup(self):
           """Weekly cleanup of old files."""
           self.logger.info("Running weekly cleanup")
           # Implement cleanup logic here
           pass

   # Usage
   if __name__ == "__main__":
       converter = ScheduledConverter(
           input_dir="incoming/",
           output_dir="converted/",
           archive_dir="processed/"
       )
       converter.start_scheduler()

See Also
--------

- :doc:`../user-guide/python-api` - Complete Python API reference
- :doc:`batch-processing` - Batch processing examples
- :doc:`../user-guide/advanced-usage` - Advanced usage patterns 