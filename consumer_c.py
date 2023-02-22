""" Authored By: Michael Pogue | Created on: 21Feb23 | Last Updated: 21Feb23 

This code will monitor incoming traffic from RabbitMQ and monitor it for 
problematic temperature fluctuations.
"""
# Import modules used.
import pika
import sys
import time
import os
from collections import deque
from time import strftime 

# Set variables to be used.
EMAIL = os.getenv("EMAIL_ADDRESS")
host = 'localhost'
data_queue = "03-food-B"
data_deque = deque(maxlen = 20)
data_warning = 1

# define a callback function to be called when a message is received
def decode_message(ch, method, properties, body):
    """ 
    Function to decode individual lines of data and monitor for temperature fluctuations.
    ---------------------------------------------------------------------------
    """
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}") 

    # Set initial queue data used to create deque.
    data_deque.append(body.decode())
    initial_data = data_deque[0]
    initial_split = initial_data.split(",")
    initial_temp = float(initial_split[1][:-1])
    # initial_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_initial)) <- A monument to failure.

    # Add continuous data to array.
    present_data = body.decode()
    present_split = present_data.split(",")
    present_temp = float(present_split[1][:-1])
    # present_temp = str(re.findall(r"[-+]?\d*\.\d+", deque_1_present)) <- A monument to failure.

    # Calculate temperature difference from the initial input with the latest.
    temperature_difference = abs(float(initial_temp) - float(present_temp))

    # Calculate if the temperature is within parameters, then send a warning message.
    if temperature_difference <= data_warning:
        degree = "\u00b0"+"F"
        print(f"ERROR: Temperature stalled with only a {round(temperature_difference, 1)}{degree} change in 10 minutes.")

    ch.basic_ack(delivery_tag = method.delivery_tag)
    time.sleep(.1)

# define a main function to run the program
def main(hn: str, qn: str):
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
        channel.queue_declare(queue = qn, durable = True)

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
        channel.basic_consume( queue = qn, on_message_callback = decode_message)

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

------------------------------------------------------------------------------------------ """
# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main(host, data_queue)
