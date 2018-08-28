#!/bin/bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY

pip install boto3 PrettyTable PTable termcolor --upgrade --user


for region in us-east-1 us-east-2 us-west-2
do
  echo "#################"
  echo "REGION: ${region}"
  export AWS_DEFAULT_REGION=${region}
  python ./ami-list/ami_list.py -r ${region}
  python ./ami-list/ec2-state.py
  echo "#################"
  echo ""
done

python ./ami-list/ami_list.py -r us-west-1
