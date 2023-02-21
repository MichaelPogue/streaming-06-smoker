""" Authored By: Michael Pogue | Created on: 21Feb23

This code is to read a CSV file and output the contents into the RabbitMQ
queue system. 
-----------------------------------------------------------------------------"""

import os
import pika
import sys
import re
from time import strftime
from datetime import datetime as dt
from collections import deque

host = "localhost"
EMAIL = os.getenv("EMAIL_ADDRESS")
queue_smoker_temp = "01-smoker"
queue_food_a = "02-food-A"
queue_food_b = "03-food-B"

main_temp_deque = deque(maxlen=5)
food_temp_a_deque = deque(maxlen=20)
food_temp_b_deque = deque(maxlen=20)

def ch1_smoker_temp(ch, method, properties, body):
    """
    
    """

    # 
    recieved_message = body.decode()
    current_temp = []

    current_temp[0] = re.findall(r"[-+]?\d*\.\d+", recieved_message)
    main_temp_deque.append(current_temp[0])

    if max(main_temp_deque) - min(main_temp_deque) >= 15:
        temp = max(main_temp_deque) - min(main_temp_deque)
        print(f"ALERT! Temperature has dropped by {abs(temp)}, abandon all hope!")


    ch.basic_ack(delivery_tag = method.delivery_tag)

def ch2_food_a_temp():
    """
    
    """
    pass

def ch3_food_b_temp():
    """
    
    """    
    pass

def main(hn: str = "localhost", qn1: str = queue_smoker_temp): #, qn2: str = queue_food_a, qn3: str = food_temp_b_deque):
    """
    
    """
    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue = qn1, durable = True)
        # channel.queue_declare(queue = qn2, durable = True)
        # channel.queue_declare(queue = qn3, durable = True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count = 1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue = qn1, on_message_callback = queue_smoker_temp)
        # channel.basic_consume( queue = qn2, on_message_callback = queue_smoker_temp)
        # channel.basic_consume( queue = qn3, on_message_callback = queue_smoker_temp)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()

if __name__ == "__main__":
    main()