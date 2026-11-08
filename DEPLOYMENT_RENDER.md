# 🌐 Render.com-এ Telegram Premium Emoji Bot ২৪/৭ (24/7) ফ্রিতে হোস্ট করার গাইড

এই বটের ভেতরে একটি **ইন-বিল্ট HTTP Health-Check Server** যুক্ত করা হয়েছে। তাই আপনি Render-এর **`Web Service (Free)`** টিয়ার ব্যবহার করে ল্যাপটপ বন্ধ থাকলেও সম্পূর্ণ ফ্রিতে ২৪ ঘণ্টা বটটি সচল রাখতে পারবেন!

---

## 📌 ধাপ ১: GitHub রিপোজিটরি

প্রজেক্টটি আপনার GitHub অ্যাকাউন্টে ইতিমধ্যে আপলোড ও পুশ করা হয়েছে:
🔗 **রিপোজিটরি লিঙ্ক:** `https://github.com/sshariyasunny/telegram-premium-emoji-bot`

---

## 📌 ধাপ ২: Render.com এ Web Service তৈরি করুন

১. ব্রাউজারে **[dashboard.render.com](https://dashboard.render.com)** এ যান এবং সাইন ইন করুন।
২. উপরের ডানে **`New +`** বাটনে ক্লিক করে **`Web Service`** সিলেক্ট করুন।
৩. আপনার GitHub রিপোজিটরি **`telegram-premium-emoji-bot`** এর পাশে **`Connect`** বাটনে ক্লিক করুন।

---

## 📌 ধাপ ৩: সেটিংস কনফিগারেশন

নিচের সেটিংসগুলো পূরণ করুন:

- **Name:** `telegram-premium-emoji-bot`
- **Region:** Singapore / Frankfurt (যেকোনো একটি)
- **Branch:** `main`
- **Language/Runtime:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  python main.py
  ```
- **Instance Type:** `Free ($0/month)`

---

## 📌 ধাপ ৪: Environment Variables (বট টোকেন)

নিচের দিকে **`Environment Variables`** সেকশনে যান এবং `Add Environment Variable` এ ক্লিক করুন:

1. **Key:** `BOT_TOKEN`  
   **Value:** `9120376953:AAG7xxKbAQDZISNyAxZpS1Qp-PD6Eo_MDRw`

2. **Key:** `DEFAULT_STYLE`  
   **Value:** `smart`

সবশেষে নিচে **`Create Web Service`** বাটনে ক্লিক করুন!  
Render স্বয়ংক্রিয়ভাবে প্রজেক্টটি ইনস্টল করে রান করবে। লগ স্ক্রিনে দেখতে পাবেন:  
`Health check HTTP server running on port...` এবং `Bot is polling for updates...`।

---

## 📌 ধাপ ৫: ২৪ ঘণ্টা এক্টিভ রাখার জন্য Keep-Alive Ping সেটআপ

Render Free Web Service যেন ১৫ মিনিট পর স্লিপ (Sleep) না হয়ে যায়, তার জন্য:

১. Render ড্যাশবোর্ড থেকে আপনার অ্যাপের ইউআরএল (URL) কপি করুন (যেমন: `https://telegram-premium-emoji-bot.onrender.com`)।
২. **[cron-job.org](https://cron-job.org)** অথবা **[uptimerobot.com](https://uptimerobot.com)** এ একটি ফ্রি অ্যাকাউন্ট খুলুন।
৩. একটি নতুন **Cron-job / Monitor** তৈরি করুন:
   - **URL:** আপনার Render অ্যাপের ইউআরএল
   - **Execution Schedule:** প্রতি `5` মিনিট (Every 5 minutes)
৪. **Save** করুন।

🎉 **ব্যাস!** এখন আপনার বটটি মেঘে (Cloud) ২৪ ঘণ্টা নিরবচ্ছিন্নভাবে অনলাইনে থাকবে—আপনার ল্যাপটপ অন থাকুক বা অফ থাকুক!

> ⚠️ **গুরুত্বপূর্ণ সতর্কতা:** Render-এ বট রান করার পর আপনার ল্যাপটপের লোকাল বটটি `stop_bot.bat` চালিয়ে বন্ধ করে রাখবেন, যাতে একসাথে দুই জায়গা থেকে পোলিং কনফ্লিক্ট না হয়।
