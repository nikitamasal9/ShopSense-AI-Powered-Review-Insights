# ShopSense-AI-Powered-Review-Insights

**ShopSense** is an AI-powered eCommerce platform built using **Django** that allows customers to submit product reviews after successful delivery. These reviews are analyzed using **Transformer models** to generate insights such as sentiment, intent, and scope type. The insights are stored and visualized using an integrated **Power BI** dashboard. The entire system is deployed on an **AWS EC2 instance** with a microservices architecture.

---

## Key Features

- AI model-based review classification using Hugging Face models
    - `[typeform/distilbert-base-uncased-mnli](https://huggingface.co/typeform/distilbert-base-uncased-mnli)` for intent & scope classification
    - `[SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions)` for emotion classification
- Seller-side product management and customer-side review system
- Reviews allowed **only after product delivery**
- Local Power BI Report Server integration
- Deployed on AWS EC2
- Microservices ensure API resilience and modularity

---

## Authors

- Nikita Masal
- Nirajan Poudel
- Laxmi Satyal


---

## Local Development Setup

### 1. Clone and Enter the Project

```bash
git clone https://github.com/nikitamasal9/ShopSense-AI-Powered-Review-Insights.git
cd shopsense  
```

### 2. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r shopsense/requirements.txt
```

### 4. Run Initial Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

## Deployment on AWS EC2 instance

### 1. Setup an EC2 instance
- Go to AWS Console → EC2 Dashboard
- Click "Launch Instance"
- Select Ubuntu Server 22.04 LTS (or similar)
- Choose an instance type:
    - t2.micro (free-tier eligible)
- Configure Security Group:
    - Add port 22 (SSH) for remote access
    - Add port 8000 (Custom TCP) for Django dev server access

### 2. Connect to the instance to open EC2 Console

### 3. Install Required Packages

```bash
sudo apt update
sudo apt install python3-pip python3
```

### 4. Follow the local deployement steps

## Screenshots
![Home Page](/Screenshots/first_page.png)
![Login Page](/Screenshots/login_page.png)
![Customer site](/Screenshots/customer_site.png)
![Add review feature on Customer site](/Screenshots/add_review.png)
![Add review page](/Screenshots/add_review2.png) 
![Seller site](/Screenshots/seller_site.png)
![PowerBI Dashboard](/Screenshots/dashboard.png) 
