import re
import time
import json
import types
import queue
from json import JSONDecodeError
try:
    from websocket import WebSocketTimeoutException, WebSocketConnectionClosedException, WebSocketException, create_connection
except:
    from .websocket import WebSocketTimeoutException, WebSocketConnectionClosedException, WebSocketException, create_connection
from threading import Thread, Event
from urllib import request

import socket
def get_ip_address(domain):
    if re.findall(r'\d+\.\d+\.\d+\.\d+', domain):
        return domain
    try:
        return socket.gethostbyname(domain)
    except: 
        return domain

def remote_client(host, debug=False):
    host = re.sub('^https?://|^:?//||^wss?://', '', host)
    host = host.split('/')[0]
    hostname, port = host.split(':', 1) if ':' in host else (host, 18999)
    hostname = get_ip_address(hostname)
    def myget(url):
        r = request.Request(url, method='GET')
        opener = request.build_opener(request.ProxyHandler(None))
        return json.loads(opener.open(r).read().decode())
    def adj_wsurl(wsurl): return re.sub('ws://[^/]+/devtools/', 'ws://{}:{}/devtools/'.format(hostname, port), wsurl)
    s = myget('http://{}:{}/json'.format(hostname, port))
    wsurl = adj_wsurl(s[0]['webSocketDebuggerUrl'])
    def try_json_result(data):
        try:
            data = json.loads(data)['result']
            return data
        except:
            return data
    def try_run_result(data):
        is_err = False
        try:
            if data['result'].get('type') == 'undefined':
                return None
            elif data['result'].get('subtype') == 'null':
                return '<NULL>'
            elif data['result'].get('value', None) != None:
                return data['result']['value']
            elif data['result'].get('description'):
                is_err = data['result']['description']
            else:
                raise Exception('err')
        except:
            return data
        if is_err:
            raise Exception(is_err)
    def is_function(obj):
        return type(obj) == types.FunctionType
    class Err: pass
    class _:
        def __init__(self, wsurl):
            self.ws = create_connection(wsurl)
            self.id = 0
            self.qret = {}
            self._xid = 0
            self.irun = {}
            self.loop_recv = Thread(target=self.start_loop)
            self.loop_recv.daemon = True
            self.loop_recv.start()
            self.cdp("Page.enable", {})
            # self.cdp("Network.enable", {})
            # self.cdp("Fetch.enable", {})
            # self.set_method_callback("Fetch.requestPaused", func)
        def start_loop(self):
            while True:
                try:
                    rdata = json.loads(self.ws.recv())
                    if debug:
                        print('------------------------------')
                        print(rdata)
                except WebSocketTimeoutException:
                    continue
                except (WebSocketException, OSError, WebSocketConnectionClosedException, JSONDecodeError) as e:
                    raise e
                method = rdata.get('method')
                if method in self.irun:
                    for xid in self.irun[method]:
                        m = self.irun[method].get(xid, None)
                        if m:
                            if is_function(m):
                                m(rdata)
                            if isinstance(m, queue.Queue):
                                m.put(rdata['params'])
                if rdata.get('id') in self.qret:
                    if rdata.get('result', Err) != Err:
                        self.qret[rdata.get('id')].put(rdata['result'])
                    elif rdata.get('error', Err) != Err:
                        self.qret[rdata.get('id')].put(rdata['error'])
                    else:
                        print(rdata, repr(rdata.get('result')))
                        raise Exception('un expect err.' + repr(rdata.get('result')))
        def get_id(self):
            self.id += 1
            return self.id
        def get_xid(self):
            self._xid += 1
            return self._xid
        def cdp(self, protocal, data, only_send=False):
            rid = self.get_id()
            cmd = { "id": rid, "method": protocal, "params": data }
            if debug:
                print('====>', rid, protocal)
            self.qret[rid] = queue.Queue()
            try:
                self.ws.send(json.dumps(cmd))
            except (OSError, WebSocketConnectionClosedException):
                self.qret.pop(rid, None)
                return
            if only_send:
                return
            while True:
                try:
                    ret = self.qret[rid].get(timeout=.15)
                    self.qret.pop(rid, None)
                    return try_run_result(ret)
                except queue.Empty:
                    continue
        def wait_once_method(self, method, timeout=10):
            self.irun[method] = self.irun.get(method, {})
            xid = self.get_xid()
            self.irun[method][xid] = queue.Queue()
            start = time.time()
            while True:
                try:
                    ret = self.irun[method][xid].get(timeout=0.15)
                    self.irun[method].pop(xid, None)
                    return ret
                except:
                    if time.time() - start > timeout:
                        raise Exception('wait_once_method {} timeout: {}'.format(method, timeout))
                    continue
        def go_url(self, url):
            self.cdp("Page.navigate", {"url": url})
            self.wait_once_method("Page.domContentEventFired")
        def set_method_callback(self, method, func):
            self.irun[method] = self.irun.get(method, {})
            self.irun[method][self.get_xid()] = func
        def run_script(self, script):
            return self.cdp('Runtime.evaluate', { 
                "expression": script, 
                "awaitPromise": True, 
                "returnByValue": True 
            })
        def add_script(self, script):
            ret = self.cdp("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            return int(ret['identifier'])
        def remove_script(self):
            idx = self.add_script("")
            for i in range(1, idx+1):
                self.cdp("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(i)})
    return _(wsurl)


if __name__ == '__main__':
    pass