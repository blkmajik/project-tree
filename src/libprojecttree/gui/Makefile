MKDIR   := md
RMDIR   := rd /S /Q
INCLUDE := ./include
UIFILES    := $(wildcard ./*.ui)
PYFILES    := $(patsubst ./%.ui,./%.py,$(UIFILES))
RCFILES	   := $(wildcard ./*.qrc)
PYRCFILES  := $(patsubst ./%.qrc,./%_rc.py,$(RCFILES))
MODULES    := $(patsubst ./%.ui,./%,$(UIFILES))
TRANSFORM = ./transform.sed
#DEPS = transform.sed icons.qrc

.PHONY: all run clean

all: $(PYFILES) $(PYRCFILES) __init__.py
	@echo "Build All"

__init__.py: $(UIFILES) $(DEPS)
	@rm -f __init__.py
	@for x in $(MODULES) ; do \
		echo "from . import $${x##*/}" >> __init__.py ; \
	done

icons_rc.py: ./icons.qrc
	@echo Building $@
	@pyrcc5 $< | $(TRANSFORM) > $@

./%.py: ./%.ui $(DEPS)
	@echo Building $@
	@pyuic5 -x $<  | $(TRANSFORM) > $@
	@echo $%

clean:
	@rm -rf *.py

