# Instabrowser
[![Build Status](https://travis-ci.org/aLkRicha/insta_browser.svg?branch=master)](https://travis-ci.org/aLkRicha/insta_browser)
[![PyPI](https://img.shields.io/pypi/v/insta_browser.svg)](https://pypi.python.org/pypi/insta_browser)
[![Code Climate](https://img.shields.io/codeclimate/github/aLkRicha/insta_browser.svg)](https://codeclimate.com/github/aLkRicha/insta_browser)

💻 Library for instagram.com automation.  
♥️ Like instagram feed, username profile, location, tag.  
📊 Get statistic of any public account.

### Requirements
* Pyhton 2.7/3
* You need to have PhantomJS or Chrome web driver for work.
    Download and place binary from archive to bin folder:
    - [PhantomJS](http://phantomjs.org/download.html)
    - [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)


### Examples
* Example of using package for getting account statistic:
    ```python
    from insta_browser import InstaMeter
    im = InstaMeter(username='al_kricha')
    im.analyze_profile()
    im.print_account_statistic()
    im.print_top_liked()
    ```
    result:
    ```commandline
    +-- https://instagram.com/al_kricha/ --------------------------+
    |   counter                    |             value             |
    +------------------------------+-------------------------------+
    |   followed                   |              402              |
    |   posts                      |              397              |
    |   comments                   |             1602              |
    |   likes                      |             20429             |
    |   following                  |              211              |
    |   video views                |             6138              |
    |                                                              |
    +--------- https://github.com/aLkRicha/insta_browser ----------+
    +--------------------------------------------------------------+
    |                       top liked posts                        |
    +--------------------------------------------------------------+
    |       https://instagram.com/p/BVIUvMkj1RV/ - 139 likes       |
    |       https://instagram.com/p/BTzJ38-DkUT/ - 132 likes       |
    |       https://instagram.com/p/BI8rgr-gXKg/ - 129 likes       |
    |       https://instagram.com/p/BW-I6o6DBjm/ - 119 likes       |
    |       https://instagram.com/p/BM4_XSoFhck/ - 118 likes       |
    |       https://instagram.com/p/BJVm3KIA-Vj/ - 117 likes       |
    |       https://instagram.com/p/BIhuQaCgRxI/ - 113 likes       |
    |       https://instagram.com/p/BM6XgB2l_r7/ - 112 likes       |
    |       https://instagram.com/p/BMHiRNUlHvh/ - 112 likes       |
    |       https://instagram.com/p/BLmMEwjlElP/ - 111 likes       |
    +--------------------------------------------------------------+
    ```

* Example of using package for liking specific user:
    ```python
    import os
    from insta_browser import browser
    
    br = browser.Browser(
        debug=True,
        chrome=False,
        cookie_path=os.path.join('var', 'cookies'),
        log_path=os.path.join('var', 'logs'),
        db_path=os.path.join('var', 'db'),
        exclude=os.path.join('var', 'exclude.txt')
    )
    
    try:
        br.auth('YOUR_INSTA_LOGIN', 'YOUR_INSTA_PASSWORD')
        br.process_user('al_kricha')
        print(br.get_summary())
    finally:
        br.close_all()
    
    ```

Other examples can be seen in my repository: [insta_bot](https://github.com/aLkRicha/insta_bot)
