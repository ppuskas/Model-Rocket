from flask import Flask, render_template, request
import asyncio
import sys
from pathlib import Path
import os

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from manage import main as manage_main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = False
    summary = None

    if request.method == 'POST':
        action = request.form.get('action')
        test_mode = 'test_mode' in request.form
        
        # Build command line arguments
        sys.argv = ['manage.py']
        if action == 'scan':
            sys.argv.append('--scan')
        elif action == 'setup':
            sys.argv.append('--setup')
        elif action == 'download':
            sys.argv.append('--download')
        
        if test_mode:
            sys.argv.append('--test')

        try:
            # Capture stdout to get the summary
            import io
            import contextlib
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                asyncio.run(manage_main())
            
            summary = output.getvalue()
            message = f"Successfully completed {action}"
        except Exception as e:
            message = f"Error during {action}: {str(e)}"
            error = True

    return render_template('index.html', message=message, error=error, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
