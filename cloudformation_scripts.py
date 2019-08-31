import boto3
import sys

cf = boto3.client('cloudformation', region_name='us-west-1')
""" :type: pyboto3.cloudformation """

cf_create_waiter = cf.get_waiter('stack_create_complete')


def launch_stack(keyname, sshlocation):
    parameters = [{'ParameterKey': key, 'ParameterValue': value} for key, value in locals().items()]

    with open('ucsc-instance-security-group.yaml', 'r') as file:
        stack_id = cf.create_stack(StackName='ucsc-assignment-9-stack',
                                   TemplateBody=file.read(),
                                   Parameters=parameters)['StackId']

    print(f'Creating stack with an id of {stack_id}...')
    cf_create_waiter.wait(StackName=stack_id)
    print('Created stack')

    stack_info = cf.describe_stacks(StackName=stack_id)['Stacks'][0]
    ip_address = [output['OutputValue'] for output in stack_info['Outputs'] if output['OutputKey'] == 'IpAddress'][0]
    return {'stack_id': stack_id, 'ip_address': ip_address}


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please call script with: [SSH KeyName] [SSH IP Address]')
        exit(1)

    print(f"IP Address of instance in stack: {launch_stack(sys.argv[1], sys.argv[2])['ip_address']}")
