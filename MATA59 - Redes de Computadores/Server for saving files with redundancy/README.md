# About:

This is a project for saving and recovering files remotely with redundancy, storing copies of a file
at multiple servers (named Zeus servers), where the management of client requests occurs through the proxy server.


## Basic usage:

1. Initialize the proxy server by configuring its address and the address of its listener. You can create 
a proxy server remotely by executing the proxy_server.py module.
2. Create as many Zeus servers as you desire at many machines by running the zeus_server.py module. In 
the configuration stage, set the listener server's address to the proxy server's listener address.
3. Execute the client.py module, connecting to an existing proxy server or creating a local proxy server.


## Zeus Server:
The Zeus server is responsible for saving and retrieving user content, using a close-type connection.

List of Commands:
```
SD:<password>:::             << Shutdown the server

GET:<username>:<filename>::  << Return the file content

PUT:<username>:<filename>:<file_length>:<bytes>  << Store the file of a client

LS:<username>:::             << Return a list of filenames of a client

DEL:<username>:<filename>::  << Delete the file of a client
```


## Proxy Server:
The proxy server is responsible for managing client requests, featuring an algorithm to distribute file 
copies and select a server to retrieve the content.

List of Commands:
```
SD:<password>::::             << Shutdown the server

GET:<username>:<filename>:::  << Return the file content

PUT:<username>:<filename>:<file_length>:<n_copies>:<bytes>  << Store the file of a client

LS:<username>::::             << Return a list of filenames of a client

LSZS:::::                     << Return a list of zeus servers

DEL:<username>:<filename>:::  << Delete the file of a client
```