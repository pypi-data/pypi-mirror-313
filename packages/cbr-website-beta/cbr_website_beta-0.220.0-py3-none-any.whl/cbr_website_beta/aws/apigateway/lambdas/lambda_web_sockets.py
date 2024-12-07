from cbr_website_beta.aws.apigateway.web_sockets.CBR__WS__Handle_Events import CBR__WS__Handle_Events

ws_handle_events = CBR__WS__Handle_Events()

def run(event, context):
    return ws_handle_events.handle_lambda(event, context)

