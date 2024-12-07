# import boto3
# from osbot_aws.helpers.IAM_User import IAM_User
#
# from osbot_aws.helpers.IAM_Role import IAM_Role
#
# from osbot_aws.apis.IAM import IAM
#
#
# class Logs_Permission_Checker:
#
#     def __init(self):
#         pass
#
#     def get_current_role_name(self):
#         sts = boto3.client('sts')
#         identity = sts.get_caller_identity()
#         arn_parts = identity['Arn'].split(':')
#         role_name = arn_parts[-1].split('/')[-1]
#         return role_name
#
#     def get_role_policies(self, role_name):
#         iam = boto3.client('iam')
#         policies = iam.list_attached_role_policies(RoleName=role_name)
#         return [policy['PolicyArn'] for policy in policies['AttachedPolicies']]
#
#     def get_policy_permissions(self, policy_arn):
#         iam = boto3.client('iam')
#         policy = iam.get_policy_version(
#             PolicyArn=policy_arn,
#             VersionId='v1'  # You might want to find the correct version dynamically
#         )
#         return policy['PolicyVersion']['Document']['Statement']
#
#
#     def check_permissions(self, required_permissions):
#         role_name = self.get_current_role_name()
#         print('----------: role_name', role_name)
#
#         iam_user = IAM_User(user_name=role_name)
#         print(f'----iam_user: policies     : {iam_user.policies()}'     )
#         print(f'----iam_user: user policies: {iam_user.user_policies()}')
#
#         iam_role = IAM_Role(role_name=role_name)
#         print(f'----iam_role: policies     : { list(iam_role.policies())}')
#         print(f'----iam_role: policies_statements: {iam_role.policies_statements()}')
#         policy_arns = iam_user.user_policies()
#         return policy_arns
#
#         # role_name = self.get_current_role_name()
#         # policy_arns = self.get_role_policies(role_name)
#
#         for policy_arn in policy_arns:
#             permissions = self.get_policy_permissions(policy_arn)
#             for permission in permissions:
#                 action = permission['Action']
#                 if set(action).intersection(set(required_permissions)):
#                     print(f"Required permissions are present in policy: {policy_arn}")
#                     return True
#         print("Required permissions are not present.")
#         return False
