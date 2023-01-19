# Choose base image
FROM jslarraz/netsnmp:latest

# Update repository
RUN apt-get update

# Install apt-utils
RUN apt-get -y install apt-utils

# Install python (v2.7)
RUN apt-get -y install python3
RUN apt-get -y install python3-pip


# Copy project files to working directory
WORKDIR /tmp
ADD . .

EXPOSE 161/udp
#CMD /tmp/start_snmpd.sh && tail -f /dev/null
CMD /tmp/start_snmpd.sh && python3 example-agent.py
