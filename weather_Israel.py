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

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
