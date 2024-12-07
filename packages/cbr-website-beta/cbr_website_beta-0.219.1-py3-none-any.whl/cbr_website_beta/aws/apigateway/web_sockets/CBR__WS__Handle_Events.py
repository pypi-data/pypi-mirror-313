from cbr_website_beta.aws.apigateway.web_sockets.CBR__WS__DyDB import CBR__WS__DyDB
from osbot_aws.aws.apigateway.apigw_dydb.WS__Handle_Events import WS__Handle_Events


class CBR__WS__Handle_Events(WS__Handle_Events):
    dydb_ws: CBR__WS__DyDB