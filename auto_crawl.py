import time

import schedule

from auto_crawl_pkgname.get_pkgnames_dayly import CrawlPkgnames

if __name__ == '__main__':
    t = CrawlPkgnames()
    t.run()
    schedule.every(2).hours.do(t.run)
    while True:
        schedule.run_pending()
        time.sleep(1)
