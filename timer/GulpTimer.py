from tkinter import *
import time
import csv

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        #self.lapstr = StringVar()
        self.e = 0
        self.startingVolume = 0
        self.endingVolume = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
        self.clickCount = 0
        
    def makeWidgets(self):                         
        """ Make the time label. """
        l1 = Label(self, text='----Sample Audio Name----',font=("Arial",25))
        l1.pack(fill=X, expand=NO, pady=1, padx=2)

        self.e = Entry(self, font=("Arial",15))
        self.e.pack(pady=2, padx=2)
        
        startingWaterVolume = Label(self, text='----Starting Water Voume----',font=("Arial",25))
        startingWaterVolume.pack(fill=X, expand=NO, pady=1, padx=2)

        self.startingVolume = Entry(self, font=("Arial",15))
        self.startingVolume.pack(pady=2, padx=2)
        
        endingWaterVolume = Label(self, text='----Ending Water Voume----',font=("Arial",25))
        endingWaterVolume.pack(fill=X, expand=NO, pady=1, padx=2)

        self.endingVolume = Entry(self, font=("Arial",15))
        self.endingVolume.pack(pady=2, padx=2)
        
        l = Label(self, textvariable=self.timestr,font=("Arial",50))
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=3, padx=2)

        l2 = Label(self, text='----Laps----',font=("Arial",15))
        l2.pack(fill=X, expand=NO, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.m = Listbox(self,selectmode=EXTENDED, height = 5,
                         yscrollcommand=scrollbar.set, font=("Arial",15), justify="center")
        self.m.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.m.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
          
    def Click(self, another_parameter):
        if self.clickCount > 0:
            self.Lap()
        elif self.clickCount == 0:            
            self.Start()
            self.clickCount += 1
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self.clickCount = 0
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self._setTime(self._elapsedtime)
        self.m.delete(0,END)

    def Lap(self):
        '''Makes a lap, only if started'''
        tempo = self._elapsedtime
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.m.insert(END, self.laps[-1])
            self.m.yview_moveto(1)
       
    def SaveCSV(self):
        '''creates a file to save the laps'''
        
        #This is the name of the audiosample
        sampleName = str(self.e.get())
        
        #water volume of the sample
        sampleVolume = str(int(self.startingVolume.get()) - int(self.endingVolume.get()))
        
        #Name of fields in csv file
        #fields =['SampleName', 'SampleVolume', 'StartTime', 'GulpTimes', 'EndTime']
        
        #First "lap" taken, represents when you start drinking
        startTime = self.laps[0]
        
        #Last "lap" taken, represents when you stop drinking
        stopTime = self.laps[-1]
        
        #Variable which will hold all "laps" between the first and last one, represents gulps
        gulpTimes = ""
        
        #Loops through all laps and only appends gulps to gulpTimes
        for lap in self.laps:
            
            if lap == startTime or lap == stopTime:
                continue
            gulpTimes += str(lap)+ "_"
        
        with open('GulpTimeElvis.csv', 'a') as lapfile:
            
            csvwriter = csv.writer(lapfile)
            
            csvwriter.writerow([sampleName,sampleVolume,startTime,gulpTimes,stopTime])

########################################################################################################

            
def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)      #always on top - might do a button for it
    sw = StopWatch(root)
    sw.pack(side=TOP)

    #Button(root, text='Lap', command=sw.Lap,height = 5, width = 10).pack(side=LEFT)
    #Button(root, text='Start', command=sw.Start,height = 5, width = 10).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop,height = 5, width = 10).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset,height = 5, width = 10).pack(side=LEFT)
    Button(root, text='Save', command=sw.SaveCSV,height = 5, width = 10).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit,height = 5, width = 10).pack(side=LEFT)
    
    root.bind("<Return>", sw.Click)   
    
    root.mainloop()

if __name__ == '__main__':
    main()