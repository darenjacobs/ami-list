#!/bin/env python

import boto3
from termcolor import colored
from collections import Counter
from operator import itemgetter

c = Counter(running=0, stopped=0)
instances = {}
my_dict = []

ec2 = boto3.resource('ec2')
for i in ec2.instances.all():
    instances = {'id': i.id, 'state': i.state['Name'], 'image': i.image_id}
    my_dict.append(instances)

    if i.state['Name'] == "running":
        c['running'] += 1
    elif i.state['Name'] == "stopped":
        c['stopped'] += 1
    else:
        print('ERROR: running state unknown')

sorted_list = sorted(my_dict, key=itemgetter('state'))

for i in sorted_list:
    print("ID: {0}\tState: {1}\tAMI ID: {2}".format(colored(i['id'], 'cyan'),
                                                    colored(i['state'],
                                                    'green'),
                                                    colored(i['image'],
                                                    'yellow')))

if c['running'] or c['stopped']:
    print("\nRunning: {0} Stopped: {1}".format(colored(c['running'], 'green'),
                                               colored(c['stopped'], 'red')))
