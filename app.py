from flask import Flask, jsonify
import boto3
import os

app = Flask(__name__)

# AWS Clients
ec2_client = boto3.client('ec2', region_name=os.environ.get('AWS_REGION', 'ap-south-1'))

@app.route('/')
def home():
    return jsonify({"message": "Server Tracker API running!"})

@app.route('/servers', methods=['GET'])
def list_servers():
    servers = []
    paginator = ec2_client.get_paginator('describe_instances')
    for page in paginator.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                servers.append({
                    "InstanceId": instance['InstanceId'],
                    "State": instance['State']['Name'],
                    "PrivateIP": instance.get('PrivateIpAddress', 'N/A'),
                    "PublicIP": instance.get('PublicIpAddress', 'N/A'),
                    "Tags": {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                })
    return jsonify(servers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
