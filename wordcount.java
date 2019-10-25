import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

// defining the class WordCount
public class WordCount {

  // defining the class TokenizerMapper
  // this class is in charge of the mapping process
  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{
    // it extends the class Mapper from mapreduce api
    // this mapper takes as input an Object (identifier of the partition) and a Text (the partition of the text)
    // it outputs a Text (a word) and an Integer (1)

    // defining the value to emit
    private final static IntWritable one = new IntWritable(1);
    // initializing the word to emit
    private Text word = new Text();

    // defining the function performed during map
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      // tokenizing the text partition
      StringTokenizer itr = new StringTokenizer(value.toString());

      // running through the tokens
      while (itr.hasMoreTokens()) {
        // setting the value of word
        word.set(itr.nextToken().toLowerCase().replaceAll("[^a-z 0-9A-Z]",""));
        // emitting the key-value pair
        context.write(word, one);
      }
    }
  }

  // defining the class IntSumReducer
  // this class is in charge of the reducing process
  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    // it extends the class Reducer from mapreduce api
    // it takes as input a Text (a word) and a list of integers (1s)
    // it outputs a Text (a word) and an integer (the frequency of the word)

    // initializing the frequency
    private IntWritable result = new IntWritable();

    // defining the function performed during reduce
    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      // initializing the the sum
      int sum = 0;
      // running through the values associated to this key
      for (IntWritable val : values) {
        // incrementing the sum
        sum += val.get();
      }
      // attributing the sum to the value to emit
      result.set(sum);
      // emitting the key-value pair
      context.write(key, result);
    }
  }

  // defining the main class containing the parameters of the job
  public static void main(String[] args) throws Exception {
    // initializing configuration
    Configuration conf = new Configuration();
    // initializing job
    Job job = Job.getInstance(conf, "word count");
    // providing job with the classes for mapper and reducer
    job.setJarByClass(WordCount.class);
    job.setMapperClass(TokenizerMapper.class); // mapper
    job.setCombinerClass(IntSumReducer.class); // combiner
    job.setReducerClass(IntSumReducer.class); // reducer
    // providing job with the output classes
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    // arguments to interpret
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    // completion of the job
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}