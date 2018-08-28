#!/bin/env python

import boto.ec2
import boto3

print("done with boto3:")
client = boto3.client('ec2')
regions = [region['RegionName'] for region in
           client.describe_regions()['Regions']]
print(regions)

regions = []
print("\ndone with boto2:")
region_list = boto.ec2.regions()
for x in region_list:
    regions.append(str(x.name))

print(regions)

# https://github.com/moul/prettytable-extras/blob/master/prettytable_extras.py
