import requests

def exec_command(cmd):
    res = {}
    if cmd['type'] == 'api':
        res['response'] = requests.get(cmd['url']).text
        
    return res