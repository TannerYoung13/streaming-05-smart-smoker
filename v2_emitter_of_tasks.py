#This version has no delay

import csv
import pika
import sys
import webbrowser
import struct
from datetime import datetime

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website."""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: bytes):
    """
    Sends a binary message to the specified queue.

    Parameters:
        host (str): The hostname or IP address of the RabbitMQ server.
        queue_name (str): The name of the queue.
        message (bytes): The binary message to be sent to the queue.
    """
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        ch = conn.channel()
        ch.queue_declare(queue=queue_name, durable=True)
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent message to {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        conn.close()

def main():
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
                send_message("localhost", "02-food-B", message)

if __name__ == "__main__":
    offer_rabbitmq_admin_site()
    main()
