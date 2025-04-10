# Description
This project consists of a web platform where developers (or anyone) can access various services to help with their daily tasks.  
The platform provides resources such as:

- URL metadata visualization
- File sharing via link
- Random user data generator (for tests, mocks...)

# Developers
- [Silvio Cabral de Melo Junior](https://github.com/SilvioCMJ)  
- [Gustavo Felipe da Costa Silva](https://github.com/gusttavofelipe)  
- [Roger Santos Vargas](https://github.com/Rogerdev02)  
- [Paulo Henrique de Oliveira Carvalho](https://github.com/Paulo-Henrique06)  

# How It Works
## Services

- **LinkPreview**:  
  When accessing the service, enter the URL you want to view metadata for in the text field and click `Pull`. The metadata  
  for that URL will then be displayed.

  Metadata cannot be obtained for URLs with the following patterns:  
  - http://example.com:8080 (specified port)  
  - http://example.com/page?query=1 (query parameter)  
  - http://example.com/page#section (fragment)  
  - http://example.com/space%20 (special character)  

- **File.io**:  
  When accessing the service, choose the file you want to share with a permitted extension, click `Send`,  
  and a URL for downloading that file will be generated.

  - It is possible to handle file formats beyond those specified by implementing in the code.
  - You can also control the time the link will be available by changing the `expires` parameter.
  - To manage configurations, visit the official [File.io](https://www.file.io/) website.

- **Random User Generator**:  
  When accessing the service, simply click the `Random User Generator` button, and random user data will be generated.

  Allowed Formats:
  - JSON (default)
  - PrettyJSON or pretty
  - CSV
  - YAML
  - XML

  To filter users by parameters such as gender, nationality, and more, consult the official [Random User Generator API](https://randomuser.me/documentation) site.
