#!/usr/bin/python3

import logging
import threading
import time 

logging.basicConfig(level=logging.DEBUG)#, format='[%(levelname)s]'
#'(%(threadname)-10s) %(message)')
logger = logging.getLogger(__name__) 

def thread1():
    logger.debug('starting')
    time.sleep(2)
    logger.debug('exiting')

def main():
    
    t1 = threading.Thread(name='Tanjot', target = thread1)
#t1.setDaemon(True)
    t1.start()
    
if __name__ == '__main__':
    
    
    main()
