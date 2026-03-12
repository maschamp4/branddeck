import os
from flask import Flask, render_template, request, send_file
import subprocess
import urllib.parse
from brand_agency_generator import extract_domain_name

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error='Please provide a valid URL')

        # Clean URL to get brand name for file searching
        try:
            if not url.startswith('http://') and not url.startswith('https://'):
                process_url = 'https://' + url
            else:
                process_url = url
            brand_name = extract_domain_name(process_url)
        except Exception as e:
            return render_template('index.html', error=f'Error processing URL: {str(e)}')

        # Run the generator script
        try:
            subprocess.run(['python', 'brand_agency_generator.py', url], check=True)
            
            # Find the generated zip file
            zip_filename = f"{brand_name}_Brand_Assets.zip"
            zip_path = zip_filename
            
            if os.path.exists(zip_path):
                return send_file(zip_path, as_attachment=True)
            else:
                return render_template('index.html', error='Zip file was not generated successfully.')
                
        except subprocess.CalledProcessError as e:
            return render_template('index.html', error='Error during generation.')
        except Exception as e:
            return render_template('index.html', error=f'An unexpected error occurred: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
