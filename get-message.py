import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/mgv8dh"
sqs = boto3.client('sqs')

def delete_message(handle):
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
    count = 0;
    with open('message.txt', 'w') as file:
        while True:
            try:
                response = sqs.receive_message(
                    QueueUrl=url,
                    AttributeNames=[
                        'All'
                    ],
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=[
                        'All'
                    ],
                    VisibilityTimeout = 300
                )
                if "Messages" in response:
                    for msg in response['Messages']:
                        order = msg['MessageAttributes']['order']['StringValue']
                        word = msg['MessageAttributes']['word']['StringValue']
                        handle = msg['ReceiptHandle']
                        file.write(f"{order},{word},{handle}\n")
                        count += 1
                        if count >= 10:
                            file.close()
                            return
                else:
                    print("No more messages in the queue.")
                    file.close()
                    break
            except ClientError as e:
                print(e.response['Error']['Message'])
                break

def reassemble_phrase():
    message = []
    with open('message.txt', 'r') as file:
        for eachline in file:
            order, word, handle = eachline.strip().split(',')
            message.append({"order": int(order), "word": word, "handle": handle})
    file.close()
    message.sort(key=lambda x: x['order'])
    reassembled_phrase = ' '.join([each['word'] for each in message])
    return reassembled_phrase


# Trigger the function
if __name__ == "__main__":
    get_message()
    reassembled_phrase = reassemble_phrase()
    print(reassembled_phrase)