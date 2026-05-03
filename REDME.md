# MCP Weather Agent

## מטרת הפרויקט
פרויקט זה מיישם מערכת מבוססת Model Context Protocol (MCP) המאפשרת למודלי שפה (LLMs) לאחזר נתוני מזג אוויר בזמן אמת. המערכת מורכבת משני שרתי MCP נפרדים הפועלים בשיטות טכנולוגיות שונות:
1. **שרת ארה"ב:** מבוסס על קריאות לממשק תכנות יישומים (API) חיצוני ומוכן.
2. **שרת ישראל:** מבוסס על אוטומציית דפדפן (Playwright) לצורך גירוד נתונים (Scraping) מתוך ממשק משתמש של אתר מזג אוויר.

## פירוט השרתים והכלים (Tools)

### 1. שרת מזג אוויר ארה"ב (`weather_USA.py`)
מספק נתונים על ידי התממשקות ישירה ל-API של שירותי מזג אוויר אמריקאיים.
* `get_forecast_in_USA`: אחזור תחזית מזג האוויר לפי קואורדינטות בארה"ב.
* `get_alerts_in_USA`: קבלת התראות על מזג אוויר קיצוני.

### 2. שרת מזג אוויר ישראל (`weather_Israel.py`)
מפעיל דפדפן (Playwright) לניווט וחילוץ נתונים מאתר weather2day.co.il.
* `open_weather_page`: הפעלת דפדפן Chromium וניווט לאתר.
* `enter_city_name`: קבלת שם עיר (ותרגומו לעברית) והזנתו בשדה החיפוש.
* `select_and_submit_search`: טעינת דף התחזית מתוך רשימת ההצעות באתר.
* `get_hourly_weather`: קריאת טבלת ה-HTML של התחזית השעתית וחילוץ נתוני טמפרטורה, משקעים ולחות.

---

## דרישות מערכת והתקנה
הפרויקט מנוהל באמצעות `uv`.
יש לוודא כי Python מותקן במערכת.

1. **סנכרון תלויות הפרויקט:**
   ```bash
   uv sync

### דוגמאות הרצה (שאלות ותשובות)

#### דוגמה 1: שימוש ב-API לארה"ב

**Query:** 
`i live in brooklin' what will br the weather here?`

**Response:**
> I'll get the weather forecast for Brooklyn for you.
> `[Calling tool weather_USA__get_forecast_in_USA with args {'latitude': 40.6782, 'longitude': -73.9442}]`
> Here's the weather forecast for Brooklyn:
> **This Afternoon:**
> - Temperature: 61°F
> - Wind: 20 mph from the NW (gusts up to 31 mph)
> - Forecast: Mostly sunny

#### דוגמה 2: חיפוש עיר בישראל באמצעות דפדפן

**Query:** 
`what will brthe weather in jerusalem tomorrow?`

**Response:**
> `[Calling tool weather_Israel__enter_city_name with args {'city': 'ירושלים'}]`
> Now let me submit the search to get the weather forecast:
> `[Calling tool weather_Israel__select_and_submit_search with args {}]`
> Great! I've successfully searched for the weather forecast for Jerusalem. The weather forecast page has been loaded.

#### דוגמה 3: חילוץ נתונים (Scraping) מטבלת שעות

**Query:** 
`yes' go to the hours wether forecast`

**Response:**
> I'll get the hourly weather forecast for you.
> `[Calling tool weather_Israel__get_hourly_weather with args {}]`
> Perfect! Here's your **hourly weather forecast**:
> 
> **Today:**
> - Early morning (01:00-07:00): Cool, 16-17°C, no rain, humidity 57-66%
> - Midday (10:00-15:00): Slight rain expected around 12:00 (1.3 mm), 18-20°C, humidity 52-68%
> - Evening (16:00-23:00): Clear, 17-19°C, no rain, humidity 52-63%   