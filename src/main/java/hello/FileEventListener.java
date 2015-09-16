package hello;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import org.springframework.stereotype.Component;

import com.mongodb.DBObject;

@Component
public class FileEventListener extends AbstractMongoEventListener<File> {

    @Autowired
    private MongoOperations mongoOperations;
	
    @Override
    public void onBeforeConvert(File file) {

    }

    @Override
    public void onBeforeSave(File file, DBObject dbo) {
    	dbo.put("name", file.getName() + "_cheese");
    }

    @Override
    public void onAfterSave(File file, DBObject dbo) {

    }

    @Override
    public void onAfterLoad(DBObject dbo) {

    }

    @Override
    public void onAfterConvert(DBObject dbo, File file) {

    }

}