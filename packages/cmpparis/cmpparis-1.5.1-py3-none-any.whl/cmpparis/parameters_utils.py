import boto3

aws_region_name = 'eu-west-3'

def get_region_name():
    return aws_region_name

### SSM Parameter Store ###

def get_parameter(system, param_name):
    try:
        ssm = boto3.client('ssm', region_name=aws_region_name)

        if 'password' in param_name:
            parameter = ssm.get_parameter(Name=f'/{system}/{param_name}', WithDecryption=True)
            param_value = parameter['Parameter']['Value']
        else:
            parameter = ssm.get_parameter(Name=f'/{system}/{param_name}')
            param_value = parameter['Parameter']['Value']

        return param_value
    except Exception as e:
        print(f"An error occurred while trying to retrieve parameter {param_name} : {e}")