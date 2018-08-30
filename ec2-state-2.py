#!/bin/env python

import boto3
from termcolor import colored
from collections import Counter
from operator import itemgetter


def get_instance_name(id):
    ec2 = boto3.resource('ec2')
    ec2_instance = ec2.Instance(id)
    instance_name = 'N/A          '
    for tag in ec2_instance.tags or []:
        if tag["Key"] == 'Name':
            instance_name = tag["Value"]
    return instance_name


def print_instance_list(*args):
    ec2_list, c_running, c_stopped = args
    state_color = ''
    for i in ec2_list:
        if i['state'] == 'running':
            state_color = 'green'
        else:
            state_color = 'red'
        print("Name: {0}\t ID: {1}\tState: {2}\tAMI ID: {3}\tType: {4}".format(
            colored(i['Name'], 'white'),
            colored(i['id'], 'cyan'),
            colored(i['state'], state_color),
            colored(i['image'], 'yellow'),
            colored(i['type'], 'cyan')))

    if c_running or c_stopped:
        print("\nRunning: {0} Stopped: {1}".format(
            colored(c_running, 'green'),
            colored(c_stopped, 'red')))


def get_instance_list():
    c = Counter(running=0, stopped=0)
    array = []
    ec2 = boto3.resource('ec2')
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
