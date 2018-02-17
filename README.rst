==============
mechanizeretry
==============

Add hang protection and retries to mechanize operations

Getting Started
***************

Install using `pip` or `easy_install`:

    pip install mechanizeretry

    easy_install mechanizeretry

Prerequisites
*************

This project requires mechanize.

Usage Example
*************

    python
    import mechanize
    from mechanizeretry import RetryBrowser
    
    browser = RetryBrowser()
    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    browser.open('http://server:8080/v1/api/endpoint', retries=5, delay=15, timeout=30)


