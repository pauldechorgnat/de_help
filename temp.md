# Hadoop
## Distributed Architectures

The volume of data created is exponentially increasing: to get a sense of this volume, each minute 103 million spam emails, 3.6 million Google searches, 450 000 tweets are exchanged. The forecast are that this volume will be multiplied by 10 in 2025. 

In order to draw value from those data, we need to be able to store and exploit them. 



### Distributed Architectures vs Classical Architecture
When faced to the problem of Big Data storage, there are mainly two ways to increase one's storing capacities or computing power:
<ul>
<li> <b>Scaling Up</b>: buying a more powerful machine</li>
<li> <b>Scaling Out</b>: buying less powerful machines and make them work together</li>
</ul>

### Some definitions 
A **cluster** is a set of machines also called **nodes**. Those machine can be linked to each other or have special network architectures. 
Generally speaking some machines are more important than other: they are more powerful and are thus more oriented toward orchestration, planning, ... <br>Those are called **master** nodes while the regular one are called **worker** or **slave**: they are the one actually doing the computations and the storing.
 
### Distributed architectures are cheaper
For decades, improvements on transistor capacities, hence on storage and computing facilities have been increasing exponentially, following Moore's law. Lately, due to physical limitations, we witnessed a downturn in this trend.  
It is now cheaper to buy cheap hardware, also called commodity hardware, in number than buying the largest possible machine. For the same computer power it is cheaper to use distributed architectures than very powerful single machines.

### Distributed architectures are more secured
There are two important aspect in distributed architectures: 
<ul>
<li><b>Partitioning</b>: data is cut into blocks of a given maximal size and spread across the cluster.</li>
<li><b>Replication</b>: data is replicated which means that we create copies of our partitions.
</ul>

@slider partition_replication_slider

At first you may think that this increases the demand for storage, which is true, but remember that storage is very cheap while data is key to business today. This partition/replication increases the security of the data. We cannot assume that the crash of a machine is an extraordinary event: this is an event that is going to happen so we need to have copies of the data that are available at any time:

@slider redundancy_security_slider

<i>In this example, a document is spread on a cluster of 6 machines. It is very simplified but we have to have 3 machines down before not being able to access this document. The likeliness of this happening in a time so short that no one can react is low. Moreover tools are designed to see when a machine is down and take action so that the data is replicated on another machine so that we have all our replicas in the cluster.<br>
In some companies where data is a very sensible issue, data is replicated inside data centers which are themselves replicated in different countries in order to avoid natural disasters (floods, earthquake, ...) or man made phenomena (attacks, war, ...).</i>