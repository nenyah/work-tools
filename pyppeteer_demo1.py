import asyncio

from pyppeteer import launch

width, height = 1366, 768


async def main():
    browser = await launch(
        headless=False,
        args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.evaluateOnNewDocument("""
            var _navigator = {};
            for (name in window.navigator) {
                if (name != "webdriver") {
                    _navigator[name] = window.navigator[name]
                }
            }
            Object.defineProperty(window, 'navigator', {
                get: ()=> _navigator,
            })
        """)
    await page.goto('https://www.tmall.com/')
    # await page.focus('.s-combobox-input-wrap > input')
    input = await page.J('.s-combobox-input-wrap > input')
    await input.type('伊婉')
    await asyncio.sleep(100)
    # await page.keyboard.type('伊婉')
    button = await page.Jx('//*[@id="mallSearch"]/form/fieldset/div/button')
    print(button)
    await button.click()
    await asyncio.sleep(100)
    # await page.tap('input#mq')
    await asyncio.sleep(100)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
