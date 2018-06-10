
all: draw

draw:
	python main.py --dontsave

oneshot:
	python main.py -l -t 1 -d --drawsteps --dontsave

static:
	python main.py --static -l --dontsave

clean:
	rm -r imgs
	mkdir imgs
