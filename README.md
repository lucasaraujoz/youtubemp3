# Instalação 
pip install requirements.txt

## Abrir portas
### Linux
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT<br>
sudo iptables -A OUTPUT -p tcp --sport 5000 -j ACCEPT<br>
sudo iptables-save | sudo tee /etc/iptables/iptables.rules<br>
sudo systemctl restart iptables
