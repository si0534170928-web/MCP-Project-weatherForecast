from mcp.server.fastmcp import FastMCP
from playwright.async_api import TimeoutError as PlaywrightTimeout
from playwright.async_api import async_playwright


mcp = FastMCP("weather-Israel")

FORECAST_URL = "https://www.weather2day.co.il/forecast"


from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP("WeatherAutomation")

# משתנים גלובליים לשמירת מצב הדפדפן והדף
browser_instance = None
page_instance = None

#A

@mcp.tool()
async def open_weather_page() -> str:
    """מפעיל דפדפן גלוי וניגש לאתר weather2day"""
    global browser_instance, page_instance
    
    if browser_instance is None:
        playwright = await async_playwright().start()
        # headless=False מאפשר לנו לראות את הפעולות על המסך
        browser_instance = await playwright.chromium.launch(headless=False)
        page_instance = await browser_instance.new_page()
    
    await page_instance.goto(FORECAST_URL)
    return "האתר נפתח בהצלחה והוא מוכן לחיפוש."

#B

@mcp.tool()
async def enter_city_name(city: str) -> str:
    """
    מקבל שם עיר ומקליד אותו בשורת החיפוש של האתר.
    הנחיה קריטית למודל: עליך להעביר את שם העיר בשפה העברית בלבד! 
    אם בקשת המשתמש היא באנגלית או בשפה אחרת, עליך לתרגם את שם העיר לעברית (למשל 'Jerusalem' -> 'ירושלים') לפני הפעלת כלי זה.
    
    Args:
        city: שם העיר לחיפוש, חובה שיהיה מוקלד בעברית בלבד (למשל: 'ירושלים', 'תל אביב').
    """
    global page_instance
    
    if page_instance is None:
        return "שגיאה: הדפדפן אינו פתוח. יש להפעיל קודם את open_weather_page."
    
    # שימוש בסלקטור המדויק שמצאנו קודם לכן להזנת הטקסט
    await page_instance.fill("#city_search_forecast", city)
    
    return f"העיר '{city}' הוזנה בהצלחה בשדה החיפוש."

#C

@mcp.tool()
async def select_and_submit_search() -> str:
    """בוחר את התוצאה הראשונה ברשימת ההצעות ומבצע את החיפוש"""
    global page_instance
    
    if page_instance is None:
        return "שגיאה: אין מופע דף פעיל. יש להריץ קודם את open_weather_page."

    try:
        # המתנה להופעת רשימת ההצעות לאחר ההקלדה
        # באתר weather2day, רצוי להמתין לעיבוד קצר של ה-DOM
        await page_instance.wait_for_timeout(500)
        
        # שימוש במקלדת לבחירת האופציה הראשונה (חץ למטה) ואישור (Enter)
        await page_instance.keyboard.press("ArrowDown")
        await page_instance.keyboard.press("Enter")
        
        # המתנה לטעינת דף התחזית החדש
        await page_instance.wait_for_load_state("load")
        
        return "החיפוש הושלם בהצלחה. דף התחזית נטען."
    except Exception as e:
        return f"שגיאה במהלך ביצוע החיפוש: {str(e)}"

#D
@mcp.tool()
async def get_hourly_weather() -> str:
    """
    קורא ומחלץ את התחזית השעתית מתוך טבלת מזג האוויר בדף הנוכחי.
    """
    global page_instance
    
    if page_instance is None or page_instance.is_closed():
        return "שגיאה: אין מופע דף פעיל. יש להריץ קודם פתיחת אתר וחיפוש."

    try:
        # המתנה לטעינת שורות הטבלה השעתית
        await page_instance.wait_for_selector("tr.hourly_data", timeout=5000)
        
        # איסוף כל השורות
        rows = await page_instance.locator("tr.hourly_data").all()
        
        if not rows:
            return "לא נמצאו נתוני תחזית שעתית בטבלה."

        extracted_data = ["נתוני תחזית שעתית:"]
        
        for row in rows:
            # חילוץ השעה מתוך תגית ה-th
            hour = await row.locator("th.hourly_hour").inner_text()
            # ניקוי השעה מטקסט עודף (בגלל ה-tooltip שיש ב-HTML)
            hour = hour.split('\n')[0].strip()
            
            # איסוף התאים (td) באותה שורה
            cells = await row.locator("td").all()
            
            if len(cells) >= 4:
                # תא 0: אייקון (מדלגים)
                # תא 1: טמפרטורה
                temp = await cells[1].inner_text()
                # תא 2: כמות גשם
                rain = await cells[2].inner_text()
                # תא 3: לחות
                humidity = await cells[3].inner_text()
                
                extracted_data.append(f"שעה: {hour} | טמפרטורה: {temp.strip()} | גשם: {rain.strip()} | לחות: {humidity.strip()}")
        
        return "\n".join(extracted_data)

    except Exception as e:
        return f"שגיאה במהלך חילוץ הנתונים מהטבלה: {str(e)}"
def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
