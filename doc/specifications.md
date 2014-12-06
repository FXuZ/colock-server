Model Specifications
========

## Server Model Hierarchy
### `User`
    - `id`: (managed by SQL self increment, elsewhere called uid) internal id to distinguish user
    - `cid`: [ GeTui ](http://www.igetui.com) client id, uploaded by user on register or retrieving account on other device
    - `ukey`: key on device for authentication, delivered to user on register or retrieving account on other device
    - `region_num`: region code of the user
    - `phone_num`: phone number of the user, uploaded on register
    - `nickname`: nickname of the user
    - `reg_time`: register time
### `Message`
    - `sender_uid`: internal id of sender
    - `receiver_uid`: internal id of receiver
    - `message_key`: hash sum of sender id, receiver id and time stamp, which is also used for uploaded filename
    - `send_time`: send time of the message, actually server time when the request arrives
    - `exist`: bool, set to false when the receiver has finished downloading and delete the file
    - `filetype`: string, type of the file

## Stored on client phone
- `cid`: received from GeTui server via SDK
- `region_num`
- `phone_num`
- `phone_num_hash`
- `ukey`
- `uid`
- list of phone contact hashes

todo:
    - friend management
    - user group management
    - friend discovery via phone contacts

## Request and Response
### Register
- request:
    - `cid`: GeTui client id from GeTui sdk
    - `region_num`: region code
    - `phone_num`: phone number
    - `nickname`
- response:
    - `uid` : user's id
    - `ukey`: a random string used as a key
todo: encryption, sms activation

### Send image
- request:
    - `phone_hash`: hash of the user phone_num
    - `ukey`: combined with phone_hash to authenticate user
    - `receiver_uid`: uid of the receiver
    - `img_file`: image file binary data

- response:
    none except http standard header

- in server:
    push message data to GeTui server, data structure is a json
    ```python
    data = {
      "sender_region": sender.region_num,
      "sender_phone": hash(sender.phone_num),
      "message_id": message.id,
      "message_key": message.message_key,
      "send_time": message.send_time,
    }
    ```
    and this should be what the client should receive.

### Get image
- request:
    - `sender_phone`: hash of sender phone number
    - `receiver_phone`: hash of receiver phone number
- response:
    - `img_file`: image file binary data
