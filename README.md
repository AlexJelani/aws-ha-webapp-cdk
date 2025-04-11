
# 📚 High-Availability Web Application (AWS CDK) Project

## 🎯 Project Objective
This project deploys a **High-Availability Web Application** using AWS CDK (Cloud Development Kit).
The following AWS services are used:

- ✅ **VPC:** Creation of public and private subnets  
- ✅ **EC2:** Management of EC2 instances with Auto Scaling  
- ✅ **ALB:** Traffic distribution using Application Load Balancer (ALB)  
- ✅ **CloudWatch:** Monitoring and CPU utilization alerts  
- ✅ **AWS Backup:** Automated snapshots for backup  

---

## 🗂️ Project Directory Structure
```
/high-availability-app
├── /cdk.out                     # Generated CloudFormation templates
├── /high_availability_app
│   ├── __init__.py
│   ├── app_stack.py             # Main CDK stack
│   └── vpc_stack.py             # VPC and networking configuration
├── /bin
│   └── app.py                   # CDK application entry point
├── /init_script
│   └── init_script.sh           # User data for EC2 instances
├── /requirements.txt            # Python dependencies
└── cdk.json                     # CDK configuration
```

---

## 🚀 Prerequisites
Before running this project, make sure the following requirements are met:

### ✅ 1. Install AWS CLI
Ensure AWS CLI is installed and configured.
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS CLI
aws configure
```

---

### ✅ 2. Install AWS CDK CLI
Install CDK CLI globally.
```bash
npm install -g aws-cdk
```

---

### ✅ 3. Set Up Python Virtual Environment
```bash
# Move to the project directory
cd high-availability-app

# Create a virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# Install required packages
pip install -r requirements.txt
```

---

## 🔥 Step 1: Create VPC and Subnets
✅ **File:** `high_availability_app/vpc_stack.py`  
This step creates the following resources:
- 2 **public subnets** (for ALB)
- 2 **private subnets** (for EC2)
- 1 **NAT Gateway** for outbound traffic

---

## 🔥 Step 2: Configure EC2 and Auto Scaling
✅ **File:** `high_availability_app/app_stack.py`  
This step creates the following resources:
- **Auto Scaling Group (ASG):** Manages EC2 instances dynamically based on CPU load.
- **Security Group:** Controls communication between ALB and EC2 instances.

---

## 🔥 Step 3: EC2 Initialization Script
✅ **File:** `init_script/init_script.sh`  
This script automates the setup of EC2 instances.

---

## 🔥 Step 4: Deploy the CDK Stack

### ✅ Synthesize CloudFormation Template
```bash
cdk synth
```

---

### ✅ Deploy CDK Stack
```bash
cdk deploy
```

---

## 🔎 Post-Deployment Verification
✅ **Checklist:**
- EC2 instances should be launched in private subnets.
- ALB should route traffic to EC2 instances.
- Auto Scaling Group should increase/decrease instances based on CPU usage.
- CloudWatch alarms should trigger if CPU utilization exceeds 80%.

---

## 📚 Troubleshooting
### ❗️ If CDK Deployment Fails
```bash
# Access issue
aws configure  # Reconfigure AWS CLI
```

### ❗️ If ALB is Not Accessible
- Double-check security group rules.
- Ensure you are accessing the correct public IP of the ALB.

---

## 🎁 Bonus: Upload to GitHub 
```bash
# Initialize GitHub repository
git init
git add .
git commit -m "Initial commit - High Availability Web App"
git branch -M main
git remote add origin <GitHub URL>
git push -u origin main
```

---

## 🎉 Congratulations!
The setup, deployment, and testing of this project are complete! 