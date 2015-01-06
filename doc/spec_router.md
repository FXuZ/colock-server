Router Specifications
========

## Summary

Router is used for handling all incoming communication received by the server. But excluding:
    - receive and send messages
    - register
    
    
## Incoming Message Format
- `Action`: unicode
- `Meta`: unicode, can be parsed as a json
- `Data`: unicode, can be parsed as a json


### `Meta` Content
- `app_version`
- `uid`
- `ukey`

### `Action` Types
1. Friendship Management
    1. `srch_phone`
    2. `srch_nickname`
    3. `block`
    4. ``
    
2. Test Reporting



