import boto.sqs
import os
import ipgetter

from boto.sqs.message import Message

# (get_home_ip_env)abisson:get-home-ip abisson$ aws --profile=staging configure

def connect_to_sqs_and_get_queue():
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.get_queue('requesthomeipresults')


def create_and_return_ip_queue():
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.create_queue('requesthomeipresults', 120)


def delete_all_queues():
    conn = boto.sqs.connect_to_region("us-east-1")
    conn.delete_queue(conn.get_queue('requesthomeipresults'))
    conn.delete_queue(conn.get_queue('requesthomeip'))


def write_message_to_queue(queue):
    m = Message()
    m.set_body(ipgetter.myip())
    queue.write(m)
    print m

if __name__ == "__main__":
    os.environ["AWS_PROFILE"] = "staging"
    queue = connect_to_sqs_and_get_queue()
    messages_queue = queue.get_messages()
    for i in range(0, len(messages_queue)):
        message = messages_queue[i]
        print "ip: %s" % message.get_body()
    delete_all_queues()
