import boto3
import sys

cf = boto3.client('cloudformation', region_name='us-west-1')
""" :type: pyboto3.cloudformation """


def launch_stack(keyname, sshlocation):
    parameters = [{'ParameterKey': key, 'ParameterValue': value} for key, value in locals().items()]

    with open('ucsc-instance-security-group.yaml', 'r') as file:
        return cf.create_stack(StackName='ucsc-assignment-9-stack',
                               TemplateBody=file.read(),
                               Parameters=parameters)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please call script with: [SSH KeyName] [SSH IP Address]')
        exit(1)

    print(f"Stack id: {launch_stack(sys.argv[1], sys.argv[2])}")
