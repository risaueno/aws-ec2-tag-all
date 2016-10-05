#!/usr/bin/python

import boto3

def lambda_handler(event, context):
    
    # Settings
    regions = ['region-1','region-2','region-3'] 
    tag_key = 'Some Tag Name'
    tag_value = 'Some Tag Value'
    
    # Checks to see if the tag already exists for an instance.
    # Wrong or empty tags with specified key are deleted. 
    def tagExists(tags, tagName, tagValue, instanceId, client):
        for i in tags:
            if i['Key'] == tagName:
                if i['Value'] == tagValue:
                    return True
                print 'Deleting empty/wrong tag for following instance'
                client.delete_tags(Resources=[instanceId],Tags=[{"Key": tagName}])
                return False
        return False

    for r in regions: 
        ec2 = boto3.resource('ec2',region_name=r)
        ec = boto3.client('ec2',region_name=r)

        reservations = ec.describe_instances()['Reservations']
        instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], [])

        for ins in instances:
            insID = ins['InstanceId']
            if tagExists(ins['Tags'], tag_key, tag_value, insID, ec):
                print insID + ": Already tagged"
            else:
                print insID + ": Tagging..."
                ec2.create_tags(
                    Resources=[insID], Tags=[{'Key': tag_key,'Value': tag_value}]
                )
