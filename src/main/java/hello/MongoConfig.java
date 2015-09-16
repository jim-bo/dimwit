package hello;

import java.net.UnknownHostException;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.mongodb.Mongo;

@Configuration
public class MongoConfig {

  /*
   * Use the standard Mongo driver API to create a com.mongodb.Mongo instance.
   */
   @Bean
   public Mongo mongo() throws UnknownHostException {
       return new Mongo("localhost");
   }
   
   @Bean
   public FileEventListener fileEventListener() {
	   return new FileEventListener();
   }
}