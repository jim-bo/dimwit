
package hello;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "matrix", path = "matrix")
public interface MatrixRepository extends MongoRepository<Matrix, String> {

	List<Matrix> findByName(@Param("name") String name);

}
