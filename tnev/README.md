# Dahua Live Streaming URLs
rtsp://192.168.2.128:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif
rtsp://admin:admin@10.7.6.67:554/cam/realmonitor?channel=1&subtype=1
rtsp://192.168.2.128:554/live


# URL Syntax
rtsp://:@:/cam/realmonitor?channel=&subtype=
  : a valid user’s username.
  :user’s password. (Cannot contain #)
  :the IP address of the IP Camera.
  :the default port is 554. It can be omitted.  
  :the channel number. It starts from 1.
  :the stream type. The of main stream is 0, extra stream 1 is 1, extra stream 2 is 2