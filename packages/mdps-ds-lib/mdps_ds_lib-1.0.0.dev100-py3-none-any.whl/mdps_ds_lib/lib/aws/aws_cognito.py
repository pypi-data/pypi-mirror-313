from mdps_ds_lib.lib.aws.aws_cred import AwsCred


class AwsCognito(AwsCred):
    def __init__(self, user_pool_id: str):
        super().__init__()
        self.__cognito = self.get_client('cognito-idp')
        self.__user_pool_id = user_pool_id

    def get_groups(self, username: str):
        response = self.__cognito.admin_list_groups_for_user(
            Username=username,
            UserPoolId=self.__user_pool_id,
            Limit=60,
            # NextToken='string'
        )
        if response is None or 'Groups' not in response:
            return []
        belonged_groups = [k['GroupName'] for k in response['Groups']]
        return belonged_groups
