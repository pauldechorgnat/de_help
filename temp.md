<hr style="border-color:#75DFC1; width:80%;"/><center>
<h1>Distributed Architectures, Hadoop and tools</h1></center>
<hr style="border-color:#75DFC1; width:80%;"/>

The volume of data created is exponentially increasing: to get a sense of this volume, each minute 103 million spam emails, 3.6 million Google searches, 450 000 tweets are exchanged. The forecast are that this volume will be multiplied by 10 in 2025. 

In order to draw value from those data, we need to be able to store and exploit them. 


<h2>Distributed Architectures vs Classical Architecture</h2>

When faced to the problem of Big Data storage, there are mainly two ways to increase one's storing capacities or computing power:
<ul>
<li> <b>Scaling Up</b>: buying a more powerful machine</li>
<li> <b>Scaling Out</b>: buying less powerful machines and make them work together</li>
</ul>
<h3>Some definitions </h3>
A <b>cluster</b> is a set of machines also called <b>nodes</b>. Those machine can be linked to each other or have special network architectures. 
Generally speaking some machines are more important than other: they are more powerful and are thus more oriented toward orchestration, planning, ... <br/>Those are called <b>master</b> nodes while the regular one are called <b>worker</b> or <b>slave</b>: they are the one actually doing the computations and the storing.
 
<h3>Distributed architectures are cheaper</h3>
For decades, improvements on transistor capacities, hence on storage and computing facilities have been increasing exponentially, following Moore's law. Lately, due to physical limitations, we witnessed a downturn in this trend.  
It is now cheaper to buy cheap hardware, also called commodity hardware, in number than buying the largest possible machine. For the same computer power it is cheaper to use distributed architectures than very powerful single machines.

<h3> Distributed architectures are more secured</h3>
There are two important aspect in distributed architectures: 
<ul>
<li><b>Partitioning</b>: data is cut into blocks of a given maximal size and spread across the cluster.</li>
<li><b>Replication</b>: data is replicated which means that we create copies of our partitions.</li>
</ul>

@slider partition_replication_slider


At first you may think that this increases the demand for storage, which is true, but remember that storage is very cheap while data is key to business today. This partition/replication increases the security of the data. We cannot assume that the crash of a machine is an extraordinary event: this is an event that is going to happen so we need to have copies of the data that are available at any time:

@slider redundancy_security_slider

<i>In this example, a document is spread on a cluster of 6 machines. It is very simplified but we have to have 3 machines down before not being able to access this document. The likeliness of this happening in a time so short that no one can react is low. Moreover tools are designed to see when a machine is down and take action so that the data is replicated on another machine so that we have all our replicas in the cluster.<br/>
In some companies where data is a very sensible issue, data is replicated inside data centers which are themselves replicated in different countries in order to avoid natural disasters (floods, earthquake, ...) or man made phenomena (attacks, war, ...).</i>
<h3>Distributed architectures speeds up computing</h3>

Partitioning data allows different machine to work on the same document at the same time. This is a fundamental  aspect of distributed architectures: since documents are spread over different machine, those machines can work in parallel at the same time. Moreover, since the data is already stored in small computable chunks on different machines, we do not need to move data from a machine to another: we just have to pick available machines that have the data. 

@slider distributed_computing_slider


<h3>But distributed architectures face some problems</h3>

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

<h2>Map Reduce</h2>

MapReduce is a programming model used widely in distributed systems to perform calculations. It has been patented by Google in 2004. MapReduce relies on the emission of key-value pairs during a Map phase and the aggregation of the values by keys during the Reduce phase.

Every partition of the data undergoes the same transformation, emitting a set of key-value pairs. This is the <b>Map</b> phase. Those pairs are emitted to a machine based on the key of the pair.

For example every pair with the key <code>key_1</code> is sent to a specific machine no matter how many keys there are. There can be different keys on a single machine but every value corresponding to a key need to be on the same machine. Creating the key-value pairs is done during the <b>Map</b> phase while the sorting and dispatching of values is called the <b>Shuffle</b> phase.

Once all sent to the right machine, values are aggregated by key to get the final result: this is the <b>Reduce</b> phase. 

<h3>WordCount</h3>
To explain how Map Reduce works, the usual example is to take the `WordCount` task, e.g. computing the frequencies of words. It is the <code>print('hello world')</code> of MapReduce.

During the <b>Map</b> phase, the partitions of the text are lowered, tokenized and for each token, we emit the token as the key and 1 as the value.

The pseudo-code for this step is the following:

<blockquote>
<code class="plaintext" onclick="copyText(this);" style="cursor:pointer;">INPUT: data (list of strings)<br>
FOR EACH partition IN data:<br>
  token_list = TOKENIZATION(partition)<br>
  FOR EACH token IN token_list:<br>
    EMIT((token, 1))</code>
</blockquote>

Remember that the <b>Shuffle</b> phase forces all values corresponding to the same key to be on the same reducing machine. So on every machine used during the <b>Reduce</b> phase, we have a set of keys, corresponding to some tokens present in the text and for each key a list of ones of length corresponding to the number of instances of this token over the partitions. 

The pseudo-code for the <b>Reduce</b> is given in the following block: the code is given only for one key because during the <b>Reduce</b>, keys are treated totally independently.

<blockquote>
<code class="plaintext" onclick="copyText(this);" style="cursor:pointer;">INPUT: key (string), list_of_values (list of integers)<br>
s = 0<br>
FOR EACH i IN list_of_values:<br>
  s = s + i<br>
EMIT((key, s))</code>
</blockquote>
  
@slider mapreduce_wordcount_slider


The succession of a <b>Map</b>, <b>Shuffle</b> and <b>Reduce</b> phases is called a <b>Job</b>. We can combine multiple Jobs to perform complicated tasks. The number of reducers and mappers is up to the operator: if they is not a mapper by partition, some mappers will will take care of multiple partitions sequentially. On the other hand, having too many machines involved in an operation, some may not be available for other operations in the same time.

<h3>Advanced MapReduce: Combiners</h3>

You may have noticed that during the Map phase of Wordcount, we have emitted the same keys twice on the same mapper machine. This can be problematic as this may increase significantly the number of values that are emitted. 

We can aggregate those values during the <b>Map</b> phase using a <b>Combiner</b>: this can be considered as a <b>Reduce</b> phase in the mapper. If we take the example of Wordcount, the new pseudo-code for the <b>Map</b> is the following: 

