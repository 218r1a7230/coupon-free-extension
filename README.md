CouponGuard – Smart Coupon Validator & Browser Extension
📌 Overview
CouponGuard is a full-stack project that helps users find working discount coupons on e-commerce websites like Amazon and BestBuy.
It consists of:
- FastAPI Backend – Stores, serves, and updates coupon data.
- Validator Engine – Uses Playwright to automatically test coupons in real browsers.
- Browser Extension (Chrome/Edge) – Displays validated coupons in real-time while shopping.
________________________________________
🚀 Features
•	🔍 Automatic Coupon Validation – Runs Playwright tests to check if coupons apply correctly.

•	📊 Success Rate Tracking – Stores coupon test results in MongoDB.

•	🧙 Browser Extension Integration – Fetches coupons via API and injects them directly into shopping sites.

•	💬 User Feedback Loop – Shoppers can mark coupons as “Worked / Didn’t Work” to improve accuracy.
________________________________________
🛠️ Tech Stack
•	Backend: FastAPI, Uvicorn, Python

•	Database: MongoDB (Motor for async access)

•	Automation: Playwright, playwright-stealth

•	Extension: Chrome Manifest V3, JavaScript, Content Scripts

•	DevOps: Docker, docker-compose, dotenv
________________________________________
⚙️ Setup & Installation
1. Clone the repo
git clone https://github.com/your-username/couponguard.git
cd couponguard
2. Backend (API + MongoDB)
Local Run
pip install -r requirements.txt
playwright install
uvicorn main:app --reload
Docker Run
docker-compose up --build
API will be available at 👉 http://localhost:8000
Docs at 👉 http://localhost:8000/docs
3. Validator
Run coupon validation tests (updates DB success rate):
python validate.py
4. Browser Extension
1.	Go to Chrome → Extensions → Manage Extensions.

2.	Enable Developer Mode.

3.	Click Load unpacked and select the /extension folder (with manifest.json).

4.	Open Amazon/BestBuy → Valid coupons panel will appear.
________________________________________
📂 Project Structure
.
├── main.py             # FastAPI backend
├── validate.py         # Coupon validator with Playwright
├── requirements.txt    # Dependencies
├── Dockerfile
├── docker-compose.yml
├── .env                # Environment variables (Mongo URI)
├── extension/
│   ├── manifest.json
│   ├── content.js
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
