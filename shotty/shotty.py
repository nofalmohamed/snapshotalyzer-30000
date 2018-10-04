import boto3
import click

session = boto3.Session(profile_name='dynamodb')
ec2 = session.resource('ec2')

def filter_instances(name):
    instances = []

    if name is not None:
        filters = [{'Name':'tag:Name', 'Values':[name]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    "Commands for instances"

@instances.command('list')
@click.option('--name', default=None,
    help="Only instances with displayName (tag Name:<name>)")
def list_instances(name):
    "List EC2 Instances"

    instances = filter_instances(name)
    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Name', '<no name>'))))

    return


@instances.command('stop')
@click.option('--name', default=None, help='Only instances with name')

def stop_instances(name):
    "Stop EC2 instances"

    instances = []

    instances = filter_instances(name)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--name', default=None, help='Only instances with name')

def start_instances(name):
    "Start EC2 instances"

    instances = []

    instances = filter_instances(name)

    for i in instances:
        print("Start {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    instances()
