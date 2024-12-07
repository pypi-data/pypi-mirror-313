from playwright.async_api import async_playwright
import time

class Playwright78:
    """paywright异步爬虫"""
    def __init__(self):
        self.cookies = []

    def setup(self, cookie_str, domain=".baidu.com", path="/"):
        # 将 Cookie 字符串解析为字典格式，并添加 domain 和 path
        cookies = []
        for cookie in cookie_str.split(';'):
            name, value = cookie.strip().split('=', 1)
            cookies.append({'name': name, 'value': value, 'domain': domain, 'path': path})
        self.cookies = cookies

    async def fetch_page(self, url):
        # 使用异步 Playwright API 启动浏览器并传入 cookies
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # 设置 headless=False 可以查看浏览器界面
            page = await browser.new_page()

            # 设置页面 Cookie
            await page.context.add_cookies(self.cookies)

            # 访问网页
            await page.goto(url)

            # 等待页面加载完成（可以根据页面元素来判断）
            await page.wait_for_selector('body')  # 根据页面加载的标志修改

            # 获取网页内容
            html_content = await page.content()

            await browser.close()
            return html_content

    def parse_content(self, html_content):
        # 这里是解析网页内容的地方，根据实际情况修改
        if "某个特定内容" in html_content:
            print("抓取到目标内容！")
        else:
            print("没有找到目标内容。")

# 示例
if __name__ == "__main__":
    # 示例 Cookie 字符串
    cookie_str = "Dev1=1"

    # 创建对象并设置 cookies
    crawler = Playwright78()
    crawler.setup(cookie_str, domain=".1m", path="/")

    # 替换为需要爬取的网址
    url = "https://bu001"
    html_content = crawler.fetch_page(url)

    # 如果获取到了网页内容，进行解析
    if html_content:
        crawler.parse_content(html_content)