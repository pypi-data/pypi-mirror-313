# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.


## Report Bugs

Report bugs on our [ZenHub Board](https://github.com/MAAP-Project/ZenHub/issues).

If you are reporting a bug, please include:

-   Any details about your environment that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug.


## Get Started!

Ready to contribute? Here's how:

1.  Fork the `dps-jupyter-extension` repo on GitHub.
2.  Clone your fork locally:
 
    ```
    git clone git@github.com:your_name_here/dps-jupyter-extension.git
    ```

3.  Set up your local, virtual environment.
Assuming you have `conda` installed, this is how you set up your fork for local development:

    ```
    conda create -n maap python=3.7
    conda activate maap
    cd dps-jupyter-extension/
    npm i
    ```

4.  Create a branch for local development:

    ```
    git checkout -b username/name_of_feature
    ```

5.  Once you have finished making your changes locally, commit your changes and push your branch to GitHub:

    ```
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin username/name_of_feature
    ```

6.  Submit a pull request through the GitHub website.



## Pull Request Guidelines

Before you submit a pull request, check that all of the required code and files have been committed and pushed to the brach.

Go to Github.com and submit a pull request. Select the _base_ branch as `develop`, `develop` is where we stage all contributions before pushing to the `main` branch. Select the branch you would like to merge into `develop` as the _compare_ branch.
Please provide a succinct title of the changes you would like to merge and detailed information on what was changed. We will then assign someone working on MAAP to review, possibly provide comments, and accept your changes.
