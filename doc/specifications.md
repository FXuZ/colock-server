Model Specifications
========

## todo:

    - [ ] friend management
    - [ ] user group management
    - [ ] friend matching via phone contacts
    - [ ] search for friend by nickname
    - [ ] add friend by uid

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

### `Friendship`
    - `src`: int, uid of the source of the relationship
    - `dest`: int, uid of target
    - `reg_time`: time of record established
    - `status`: int, flags that indicates the relationships. `status` is a 2-digit decimal integer.
    Each digit indicates a status, normal = 1, block = 0, intimate = 2. Unit digit is from `src` to `dest` and tens digit is from `dest` to `src`.

## Stored on client phone
- `cid`: received from GeTui server via SDK
- `region_num`
- `phone_num`
- `phone_num_hash`
- `ukey`
- `uid`
- list of phone contact hashes

## Data transfer standard

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
todo:
    - [ ] encryption
    - [ ] sms activation

### Send image
- request: /send/
    - `phone_hash`: hash of the user `phone_num`
    - `ukey`: combined with `phone_hash` to authenticate user
    - `receiver_uid`: uid of the receiver
    - `img_file`: image file binary data

- response:
    none except http standard header

- in server:
    push message data to GeTui server, data structure is a json
    ```python
    data = {
      "type": "message",
      "sender_region": sender.region_num,
      "sender_phone": hash(sender.phone_num),
      "message_id": message.id,
      "message_key": message.message_key,
      "send_time": message.send_time,
    }
    ```
    and this should be what the client should receive.

### Get image
- request: /download/
    - `message_id`: message id received from getui push message
    - `message_key`: message key
- response:
    - `img_file`: image file binary data

### Add friend
- request:

### Find friend

### Accept/Decline friend request
