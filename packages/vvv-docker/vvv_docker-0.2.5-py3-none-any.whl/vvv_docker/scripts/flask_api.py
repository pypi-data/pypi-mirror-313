import vvv_docker
vvv = vvv_docker.init_worker('/root/vvv/vvv_test')
vvv.wrun_onnxruntime('vvv_test', r'''
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
''', ports=["18881:8000"]) # localfile if set auto update and set in docker