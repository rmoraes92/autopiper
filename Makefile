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


# Helps to run the autopiper CLI commands
# in the local environment
# without needing to install autopiper globally

init:
	poetry run autopiper init

tts:
	poetry run autopiper text-to-speech \
		hello.txt \
		hello.wav \
		--voide-model-id en_US-amy-low
