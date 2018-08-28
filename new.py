#!/bin/env python

import boto3
from termcolor import colored
from collections import Counter

c = Counter(running=0, stopped=0)
instance = {}

ec2 = boto3.resource('ec2')
for i in ec2.instances.all():
    instances = {'id': i.id, 'state': i.state, 'image': i.image_id}
    if i.state['Name'] == "running":
        c['running'] += 1
    elif i.state['Name'] == "stopped":
        c['stopped'] += 1
    else:
        print('ERROR: running state unknown')


my_list = sorted(instances, key=lambda key: instances[key])

for id, state in instances.items():
    # print ("ID: %s, State: %s Image: %s" % id, state, instances['image'])
    print (id, state)


if c['running'] or c['stopped']:
    print("\nRunning: {0} Stopped: {1}".format(colored(c['running'], 'green'),
                                               colored(c['stopped'], 'red')))
