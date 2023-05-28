import requests
import mqtt_executor as mqtt

def exec_command(cmd):
    #res = {}
    if cmd['type'] == 'api':
        cmd['response'] = requests.get(cmd['url']).text
    
    elif cmd['type'] == 'mqtt':
        cmd['response'] = mqtt.get_retained_message(
            cmd['topic']
        )
    
    return cmd