<blockquote>
<code class="plaintext" onclick="copyText(this);" style="cursor:pointer;">INPUT: data (list of strings)<br>
temp = DICTIONARY(string, integer)<br>
FOR EACH partition IN data:<br>
  token_list = TOKENIZATION(partition)<br>
  FOR EACH token IN token_list:<br>
    IF token in temp.keys:<br>
       temp.set(token, 1 + temp.get(token))<br>
    ELSE:<br>
       temp.set(token, 1)<br>
FOR EACH token IN temp.keys:<br>
  EMIT((token, temp.get(token))</code>
</blockquote>

@slider wordcount_combiner_slider

<h3>Advanced MapReduce: Partitioners</h3>

During the <b>Shuffle</b> phase, the values are sent to specific machines according to the associated keys. The default rule is generally: 

<center><code> number of the reducer machine(key) = HASH_FUNCTION(key) MOD number of reducer machines</code></center>

This ensures an even distribution of keys over reducer nodes: each machine should receive about the same number of different keys. The issue with that is that in some particular cases, some keys can be over-represented. This can create a bottleneck which will slow down the execution of the jobs.  
 
@slider mapreduce_partitioners_slider


<i>In this example, the key <code>key1</code> is over-represented. <br/>If we let the default partitioner take care of the <b>Shuffle</b>, then one of the reducer is going to receive much more data to process than the other but if we take into account the a priori knowledge of the distribution of values, we can define a partitioner that will balance the workload over the reducers.</i>

Partitioners cannot be coded dynamically: you have to know a priori the balance of values by key to implement one that will balance evenly the workload.

<h2>Apache Hadoop</h2>

Apache Hadoop is an Open Source framework for distributed architectures. It was first released in 2006 by Yahoo! but is now an Apache Foundation project. It is a widely used tool in Big Data to manage distributed storage and computing. 

<center><img src="https://github.com/pauldechorgnat/de_help/raw/master/static/Hadoop.png" style="width:20%"/></center>
<h3>Hadoop components</h3>

Hadoop is mainly composed of 3 components: 
<ul>
<li><b>HDFS</b> (Hadoop Distributed File System): HDFS is in charge a of partition, replication, orchestration of data. </li>
<li><b>YARN</b> (Yet Another Resource Negociator): YARN is in charge of orchestrating jobs and attributing resources.</li>
<li><b>Hadoop MapReduce</b>: Hadoop MapReduce is a Java API that implements the meta-class to perform MapReduce Jobs</li>
</ul>

While it is coded in Java, Hadoop allows also to use other programming languages by writing in and parsing the standard output directly. This allows us to code MapReduce Jobs in Python, Ruby, or any other language given that you can read from the standard output. This utility is called <b>Hadoop Streaming</b>.

<h4>HDFS</h4>

As stated before, <b>HDFS</b> is in charge of distributed storage. There are multiple daemons running in HDFS: 
<ul>
<li><b>Datanode</b>: datanode is the daemon running on the slave nodes and that is in charge of allocating the interacting with the other daemons to make the data stored on the machine available.</li>
<li><b>Namenode</b>: the namenode is a daemon running on a master node: it contains meta-data about the location of the partitions. The namenode interacts with the datanodes to read or write data. </li>
<li><b>SecondaryNamenode</b>: secondary namenodes are daemons running on other master nodes. They are taking snapshots of the namenode at regular time intervals. If the namenode crashes, they are able to take over its role</li>
</ul>
<h4>YARN</h4>
<b>YARN</b> is in charge of orchestrating work and jobs. There are several daemons running within YARN: 
<ul>
<li>The <b>Resource Manager</b> is the daemon in attributing resources to the different worker nodes. It runs on a master node.</li>
<li>The <b>Application Manager</b> is triggered by a client application. It is in charge of orchestrating jobs during the runtime of the application and asks the <b>Resource Manager</b> for resources.</li>
<li>The <b>Node Manager</b> is a daemon running on the worker nodes. It communicates with the <b>Resource Manager</b> at all time and with the <b>Application Manager</b> during the runtime of the application.</li>
<li><b>Containers</b> are the daemons triggered by the <b>Resource Manager</b> at the start of an application. They are in charge of the actual work. In fact, containers are <a href="https://en.wikipedia.org/wiki/Java_virtual_machine">JVM</a> with allocated disk and memory.</li>
</ul>

@slider slider_yarn_working

The code of an application contains information about the location of the files (in HDFS or locally), about the number of mappers and reducers and of course the code of Mappers, Combiners, Partitioners and Reducers. 

When it is launched, the <b>Resource Manager</b> triggers an <b>Application Manager</b> on one of the worker nodes. The <b>Application Manager</b> knows the resource needed (number of mappers and reducers) and asks the <b>Resource Manager</b> for those resources. 

The <b>Resource Manager</b> launches containers that includes a <b>JVM</b> and the code of the mappers and the reducers and communicates the address and ids of the containers to the <b>Application Manager</b>. 

Then, those containers communicate to the <b>Application Manager</b> which is in charge of orchestrating the jobs. The communication goes through the <b>Resource Manager</b> because <b>Hadoop</b> is based on a share-nothing model, e.g. worker nodes are only linked to the master nodes not one to each other. This leaves the <b>Resource Manager</b> available for other applications to be run on other nodes. 



<h2>Installing Hadoop</h2>
<i>In this part, we are going to install <b>Hadoop</b> in a pseudo-distributed mode. The components have already been downloaded but the setting must be done.</i>
<h3>Installation modes</h3>

There are 3 available installation modes: 
<ul>
<li><b>Distributed mode</b>: This is the standard mode: the installation is spread over a cluster with worker nodes and slave nodes. </li>
<li><b>Pseudo-distributed mode</b>: This mode is a demonstration mode: we simulate the functioning in a distributed mode on a single machine by routing the pseudo-nodes to different ports of the machine. </li>
<li><b>Stand-alone mode</b>: This is also a demonstration mode where one machine is taken as a single node network and the local file system is used in place of the distributed one.</li>
</ul>
<h3>Configuration files</h3>

The installation files are located under the archive <code>/home/ubuntu/hadoop-2.7.3.tar.gz</code>. 
<i>It has been downloaded from <a href="https://hadoop.apache.org/releases.html">Hadoop</a> website. </i>

First, we need to decompress the archive:
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">tar xvf /home/ubuntu/hadoop-2.7.3.tar.gz<br>
mv ~/hadoop-2.7.3 ~/hadoop</code>
</blockquote>

To check that it indeed has been decompressed, you can use the command: 
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">ls -l | grep hadoop</code>
</blockquote>


You should see both the archive and the folder with the same name (except the extension).


Now we need to edit the <code>/home/ubuntu/.bashrc</code> file to give it paths to Hadoop files. 

<i>We are going to use <code>nano</code> but you can use any text editor you want.</i>
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/.bashrc</code>
</blockquote>

Append those lines to the file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;"># HADOOP PATHS<br>
export JAVA_HOME=/usr<br>
export PATH=$PATH:/usr/bin/java<br>
export HADOOP_HOME=/home/ubuntu/hadoop<br>
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop<br>
export HADOOP_MAPRED_HOME=$HADOOP_HOME<br>
export HADOOP_COMMON_HOME=$HADOOP_HOME<br>
export HADOOP_HDFS_HOME=$HADOOP_HOME<br>
export YARN_HOME=$HADOOP_HOME<br>
export PATH=$PATH:$HADOOP_HOME/bin</code>
</blockquote>

Close the file and commit those changes with the <code>source</code>: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">source /home/ubuntu/.bashrc</code>
</blockquote>

We are going to check that <b>Java</b> and <b>Hadoop</b> are installed: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">java -version | grep openjdk<br>
hadoop version | grep Hadoop</code>
</blockquote>

You should see the version of the two softwares. 

We are now going to shape the cluster. 

There are several files that need to be edited. 

<h4><b>core-site.xml</b></h4>
This file contains settings for the <b>namenode</b>. The namenode address will be on local port 9000. 

Open the file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/hadoop/etc/hadoop/core-site.xml</code>
</blockquote>

Within the tags <code>&lt;configuration</code>, paste the following lines:

<blockquote>
<code class="html" onclick="copyText(this);" style="cursor:pointer;">&lt;property&gt;<br>
&lt;name&gt;fs.default.name&lt;/name&gt;<br>
&lt;value&gt;hdfs://localhost:9000&lt;/value&gt;<br>
&lt;/property&gt;</code>
</blockquote>
<h4><b>hdfs-site.xml</b></h4>
This file contains information about how HDFS functions: we are going to choose a replication factor of 2, e.g. there will be 3 copies of each file. We will specify also a local directory to store namenode data and the datanode data. Finally, we need to tell him not to check for security clearance at each action. 

Open the file:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/hadoop/etc/hadoop/hdfs-site.xml</code>
</blockquote>

Within the tags <code>&lt;configuration&gt;</code>, paste the following lines:

<blockquote>
<code class="html" onclick="copyText(this);" style="cursor:pointer;">&lt;property&gt;<br>
&lt;name&gt;dfs.replication&lt;/name&gt;<br>
&lt;value&gt;2&lt;/value&gt;<br>
&lt;/property&gt;<br>
&lt;property&gt;<br>
&lt;name&gt;dfs.permission&lt;/name&gt;<br>
&lt;value&gt;false&lt;/value&gt;<br>
&lt;/property&gt;<br>
&lt;property&gt;<br>
    &lt;name&gt;dfs.name.dir&lt;/name&gt;<br>
    &lt;value&gt;/home/ubuntu/data/namenode_data&lt;/value&gt;<br>
&lt;/property&gt;<br>
&lt;property&gt;<br>
    &lt;name&gt;dfs.data.dir&lt;/name&gt;<br>
    &lt;value&gt;/home/ubuntu/data/datanode_data&lt;/value&gt;<br>
&lt;/property&gt;</code>
</blockquote>
<h4><b>mapred-site.xml</b></h4>

In this file, we will simply state that the resource manager that will be used is YARN.

First, we need to copy/paste the template of this configuration file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp /home/ubuntu/hadoop/etc/hadoop/mapred-site.xml.template /home/ubuntu/hadoop/etc/hadoop/mapred-site.xml</code>
</blockquote>

Open the file:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/hadoop/etc/hadoop/mapred-site.xml</code>
</blockquote>

Within the tags <code>&lt;configuration&gt;</code>, paste the following lines:

<blockquote>
<code class="html" onclick="copyText(this);" style="cursor:pointer;">&lt;property&gt;<br>
&lt;name&gt;mapreduce.framework.name&lt;/name&gt;<br>
&lt;value&gt;yarn&lt;/value&gt;<br>
&lt;/property&gt;</code>
</blockquote>
<h4><b>yarn-site.xml</b></h4>

This files contains <b>YARN</b> settings. We simply tell him what <b>Java</b> classes should be used for the shuffle step: 

Open the file:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/hadoop/etc/hadoop/yarn-site.xml</code>
</blockquote>

Within the tags <code>&lt;configuration&gt;</code>, paste the following lines:

<blockquote>
<code class="html" onclick="copyText(this);" style="cursor:pointer;">&lt;property&gt;<br>
&lt;name&gt;yarn.nodemanager.aux-services&lt;/name&gt;<br>
&lt;value&gt;mapreduce_shuffle&lt;/value&gt;<br>
&lt;/property&gt;<br>
&lt;property&gt;<br>
&lt;name&gt;yarn.nodemanager.auxservices.mapreduce.shuffle.class&lt;/name&gt;<br>
&lt;value&gt;org.apache.hadoop.mapred.ShuffleHandler&lt;/value&gt;<br>
&lt;/property&gt;</code>
</blockquote>
<h4><b>hadoop-env.sh</b></h4>
In this file, we will just specify where <b>Hadoop</b> can find <b>Java</b>.

Open the file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/hadoop/etc/hadoop/hadoop-env.sh</code>
</blockquote>

Append this line to the file:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">export JAVA_HOME=/usr</code>
</blockquote>


One last thing to do is to generate SSH keys: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">ssh-keygen</code>
</blockquote>

Follow the default instructions (no password and default name) then add the key to the authorized keys: 
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp .ssh/id_rsa.pub .ssh/authorized_keys</code>
</blockquote>
<h3>Initialization</h3>


First we need to format the namenode: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs namenode -format </code>
</blockquote>

You can check that a folder has been created by using the following command:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">ls -l /home/ubuntu/data</code>
</blockquote>

Now we can start the daemons for <b>HDFS</b>: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">/home/ubuntu/hadoop/sbin/start-dfs.sh</code>
</blockquote>

You can see which <b>Java</b> processes are running at anytime by using the command <code>jps</code>.

If you run this command here, you should see: 
<ul>
<li>DataNode</li>
<li>NameNode</li>
<li>SecondaryNameNode</li>
</ul>

Now we can start <b>YARN</b> daemons:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">/home/ubuntu/hadoop/sbin/start-yarn.sh</code>
</blockquote>

If you run <code>jps</code>, you should see: 
<ul>
<li>ResourceManager</li>
<li>NodeManager</li>
</ul>
<h3>HDFS practice</h3>

For this part, we have downloaded a book from <a href="https://www.gutenberg.org/">Project Gutenberg</a> library: The Adventures of Sherlock Holmes. It is a simple text file available on your local file system at <code>/home/ubuntu/datasets/books/sherlock_holmes.txt</code>. You can check the headers of the book with the following command: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">head -n 20 /home/ubuntu/datasets/books/sherlock_holmes.txt</code>
</blockquote>

Most of the commands that we are going to use are based on the same pattern: <code>hdfs dfs -...</code> and we simply to write those commands into the shell. 

First, let's create a folder named <code>data</code> in our distributed file system: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -mkdir /data</code>
</blockquote>

You can check that the folder has indeed been created in the distributed file system and not in the local one by checking both systems at the root: 

<b>Local file system</b>
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">ls / | grep data</code>
</blockquote>
<b>HDFS</b>
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls / | grep data</code>
</blockquote>
<code class="bash">hdfs dfs -ls</code> is used in the same way <code>ls</code> is used in a usual shell. HDFS is organised as any UNIX file sytem, starting from the root <code>/</code>. 

We can also use the <code>-R</code> argument to have a recursive view of the folders: 
<code class="bash">hdfs dfs -ls -R /</code>. 

Notice that we always need to specify the absolute path as there are no current directory in <b>HDFS</b>.


We are now about to put our book into <b>HDFS</b>: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -put /home/ubuntu/datasets/books/sherlock_holmes.txt /data/</code>
</blockquote>

We can also use <code>-copyFromLocal</code>
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -copyFromLocal /home/ubuntu/datasets/books/sherlock_holmes.txt /data/</code>
</blockquote>

The main difference between those two commands is that <code>-put</code> can handle multiple files at once while <code>-copyFromLocal</code> cannot. 

The syntax is: 
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -put &lt;local_file_path&gt; &lt;distributed_path&gt;</code>
</blockquote>

This command is very similar to <code>cp</code> or <code>scp</code>.

We can check that the file is indeed here: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls -R /</code>
</blockquote>

Or print its content using <code>-cat</code>: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -cat /data/sherlock_holmes.txt</code>
</blockquote>

The contrary can be done using <code>-get</code>: 
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -get &lt;distributed_path&gt; &lt;local_path&gt;</code>
</blockquote>
 


Of course we can do a lot of the usual commands of a filesystem: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;"># removing a file<br>
hdfs dfs -rm /path/to/file<br>
# removing a folder <br>
hdfs dfs -rm -r /path/to/folder<br>
# copying a file from and to the distributed file system<br>
hdfs dfs -cp /path/to/file1 /path/to/file2<br>
# copying a folder from and to the distributed file system<br>
hdfs dfs -cp -r /path/to/folder1 /path/to/folder2<br>
# moving  a file from and to the distributed file system <br>
hdfs dfs -mv /path/to/file /new/path/to/file<br>
# moving  a folder from and to the distributed file system <br>
hdfs dfs -mv -r /path/to/folder /new/path/to/folder</code>
</blockquote>

We can also use regular expressions to address multiple files at the same time. 

<h4>User Interface</h4>

HDFS has also a way to visualize the file system information: if you open a window on the 50070 port, you should be able to see the UI. 
For example, you can see your files in <code>Utilities&gt;Browse the file system </code>.


<h4>Exercise</h4>
<i>In the folder <code>/home/ubuntu/books</code> there are <code>moby_dick.txt</code> and <code>alice.txt</code>. Try to do the following:
<ul>
<li>create a folder <code>/data/books</code>.</li>
<li>copy both books from local file system to this folder.</li>
<li>copy the file <code>sherlock_holmes.txt</code> on <b>HDFS</b> to this new folder. </li>
<li>print the content of those files.</li>
<li>make a copy of the folder <code>/data/books_backup</code>.</li>
<li>make a copy of <code>moby_dick.txt</code> named <code>moby_dick2.txt</code> in the same folder.</li>
<li>delete those two files from this folder in one command using a regular expression.</li>
<li>delete the folder <code>/data/books</code>.</li>
</ul>
</i>
<h3>MapReduce practice</h3>


We are going to execute a <b>MapReduce</b> job performing wordcount. 

<h4>Hadoop MapReduce</h4>

In this first part, we will perform a <b>WordCount</b> on <code>sherlock_holmes.txt</code> using the <b>Hadoop MapReduce Java</b> library. The application is already coded and compiled in the file <code>wordcount.jar</code> but it is available <a href="lien-vers-wordcount.java">here</a>. Feel free to read this file to get the pattern on <b>MapReduce</b> job implementation. You'll note that we did not specify a number of mappers and reducers, so there will be only one of each by default. 

To run this file, the syntax is the following: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hadoop jar /home/ubuntu/code/wordcount.jar WordCount /data/sherlock_holmes.txt /output_wordcount</code>
</blockquote>

More generally, to perform a <b>MapReduce</b>, we can do the following:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hadoop jar /path/to/jar/file ClassName ...</code>
</blockquote>

Here the two arguments are the input file and an output folder. Note that this folder should not exist before running this code. 
Once run, you can see that Hadoop is very wordy: there are a lot of information and it is sometimes difficult to read through it. 

Now we can check the result of our job: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls -R /output_wordcount</code>
</blockquote>

As you can see a file named <code>part-r-00000</code> has been created. It contains the result of the Job. 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -cat /output_wordcount/part-r-00000</code>
</blockquote>

This name corresponds to the fact that we have the output of a single reducer. If we had multiple reducers, we would have different files corresponding to the different partitions of our results with names incremented by 1 for each reducer. 

<h3>Hadoop Streaming with Python</h3>

As stated before, <b>Hadoop Streaming</b> allows us to perform <b>MapReduce</b> jobs using other languages than <b>Java</b>. 

In this part we are going to run a <b>MapReduce</b> job using <b>Python</b>.
In the folder <code>/home/ubuntu/code</code>, you can find <code>mapper.py</code> and <code>reducer.py</code>. Feel free to read their content: we are basically doing the same thing as before but with <b>Python</b> we are only printing out results in the standard output. Note also that we need to specify which command is used at the beginning of the file. 

Before running the command, we are just going to alias the command: this will ease the command. 

Open <code>.bashrc</code>:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano /home/ubuntu/.bashrc</code>
</blockquote>

Append the following lines to the file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">alias hadoop_streaming="hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar"</code>
</blockquote>

Do not forget to commit the changes to this file with <code>source ~/.bashrc</code>.

You can run the job by doing the following command: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hadoop_streaming \<br>
-file ~/code/mapper.py \<br>
-mapper ~/code/mapper.py \<br>
-file ~/code/reducer.py \<br>
-reducer ~/code/reducer.py \<br>
-input /data/sherlock_holmes.txt \<br>
-output /output_wordcount_streaming</code>
</blockquote>

We have to specify the code files twice because they are not hosted on the distributed file system. Moreover the output argument is still a non-existing folder in <b>HDFS</b>.

You can check the results: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls -R /output_wordcount_streaming<br>
hdfs dfs -cat /output_wordcount_streaming/part-00000</code>
</blockquote>

The code is a bit simpler than before so the results are a bit rougher. Yet we get the same idea. 

<h4>Exercise</h4>
<i>In this part, we will use the file <code>sentiment.csv</code> in the folder <code>/home/ubuntu/datasets</code>. This file contains two columns: the first represents the text of tweets while the second represents the sentiment (0 is for negative, 1 for positive). 

You shall do the following: 
<ul>
<li>put the file <code>sentiment.csv</code> into <b>HDFS</b>.</li>
<li>create a mapper and a reducer scripts in <b>Python</b> that will count the number of positive and negative tweets.</li>
<li>run this job and get its output into a folder <code>/output_count</code>.</li>
<li>import this file from <b>HDFS</b> into the <code>/home/ubuntu/datasets</code> folder.</li>
</ul>
</i>
<h3>Conclusion on Hadoop</h3>

In this part, we have seen the importance of distributed systems and the advantages it presents compared to classical architectures. We have also seen how to code in a framework like <b>MapReduce</b> and how to use specifically <b>Hadoop</b>. 

The whole <b>Hadoop</b> framework is interesting as it is one of the main cornerstone of many tools: we shall see some of them in the following lessons: Hive, Pig, Spark, HBase, ...

<h2>Hive</h2>
<h3>Introduction</h3>

Hive is a very interesting element of the Data Engineer toolbox. It provides a SQL-like interface for tabular data. Development started in 2007 at Facebook and it was first released as an Open Source project in 2015. Today, Hive is managed by the Apache Foundation. 

<center><img src="https://github.com/pauldechorgnat/de_help/raw/master/static/Hive.png" style="width:20%"/></center>


Hive is an abstraction of a relational database management system (RDBMS) but relies on Hadoop for distribution (repartition, partition, replication, …) and computation. It uses HQL (for Hive Query Language) which is a SQL like query language. 

Data is stored as flat files in HDFS and queries are actually translated from HQL to MapReduce jobs using YARN.

<h3> A word on execution planning</h3>

There is an important component of Hive, the metastore. The metastore is a local relational database used to store metadata on the location of the flat files in HDFS and the schema of the tables. 

The other important components of Hive are: 
<ul>
<li><b>CLI</b> (Command Line Interface): interface for the user to type in queries.</li>
<li><b>driver</b>: daemon that interprets queries and is the interface between the CLI, the compiler and the execution engine.</li>
<li><b>compiler</b>: daemon in charge of parsing the queries, dealing with the metadata needs and creating the DAG of the execution.</li>
<li><b>execution engine</b>: daemon in charge of interpreting the queries into MapReduce jobs and making the interface with Hadoop.</li>
</ul>

The mechanics are shown in the following figure: 

@slider hive_execution_slider 


<div class="alert-info">
<span class="glyphicon glyphicon-info-sign"> <b>DAGs</b> (Directed Acyclic Graphs) are a very important concept of execution planning. A DAG is a graph whose nodes are individual tasks and edges represent dependencies between those tasks. The goal of a DAG is to be optimized: tasks that can be performed at once are regrouped and independent tasks are set to be run in parallel. 
</span></div>
<h3> Partitioning </h3>

As stated before, Hive is not really a <b>RDBMS</b>: it acts like it but it is truly HDFS that is storing the files. In fact, <b>Hive</b> is just an interface that allows to make SQL-like queries on very large datasets: the ability to distribute files on several machines, hence the larger capacities, is what make Hive more interesting than a regular RDBMS. 

But some queries may take a while to perform because of the size of the datasets... In order to speed up queries, Hive has been implemented with the ability to partition data on different columns. For example, if you imagine a dataset with clients. We could partition it on the nationality of our clients. This means that we will have one file for each nationality. This file can be partitioned but each partition will contain one and only one nationality. This means that queries based on nationality will be highly sped up as there are no need to check every record. 

You can have multiple levels of partitioning (nationality, age group, gender, ...). 

<h3>Installation</h3>

In this part, we will install Hive. We will have to configure Hive and install an external relational database to serve as Metastore. There are multiple available choices but we will use <a href="https://db.apache.org/derby/">Apache Derby</a>.

First we need to decompress the archive files (to ease the use of these folders we will rename them): 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">tar xvf ~/apache-hive-2.3.6-bin.tar.gz<br>
tar xvf ~/db-derby-10.13.1.1-bin.tar.gz<br>
mv ~/apache-hive-2.3.6-bin ~/hive<br>
mv ~/db-derby-10.13.1.1-bin ~/derby</code>
</blockquote>


Then we need to update the paths in the <code>~/.bashrc</code> file:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano ~/.bashrc</code>
</blockquote>


In this file we will paste the following lines:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;"># PATHS FOR HIVE<br>
export HIVE_HOME=/home/ubuntu/hive<br>
export HIVE_CONF_DIR=$HIVE_HOME/conf<br>
export PATH=$PATH:$HIVE_HOME/bin<br>
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/*<br>
# PATHS FOR DERBY<br>
export DERBY_HOME=/home/ubuntu/derby<br>
export PATH=$PATH:$DERBY_HOME/bin<br>
export CLASSPATH=$CLASSPATH:$DERBY_HOME/lib/derby.jar:$DERBY_HOME/lib/derbytools.jar</code>
</blockquote>

Save the changes, close the file and commit the changes to the system with <code>source ~/.bashrc</code>.

Then we need to create folders in HDFS where data will be stored and change their rights (within HDFS) to give writing priviledges to group user.

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -mkdir -p /user/hive/warehouse<br>
hdfs dfs -mkdir /tmp<br>
hdfs dfs -chmod g+w /user/hive/warehouse<br>
hdfs dfs -chmod g+w /tmp</code>
</blockquote>

There are some configuration files to change too: copy the <code>$HIVE_HOME/conf/hive-env.sh.template</code> file and change its name. 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp $HIVE_HOME/conf/hive-env.sh.template $HIVE_HOME/conf/hive-env.sh<br>
nano $HIVE_HOME/conf/hive-env.sh</code>
</blockquote>

Add the line: <code>export HADOOP_HOME=/home/ubuntu/hadoop</code>, save and close the file. We need also to change the file containing the whole configuration of Hive:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp $HIVE_HOME/conf/hive-default.xml.template $HIVE_HOME/conf/hive-site.xml<br>
nano $HIVE_HOME/conf/hive-site.xml</code>
</blockquote>

This file contains a lot of information, a lot of parameters... To navigate through this file, you can use <code>ctrl + w</code> to look for a particular term. 

Here we need to make the following changes
<ul>
<li> <code>javax.jdo.option.ConnectionURL</code> property: <code>jdbc:derby:;databaseName=/home/ubuntu/hive/bin/metastore_db;create=true</code> value</li>
<li><code>hive.exec.local.scratchdir</code> property: <code>/tmp/hivedir</code> value </li>
<li><code>hive.downloaded.resources.dir</code> property: <code>/home/ubuntu/hive/tmp/${hive.session.id}_resources</code> value</li>
</ul>

We need to create a last file for Hive: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">nano $HIVE_HOME/conf/jpox.properties</code>
</blockquote>

In this file we need to paste the following lines: 

<blockquote>
<code onclick="copyText(this);" style="cursor:pointer;">javax.jdo.PersistenceManagerFactoryClass=org.jpox.PersistenceManagerFactoryImpl<br>
org.jpox.autoCreateSchema=false<br>
org.jpox.validateTables=false<br>
org.jpox.validateColumns=false<br>
org.jpox.validateConstraints=false<br>
org.jpox.storeManagerType=rdbms<br>
org.jpox.autoCreateSchema=true<br>
org.jpox.autoStartMechanismMode=checked<br>
org.jpox.transactionIsolation=read_committed<br>
javax.jdo.option.DetachAllOnCommit=true<br>
javax.jdo.option.NontransactionalRead=true<br>
javax.jdo.option.ConnectionDriverName=org.apache.derby.jdbc.ClientDriver<br>
javax.jdo.option.ConnectionURL=jdbc:derby://hadoop1:1527/metastore_db;create=true<br>
javax.jdo.option.ConnectionUserName=APP<br>
javax.jdo.option.ConnectionPassword=mine</code>
</blockquote>

We also need a directory for derby:
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">mkdir $DERBY_HOME/data</code>
</blockquote>

Finally, the last step of the installation the initialization of the derby database:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">$HIVE_HOME/bin/schematool -dbType derby -initSchema</code></blockquote>

Now Hive should be installed and you should be able to launch it through the <code>hive</code> command (to leave the CLI, type in <code>exit</code>).

<h3>Practice</h3>

In this part, we will try to show you how Hive works. First we need to put a file into HDFS: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -put /home/ubuntu/datasets/movies/ratings.csv /ratings.csv<br>
hdfs dfs -put /home/ubuntu/datasets/movies/movies.csv /movies.csv</code>
</blockquote>


Check that the file is indeed uploaded:
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls /</code>
</blockquote>

Next, open Hive CLI with <code>hive</code>. As with a lot of relational databases, you can use <code>SHOW DATABASES;</code> to see what databases are already in Hive. We will need to use one of them to carry on. Here we will of course need to create one:

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">CREATE DATABASE my_hive_db;<br>
USE my_hive_db;</code>
</blockquote>

We should see what the tables in <code>my_hive_db</code> are with <code>SHOW TABLES;</code>: there are no tables yet. 

To create a table the syntax is very similar to regular RDBMS. Here we want to create a table <code>ratings</code>.

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">CREATE TABLE ratings<br>
(userid int, <br>
movieid int, <br>
rating double, <br>
time_stamp int) <br>
ROW FORMAT DELIMITED<br>
 FIELDS TERMINATED BY ","<br>
LINES TERMINATED BY "\n" <br>
STORED AS TEXTFILE;</code>
</blockquote> 

Note that we need to specify some things that are unusual at this step: how data is and will be stored. 

To load data into the table, the syntax is similar to regular RDBMS syntax: 

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">LOAD DATA INPATH '/ratings.csv' <br>
INTO TABLE ratings;</code>
</blockquote>

Notice that the path to the file is the HDFS path. If we want to load a file from the local file system, we can use the following tweak: <code>LOAD DATA LOCAL INPATH ... </code>. 

Once you have loaded the file, quit Hive with the <code>exit</code> command. 

To illustrate how Hive works we are going to list the files at the root of HDFS: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls /</code>
</blockquote>

The file <code>ratings.csv</code> has disappeared. In fact, it has been moved into the <code>/user/hive/warehouse</code>. We can list recursively the content of this folder: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls -R /user/hive/warehouse/</code>
</blockquote>

You should see that a folder <code>db.my_hive_db</code> has been created. It contains a folder <code>ratings</code> that correspond to the table in question and its content is a file <code>part-00000</code>. If the file was larger we could have had multiple partitions. 


We can print the content of this file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -cat /user/hive/warehouse/db.my_hive_db/ratings/part-00000</code>
</blockquote>

The content of the file has not been changed. 

Now let's return to Hive CLI: <code>hive</code>.

We are going to create a table to illustrate the Hive partitioning abilities. To create a partitioned table, we need to specify on which variable we want to partition: 


<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">USE my_hive_db;<br>
CREATE TABLE ratings_part <br>
(userId int, movieId int, times int)<br>
PARTITIONED BY (rating double) <br>
STORED AS TEXTFILE;</code>
</blockquote>


We want to partition the table on the <code>rating</code> column so we have to specify it in last position. To insert data into the table, we will use a query on the <code>ratings</code> table: 

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">INSERT INTO TABLE ratings_part<br>
PARTITION (rating)<br>
SELECT userId, movieId, time_stamp, rating<br>
FROM ratings</code>
</blockquote>

The <code>rating</code> column is in last place because of the definition of the table <code>ratings_part</code>. Once these commands are launched into Hive CLI, return to the shell and launch the following command to inspect the content of HDFS:

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls -R /user/hive/warehouse/my_hive_db.db</code>
</blockquote>

You can see that the folder <code>ratings_part</code> is subdivided in multiple subfolders corresponding to the different partitions of the column <code>rating</code>.

We will just try to see if there are differences between the two tables: connect to the Hive CLI and run the following command: 

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">USE my_hive_db;<br>
SELECT COUNT(*) AS nb_ratings, rating FROM ratings<br>
GROUP BY rating; </code>
</blockquote>

Once you have seen the time taken to run the query, run the following: 

<blockquote>
<code class="SQL" onclick="copyText(this);" style="cursor:pointer;">SELECT COUNT(*) AS nb_ratings, rating FROM ratings_part<br>
GROUP BY rating; </code>
</blockquote>

You should see a difference between the two tables: in the first case, we have to check every line while in the second case, the ratings are already stored in different partitions, so the query takes less time.

We are not going to go deeper on Hive for the moment: this is an interesting tool to use the power and the accessibility of RDBMS in a distributed framework.

<h2>Pig</h2>

Apache Pig is a useful tool to perform data manipulation in a distributed environment. It has its own language: <b>Pig Latin</b> and abstracts MapReduce jobs. The idea behind Pig is to simplify the use of MapReduce: for example, the wordcount jobs take about 60 lines in <b>Java</b> while it takes  5 lines with Pig. 

<center><img src="https://github.com/pauldechorgnat/de_help/raw/master/static/Pig.png" style="width:20%"/></center>


Moreover, Pig is using lazy evaluations and DAGs to optimize the queries: the queries are passed through a parser, an optimizer, a compiler and then an execution engine to run the queries. Pig can use different orchestrators (Yarn, Spark, Tez, ...) 

<h3>Installation</h3>

In this part, we are going to install Pig. 

First extract the archive: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">tar xvf ~/pig-0.17.0.tar.gz<br>
mv ~/pig-0.17.0 ~/pig</code>
</blockquote>

We simply need to add paths to the Pig in the <code>~/.bashrc</code> file.

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;"># PIG PATHS <br>
export PIG_HOME=/home/ubuntu/pig<br>
export PATH=$PATH:$PIG_HOME/bin<br>
export PIG_CLASSPATH=$HADOOP_HOME/etc/hadoop<br>
# HCATALOG PATHS<br>
export HCAT_HOME=$HIVE_HOME/hcatalog<br>
export PATH=$PATH:$HCAT_HOME/bin</code>
</blockquote>

Next, we need to launch Hadoop Job History Server: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver</code>
</blockquote>

Now to check that Pig is working, just run <code>pig</code>. This should open Pig CLI <code>grunt</code>. To leave this interface, you can use <code>quit</code>.

<h3>Pig Latin</h3>

The basic data structure is called a relation in Pig. It is basically a list of named objects. Those objects are of the same type: this means that the structure needs a schema. To load data, we use the <code>LOAD</code> keyword as following:

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">movies = LOAD 'hdfs:///movies.csv USING PigStorage(',') AS (id:int, title:chararray, genres:chararray);</code>
</blockquote> 

Except if you have missed the right path to the file, there should not be a lot of information printed when this command is launched: it is because of the lazy evaluation.

Here the schema is introduced by the <code>AS</code> keyword: here we have a column of integers and two columns of strings. 

The keyword <code>USING</code> introduces the function used to load data. There are many different functions corresponding to different file types. We will see later how to load directly data from Hive with a different function. 

If we want to execute the operations completely of partly, we can use the following keywords: 
<ul>
<li><code>describe movies;</code>: this line returns the schema of the relation.</li>
<li><code>illustrate movies;</code>: this line returns a line of the relation as an example.</li>
<li><code>explain movies;</code>: this line returns the different steps in the DAGs to get to this relation.</li>
<li><code>dump movies;</code>: this line prints out the content of the relation.</li>
<li><code>STORE moveis INTO 'hdfs:///movies2.csv' USING PigStorage(',');</code>: this line writes the content of the relation into a file in HDFS.</li>
</ul>

To perform map operations, we can use the <code>FOREACH</code> and <code>GENERATE</code> keywords. For example, if we want to create a relation with only the column <code>genre</code>, we can use: 

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">genres_list = FOREACH movies GENERATE genres AS genres_of_the_movie;</code>
</blockquote>

This line of code creates a relation named <code>genres_list</code> with the following schema <code>(genres_of_the_movie: chararray)</code>.

We can also perform flatmap operations (eg generating multiple lines per line), using the <code>FLATTEN</code> keyword: 

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">unique_genre_list = FOREACH genres_list GENERATE FLATTEN(STRSPLIT(genres_of_the_movie, '\\|')) as genre;</code>
</blockquote>

As a reminder, the content of the column <code>genres_of_the_movie</code> is a pipe (<code>|</code>) separated file. 

We can perform Group By operations with <code>GROUP</code>: 

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">genres_group = GROUP unique_genre_list BY genre;</code>
</blockquote>

If you illustrate the content of the relation, you will see that it is similar to a dictionary with the values being list of keys: for example, <code>{'comedy': ['comedy', 'comedy'], ...}</code>. 

To reduce this relation, we can use <code>FOREACH</code> once again: 

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">genres_count = FOREACH genres_group GENERATE group AS genre, COUNT(unique_genre_list) AS nb_movies;</code>
</blockquote> 

Notice that in this example, we have done something very similar to the wordcount example.

There are also other keywords that can be used (that are very similar to <code>SQL</code>): 
<ul>
<li><code>FILTER ... BY ...</code></li>
<li><code>ORDER ... BY ...</code></li>
<li><code>JOIN ... BY ... LEFT ... BY </code></li>
<li><code>UNION ..., ...</code></li>
<li>...</li>
</ul>

One other interesting thing is the ability to use user defined functions (UDFs). UDFs are specified in a Java archive and must follow certain <a href="https://pig.apache.org/docs/latest/udf.html">rules</a>. To import a function, you can use: 

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">REGISTER '&lt;path_to_the_jar_file&gt;';<br>
DEFINE &lt;alias_name&gt; &lt;full.name.of.the.function&gt;;<br>
&lt;/full.name.of.the.function&gt;&lt;/alias_name&gt;&lt;/path_to_the_jar_file&gt;</code>
</blockquote>

Pig is interesting because there are a lot of different pre-defined functions (maths, text, ...) and you can define your own functions. Moreover it can be linked easily to Hive. For this you need to launch <code>grunt</code> with the commande <code>pig -useHCatalog</code> and use the following syntax while loading data:

<blockquote>
<code class="pig" onclick="copyText(this);" style="cursor:pointer;">&lt;relation_name&gt; = LOAD '&lt;database_name&gt;.&lt;table_name&gt;' <br>
USING org.apache.hive.hcatalog.pig.HCatLoader();<br>
&lt;/table_name&gt;&lt;/database_name&gt;&lt;/relation_name&gt;</code>
</blockquote>

And to store data directly in Hive, we can use the <code>org.apache.hive.hcatalog.pig.HCatStorer()</code>.

In some aspects, Hive and Pig are quite similar. They both can be used for Data Manipulation but the first one can also store data as an abstracted relational database. This is the main difference but the two tools also do not have the syntax. Basically, Pig is more advanced in terms of customization but it is really up to the user of these tools. 

<h2>Sqoop</h2>

Finally, this last part will deal with Apache Sqoop: this tool can be used for ETL (Extract Transform Load) pipelines. Basically, Sqoop is used to transfer data from relational databases to HDFS (and the other way around). 

<center><img src="https://github.com/pauldechorgnat/de_help/raw/master/static/Sqoop.png" style="width:20%"/></center>


This can be very interesting to use the power of distributed computing power on regular databases, or to store transformed data into a datalake based on Hadoop. 

<h3>Installation</h3>

First we must decompress the archive: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">tar xvf ~/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz<br>
mv sqoop-1.4.7.bin__hadoop-2.6.0 ~/sqoop</code>
</blockquote>

Open the file <code>~/.bashrc</code> and paste the following lines: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">export SQOOP_HOME=/home/ubuntu/sqoop<br>
export PATH=$PATH:$SQOOP_HOME/bin</code>
</blockquote>

Save, close and commit (using <code>source ~/.bashrc</code>) this file. 

Next we need to change a few lines in the configuration file: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp $SQOOP_HOME/conf/sqoop-env-template.sh $SQOOP_HOME/conf/sqoop-env.sh<br>
nano $SQOOP_HOME/conf/sqoop-env.sh</code>
</blockquote>

Paste those lines: 
<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">export HADOOP_COMMON_HOME=$HADOOP_HOME<br>
export HADOOP_MAPRED_HOME=$HADOOP_HOME</code>
</blockquote>

Finally, there is a file that we need to put into the <code>$SQOOP_HOME/lib</code> folder: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">cp /usr/share/java/mysql* $SQOOP_HOME/lib</code>
</blockquote>
<h3>Practice Sqoop</h3>

The main features of Sqoop are pretty easy to use. On your machine, we have installed <b>MySQL</b>: it contains a database named <code>my_db</code> and a table called <code>movies</code>. 

To import data from MySQL to HDFS, the syntax is the following: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">sqoop import --connect jdbc:mysql://localhost:3306/my_db \<br>
--username hduser \<br>
--P \<br>
--table movies \<br>
--m 1 \<br>
--target-dir /data/movies \<br>
--fields-terminated-by '^'</code>
</blockquote>

We are using <code>sqoop import</code> to import data and the arguments are:
<ul>
<li><code>--connect</code>: we have the Java DataBase Connector <code>jbdc</code>, the name of the RDBMS <code>mysql</code>, the open port of the RDBMS <code>localhost:3306</code> and the database name <code>my_db</code>.</li>
<li><code>--username</code>: indicates the username in MySQL</li>
<li><code>--P</code>: indicates that we want to type in our password. Here the password is <code>password</code>.</li>
<li><code>--table</code>: name of the table we want to import <code>movies</code>.</li>
<li><code>--m</code>: the number of mappers to use.</li>
<li><code>--target-dir</code>: the name of the directory to put the data in.</li>
<li><code>--fields-terminated-by</code>: the character to use to separate the fields</li>
</ul>

Once you have run this command, you can check if the data has been imported into HDFS. 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">hdfs dfs -ls /data/movies<br>
hdfs dfs -cat /data/movies/part-m-00000</code>
</blockquote>

Instead of importing the whole table, you can also import only some of it using the argument <code>--query</code>: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">sqoop import --connect jdbc:mysql://localhost:3306/my_db \<br>
--username hduser \<br>
--P \<br>
--query "SELECT * FROM movies WHERE movies.genres = 'comedy' AND \$CONDITIONS" \<br>
--m 1 \<br>
--target-dir /data/comedies \<br>
--fields-terminated-by '^'</code>
</blockquote>

This is very useful for ETL pipelines. Notice that we need to specify a condition with <code>WHERE</code> and the condition has to contain <code>\$CONDITIONS</code>. 

Arguments for the export from HDFS to MySQL are approximately the same: 
<ul>
<li>use <code>sqoop export</code> instead of <code>sqoop import</code>.</li>
<li>use <code>table</code> to indicate the table in which to place the data.</li>
<li>use <code>--fields-terminated-by</code> to indicate how to parse the file.</li>
<li>use <code>--export-dir</code> to indicate what is the path to the file to export in HDFS.</li>
</ul>

One other feature that is interesting is the ability to import data directly into Hive: 

<blockquote>
<code class="bash" onclick="copyText(this);" style="cursor:pointer;">sqoop import --connect jdbc:mysql://localhost:3306/my_db \<br>
   --username hduser --P \<br>
   --table movies \<br>
   --hive-import \<br>
   --hive-table my_db.movies \<br>
   -m 1</code>
</blockquote>

The table does not need to be created as Sqoop will create it during this command. If we want to import only a query, use the <code>--query</code> argument as before and if you want to import all the tables, change <code>sqoop import</code> to <code>sqoop import-all-tables</code> and <code>hive-table</code> to <code>hive-database</code>.

<h1>Conclusion</h1>

In this lecture, we have seen the advantages of distributed over classical architecture: security, computation and storage capacities enhanced, cost-efficient, ... Hadoop is the main framework in this domain as it is Open Source and that a lot of tools are based on its source code: Hive and Pig are useful to manipulate data, create datasets that can be used by Data Scientists and Data Analysts and provide interfaces that are more useful while Sqoop is used to do ETL pipelines. 
