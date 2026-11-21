# Pi-hole Installation via Docker (Docker for DNS)

## Docker for DNS (i.e. piHole)

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo nano /etc/systemd/resolved.conf
# Un-comment or add the following line under the [Resolve] section:
textDNSStubListener=no

sudo systemctl restart systemd-resolved

mkdir -p ~/pihole
cd ~/pihole
nano docker-compose.yml

version: "3"

services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
    environment:
      TZ: 'America/New_York'
      FTLCONF_webserver_api_password: 'YourSecurePasswordHere'
      FTLCONF_dns_listeningMode: 'all'
    # Volumes persist your adlists and settings across container updates
    volumes:
      - './etc-pihole:/etc/pihole'
      - './etc-dnsmasq.d:/etc/dnsmasq.d'
    cap_add:
      - NET_ADMIN
    restart: unless-stopped

# start in background
docker compose up -d

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

sudo nano /etc/systemd/resolved.conf
DNSStubListener=no

sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved
cd ~/pihole
docker compose up -d

# Accessing the Dashboard:
# Find your Linux machine's local IP address by running hostname -I in the terminal.
# Open your web browser and navigate to: http://192.168.5.216/admin.
# Log in using the password you set in the docker-compose.yml file.

# fix not found
cd ~/pihole
nano docker-compose.yml
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"  # <-- Changed host port from 80 to 8080

docker compose up -d --force-recreate
http://192.168.5.216:8080/admin/login

# set dns to 192.168.5.216

# make the IP static in router setup

# Turn off advanced DNS in browsers. See 'Firefox Tweaks' and 'Chrome Tweaks'
```
