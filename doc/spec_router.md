Router Specifications
========

## Summary

Router is used for handling all incoming communication received by the server. But excluding:
    - receive and send messages
    - register
    
    
## Incoming Message Format
- `App Version`: unicode
- `Action`: unicode
- `Meta`: unicode, can be parsed as a json
- `Data`: unicode, can be parsed as a json


### `Meta` Content
- `uid`
- `ukey`

### `Action` Types
1. Friendship Management
    1. `Friend.srch_phone`
    2. `Friend.srch_nickname`
    3. `Friend.block`
    4. `Friend.`
    
2. Test Reporting



