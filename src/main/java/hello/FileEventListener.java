package hello;

import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import com.mongodb.DBObject;

public class FileEventListener extends AbstractMongoEventListener<File> {

    @Override
    public void onBeforeConvert(File file) {

    }

    @Override
    public void onBeforeSave(File file, DBObject dbo) {
    	file.setName(file.getName() + "_cheese");
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