#!/bin/env python

import boto3
from termcolor import colored

ec2 = boto3.resource('ec2')
for i in ec2.instances.all():
    print("ID: {0}\tState: {1}\tAMI ID: {2}".format(
        colored(i.id, 'cyan'),
        colored(i.state['Name'], 'green'),
        colored(i.image_id, 'yellow')
    ))