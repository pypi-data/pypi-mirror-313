import vvv_docker
vvv = vvv_docker.init_worker()
vvv.wrun_onnxruntime('vvv_test', '''
import io
import json
import base64

import flask
import requests
import cv2 # opencv-python-headless
import numpy as np
from PIL import Image
import onnxruntime as ort

def read_b64img(b64img):
    import os
    import tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    temp_name = temp.name
    try:
        img = base64.b64decode(b64img.split('base64,')[-1].encode())
        with open(temp_name, 'wb') as temp_file:
            temp_file.write(img)
        img = cv2.imdecode(np.fromfile(temp_name, dtype=np.uint8), 1)
    finally:
        os.remove(temp_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (40, 40))
    img = np.transpose(img, (2,1,0))
    img = np.expand_dims(img.astype(np.float32), axis=0)
    return img

class_path = "clz_net.claz"
model_path = "clz_net.onnx"
with open(class_path) as f:
    d = json.loads(f.read())

class_types = d['class_types']
session = ort.InferenceSession(model_path)

# empty img for test.
b64img = 'data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABmAFYDASIAAhEBAxEB/8QAGAABAQEBAQAAAAAAAAAAAAAAAAECAwT/xAAqEAACAQIEBgIDAAMAAAAAAAAAARECIRJh0fAxQVFxgaHB4SKRsULi8f/EABgBAQEBAQEAAAAAAAAAAAAAAAABAgMK/8QAKBEAAgECBQIHAQEAAAAAAAAAAAERIfACEjFh0VFxIkFSgZGx8cGh/9oADAMBAAIRAxEAPwD0AA9EB5HwAAAADDxOHRrem3N1gRqYyclAMJttJuVKp104uWAADcL0Py/l/M6uAAAheh+X8v5nVwAANtpVYABqlJuH00MPGopr27X7dgZB1wLq/WgwLq/WhzzN0bunFywYaWFPm3roRRN3C3kzrhUJXhfepzqSThdNSaANUxZtveSMlSnml3sGo5p9nJrNi6u/z76sEBUp5pd7AZsXV3+ffVg61ptW66mFQ5vZd19nXxP7+Gizkl+/ls3ibafhatc3WM51vcX7dp54F1frQqpScqTQORHicOjW9NubrAAFWq86owsTlS6efal/oMulNy5NA04h+GN/i7cbz4d/i7T2nm6Uo5y0r59oNYKe3nWStTGTkpgudb3F+3acYKc3vKAbAGZ+l3HP+d4AAuZujd04uWcdCqJu4W8maijq9+CUtJ36aG3Wotd9n9ELmbo3dOLlmGqYs23vJGTTqbUOCKJu4W8mNCEKom7hbyZqKOr34KnQnKb34Lmbo3dOLlgy1TFm295IydK6k1Z888zmQaAAAubF1d/n31ZY/Gc49BRN3C3kzSjDdwsXx2ZU6E5Te/AIFhUulttJ8f8AiEqqn8rX5dvJp1Jpw+T6ko4Pv8IAzFHV78FToTlN78G20uJMa5XfS+gAx09fT0GOnr6ehl1tf4x3n6NYoSb5xw7AEbpahv09DDVMWbb3kjeOnNbykN0tQ36egBMNKSbbUxvgC4rJU3ayfD1kACqKaVL438tZdhjp6+noWVSlPDgFUnwf9AJKqlJ8ipJKEUAAjaSu432ZSNpcQDDdL41P9f6mk6XbjC5rxzQx09fT0Kqk+D/oBhVJNykkpUpX4m1Unwf9CpSbd7lAAAAAAAAAAAAAAAAAAAAAAP/Z'
input_data = read_b64img(b64img)
outputs = session.run(None, {'input': input_data})
output = outputs[0][0].tolist()
print(output,max(output))
output = class_types[output.index(max(output))]


print(output)
print()


import json
import flask
import requests
from flask import Flask, request, make_response
app = Flask(__name__)
@app.route('/', methods=['GET'])
def main():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>test</title>
    <meta charset="utf-8">
    <script type="text/javascript" src="/test_js.js"></script>
</head>
<body>
    <form id="myForm">
        <label for="aaa">参数 aaa:</label><input type="text" id="aaa" style="width: 800px"><br><br><script>init_storage("aaa")</script>
        <label for="bbb">参数 bbb:</label><input type="text" id="bbb" style="width: 800px"><br><br><script>init_storage("bbb")</script>
        <button type="submit" id="test_get">get提交</button>
        <button type="submit" id="test_post">post提交</button>
    </form>
    <h3>返回参数:</h3>
    <textarea id="response" rows="100" style="width: 100%" readonly></textarea>
</body>
</html>
"""

@app.route('/test_js.js', methods=['GET'])
def test_js():
    rdata = """
var k = []
var l = localStorage
function init_storage(id){
    var v = document.getElementById(id)
    v.addEventListener('input', function(e){l[id] = v.value.trim()})
    v.value = l[id] || ''; if (k.indexOf(id) == -1){ k.push(id) }
    v.ondragover = function(e) { e.preventDefault(); }
    v.ondrop = function(e) {
        e.preventDefault(); var f = e.dataTransfer.files[0]; var fr = new FileReader(); fr.readAsDataURL(f);
        fr.onload = function(e) { l[id] = v.value = this.result.trim(); } } }
window.onload = function(){
    function get_all_kv(){
        var r=[]; for (var i = 0; i < k.length; i++) { var n=k[i];var v=l[n];r.push(n+'='+encodeURIComponent(v)) }
        return r.join('&') }
    function res(p){p.then(response => response.text()).then(data => {
            document.getElementById('response').value = data;
        })}
    test_get.addEventListener('click', function(event) {
        event.preventDefault(); res(fetch('/api_get?' + get_all_kv()))
    });
    test_post.addEventListener('click', function(event) {
        event.preventDefault(); res(fetch('/api_post', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: get_all_kv() }))
    });
}
    """
    response = make_response(rdata)
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/api_get', methods=['GET'])
def api_get():
    adict = dict(request.args)
    rdict = adict
    rdata = json.dumps(rdict, indent=4, separators=(',', ':'), ensure_ascii=False)
    response = make_response(rdata)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api_post', methods=['POST'])
def api_post():
    fdict = dict(request.form)
    rdict = fdict
    rdata = json.dumps(rdict, indent=4, separators=(',', ':'), ensure_ascii=False)
    response = make_response(rdata)
    response.headers['Content-Type'] = 'application/json'
    return response

app.run('0.0.0.0', port=8000)
''', ports=["18881:8000"], files=["clz_net.claz", "clz_net.onnx"]) # localfile if set auto update and set in docker