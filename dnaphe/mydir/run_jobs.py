import requests
#from threading import Timer
#import logging
#from . import jobs

#logging.basicConfig(filename='/home/dregmi/mydir/dly.log', filemode='w', format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
#t = 1
#logging.info('initiating master job')
#def  run_job():
#    if t==1:
#        logging.debug(" entered run_job function \n setting up timer for 5 hrs and starting timer.")
#        Timer(18000.0, run_job).start()
#        logging.debug(" timer set and started... running jobs.")
#        try:
#            r=requests.get('https://www.dnaphe.com/jobs/')
#            r.close()
#        except Exception as e:
#            logging.debug("error occured..", exc_info=True)

#run_job()


r=requests.get('https://www.dnaphe.com/jobs/')
r.close()
