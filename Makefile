all: show showi
rules.py: extract_rules.py data.py
	python2 ./extract_rules.py
data.py: extract_interp.py
	python2 ./extract_interp.py
hqx.py: data.py rules.py
hq%x.png: hqx.py
	python2 ./hqx.py $*
show: hq2x.png hq3x.png hq4x.png
	feh hqx*.png
hq2x-%.png: hqx.py
	python2 ./hqx.py 2 $*
interp: hq2x-00_0.png hq2x-00_11.png hq2x-00_12.png hq2x-00_20.png hq2x-00_60.png hq2x-00_61.png hq2x-00_70.png hq2x-00_90.png hq2x-00_100.png
showi: interp
	feh hqx*-*.png
clean:
	$(RM) *.pyc hqx*.png data.py rules.py
re: clean all
.PHONY: all show showi clean re
