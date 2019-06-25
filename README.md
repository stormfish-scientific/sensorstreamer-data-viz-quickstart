# SensorStreamer Data Visualization Quickstart Template

By Stormfish Scientific Corporation

Copyright (C) 2019 Stormfish Scientific Corporation

https://www.stormfish.io

Version: 1.0.0-alpha

Date: 2019-June-25


## Distribution

The SensorStreamer Data Visualization Quickstart is free software: you
can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later
version.

SensorStreamer Data Visualization Quickstart is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the MIT License for more details.

You should have received a copy of the MIT License along with this
program.  If not, see <https://opensource.org/licenses/MIT>.

Use of this software is constitutes acceptance of the terms of the
license.  See LICENSE file for details.

## Purpose:

##  How to Use:

### Requirements

 * docker - Developed and tested on Docker version 18.09.6
 
 * docker-compose - Developed and tested on docker-compose version 1.23.1

### 1) Initialize data folders

To initialize the data folders with the correct permissions run the following command:

$ ./initialize.sh

### 2) Configure Server

Edit the docker-compose.yml file to suit your needs.  The defaults
will likely be sufficient to get started.  The initial grafana
username and password default to "admin" and "admin", respectively.
The default password can be changed by modified the GF_SECURITY_ADMIN_PASSWORD
environment variable in the grafana service definition.

### 3) Launch Services

$ docker-compose up -d

### 4) Install SensorStreamer on Android Device

SensorStreamer is available here: https://play.google.com/store/apps/details?id=cz.honzamrazek.sensorstreamer&hl=en_US

Create a connection to the server machine using tcp client setting.
* Connection type: TCP client
  
* Hostname: IP or hostname of server hosting this package
  
* Port: 57175
  
Click "Save connection"

Create a packet definition:

* Packet type: "JSON"

* Select everything except proximity

Choose "High period (200 ms)" and START.

### 5) Usage

Once the server is running, the various components can be accessed on
the following ports on the server system (replace x.x.x.x with the
ip address or domain name of the server system):

* http://x.x.x.x:5601 - Kibana 
* http://x.x.x.x:9200 - Elasticsearch
* http://x.x.x.x:3000 - Grafana

### 6) Setup Kibana Index Pattern

With your browser connect to Kibana using the URL template above.

Click on the Management cog on the left side of the screen.

Click on "Index Patterns"

Click "Create Index Pattern"

If it says "Couldn't find any Elasitsearch data" this means your
SensorStreamer app did not deliver any data.  Run the SensorStreamer
app to generate some data.  Also, you may check the server log output
for issues:

$ docker-compose logs

On the screen that says, "Step 1 of 2: Define index pattern", enter
sensor-stream-* as the index pattern.

Click "Next step"

On the screen that says, "Step 2 of 2: Configure settings", select
@timestamp from the dropdown.

Click "Create index pattern"

Once that completes, click on the "Discover" icon on the left of the
screen.

You should now have access to the sensor data.

