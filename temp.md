<hr style="border-color:#75DFC1; width:80%;"><center>
<h1>Hadoop</h1>
<h2>Distributed Architectures</h2></center>
<hr style="border-color:#75DFC1; width:80%;">

The volume of data created is exponentially increasing: to get a sense of this volume, each minute 103 million spam emails, 3.6 million Google searches, 450 000 tweets are exchanged. The forecast are that this volume will be multiplied by 10 in 2025. 

In order to draw value from those data, we need to be able to store and exploit them. 


<h2>Distributed Architectures vs Classical Architecture</h2>

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

### Distributed architectures speeds up computing

Partitioning data allows different machine to work on the same document at the same time. This is a fundamental  aspect of distributed architectures: since documents are spread over different machine, those machines can work in parallel at the same time. Moreover, since the data is already stored in small computable chunks on different machines, we do not need to move data from a machine to another: we just have to pick available machines that have the data. 

@slider distributed_computing_slider

### But distributed architectures face some problems

As you might have guessed by now, the organisation of the cluster is very important and needs to be managed well: the cluster needs to know where pieces of data are stored, which machines are available to compute and how the results of a computation should be handled: this task is not trivial and that is why we have some tools such as <i>Hadoop</i> to perform this part. 

Moreover, the <b>CAP theorem</b> limits the possibilities of distributed systems: this theorem states that you cannot achieve perfect <b>availability</b> or perfect <b>consistency</b> of your data if your data is spread across a cluster.

<i>Think for example of a company that allows you to book airplane tickets. The availability of a given seat is going to be stored on different nodes at the same time. If Alice books the seat on a node, the information needs some time to be updated on the other nodes. If Bob wants to book the same seat, there are two possibilities:
<ul>
<li>you let Bob book the seat: the data is available but it is not coherent and you have to find a way to resolve this conflict.</li>
<li>you stop Bob from booking the seat: the data is no longer available but it will remain consisten.</li>
</ul>
</i>

@slider cap_theorem_slider 

<b>CAP</b> actually stands for <b>Consistency</b>, <b>Availability</b> and <b>Partition Tolerance</b>: the theorem states that you cannot have the three at the same time. 

## Map Reduce

MapReduce is a programming model used widely in distributed systems to perform calculations. It has been patented by Google in 2004. MapReduce relies on the emission of key-value pairs during a Map phase and the aggregation of the values by keys during the Reduce phase.

Every partition of the data undergoes the same transformation, emitting a set of key-value pairs. This is the <b>Map</b> phase. Those pairs are emitted to a machine based on the key of the pair.

For example every pair with the key <code>key_1</code> is sent to a specific machine no matter how many keys there are. There can be different keys on a single machine but every value corresponding to a key need to be on the same machine. Creating the key-value pairs is done during the <b>Map</b> phase while the sorting and dispatching of values is called the <b>Shuffle</b> phase.

Once all sent to the right machine, values are aggregated by key to get the final result: this is the <b>Reduce</b> phase. 

### WordCount
To explain how Map Reduce works, the usual example is to take the `WordCount` task, e.g. computing the frequencies of words. It is the <code>print('hello world')</code> of MapReduce.

During the <b>Map</b> phase, the partitions of the text are lowered, tokenized and for each token, we emit the token as the key and 1 as the value.

The pseudo-code for this step is the following:

<blockquote>
INPUT: data <i>(list of strings)</i><br><br>
FOR EACH partition IN data:<br>
&emsp;&emsp;token_list = TOKENIZATION(partition)<br>
&emsp;&emsp;FOR EACH token IN token_list:<br>
&emsp;&emsp;&emsp;&emsp;EMIT((token, 1))<br>
</blockquote>

Remember that the <b>Shuffle</b> phase forces all values corresponding to the same key to be on the same reducing machine. So on every machine used during the <b>Reduce</b> phase, we have a set of keys, corresponding to some tokens present in the text and for each key a list of ones of length corresponding to the number of instances of this token over the partitions. 

The pseudo-code for the <b>Reduce</b> is given in the following block: the code is given only for one key because during the <b>Reduce</b>, keys are treated totally independently.

<blockquote>
INPUT: key <i>(string)</i>, list_of_values <i>(list of integers)</i><br><br>
s = 0<br>
FOR EACH i IN list_of_values:<br>
&emsp;&emsp;s = s + i<br>
EMIT((key, s))
</blockquote>
  
@slider mapreduce_wordcount_slider

The succession of a <b>Map</b>, <b>Shuffle</b> and <b>Reduce</b> phases is called a <b>Job</b>. We can combine multiple Jobs to perform complicated tasks. The number of reducers and mappers is up to the operator: if they is not a mapper by partition, some mappers will will take care of multiple partitions sequentially. On the other hand, having too many machines involved in an operation, some may not be available for other operations in the same time.

### Advanced MapReduce: Combiners

You may have noticed that during the Map phase of Wordcount, we have emitted the same keys twice on the same mapper machine. This can be problematic as this may increase significantly the number of values that are emitted. 

We can aggregate those values during the <b>Map</b> phase using a <b>Combiner</b>: this can be considered as a <b>Reduce</b> phase in the mapper. If we take the example of Wordcount, the new pseudo-code for the <b>Map</b> is the following: 

