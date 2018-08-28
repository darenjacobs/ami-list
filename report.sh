#!/bin/bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY

pip install boto3 PrettyTable PTable termcolor --upgrade --user
git clone https://github.com/darenjacobs/ami-list.git

echo "#################"
echo "US EAST Region 1"
export AWS_DEFAULT_REGION=us-east-1
python ./ami-list/ami_list.py -r us-east-1
python ./ami-list/ec2-state.py
echo "#################"
echo ""

echo "#################"
echo "US East Region 2"
export AWS_DEFAULT_REGION=us-east-2
python ./ami-list/ami_list.py -r us-east-2
python ./ami-list/ec2-state.py
echo "#################"
echo ""

echo "#################"
echo "US West Region 2"
export AWS_DEFAULT_REGION=us-west-2
python ./ami-list/ami_list.py -r us-west-2
python ./ami-list/ec2-state.py
echo "#################"
echo ""

python ./ami-list/ami_list.py -r us-west-1
