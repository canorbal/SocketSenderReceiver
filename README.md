#SocketSenderReceiver

Program for file copying with sockets.

Requirements:
```
python3
```

Usage:
	
* Sender
```
python3 main.py -send -ip <IP> -threads <N_THREADS> -file <FILENAME>
```

* Receiver
```
python3 main.py -receive
```

You may specify port and time for sleeping between sequential sendings in ```config.py```

		
		