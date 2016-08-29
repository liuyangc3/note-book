## Name Services
Once an user is authenticated, many applications still need access to user information.
This information is traditionally contained in text files (/etc/passwd, /etc/shadow, and /etc/group),
or be provided by name services. (such as LDAP)
##  Name Service Switch
a method originated from the Sun C library that permits to obtain information from various name services through a common API.

in /etc/nsswitch.conf the name service providers for every supported database are specified.

The databases currently supported by NSS (they are the maps provided by NIS.) are:
* aliases: Mail aliases.
* ethers: Ethernet numbers.
* group: Groups of users.
* hosts: Host names and numbers.
* netgroup: Network wide list of host and users.
* network: Network names and numbers.
* protocols: Network protocols.
* passwd: User passwords.
* rpc: Remote procedure call names and numbers.
* services: Network services.
* shadow: Shadow user passwords.

