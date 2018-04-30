
all: draw

draw:
	python citygen.py

oneshot:
	python citygen.py -l -t 1 -d --drawsteps

static:
	python citygen.py --static -l

clean:
	rm -r imgs
	mkdir imgs
