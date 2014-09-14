from flask import Flask, send_file, request
import subprocess, os, re
app = Flask(__name__)

hashes = set()
image_dir = 'avatars'
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

def get_path(fname):
    i = 1
    while True:
        path = os.path.join(image_dir, fname.replace('.', '%05d.' % i))
        if not os.path.exists(path):
            return path, i
        i += 1

@app.route('/')
def index():
    return send_file('faces.html', 'text/html')

@app.route('/facesjs/faces.js')
def js():
    return send_file('facesjs/faces.js', 'application/javascript')

@app.route("/svg", methods=['POST'])
def svg():
    svg = request.data
    h = hash(svg)
    if h in hashes:
        print 'face already exists'
        return 'face already exists'
    hashes.add(h)
    width, height = re.search('viewBox="\d+ \d+ (\d+) (\d+)"', svg).groups()
    background = '<rect width="%s" height="%s" style="fill:white" />' % (width, height)
    svg = re.sub(r'(<svg.*?>)', r'\1' + background, svg)

    svgpath = 'face.svg'
    open(svgpath, 'w').write(svg)
    imagepath, i = get_path('face.png')
    if i > 1000:
        os.remove(svgpath)
        print 'generated all images'
        return 'generated all images', 500
    subprocess.call('inkscape -f %s -e %s' % (svgpath, imagepath), shell = True)
    os.remove(svgpath)
    print 'image saved to %s' % imagepath
    return 'processed'

if __name__ == "__main__":
    app.run(debug=True)