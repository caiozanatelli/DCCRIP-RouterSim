# DCCRIP-RouterSim

## Description

This work tackles the creation of a router simulator that implements a distance-vector routing protocol with network load balance, routing measures, and some optimizations. 

## Execution & Parameters

In the project root directory, use the following command in order to run the software:

```bash
python3 routersim.py --addr ADDR --update-period PERIOD [--startup-commands FILE]
```

## Message Types

Message transmission is performed using UDP (User Datagran Protocol) and packets are encoded in JSON (JavaScript Object Notation) in order to allow future extensions of funcionality and also for usage simplicity. All types of message contain as default the following fields: <b>source</b>, <b>destination</b>, and <b>type</b>, where <i>type</i> indicates the message type, which can be:

* <b>data</b>: data message;
* <b>update</b>: route update message;
* <b>trace</b>: trace message.

#### Data Message

Data messages have an additional field named <b>payload</b> whose type is <i>string</i>. The simulator displays this field every time a data message reaches a router.

#### Trace Message

Trace messages have an additional field named <b>distances</b> containing a dictionnary with the minimum known distance to some destination IP.

#### Route Update Message

Route update messages have an additional field named <b>hops</b> that contain a list of IPs indicating all the routers the message have passed through. When the message arrives at the destination, it is encoded in JSON format and inserted into a data message. The new message then returns to the source.

## Router Features

As said above, the router simulator presented in this project implements a distance-vector routing protocol with network load balance. We show below all the implemented features.

#### Links

#### Routes

#### Periodic Updates

#### Split Horizon

#### Network Load Balance

#### Immediate Re-Routing

#### Out-of-Date Routes Removal
