import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import infoCrawler

url = 'https://ars.electronica.art/center/de/program/'
exb_nums = 6
titles_selector = ".col-lg-3 .card .card-body .card-title"
dates_selector = ".col-lg-3 .card .card-body .card-text strong, .card-text"
thumbnails_selector = ".col-lg-3 .card img"
details_links_selector = ".col-lg-3 > a"
details_content_selector = ".entry-content > p"
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