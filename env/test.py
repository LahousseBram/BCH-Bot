import sys, os, psutil, logging

print('Restarting...')

os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)