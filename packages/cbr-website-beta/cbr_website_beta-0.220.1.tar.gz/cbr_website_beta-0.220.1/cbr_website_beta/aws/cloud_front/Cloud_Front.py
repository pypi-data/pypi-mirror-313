from unittest import TestCase

from osbot_aws.aws.cloud_front.Cloud_Front import Cloud_Front as OSBot_AWS__Cloud_Front
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_guid


class Cloud_Front(OSBot_AWS__Cloud_Front):

    def distribution_create(self, create_kwargs):
        target           = create_kwargs.get('target' )
        cname_alias      = create_kwargs.get('cname'  )
        origin_id        = target
        domain_name      = target
        target_origin_id = target

        cache_policy_id          = '4135ea2d-6df8-44a3-9df3-4b5a84be39ad'
        origin_request_policy_id = 'b689b0a8-53d0-40ab-baf2-68738e2966ac'
        amc_certificate_arn      = 'arn:aws:acm:us-east-1:654654216424:certificate/1834a525-23d5-4931-b6f1-784aa962b9bb'
        caller_reference = random_guid()
        origin_item      = { 'Id'               : origin_id                                                              ,
                             'DomainName'       : domain_name                                                            ,
                             'CustomOriginConfig': { 'HTTPPort'              : 80                                       ,
                                                     'HTTPSPort'             : 443                                      ,
                                                     'OriginProtocolPolicy'  : 'https-only'                             ,
                                                     'OriginSslProtocols'    : { 'Quantity': 1, 'Items': [ 'TLSv1.2' ] },
                                                     'OriginReadTimeout'     : 30                                       ,
                                                     'OriginKeepaliveTimeout': 5                                        },
                             'ConnectionAttempts': 3                                                                     ,
                             'ConnectionTimeout' : 10                                                                    }
        distribution_config = { 'CallerReference'     : caller_reference                                                                 ,
                                'Aliases'             : { 'Quantity': 1, 'Items': [ cname_alias ]}                                       ,
                                'Origins'             : { 'Quantity': 1, 'Items': [ origin_item ]}                                       ,
                                'DefaultCacheBehavior': { 'TargetOriginId'      : target_origin_id                                      ,
                                                          'ViewerProtocolPolicy': 'redirect-to-https'                                   ,
                                                          'AllowedMethods'       : { 'Quantity'      : 2                               ,
                                                                                     'Items'         : [ 'HEAD', 'GET' ]               ,
                                                                                     'CachedMethods' : { 'Quantity': 2                 ,
                                                                                                         'Items'   : [ 'HEAD', 'GET' ]}},
                                                          'Compress'             : True                                                 ,
                                                          'CachePolicyId'        : cache_policy_id                                      ,
                                                          'OriginRequestPolicyId': origin_request_policy_id                             },
                                'Comment'               : cname_alias                                                                    ,
                                'PriceClass'            : 'PriceClass_All'                                                               ,
                                'Enabled'               : True                                                                           ,
                                'ViewerCertificate'     : { 'ACMCertificateArn'           : amc_certificate_arn                         ,
                                                            'CertificateSource'           : 'acm'                                       ,
                                                            'SSLSupportMethod'            : 'sni-only'                                  ,
                                                            'MinimumProtocolVersion'      : 'TLSv1.2_2021'                              ,
                                                            'CloudFrontDefaultCertificate': False                                       },
                                'Restrictions'          : { 'GeoRestriction'              : { 'RestrictionType'  : 'none'              ,
                                                                                              'Quantity'         : 0                   }},
                                'HttpVersion'           : 'http2'                                                                        ,
                                'IsIPV6Enabled'         : True                                                                           }

        # Create the CloudFront distribution
        response = self.client().create_distribution(DistributionConfig=distribution_config)
        return response.get('Distribution')



class test_Cloud_Front(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cloud_front = Cloud_Front()

    def test_distribution_create(self):
        version          = 'v0.105.2b'
        version_fixed    = version.replace('.', '-')
        function_url     = self.cloud_front.util_lambda_function_url(version_fixed)
        cname            = f'{version_fixed}.dev.aws.cyber-boardroom.com'
        cf_create_kwargs = dict(cname         = cname        ,
                                function_url  = function_url ,
                                version       = version      ,
                                version_fixed = version_fixed)
        response         = self.cloud_front.distribution_create(cf_create_kwargs)
        pprint(response)

    def test_create_domain(self):
        version                 = 'v0.105.2b'
        version_fixed           = version.replace('.', '-')
        cname                   = f'{version_fixed}.dev.aws.cyber-boardroom.com'
        alias_hosted_zone_id    = 'Z2FDTNDATAQYW2'
        hosted_zone_id          = 'Z05928161JB8L596PJ130'
        cloud_front_domain_name = 'dfq6zt3ic86b.cloudfront.net'

        dns_create_kwargs       = dict(cname                = cname                   ,
                                       target               = cloud_front_domain_name ,
                                       alias_hosted_zone_id = alias_hosted_zone_id    ,
                                       hosted_zone_id       = hosted_zone_id          ,
                                       version_fixed        = version_fixed           )
        response                = self.cloud_front.add_dns_entry_for_cloud_front(dns_create_kwargs)
        pprint(response)

    def test_distributions(self):
        with self.cloud_front as _:
            pprint(_.distributions())

