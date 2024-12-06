# st-iframe-postmessage

This component sends postMessage to the window where Streamlit application is embedded in iframe

## Installation instructions

```sh
pip install st-iframe-postmessage
```

# Usage instructions

```python
import streamlit as st

from st_iframe_postmessage import st_iframe_postmessage

st_iframe_postmessage(message={"message": "Hello World"})
```
