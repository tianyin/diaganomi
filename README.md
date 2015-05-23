# diaganomi
Anonymize the logs before sending out for diagnosis

The goal of this project is to build an open-source anonymizer for the logs that you want to send out for diagnosis purposes (e.g., copy-and-paste on StackOverflow or Pastebin). 

##The problem##

When I encounter problems in configuring or using open-source software, I often ask on the mailing list and online forums (e.g., StackOverflow, ServerFault) by posting the error logs. Sometimes, the peer helpers also ask me to post the logs so that they can examine them to ease the diagnosis. 

The annoying fact is that the logs usually contain sensitive information which I don't want to make public, mainly including:
- IP addresses
- hostname
- user and group names 
- files and directories. 

These information does not help the diagnose but would be leveraged by attackers (now they can know the IP and username of my machine! and they know the particular version of software I'm using T_T).

Yup, I should replace ("%s/x/y/g") these information in the logs before sending them out. But I'm always miss some important ones, like today I replaced all the IPs with xxx.xxx.xxx.xxx but forget to replace the hostnames >_<.

##Unavailability of ```lr_anonymize``` source code

There is a package called lire built by LogReport in 2006. It includes a tool called ```lr_anonymize``` which is supposed to do me the favor but it does not work well. For example, it treats any pattern of xxx.xxx.xxx.xxx as a hostname!! so my 
```
java.io.IOException: Failed on local exception: java.io.EOFException; Host Details : local host is: "tianyin-h8-1160t.ucsd.edu/127.0.1.1"; destination host is: "xxx.xxx.xxx.xxx":9000; 
  at org.apache.hadoop.net.NetUtils.wrapException(NetUtils.java:764)
  at org.apache.hadoop.ipc.Client.call(Client.java:1351)
  at org.apache.hadoop.ipc.Client.call(Client.java:1300)
  at org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:206)
```
becomes:
```
1.example.com: Failed on local exception: 2.example.com; Host Details : local host is: "3.example.com/10.0.0.1"; destination host is: "4.example.com":9000; 
  at 5.example.com(6.example.com:764)
  at 7.example.com(8.example.com:1351)
  at 7.example.com(8.example.com:1300)
  at 9.example.com$10.example.com(11.example.com:206)
```

Well, I'd like to get the source code and improve it to work for me. But surprisingly, I cannot find it online... The website of LogReport is now redirected to a weird Japanese website...

So let's make a new one.
