iSimple IRC Server

Code messages has been replaced with text messages, for example:
0 - JOIN
1 - BROADCAST
2 - MSG
3 - PRIVMSG
4 - REGISTER (When script is run, REGISTER msg is sent. No need to send it further)

Flow[v1_0]:
    Start the server by - python server_working.py (port by default is 12345, and listens on all interfaces)
    Start the client by - python eclient.py <hostname> <port> <name> (note that hostname and port here are of server)
    User gets registered in when starting the eclient.py (note <name> in previous step), so no need to register again
    0 some_group_name -> this will allow user to join some group
     - if group is not there it is created
     - all the members of group are send message that particular user has joined the group
    2 some_group_name "message" -> this will send message to all members of some_group_name
    3 some_user_name "message" -> this will send private message to user some_user_name
    1 ?? ?? -> currently broadcast functionality is not proper

Zync
- Add new servers on the fly (currently, support is not there spawning servers on remote hosts)
- Stop current servers
- List all servers
- Start cache server
- Get performance stats (currently, only basic stats like number of groups, clients are printed)
