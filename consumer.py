"""
    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  

    Author:    Dr. Denise Case
    Edits by:  Michael Pogue
    Date:      Feburary 07, 2023

"""

import pika
import sys
import time
import re
import os
from collections import deque
from time import strftime # Importing time module to track production and consumption times.

EMAIL = os.getenv("EMAIL_ADDRESS")
host = 'localhost'
queue_1 = "01-smoker"
queue_2 = "02-food-A"
queue_3 = "03-food-B"
deque_1 = deque(maxlen = 5)
deque_2 = deque(maxlen = 20)
deque_3 = deque(maxlen = 20)

# define a callback function to be called when a message is received
def decode_smoker_messages(ch, method, properties, body):
    """ 
    test
    ---------------------------------------------------------------------------
    """
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}") # at {strftime('%H:%M:%S')} from 01-smoker")
    # simulate work by sleeping for the number of dots in the message
    # time.sleep(body.count(b"."))

    # Deque 
    deque_1.append(body.decode())

    # Deque Initial
    initial_data = deque_1[0]
    initial_split = initial_data.split(",")
    initial_temp = float(initial_split[1][:-1])
    # initial_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_initial))

    # Deque Present
    present_data = body.decode()
    present_split = present_data.split(",")
    present_temp = float(present_split[1][:-1])
    # present_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_present))

    # Calculate temperature difference
    temperature_difference = abs(float(initial_temp) - float(present_temp))

    # Temperature difference
    if temperature_difference >= 15:
        print(f"     A fluctuation of in temperature has been detected.")
        print(f"     Smoker temperature has decreased from {initial_temp} to {present_temp}.")
        print(f"     A change of more than {temperature_difference}")

    ch.basic_ack(delivery_tag = method.delivery_tag)
    time.sleep(1)

def decode_food_a_messages(ch, method, properties, body):
    """ 
    test
    ---------------------------------------------------------------------------
    """
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}") # at {strftime('%H:%M:%S')} from 01-smoker")
    # simulate work by sleeping for the number of dots in the message
    # time.sleep(body.count(b"."))

    # Deque 
    deque_1.append(body.decode())

    # Deque Initial
    initial_data = deque_1[0]
    initial_split = initial_data.split(",")
    initial_temp = float(initial_split[1][:-1])
    # initial_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_initial))

    # Deque Present
    present_data = body.decode()
    present_split = present_data.split(",")
    present_temp = float(present_split[1][:-1])
    # present_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_present))

    # Calculate temperature difference
    temperature_difference = abs(float(initial_temp) - float(present_temp))

    # Temperature difference
    if temperature_difference >= 15:
        print(f"     A fluctuation of in temperature has been detected.")
        print(f"     Smoker temperature has decreased from {initial_temp} to {present_temp}.")
        print(f"     A change of more than {temperature_difference}")

    ch.basic_ack(delivery_tag = method.delivery_tag)
    time.sleep(1)

def decode_food_b_messages(ch, method, properties, body):
    """ 
    test
    ---------------------------------------------------------------------------
    """
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}") # at {strftime('%H:%M:%S')} from 01-smoker")
    # simulate work by sleeping for the number of dots in the message
    # time.sleep(body.count(b"."))

    # Deque 
    deque_1.append(body.decode())

    # Deque Initial
    initial_data = deque_1[0]
    initial_split = initial_data.split(",")
    initial_temp = float(initial_split[1][:-1])
    # initial_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_initial))

    # Deque Present
    present_data = body.decode()
    present_split = present_data.split(",")
    present_temp = float(present_split[1][:-1])
    # present_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_present))

    # Calculate temperature difference
    temperature_difference = abs(float(initial_temp) - float(present_temp))

    # Temperature difference
    if temperature_difference >= 15:
        print(f"     A fluctuation of in temperature has been detected.")
        print(f"     Smoker temperature has decreased from {initial_temp} to {present_temp}.")
        print(f"     A change of more than {temperature_difference}")

    ch.basic_ack(delivery_tag = method.delivery_tag)
    time.sleep(1)

# define a main function to run the program
def main(hn: str = "localhost", qn1: str = "01-smoker", qn2: str = "02-food-A", qn3: str = "03-food-B"):
    """ 
    Continuously listen for task messages on a named queue.
    ---------------------------------------------------------------------------
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
        channel.queue_declare(queue = qn2, durable = True)
        channel.queue_declare(queue = qn3, durable = True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue = qn1, on_message_callback = decode_smoker_messages)
        channel.basic_consume( queue = qn2, on_message_callback = decode_food_a_messages)
        channel.basic_consume( queue = qn3, on_message_callback = decode_food_b_messages)

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


"""  
Launch Code!
------------------------------------------------------------------------------------------ """
# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main(host, queue_1, queue_2, queue_3)
