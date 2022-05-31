import gc, os

if 'main.py' in os.listdir():
	__import__('main')

gc.collect()
