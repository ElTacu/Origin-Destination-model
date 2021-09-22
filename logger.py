import os
from datetime import datetime
class Logger(object):
    def __init__(self, path):
        self.path = path
        self.startTime = datetime.now()


    def ini_log(self, log_name):
        self.file = os.path.join(self.path, "Log {}.txt".format(log_name))
        if os.path.exists(self.file):
            os.remove(self.file)
        self.log = open(self.file, "w")
        self.log.write("Log for {} started {}\n".format(log_name, self.startTime.strftime("%Y-%m-%d %H:%M:%S") ))
        
    def write_values(self, inobj, name):
        self.log.write("\nAttributes for {}".format(name))
        try:
            for k,v in inobj.__dict__.iteritems():
                self.log.write("\n{},{}".format(k,v)) 
        except AttributeError:
             for k,v in inobj.iteritems():  
                 self.log.write("\n{},{}".format(k,v))
        self.log.write("\n")    
        
    def msg(self,msg):
        self.log.write("\n{}".format(msg))       
        self.log.write("\n")
                
                
    def close(self):
        self.log.write("\nModel ran successfully")
        runtime = datetime.now() - self.startTime
        self.log.write("\nTotal run time was {}".format(runtime))    
        self.log.close()

                
#os.chdir("C:\Users\djimenez.MRCOG-NM\Desktop/xml_dc_uni_done_model")
#log = logger("C:\Users\djimenez.MRCOG-NM\Desktop/xml_dc_uni_done_model", "test")   
