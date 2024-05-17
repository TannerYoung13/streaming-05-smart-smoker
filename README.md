## Tanner Young
## 5/16/2024

# streaming-05-smart-smoker

> Streaming data may come from web analytics, social media, smart devices, and more. In these next two modules, we'll look at implementing analytics for a "smart smoker" (as in slow cooked food). 

We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channel2 = Food A Temp --> send to message queue "02-food-A"
[3] Channel3 = Food B Temp --> send to message queue "03-food-B"
Requirements

RabbitMQ server running
pika installed in your active environment
RabbitMQ Admin

See http://localhost:15672/Links to an external site.

## Before You Begin

1. Fork this starter repo into your GitHub.
1. Clone your repo down to your machine.
1. View / Command Palette - then Python: Select Interpreter
1. Select your conda environment. 
1. Make sure to import pike or copy the file from a previous module

## Explanation:
1. Function offer_rabbitmq_admin_site: Prompts the user to open the RabbitMQ Admin website.
2. Function send_message: Sends a binary message to the specified RabbitMQ queue. The message is packed into a binary format using the struct module.
3. Function main: Reads the CSV file. Skips the header row. For each row in the CSV, extracts the timestamp and temperature values. If a temperature value is present, it packs the timestamp and temperature into a binary message using struct.pack and sends it to the appropriate queue.