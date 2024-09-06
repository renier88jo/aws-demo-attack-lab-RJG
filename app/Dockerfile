FROM lunasec/tomcat-9.0.59-jdk11

ADD src/ /helloworld/src
ADD pom.xml /helloworld

#  Build spring app
RUN apt update && apt install maven -y
WORKDIR /helloworld/
RUN mvn clean package

#  Deploy to tomcat
RUN mv target/helloworld.war /usr/local/tomcat/webapps/

EXPOSE 8080

ENTRYPOINT ["catalina.sh", "run"]

# Twistlock Container Defender - app embedded
ADD twistlock_defender_app_embedded.tar.gz /twistlock/
ENV DEFENDER_TYPE="appEmbedded"
ENV DEFENDER_APP_ID="springapp"
ENV FILESYSTEM_MONITORING="true"
ENV WS_ADDRESS="wss://us-west1.cloud.twistlock.com:443"
ENV DATA_FOLDER="/twistlock/"
ENV INSTALL_BUNDLE="eyJzZWNyZXRzIjp7InNlcnZpY2UtcGFyYW1ldGVyIjoiVU5LdXpCQk9hejBGQ0hnWW5oV25zYmlYQVNmVnZlK0FzTWNScTB0MDVhbWtjYmxOTGdLT0JuTzNXWnd6RHVBOW10cGpWNVErbVBJMGZJSHl0Nnh4TGc9PSJ9LCJnbG9iYWxQcm94eU9wdCI6eyJodHRwUHJveHkiOiIiLCJub1Byb3h5IjoiIiwiY2EiOiIiLCJ1c2VyIjoiIiwicGFzc3dvcmQiOnsiZW5jcnlwdGVkIjoiIn19LCJjdXN0b21lcklEIjoidXMtNC0xNjEwNTYzMDciLCJhcGlLZXkiOiJtSFh5ZlFDMVJtbE00dVhjK2FSbVVMU1cxREdITVpobzZFKzhybGZ5K2YwOXJoSC8rR3ZEQmJjamhWSHlSWlFpaTlQelV2cWxmRGN2K2xVYUhJenluUT09IiwibWljcm9zZWdDb21wYXRpYmxlIjpmYWxzZSwiaW1hZ2VTY2FuSUQiOiI5MDE2NzE1MS1kYzY4LWZlMzQtODlmYi00OTNhYmE3NzNlZjYifQ=="
ENV FIPS_ENABLED="false"
ENTRYPOINT ["/twistlock/defender", "app-embedded", "catalina.sh", "run"]
