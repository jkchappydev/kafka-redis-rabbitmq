.PHONY: doctor setup dev verify smoke
doctor setup dev verify smoke:
	python3 scripts/harness.py $@
