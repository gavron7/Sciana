import os, time
import configparser, ast

class cfg:
    def load():
        Config = configparser.ConfigParser()
        Config.read(mdir()+"/sciana.cfg")
        return Config
    def get(co,co2):
        Config=cfg.load()
        return Config.get(co,co2)

def log(co):
    print(time.time(),co)

def mdir():
    return os.path.dirname(os.path.realpath(__file__))

