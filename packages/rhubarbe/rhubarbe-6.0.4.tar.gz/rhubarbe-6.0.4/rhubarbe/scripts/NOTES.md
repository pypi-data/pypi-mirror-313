# EATON PDUs

## ssh

### setup

* created a root user with our usual password; used the web interface for that

### caveats

* using ssh is a pain; very slow to respond, and probably can't cope with multiple concurrent accesses
* requires odd options (see the `pdu` script)

  ```shell
  sshpass -ponecalvin ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -oPreferredAuthentications=password root@c007-pdu-top.pl.sophia.inria.fr
  sshpass -ponecalvin ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -oPreferredAuthentications=password root@c007-pdu-bottom.pl.sophia.inria.fr
  sshpass -ponecalvin ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -oPreferredAuthentications=password root@192.168.4.107
  ```

* TODO
  * create shell aliases to speed that up
  * add a hostname to refer to the PDU

* the code for r2lab (daisy chain of 2) does not seem to work as-is with the 2 PDUs in C007 (no chain)

### tricks

* get the length of an array with `.Count`
* apply the same stuff on all elements in an array `Array[x]`  
  result will be separated with a `|`

## SNMP

### setup

* used the web interface to
  * enable SNMP (picked v1 & v3)
  * grant read-only access right to the 'public' SNMPv1 user

NOTE: not done yet on 192.168.4.107

### linux setup

```shell
dnf install net-snmp net-snmp-utils
# ou est-ce que ceci suffit ?
dnf install net-snmp-utils
```

### resources

* got the PDF somewhere on the internet - not quite sure where to be honest
* got the MIB through the web interface (there is a link on the SNMP page)
