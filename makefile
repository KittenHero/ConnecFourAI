BASHPATH:=$(shell which bash)
SHELL:=$(BASHPATH) -O globstar
undefine BASHPATH

LS_NO_SPACE=$(shell ls $(1) 2> /dev/null | grep -v ' ')
UNIQ_DIRS=$(shell echo $(dir $(1))|tr ' ' '\n'|sort|uniq|tr '\n' ' ')

MAIN=ConnectFour.py

TESTPATH=.tests/
TESTS:=$(call LS_NO_SPACE, **/*.in)
RESULTS:=$(addprefix $(TESTPATH), $(TESTS:.in=.out))
TESTSUBDIRS:=$(call UNIQ_DIRS, $(RESULTS))

ifeq (run, $(firstword $(MAKECMDGOALS)))
RUN_ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS)) # extract args
$(RUN_ARGS): # empty rule
	@
endif

.PHONY: clean test FORCE run

test: $(MAIN) $(RESULTS)

run: $(MAIN)
	python $(MAINT) $(RUN_ARGS)

clean:
	rm -rf $(TESTPATH)

$(TESTSUBDIRS):
	@mkdir -p $@

# allows use of runtime vars in prereq via $$ escape
.SECONDEXPANSION:

$(TESTPATH)%.out: %.in %.exp $(MAIN) FORCE | $$(dir $$@)
	@xargs python $(MAIN) < $< | tee $@ | diff - $(word 2, $^)
	@echo passed $(basename $(notdir $@))

$(TESTPATH)%.out: %.in $(MAIN) FORCE | $$(dir $$@)
	@xargs python $(MAIN) < $< > $@
	@echo no errors $(basename $(notdir $@))
