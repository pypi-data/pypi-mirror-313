project := "tablequiz"
quiz := "example_quiz.yaml"

default: serve

summary quiz=quiz:
  tablequiz summary {{quiz}}

develop quiz=quiz:
  watchfiles "tablequiz serve {{quiz}}" .

serve quiz=quiz:
  tablequiz serve {{quiz}}

lint:
  ruff check
  ruff format --check
  mypy --strict {{project}}

fix:
  ruff check --fix
  ruff format

uv-sync:
  uv sync

#
# Release Management
#

# Add a CHANGELOG.md entry, e.g. just changelog-add added "My entry"
changelog-add TYPE ENTRY:
    changelog-manager add {{TYPE}} {{ENTRY}}

# Find out what your next released version might be based on the changelog.
next-version:
    changelog-manager suggest

# Build and create files for a release
prepare-release:
    #!/bin/bash
    set -xeuo pipefail
    changelog-manager release
    hatch version $(changelog-manager current)
    uv lock
    hatch clean
    hatch build

# Tag and release files, make sure you run 'just prepare-release' first.
do-release:
    #!/bin/bash
    set -xeuo pipefail
    VERSION=$(changelog-manager current)
    HATCH_VERSION=$(hatch version)
    if [ "${VERSION}" != "${HATCH_VERSION}" ]; then
        echo "Mismatch between changelog version ${VERSION} and hatch version ${VERSION}"
        exit 1
    fi
    git add CHANGELOG.md {{project}}/__init__.py uv.lock
    mkdir -p build
    changelog-manager display --version $VERSION > build/release-notes.md
    if [ ! -f dist/{{project}}-${VERSION}.tar.gz ]; then
        echo "Missing expected file in dist, did you run 'just prepare-release'?"
        exit 1
    fi
    git commit -m"Release ${VERSION}"
    git tag $VERSION
    git push origin $VERSION
    git push origin main
    gh release create $VERSION --title $VERSION -F build/release-notes.md ./dist/*
    hatch publish
    hatch clean
