env=local

ifneq (,$(wildcard $(env).env))
include $(env).env
endif

test:
	poetry run python -m unittest discover -s tests

publish_to_pypi:
	poetry publish --build --skip-existing


tail_cicd:
	gh run watch
