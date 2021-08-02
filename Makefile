# Rather than bother with conda just use a venv

POETRY_ACTIVATE=$$(source .venv/bin/activate)

.PHONY: env

clean:
	@find . -name '*.pyc' -exec rm -v {} \;


env:
	@poetry install -vvv
	@($(POETRY_ACTIVATE))

activate:
	@($(POETRY_ACTIVATE))

