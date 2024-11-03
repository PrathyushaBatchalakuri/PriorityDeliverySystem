# AVL Tree Order Management System

## Overview

This project implements an AVL tree-based order management system designed to efficiently handle order operations such as creation, cancellation, and updating of delivery times. The system maintains the order of processing based on dynamic priorities, ensuring efficient insertion, deletion, and retrieval that adapt to changes in order details and processing times.

## Features

- **Create Orders**: Insert new orders into the system with calculated priorities and estimated arrival times (ETAs).
- **Cancel Orders**: Remove orders from the system, adjusting the tree structure and priorities as needed.
- **Update Delivery Times**: Modify the delivery time of existing orders and recalculate the ETAs for affected subsequent orders.
- **Query Orders**: Retrieve orders based on their ID or delivery time window.
- **Order Ranking**: Determine the sequence of order deliveries relative to other orders in the system.

## Structure

The project consists of two main classes:
- `treeNode`: Represents an order with attributes like order ID, creation time, order value, delivery time, ETA, priority, and pointers to child nodes and parent in the AVL tree.
- `avlTree`: Manages the AVL tree operations such as insertion, deletion, rotations for balancing, and node adjustments.

## Usage

The program reads commands from a text file specified as an argument upon execution. Supported commands include:

- `createOrder(orderId, currentSystemTime, orderValue, deliveryTime)`: Create a new order.
- `cancelOrder(orderId, currentSystemTime)`: Cancel an existing order.
- `print(orderId)`: Print details of a specific order.
- `print(time1, time2)`: Print orders scheduled within a specific time frame.
- `getRankOfOrder(orderId)`: Get the delivery rank of an order.
- `updateTime(orderId, currentSystemTime, newDeliveryTime)`: Update the delivery time for an order.

Commands should be provided in a text file, with each command on a new line, and the program will output results to a separate file with the same name as the input but appended with `_output_file.txt`.

## Example Input
```sh
createOrder(1001, 1,100, 4)
createOrder(1002, 2, 150, 7)
createOrder(1003, 8, 50, 2)
print(2, 15)
createOrder(1004, 9, 300, 12)
getRankOfOrder(1004)
print(45, 55)
createOrder(1005, 15, 400, 8)
createOrder(1006, 17, 100, 3)
cancelOrder(1005, 18)
getRankOfOrder(1004)
createOrder(1007, 19, 600, 7)
createOrder(1008, 25, 200, 8)
updateTime(1007, 27, 12)
getRankOfOrder(1006)
print(55,85)
createOrder(1009, 36, 500, 15)
createOrder(1010, 40, 250, 10)
Quit()
```

## Example Output
```sh
Order 1001 has been created - ETA: 5
Order 1002 has been created - ETA: 16
Order 1003 has been created - ETA: 25
Order 1001 has been delivered at time 5.
There are no orders in that time period.
Order 1004 has been created - ETA: 35
Updated ETAs: [1002:16, 1004: 35, 1003: 49]
Order 1004 will be delivered after 1 order.
[1003]
Order 1005 has been created - ETA: 59
Order 1006 has been created - ETA: 70
Order 1002 has been delivered at time 16.
Order 1005 has been canceled.
Order 1004 will be delivered after 0 orders.
Updated ETAs: [1004:35, 1003: 49, 1006:54]
Order 1007 has been created - ETA: 58
Updated ETAs: [1004: 35, 1003: 49, 1007:58, 1006:68]
```


### Installation and Execution

No additional libraries are required to run this project as it uses Python's standard libraries. 

To execute the program, run:
```bash
python avl_order_system.py input_file.txt
```

Replace `input_file.txt` with the path to your input file.

## Development Environment

This project was developed using Python 3.8.
