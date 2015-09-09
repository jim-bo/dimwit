
package hello;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "file", path = "file")
public interface FileRepository extends MongoRepository<File, String> {

	List<File> findByName(@Param("name") String name);

}
