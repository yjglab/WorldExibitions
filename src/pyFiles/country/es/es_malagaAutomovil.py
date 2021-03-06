import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import infoCrawler

url = 'https://www.cristobalbalenciagamuseoa.com/descubre/exposiciones-actuales/'
exb_nums = 2
titles_selector = ".ficha--exposiciones-actuales .heading"
dates_selector = ".ficha--exposiciones-actuales .fecha"
thumbnails_selector = ".ficha--exposiciones-actuales img"
details_links_selector = "meta"
details_content_selector = ".ficha--exposiciones-actuales p:nth-of-type(3)"
category = "museum"

infoCrawler.print_msm_data(
    url, 
    exb_nums,
    titles_selector, 
    dates_selector, 
    thumbnails_selector, 
    details_links_selector,
    details_content_selector,
    category,
    )