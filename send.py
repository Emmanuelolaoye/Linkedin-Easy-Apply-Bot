# import BS4
# import selenium
import pyppeteer
# import job
import database
# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='hello')
#
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")
#
# connection.close()


#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")


class Link:

    def __init__(self, timestamp, url, channel, queue_name):

        self.timestamp = timestamp
        self.url = url
        self.channel = channel
        self.queue_name = queue_name



    def get_url(self):
        return self.url


    # create message



    def send_link_to_queue(self):

        self.channel.basic_publish(exchange='',
                              routing_key=self.queue_name,
                              body=self.)
        print(" [x] Sent 'Hello World!'")

        pass



# def procces_links(list_of_links):
#
#     for jobs_links in list_of_links:
#
#         new_job = job.extract_job_info(jobs_links)
#





















    # pass