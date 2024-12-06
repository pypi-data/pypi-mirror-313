# Dakiya Python Client



# Build and Upload

```
make build
make upload
```

# Usage

```
from dakiya import transmitter

var = {
    "who": "Shamail",
    "time": "1:10",
}
result = transmitter.send_email("nitrox/welcome.html", to = "john.doe@example.com", subject = "Hello World!", attachments=[open("/tmp/image.png", "rb+")], **var)
```





