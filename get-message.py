#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/mgv8dh"
sqs = boto3.client('sqs')

def delete_message(handles):
    for handle in handles:
        try:
            # Delete message from SQS queue
            sqs.delete_message(
                QueueUrl=url,
                ReceiptHandle=handle
            )
            print("Message deleted")
        except ClientError as e:
            print(e.response['Error']['Message'])


def get_message():
    messages = []
    handles = []
    try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
        while (len(messages) < 10):
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                messages.append((order, word))
                handles.append(handle)

                # Print the message attributes - this is what you want to work with to reassemble the message
                # print(f"Order: {order}, Word: {word}")

        # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)
            
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])
        
    return messages, handles
    
def reassemble_phrase():
    messages, handles = get_message()
    messages.sort()
    reassembled_phrase = ' '.join(word for _, word in messages)
    delete_message(handles) # Comment out to delete all messages 
    return reassembled_phrase

# Trigger the function
if __name__ == "__main__":
    reassembled_phrase = reassemble_phrase()
    print(reassembled_phrase)
