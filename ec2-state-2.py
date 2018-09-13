#!/bin/env python

import boto3
from termcolor import colored
from collections import Counter
from operator import itemgetter


ec2 = boto3.resource('ec2')


def get_instance_name(id):
    ec2_instance = ec2.Instance(id)
    instance_name = ''
    for tag in ec2_instance.tags or []:
        if tag["Key"] == 'Name':
            instance_name = tag["Value"]
    return instance_name


def print_instance_list(*args):
    ec2_list, count_running, count_stopped = args
    state_color = ''
    for i in ec2_list:
        if i['state'] == 'running':
            state_color = 'green'
        else:
            state_color = 'red'

        if i['Name']:
            print("Name: {:<40s} ID: {:<40s}".format(
                colored(i['Name'], 'blue'),
                colored(i['id'], 'cyan'))),
        else:
            print(' '*37),
            print("ID: {:<40s}".format(colored(i['id'], 'cyan'))),
        print("State: {} AMI ID: {} Type: {}".format(
            colored(i['state'], state_color),
            colored(i['image'], 'yellow'),
            colored(i['type'], 'cyan')))

    if count_running or count_stopped:
        print("\nRunning: {0} Stopped: {1}".format(
            colored(count_running, 'green'),
            colored(count_stopped, 'red')))


def get_instance_list():
    c = Counter(running=0, stopped=0)
    array = []
    for i in ec2.instances.all():
        instance_name = get_instance_name(i.id)
        instances = {'Name': instance_name, 'id': i.id,
                     'state': i.state['Name'], 'image': i.image_id,
                     'type': i.instance_type}
        array.append(instances)

        if i.state['Name'] == "running":
            c['running'] += 1
        elif i.state['Name'] == "stopped":
            c['stopped'] += 1
        else:
            print('ERROR: running state unknown')

    sorted_list = sorted(array, key=itemgetter('state'))
    print_instance_list(sorted_list, c['running'], c['stopped'])


if __name__ == '__main__':
    get_instance_list()