<blockquote>
INPUT: data <i>(list of strings)</i><br><br>
temp = DICTIONARY(string, integer)<br>
FOR EACH partition IN data:<br>
&emsp;&emsp;token_list = TOKENIZATION(partition)<br>
&emsp;&emsp;FOR EACH token IN token_list:<br>
&emsp;&emsp;&emsp;&emsp;IF token in temp.keys:<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; temp.set(token, 1 + temp.get(token))<br>
&emsp;&emsp;&emsp;&emsp;ELSE:<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; temp.set(token, 1)<br>
<br>
FOR EACH token IN temp.keys:<br>
&emsp;&emsp;EMIT((token, temp.get(token))
</blockquote>

@slider wordcount_combiner_slider

### Advanced MapReduce: Partitioners

During the <b>Shuffle</b> phase, the values are sent to specific machines according to the associated keys. The default rule is generally: 

<center><code> number of the reducer machine(key) = HASH_FUNCTION(key) MOD number of reducer machines</code></center>

This ensures an even distribution of keys over reducer nodes: each machine should receive about the same number of different keys. The issue with that is that in some particular cases, some keys can be over-represented. This can create a bottleneck which will slow down the execution of the jobs.  
 
@slider mapreduce_partitioners_slider

<i>In this example, the key <code>key1</code> is over-represented. <br>If we let the default partitioner take care of the <b>Shuffle</b>, then one of the reducer is going to receive much more data to process than the other but if we take into account the a priori knowledge of the distribution of values, we can define a partitioner that will balance the workload over the reducers.</i>

Partitioners cannot be coded dynamically: you have to know a priori the balance of values by key to implement one that will balance evenly the workload.

## Apache Hadoop

Apache Hadoop is an Open Source framework for distributed architectures. It was first released in 2006 by Yahoo! but is now an Apache Foundation project. It is a widely used tool in Big Data to manage distributed storage and computing. 

<h3>Hadoop components</h3>

Hadoop is mainly composed of 3 components: 
<ul>
<li><b>HDFS</b> (Hadoop Distributed File System): HDFS is in charge a of partition, replication, orchestration of data. </li>
<li><b>YARN</b> (Yet Another Resource Negociator): YARN is in charge of orchestrating jobs and attributing resources.</li>
<li><b>Hadoop MapReduce</b>: Hadoop MapReduce is a Java API that implements the meta-class to perform MapReduce Jobs</li>
</ul>

While it is coded in Java, Hadoop allows also to use other programming languages by writing in and parsing the standard output directly. This allows us to code MapReduce Jobs in Python, Ruby, or any other language given that you can read from the standard output. This utility is called <b>Hadoop Streaming</b>.

<h3>HDFS</h3>

As stated before, <b>HDFS</b> is in charge of distributed storage. There are multiple daemons running in HDFS: 
<ul>
<li><b>Datanode</b>: datanode is the daemon running on the slave nodes and that is in charge of allocating the interacting with the other daemons to make the data stored on the machine available.</li>
<li><b>Namenode</b>: the namenode is a daemon running on a master node: it contains meta-data about the location of the partitions. The namenode interacts with the datanodes to read or write data. </li>
<li><b>SecondaryNamenode</b>: secondary namenodes are daemons running on other master nodes. They are taking snapshots of the namenode at regular time intervals. If the namenode crashes, they are able to take over its role</li>
</ul>

<h3>YARN</h3>

<b>YARN</b> is in charge of orchestrating work and jobs. There are several daemons running within YARN: 
<ul>
<li>The <b>Resource Manager</b> is the daemon in attributing resources to the different worker nodes. It runs on a master node.</li>
<li>The <b>Application Manager</b> is triggered by a client application. It is in charge of orchestrating jobs during the runtime of the application and asks the <b>Resource Manager</b> for resources.</li>
<li>The <b>Node Manager</b> is a daemon running on the worker nodes. It communicates with the <b>Resource Manager</b> at all time and with the <b>Application Manager</b> during the runtime of the application.</li>
<li><b>Containers</b> are the daemons triggered by the <b>Resource Manager</b> at the start of an application. They are in charge of the actual work. In fact, containers are <a href="https://en.wikipedia.org/wiki/Java_virtual_machine">JVM</a> with allocated disk and memory.</li>
</ul>

<center>?????????????????????????????????????????????????????????????????????????????????????????????????????????</center>


The code of an application contains information about the location of the files (in HDFS or locally), about the number of mappers and reducers and of course the code of Mappers, Combiners, Partitioners and Reducers. 

When it is launched, the <b>Resource Manager</b> triggers an <b>Application Manager</b> on one of the worker nodes. The <b>Application Manager</b> knows the resource needed (number of mappers and reducers) and asks the <b>Resource Manager</b> for those resources. 

The <b>Resource Manager</b> launches containers that includes a <b>JVM</b> and the code of the mappers and the reducers and communicates the address and ids of the containers to the <b>Application Manager</b>. 

Then, those containers communicate to the <b>Application Manager</b> which is in charge of orchestrating the jobs. The communication goes through the <b>Resource Manager</b> because Hadoop is based on a share-nothing model, e.g. worker nodes are only linked to the master nodes not one to each other. This leaves the <b>Resource Manager</b> available for other applications to be run on other nodes. 


















