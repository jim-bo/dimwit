package hello;

import org.springframework.data.annotation.Id;

public class File {

	@Id private String id;

	private String name;
	private String upload_url;
	private Boolean ready;
	
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getUpload_url() {
		return upload_url;
	}
	public void setUpload_url(String upload_url) {
		this.upload_url = upload_url;
	}
	public Boolean getReady() {
		return ready;
	}
	public void setReady(Boolean ready) {
		this.ready = ready;
	}
}
