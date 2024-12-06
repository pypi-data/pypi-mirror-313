var table = undefined

    function setup_table() {
        var table_config = { dom        : '<"top"f>rt<"bottom"i><"clear">',
                             pageLength : -1                              ,
                             order      : [[1, 'desc']]                   ,
                             columnDefs : [ { targets: 0, width: '10px' }  ,
                                            { targets: 1, width: '10%' }  ,
                                            { targets: 2, width: '10%' }  ,
                                            { targets: 0, // New index column
                                              orderable: false, // Makes the index column non-orderable
                                              searchable: false, // Makes the index column non-searchable
                                              render: function(data, type, row, meta) {
                                                 return meta.row + 1; // Uses the row's meta-data to start index at 1
                                              }}]}
        table = $('#table-logs').DataTable(table_config);
    }
    function add_row(message)
    {
        let when  = message.when
        let topic = message.topic
        let data  = message.data
        if (typeof data != 'string') {
            data = JSON.stringify(data)
        }
        table.row.add([ 0, when, topic, data]).draw(false)
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
            }
            add_row(ws_message)
        }
    }

    function set_ws_connection()
    {
        //$('#debug_message').html('about to create a WS connection')

        let ws = new WebSocket("{{ user_data.get('endpoint_url') }}")
        ws.onopen = function () {
            //$('#debug_message').html('WS connection open')
            //console.log('Created a WS connection')

            send__register_browser()
            //submit_ws_message()
        };
        ws.onmessage = on_message
        // Handle WebSocket closure
        ws.onclose = function (event) {
            //console.log('WebSocket closed:', event);
        };

        // Handle potential closure errors
        ws.onerror = function (event) {
            console.error('WebSocket error observed:', event);
        };


        //console.log(ws)
        window.ws = ws
    }
    function send__register_browser() {
        let message = { command: 'register', name : 'qa-device', state: 'connected'}
        ws.send(JSON.stringify(message))
    }

    $(document).ready(function() {
        setup_table()
        set_ws_connection()
    });

