.PHONY: build-python-package
build-python-package:
	rm -rf ../dist
	poetry build

.PHONY: upload-python-package-test
upload-python-package-test: build-python-package
	@$(shell cat .env); twine upload \
    --repository-url https://test.pypi.org/legacy/ \
	--password "$${TWINE_TOKEN_DEV}" \
    ../dist/* \
	--verbose;

.PHONY: upload-python-package
upload-python-package: build-python-package
	@$(shell cat .env); twine upload \
	--password "$${TWINE_TOKEN_PROD}" \
    ../dist/* \
	--verbose;

.PHONY: bump-minor
bump-minor: build-python-package
	bump2version minor
	git add -A
	git commit -m "Bumped package version"
	git push origin
	git push origin --tags

.PHONY: bump-patch
bump-patch: build-python-package
	bump2version patch
	git add -A
	git commit -m "Bumped patch package version"
	git push origin
	git push origin --tags
