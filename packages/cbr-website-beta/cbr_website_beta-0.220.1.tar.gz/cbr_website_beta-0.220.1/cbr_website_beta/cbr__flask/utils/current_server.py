# todo: find a better solution to get the DNS name of the current server, since at the moment
#       it requests an hard-coded value added to CloudFront (Cloudfront-Domain)
from flask import request


def current_server():
    cloud_front_domain = request.headers.get('Cloudfront-Domain')
    if cloud_front_domain:
        server_url = cloud_front_domain
    else:

        forwarded_proto = request.headers.get('X-Forwarded-Proto', 'http')          # Fallback to checking for 'X-Forwarded-Proto' and 'Host' headers
        host = request.headers.get('Host', request.host)                                   # Use 'Host' header if forwarded
        server_url = f"{forwarded_proto}://{host}"
    if server_url.endswith('/') is False:
        server_url += '/'
    return server_url

# if 'http://' in current_server:                                                             # todo: figure out better solution for this (currently seen when proxying traffic via ngrok)
    #     if current_server.startswith('http://localhost') is False:                              # can't do this for localhost
    #         if current_server.startswith('http://127.0.0.1') is False:  # can't do this for localhost
    #             print(f'note: need to fix current_server since it is http: {current_server}')       # todo: add to main logging class (when wired up to DynamoDB)
    #             current_server = current_server.replace('http://', 'https://')