import boto3
import argparse
import yaml

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
    parser = argparse.ArgumentParser(
        usage='launch_stack.py [-h] --file FILE | --key KEY --ip-address IP_ADDRESS',
        description='Create a stack with a web server. Requires a YAML file with params or entered via command line.'
    )

    parser.add_argument('--file', '-f', help='Parameters for cloudformation in YAML format.]', type=argparse.FileType('r'))

    parser.add_argument('key-name', nargs='?', help='SSH Key Name')
    parser.add_argument('ip-address', nargs='?', help='IP Address for ssh')

    args = vars(parser.parse_args())

    if not args['file'] and not (args['key-name'] and args['ip-address']):
        print('Either [--file FILE] or [key ip-address] is required')
        exit(1)

    if args['file']:
        params = yaml.safe_load(args['file'].read())
    else:
        params = {
            'key_name': args['key-name'],
            'ip_address': args['ip-address']
        }

    print("IP Address of instance in stack: "
          f"{launch_stack(params['key_name'], params['ip_address'])['ip_address']}")

    print('Please wait a moment for instance to finish initialization.')
