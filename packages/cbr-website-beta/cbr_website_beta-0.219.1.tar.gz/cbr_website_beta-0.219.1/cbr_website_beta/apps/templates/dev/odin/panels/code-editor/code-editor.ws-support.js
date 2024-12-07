

function set_ws_connection()
    {
        //$('#debug_message').html('about to create a WS connection')

        window.ws     = new WebSocket("{{ user_data.get('endpoint_url') }}")
        ws.onopen     = send__register_browser
        ws.onmessage  = on_message
    }

function send__register_browser() {
    let message = { command: 'register', name : 'qa-device', state: 'connected'}
    ws.send(JSON.stringify(message))
}

    function on_message (message) {
        //console.log('Received:', message.data);
        ws_message = JSON.parse(message.data)
        if (ws_message.topic === 'system'){
            ws.close()
            console.log('>>> System message (reloading panel) <<<<')
            loadPanel()
        }
        else {
            if (ws_message.data?.eval) {
                let js_script = ws_message.data.eval
                eval(js_script)
                ws_message.data = `executed js script with size ${js_script.length}`
                console.log(ws_message)
            }
        }
    }

set_ws_connection()