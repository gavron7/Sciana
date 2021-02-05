#!/usr/bin/python3

print("URUCHAMIANIE SCIANY")

import modules.window as MW
import time

is_running=0
global logtime
logtime=0

ss=MW.Startup()
window=MW.Sciana()

def log(co,visible=True):
    global is_running
    print(time.time(),co)
    if (visible==True):
        if (is_running==0):
            ss.logtext.config(text=co, bg='yellow')
            ss.startupscreen.update()
        else:
            window.f_logs.config(text=co)
            window.root.update()
            logtime=time.time()

log("Ładowanie biblioteki PIL")
from PIL import Image, ImageTk
log("Ładowanie biblioteki MQTT")
import modules.f_mqtt as mqttlib
log("Ładowanie biblioteki funkcji")
import funkcje as funkcje

libs=[ 'os', 'io', 'subprocess', 'locale', 'urllib' , 'requests', 'json', 'psutil' ]
for i in libs:
    log("Ładowanie biblioteki "+i)
    try:
        module_obj = __import__(i)
        globals()[i] = module_obj
    except ImportError:
        sys.stderr.write("ERROR: missing python module: " + module + "\n")
        sys.exit(1)

global Config

locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")

def GetNews():
    global nid,ntitle
    log("Pobieranie newsów")
    ntitle=[]
    for newsurl in newsy:
        proc = subprocess.Popen("php "+funkcje.mdir()+"/modules/news.php " + newsurl, shell=True, stdout=subprocess.PIPE)
        feed = str(proc.stdout.read().decode('utf-8'))
        feed = [e.strip() for e in feed.split('-*NEXT*-')]
        feed.pop(0)
        for i in range(0,len(feed),2):
            ntitle.append(feed[i])
    log("Pobrano "+str(len(ntitle))+" nagłówków")
    nid=0
    window.root.after(int(Config.get("news","refresh"))*1000,GetNews)

def tick(time1=''):
    localtime = time.strftime("%A, %d %B %Y", time.localtime()) 
    time2 = time.strftime("%H:%M")
    if time2 != time1:
        time1 = time2
        window.clock_frame.config(text=time2)
        window.date_frame.config(text=localtime)
    window.clock_frame.after(250, tick)

def tickk(time3=''):
    time4 = time.strftime("%S")
    if time4 != time3:
        time3 = time4
        window.clock_frame2.config(text=time4)
    window.clock_frame2.after(250, tickk)

def ShowNews():
    global ntitle, nid
    txt=ntitle[nid]
    if is_running==1:
        log("Wyświetlenie nagłówka "+str(nid+1)+"/"+str(len(ntitle)),False)
    window.newstitle.config(text=txt)
    nid+=1
    if (nid>=len(ntitle)):
        nid=0
    window.newstitle.after(int(Config.get("news","showfor"))*1000,ShowNews)

nid=0
Config=funkcje.cfg.load()
kalendarze = [e.strip() for e in Config.get('kalendarz', 'url').split('\n')]
newsy = [e.strip() for e in Config.get('news', 'url').split('\n')]

GetNews()
tick()
tickk()
ShowNews()

def on_message(client, userdata, msg):
        w=str(msg.payload.decode("utf-8","ignore"))
        t=msg.topic
        wj=json.loads(w)
        if t=='ENERGIA':
            v=wj
            kolory1=[ 'grey', 'green', 'white', 'white','white' ]
            kolory2=[ 'black', 'black', 'black', 'green', 'red' ]
            max=3000
            auto=round(v*(len(kolory1)-1)/max)
            if (auto>len(kolory1)-1):
                auto=len(kolory1)-1
            txt=str(round(v)) + "W"
            window.energia.config(text=txt, bg=kolory2[auto], fg=kolory1[auto])

mqtt=mqttlib.mqtt()
mqtt.broker=Config.get('mqtt','broker')
mqtt.temat=Config.get('mqtt','topic')
mqtt.client.on_message = on_message

mqtt.connect()
ot=time.time()-(24*3600)
ot1=ot
logtime=ot
ss.startupscreen.destroy()
window.root.deiconify()

class Monkey(object):
    def __init__(self):
        self._cached_show = 0
        self._cached_stamp = 0
        self.filename = '/tmp/sciana.txt'

    def ook(self):
        if os.path.exists(self.filename):
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                with open ("/tmp/sciana.txt", "r") as myfile:
                    data=myfile.read()
                window.inne.config(text=data)
                self._cached_show=1
        else:
            if self._cached_show==1:
                window.inne.config(text='')
                self._cached_show=0

ffile=Monkey()
is_running=1
pstime=0
while True:
    if time.time()-ot>=.25:
        window.root.update()
        ot=time.time()
        ffile.ook()
    if time.time()-ot1>=int(Config.get("pogoda","refresh")):
        log("Pobieranie informacji pogodowych")
        window.getweather()
        window.kalendarz()
        ot1=time.time()
        log("Informacje pogodowe pobrane, następne za " +str(Config.get("pogoda","refresh"))+" sekund")
    if time.time()-logtime>60:
        log("")
        logtime=time.time()+(1000*3600)
    mqtt.loop()
    if time.time()-pstime>60:
        stat = psutil.cpu_percent(percpu=True)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        avg=psutil.getloadavg()
        print(avg)
        window.info.config(text=str(avg[2])+"%")
        pstime=time.time()

