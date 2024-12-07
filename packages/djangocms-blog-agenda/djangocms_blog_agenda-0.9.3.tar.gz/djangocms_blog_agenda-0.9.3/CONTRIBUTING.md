# Contributing

How can you contribute to this project ?

## Add issue

You can help by finding new issues & reporting them by creating [new issues](https://gitlab.com/kapt/open-source/djangocms-blog-agenda/-/issues/new?issue).

## Add code

You can help by picking an issue, or choosing to add a new feature (create an issue before you start coding).

0. Create a new issue, receive positive feedback.

1. Fork the repo, clone it.

2. Install pre-commit & unit tests dependencies.
    ```bash
    python3 -m pip install pre-commit
    ```

3. Install pre-commit hooks.
    ```bash
    pre-commit install
    ```

4. Create new branch.
    ```bash
    git checkout -b mybranch
    ```

5. Add your code.

7. Add yourself in [AUTHORS.md](AUTHORS.md).

8. Commit, push.
    *Make sure that pre-commit runs isort, black and flake8.*

9. Create a [Pull Request](https://gitlab.com/kapt/open-source/djangocms-blog-agenda/-/merge_requests/new).

10. ![That's all folks!](https://i.imgur.com/o2Tcd2E.png)

----

### Commit description guidelines

We're using bluejava's [git-commit-guide](https://github.com/bluejava/git-commit-guide) for our commits description. Here's a quick reference:

![Reference git-commit-guide](https://raw.githubusercontent.com/bluejava/git-commit-guide/master/gitCommitMsgGuideQuickReference.png)
