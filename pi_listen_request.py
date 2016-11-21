import boto.sqs
import os
import ipgetter

from boto.sqs.message import Message

# (get_home_ip_env)abisson:get-home-ip abisson$ aws --profile=staging configure

def connect_to_sqs_and_get_queue():
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.get_queue('requesthomeip')


def create_and_return_ip_queue():
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.create_queue('requesthomeipresults', 120)


def write_message_to_queue(queue):
    m = Message()
    m.set_body(ipgetter.myip())
    queue.write(m)
    print m

if __name__ == "__main__":
    os.environ["AWS_PROFILE"] = "staging"
    queue = connect_to_sqs_and_get_queue()
    print queue
    messages_queue = queue.get_messages()
    if len(messages_queue) > 0:
        ip_results_queue = create_and_return_ip_queue()
        write_message_to_queue(ip_results_queue)
