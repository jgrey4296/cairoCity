
all: draw

draw:
	python main.py -l --drawsteps

oneshot:
	python main.py -l -t 1 -d --drawsteps --dontsave

static:
	python main.py --static -l --dontsave

clean:
	-rm imgs/*
	-rm theDCEL.dcel

