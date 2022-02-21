# backend

Collects information that is posted to this api.
Info collected:
1. name
2. email
3. preferred scm
4. number of colleagues 

Validates the passed information, then sends a thank you email to the passed address.

Sends an email to an address specified in a local .env file. The email contains all of the information passed in the post request. 


Things like email credentials and server address/ports are stored in a local .env file. 