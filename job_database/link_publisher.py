
import pika










def publish_link(list_of_links):

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'urls'

    channel.queue_declare(queue=queue_name)




    for links in list_of_links:

        pass

    connection.close()

