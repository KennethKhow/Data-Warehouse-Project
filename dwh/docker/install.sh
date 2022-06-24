apt update && apt upgrade -y
apt install curl gcc libmariadb-dev nano unzip -y
apt install software-properties-common -y
mkdir /opt/oracle && cd /opt/oracle
curl -O https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip
curl -O https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-sqlplus-linux.x64-19.8.0.0.0dbru.zip
unzip instantclient-basic-linux.x64-19.8.0.0.0dbru.zip -d /opt/oracle
unzip instantclient-sqlplus-linux.x64-19.8.0.0.0dbru.zip -d /opt/oracle
apt install libaio1 libaio-dev -y
rm *.zip && cd ../..
echo 'export PATH="$PATH:/opt/oracle/instantclient_19_8"' >> ~/.profile && echo 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/oracle/instantclient_19_8"' >> ~/.profile