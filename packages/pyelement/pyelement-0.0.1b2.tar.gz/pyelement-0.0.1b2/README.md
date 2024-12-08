# pyelement
Send messages to element.io messanger from python

### Install pyelement
```pip install pyelement```

### Usage example

```
element = Element(messanger_path="https://host.ru", email = "your_mail@mail.ru", password = "secret_password"))
```
OR use a token (preferred way). It'll not create additional session
```
element = Element(messanger_path="https://host.ru", token = "secret_token"))
```

If you don't have token get it:
```
element = Element(messanger_path="https://host.ru", email = "your_mail@mail.ru", password = "secret_password"))
token = element.get_token()
```

Send message
```
element.send_message(room_name="RoomName", message="Hello from pyelement!")
```
You can find room name in settings section of the room

Log out
```
element.logout()
```