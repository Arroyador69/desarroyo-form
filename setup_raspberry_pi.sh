#!/bin/bash
# 🍓 CONFIGURAR WEBHOOK EN RASPBERRY PI
# Script para independencia total del sistema

echo "🍓 Configurando DesArroyo Tech Webhook en Raspberry Pi..."
echo "=================================================="

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install -y python3-pip python3-venv nginx

# Crear directorio del proyecto
mkdir -p /home/pi/desarroyo-webhook
cd /home/pi/desarroyo-webhook

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install flask gunicorn pytz

# Copiar el servidor webhook
cp ~/desarroyo-form/railway_webhook_server.py webhook_server.py

# Crear servicio systemd
sudo tee /etc/systemd/system/desarroyo-webhook.service > /dev/null <<EOF
[Unit]
Description=DesArroyo Tech Webhook Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/desarroyo-webhook
ExecStart=/home/pi/desarroyo-webhook/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 webhook_server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configurar nginx como proxy reverso
sudo tee /etc/nginx/sites-available/desarroyo-webhook > /dev/null <<EOF
server {
    listen 80;
    server_name your-raspberry-pi-ip;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Activar sitio
sudo ln -s /etc/nginx/sites-available/desarroyo-webhook /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Iniciar servicios
sudo systemctl daemon-reload
sudo systemctl enable desarroyo-webhook
sudo systemctl start desarroyo-webhook
sudo systemctl restart nginx

echo ""
echo "✅ Webhook configurado en Raspberry Pi!"
echo "🌐 URL: http://$(hostname -I | cut -d' ' -f1)/webhook-llamada"
echo "🔧 Para configurar en Twilio:"
echo "   1. Instalar ngrok: sudo apt install ngrok"
echo "   2. Ejecutar: ngrok http 80"
echo "   3. Usar URL de ngrok en Twilio"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: sudo journalctl -u desarroyo-webhook -f"
echo "   - Reiniciar: sudo systemctl restart desarroyo-webhook"
echo "   - Estado: sudo systemctl status desarroyo-webhook" 