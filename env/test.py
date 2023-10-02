import sys, os, psutil, logging, requests, time, subprocess

print("test")
os.execl(sys.executable, 'python', __file__, *sys.argv[1:])