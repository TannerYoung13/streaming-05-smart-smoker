"""
This program reads temperature data from a CSV file and sends messages to RabbitMQ queues.
The data is read every 30 seconds, and messages are sent to the corresponding queues.

"""

import pika
import sys
import webbrowser
import csv
import struct
from datetime import datetime
import time

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/")
        print()

def send_message(host: str, queue_name: str, message: bytes):
    """
    Creates and sends a binary message to the specified queue.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (bytes): the binary message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent message to {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

def main():
    """Reads data from CSV file and sends it to RabbitMQ queues."""
    with open("smoker-temps.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        
        for data_row in reader:
            timestamp_str = data_row[0]
            smoker_temp = data_row[1]
            food_a_temp = data_row[2]
            food_b_temp = data_row[3]

            # Convert timestamp string to Unix timestamp (float)
            timestamp = datetime.strptime(timestamp_str, "%m/%d/%y %H:%M:%S").timestamp()

            if smoker_temp:
                message = struct.pack('!df', timestamp, float(smoker_temp))
                send_message("localhost", "01-smoker", message)
            
            if food_a_temp:
                message = struct.pack('!df', timestamp, float(food_a_temp))
                send_message("localhost", "02-food-A", message)
            
            if food_b_temp:
                message = struct.pack('!df', timestamp, float(food_b_temp))
                send_message("localhost", "03-food-B", message)
            
            # Sleep for 30 seconds before reading the next row
            time.sleep(30)

# Standard Python idiom to indicate main program entry point
if __name__ == "__main__":  
    offer_rabbitmq_admin_site()
    main()
