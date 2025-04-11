#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "Starting user data script execution"
yum update -y
echo "Yum update completed"
yum install -y httpd
echo "Apache installed"
systemctl start httpd
echo "Apache started"
systemctl status httpd
echo "Apache status checked"
systemctl enable httpd
echo "Apache enabled to start on boot"
echo "<h1>Hello from High-Availability Web App!</h1><p>Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>" > /var/www/html/index.html
echo "Index.html created"
cat /var/www/html/index.html
echo "Index.html content verified"
echo "User data script completed"
