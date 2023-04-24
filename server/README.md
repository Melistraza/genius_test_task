# Python

### Run Server
> python3 web_transport.py certificate.pem certificate.key

### Kill
> kill -15 $(lsof -ti:4433)

### Browser MacOS
>For local testing with browser
> 
> /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --origin-to-force-quic-on=localhost:4433 --ignore-certificate-errors-spki-list=dRdC5nAgSeEPsnMF9SvWeoPshvK0SHUp52dnbJlPmxM=

### Install Driver for testing
```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
```

### Run tests
> python tests.py