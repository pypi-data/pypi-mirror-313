build-dev:
	@rm -f python/finance_core/*.so
	maturin develop

build-prod:
	@rm -f python/finance_core/*.so
	maturin develop --release

clean:
	rm -rf `find . -name __pycache__`
