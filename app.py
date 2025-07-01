from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    image_file = request.files['image']
    width = int(request.form.get('width', 40))
    height = int(request.form.get('height', 40))
    margin_right = int(request.form.get('margin_right', 10))
    margin_bottom = int(request.form.get('margin_bottom', 10))
    
    img = Image.open(image_file)
    img = img.resize((width, height))
    
    # Create new image with margins
    new_img = Image.new('RGBA', (width + margin_right, height + margin_bottom), (0, 0, 0, 0))
    new_img.paste(img, (0, 0))
    
    img_io = io.BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)