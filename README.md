# DCCRIP-RouterSim

## Description

This work tackles the creation of a router simulator that implements a distance-vector routing protocol with network load balance, routing measures, and some optimizations. 

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

Links between routers are stored in a dictionnary where addresses of adjacent routers are the keys and the stored value represents the cost.

#### Routes

Routes are stored in a dictionnary where the router's destination address is the key and the stored value is a list of tuples containing the addresses of the router that informed both route and cost.

#### Periodic Updates

Periodic updates are performed every &pi; seconds, where &pi; is update period parameter. Internally, this is implemented using a timer that sends an update message every &pi; seconds.

#### Split Horizon

Update messages that have been sent contain the routes learnt by the router. In order to reduce chances of counting infinity, sent routes ignore those to the router to which the message is destined as well as all routes learnt by it.

#### Network Load Balance

In cases where there exist multiple routes with the minimum cost, the decision is made in a random way. We chose this strategy because load balance implemented through <i>round-robin</i> would not make sense due to the dynamism inherent to the topology.

#### Immediate Re-Routing

Routes evaluation is performed immediately before sending each message, and hence topology changes will not impact message transmissions.

#### Out-of-Date Routes Removal

If a router does not send update messages for a period of 4&pi; seconds, every route that has been learnt so far will be removed. This is also implemented using a timer.

## Usage

In the project root directory, use the following command in order to run the software:

```bash
python3 routersim.py --addr ADDR --update-period PERIOD [--startup-commands FILE]
```
