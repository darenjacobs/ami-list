#!/bin/env python

import sys
import argparse
import boto3
from botocore.exceptions import ClientError
from collections import OrderedDict
from prettytable import PrettyTable


def parse_args():
    default_region = 'us-east-1'
    help_text = ('List FHLBNY AMI images and EC2 instances attached AMI'
                 ' Images. By default BOTO3 establishes connections in the'
                 ' following order:\n1. Credential passed as argumetns to'
                 'boto.client()\n2. Environemnt Variables\n3. Shared'
                 'credentials file (~/.aws/credentials)\n4. IAM Assume Role')

    # Create argument parser
    parser = argparse.ArgumentParser(
        prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter,
        description=help_text)

    parser.add_argument('-k', '--aws-key', type=str, default='', help="""
                        Optional. Overrides Environment Variable and AWS
                        Credentials file.  Required with -s, --aws-secret
                        argument.""")

    parser.add_argument('-s', '--aws-secret', type=str, default='', help="""
                        Optional. Overrides Environment Variable and AWS
                        Credentials file.  Required with -k, --aws-key
                        argument.""")

    parser.add_argument('-r', '--region', type=str, default=default_region,
                        help="""Optional. """)

    return parser.parse_args()


def start_session(Args):
    valid_regions = ['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1',
                     'ap-northeast-2', 'ap-northeast-1', 'sa-east-1',
                     'ca-central-1', 'ap-southeast-1', 'ap-southeast-2',
                     'eu-central-1', 'us-east-1', 'us-east-2', 'us-west-1',
                     'us-west-2']
    global region
    aws_key = Args.aws_key
    aws_secret = Args.aws_secret
    region = Args.region

    # Check AWS ID key length
    if aws_key and (len(aws_key) < 16 or len(aws_key) > 128):
        print('Error: Invalid AWS Key, %s' % aws_key)
        sys.exit(1)

    # ID & key, you can't have one without the other
    if (aws_secret and not aws_key) or\
       (aws_key and not aws_secret):
        print('Error: Did not received both AWS Access Key ID and AWS'
              'Secret Key. Please provide both.')
        sys.exit(1)

    # Check for valid region
    if region not in valid_regions:
        print('Error: Invalid AWS Region, %s' % region)
        sys.exit(1)

    return boto3.Session(aws_access_key_id=aws_key,
                         aws_secret_access_key=aws_secret,
                         region_name=region)


def list_ami():
    session = start_session(args)
    ec2 = session.resource('ec2')
    row = []
    a_images = []
    e_images = []
    not_used = []
    used = []
    try:
        for image in list(ec2.images.filter(Owners=['self'])):
            a_images.append(image.id)
    except ClientError as e:
        print('Exception listing ami images: %s' % e)

    try:
        for i in ec2.instances.all():
            e_images.append(i.image_id)

        e_images = sorted(list(OrderedDict.fromkeys(e_images)))
    except ClientError as e:
        print('Exception listing ec2 ami images %s' % e)

    for image in a_images:
        if image not in e_images:
            not_used.append(image)
        else:
            used.append(image)

    row.append('\n'.join(a_images))
    row.append('\n'.join(e_images))
    row.append('\n'.join(not_used))
    row.append('\n'.join(used))

    table = PrettyTable()
    table_str = ("FHLBNY AMI Images region: %s" % region)
    field_names = (["FHLBNY AMI Images", "EC2 attached Images", "Unused"
                    "FHLBNY Images", "Used FHLBNY Images"])
    table.title = (str(table_str))
    table.field_names = field_names
    table.align["FHLBNY AMI Images"] = "l"
    table.align["EC2 attached"] = "r"
    table.align["Unused FHLBNY AMI Images"] = "l"
    table.align["Used FHLBNY Images"] = "r"
    table.add_row(row)

    return table


def print_table():
    table = list_ami()
    if len(str(table)) < 609:
        print('There are no AMI images in region %s' % region)
        sys.exit(0)
    filename = ("ami_list-%s.txt" % region)
    target = open(filename, 'w')
    print('Writing table to file %s' % filename)
    target.write(str(table))
    target.close()


if __name__ == '__main__':
    args = parse_args()

    print('You are running the script with arguments: ')
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    print(list_ami())
    print_table()
