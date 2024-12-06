# Integration Test

This module runs integration tests against a live environment.  The goal is to catch anything before it's deployed.
However you can also use this as a learning tool or a base on how to use our API's.

## Requirements
The integration tests will require the following:

### Environment Vars
|Variable Name|Description|
|--|--|
|APLOS_API_DOMAIN|The full domain. e.g. app.aplos-nca.com| 


### Users
You will need valid user accounts with the appropriate permissions for the endpoints they are executing.

If you are testing permission bounderies then you should set up multiple users with different permissions.