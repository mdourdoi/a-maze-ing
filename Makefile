ENV_NAME=new_test

venv:
	./scripts/setup_env.sh ${ENV_NAME}

clean:
	rm -rf ${ENV_NAME}
