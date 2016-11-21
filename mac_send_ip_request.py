import boto.sqs
import os

from boto.sqs.message import Message

# (get_home_ip_env)abisson:get-home-ip abisson$ aws --profile=staging configure
def connect_to_sqs_and_create_queue():
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.create_queue('requesthomeip', 120)

def write_message_to_queue(queue):
    m = Message()
    m.set_body('request_ip')
    queue.write(m)
    print m

if __name__ == "__main__":
    os.environ["AWS_PROFILE"] = "staging"
    queue = connect_to_sqs_and_create_queue()
    write_message_to_queue(queue)
