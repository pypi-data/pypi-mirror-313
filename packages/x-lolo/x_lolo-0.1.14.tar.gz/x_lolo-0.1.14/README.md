
# x_lolo

x_lolo is a Python library that allows direct use of Twitter's (formerly X) unofficial API without intermediaries, enhancing security.

## Key Features

- Direct interaction with Twitter's unofficial API
- Developed based on reverse engineering of the API
- Utilizes the HTTPS proxy [mitmproxy](https://mitmproxy.org/) for traffic analysis
- No dependency on web scraping tools like Selenium
- Automation capabilities for various Twitter interactions

## Objectives

- Provide a simple Python interface to interact with Twitter's API
- Offer a secure alternative to traditional authentication methods
- Allow developers to access Twitter features without relying on third-party services

## Project Status

The project is currently under development. It is designed for developers who need direct control over interactions with Twitter's API. 
For now, you can only log in, save the session, and create a post. Other functionalities are in development.

### Example test:

```python 
from x_lolo.session import Session
new_session = Session(load_from="session_data.yaml")

post = new_session.add_post("here is a post")

print(post.__dict__)
```


The project is hosted at: https://github.com/mohaskii/x_lolo_project/

Contributions are welcome!

Your help in making x_lolo better is greatly appreciated!