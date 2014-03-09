#!/bin/python2

import os
import sys

def execute(commandline):
    def inner():
        os.execlp(commandline[0], *commandline)
    return inner

actions = {
    'scrape_kickstarter': execute(['scrapy', 'crawl', 'kickstarter', '-s', 'JOBDIR=crawls/kickcrawl1']),
    'scrape_mobygames': execute(['scrapy', 'crawl', 'mobygames', '-s', 'JOBDIR=crawls/mobycrawl1']),
    'cleanpost': execute(['python2', 'kickstarter/nonspider/cleanpost.py']),
    'post_cleannames': execute(['scrapy', 'runspider', 'kickstarter/nonspider/post_cleannames.py']),
    'post_analyzetext': execute(['python2', 'kickstarter/nonspider/post_analyzetext.py']),
    'final_report': execute(['python2', 'kickstarter/nonspider/final_report.py'])
}

def print_usage():
    print('Usage: run.py [{0}]'.format('|'.join(actions.keys())))
    sys.exit(1)

if len(sys.argv) < 2:
    print_usage()

if sys.argv[1] not in actions:
    print('Unknown argument ' + sys.argv[1])
    print_usage()

actions[sys.argv[1]]()

