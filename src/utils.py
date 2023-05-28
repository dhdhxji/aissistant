import requests
import mqtt_executor as mqtt

def exec_command(cmd):
    res = {}
    if cmd['type'] == 'api':
        res['response'] = requests.get(cmd['url']).text
    
    elif cmd['type'] == 'mqtt':
        res['response'] = mqtt.get_retained_message(
            cmd['topic']
        )
    
    return res