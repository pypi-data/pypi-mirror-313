from firecrawl import FirecrawlApp
import logging, traceback

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

def get_firecrawl(link, firecrawl_key):
    str1 = ''
    try:
        firecrawl_app = FirecrawlApp(api_key=firecrawl_key)
        scrape_result = firecrawl_app.scrape_url(link, params={'formats': ['rawHtml']})
        str1 = scrape_result['rawHtml']
    except:
        logging.error(traceback.format_exc())
    return str1

# from assets.requests.fctfirecrawl import get_firecrawl
# if __name__ == '__main__':
#     str1 = get_firecrawl(link=link, firecrawl_key=self.firecrawl_key)
