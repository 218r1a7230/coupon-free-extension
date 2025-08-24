import asyncio
from playwright.async_api import async_playwright, ProxySettings
from playwright_stealth import stealth_async
from motor.motor_asyncio import AsyncIOMotorClient
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "coupon_guard"
COLLECTION_NAME = "coupons"

# Sample proxy list (replace with real proxies from a provider)
PROXIES = [
    "http://proxy1:port@user:pass",
    "http://proxy2:port@user:pass",
    # Add more or fetch from API
]

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def test_coupon_on_site(browser, coupon):
    # Rotate proxy
    proxy = random.choice(PROXIES)
    context = await browser.new_context(proxy=ProxySettings(server=proxy))
    page = await context.new_page()
    await stealth_async(page)  # Avoid detection

    # Site-specific logic (simplified example for Amazon)
    if coupon['site'] == 'amazon':
        await page.goto("https://www.amazon.com/dp/B08N5WRWNZ")  # Sample product
        await page.click("#add-to-cart-button")
        await page.goto("https://www.amazon.com/gp/cart/view.html")
        await page.fill("#coupon-input", coupon['code'])  # Pseudo-selector; adapt to real
        await page.click("#apply-coupon")
        # Check if discount applied (e.g., evaluate JS or text)
        success = await page.is_visible(".discount-applied")  # Pseudo-check
    elif coupon['site'] == 'bestbuy':
        # Similar logic for BestBuy
        await page.goto("https://www.bestbuy.com/site/product")
        # ... add to cart, apply code, check
        success = False  # Placeholder

    await context.close()
    return success

async def validate_coupons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        coupons = await collection.find().to_list(None)
        for coupon in coupons:
            success = await test_coupon_on_site(browser, coupon)
            new_tests = coupon.get("tests", 0) + 1
            new_successes = coupon.get("successes", 0) + (1 if success else 0)
            success_rate = new_successes / new_tests if new_tests > 0 else 0
            
            await collection.update_one(
                {"_id": coupon["_id"]},
                {"$set": {
                    "tests": new_tests,
                    "successes": new_successes,
                    "success_rate": success_rate,
                    "validated_at": datetime.utcnow()
                }}
            )
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(validate_coupons())