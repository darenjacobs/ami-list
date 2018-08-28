#!/bin/env python

import boto3
from termcolor import colored
from collections import Counter

c = Counter(running=0, stopped=0)

ec2 = boto3.resource('ec2')
for i in ec2.instances.all():
    if i.state['Name'] == "running":
        c['running'] += 1
        print("ID: {0}\tState: {1}\tAMI ID: {2}".format(
            colored(i.id, 'cyan'),
            colored(i.state['Name'], 'green'),
            colored(i.image_id, 'yellow')
        ))

for i in ec2.instances.all():
    if i.state['Name'] == 'stopped':
        c['stopped'] += 1
        print("ID: {0}\tState: {1}\tAMI ID: {2}".format(
            colored(i.id, 'cyan'),
            colored(i.state['Name'], 'red'),
            colored(i.image_id, 'yellow')
        ))

if c['running'] or c['stopped']:
    print("\nRunning: {0} Stopped: {1}".format(colored(c['running'], 'green'),
                                               colored(c['stopped'], 'red')))
