.PHONY: build-python-package
build-python-package:
	rm -rf ./dist
	poetry build

.PHONY: upload-python-package
upload-python-package: build-python-package
	@$(shell cat .env); twine upload \
    --repository-url https://test.pypi.org/legacy/ \
	--password "$${TWINE_TOKEN}" \
    ../dist/* \
	--verbose;

.PHONY: bump-minor
bump-minor: build-python-package
	bump2version minor
	git add .
	git commit -m "Bumped package version"
	git push origin --tags