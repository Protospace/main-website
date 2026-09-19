# Protospace Website

The Protospace WordPress site has been replaced with static HTML and CSS pages. Static files improve security, reduce maintenance, and provide faster page loads without a database or server-side CMS.

## Editing the site

1. Open the [Protospace repository](https://github.com/Protospace/main-website) on GitHub and click **Fork**. Create the fork under your own GitHub account.
2. Clone your fork and configure the Protospace repository as `upstream`:

   ```bash
   git clone git@github.com:YOUR-USERNAME/main-website.git
   cd main-website/
   git remote add upstream git@github.com:Protospace/main-website.git
   ```

3. Create a branch for your change:

   ```bash
   git checkout -b update-page
   ```

4. Edit the HTML pages, `styles.css`, or files in `assets/`. Preview the site locally with any static web server, for example:

   ```bash
   python3 -m http.server
   ```

5. Commit your changes and push the branch to your fork:

   ```bash
   git add .
   git commit -m "Update page content"
   git push -u origin update-page
   ```

6. Go to your fork on GitHub and click **Compare & pull request**. Set the base repository to `Protospace/main-website`, choose `master` as the base branch, describe what changed, and submit the pull request.

   Maintainers will review the pull request, request changes if needed, and merge it when it is ready. After your pull request is merged, you can sync your fork before starting another change:

   ```bash
   git checkout master
   git fetch upstream
   git reset --hard upstream/master
   git push origin master --force-with-lease
   ```

There is no build step. Edit the generated HTML and CSS files directly. Keep the existing responsive layout, local asset paths, accessibility text, metadata, and external Wiki/Portal links intact.

## Deploying changes

The production server will automatically pull changes from this repo every 5 minutes.

## Using a coding agent

A coding agent can be helpful for larger content, layout, accessibility, and consistency changes. Give it a focused task and ask it to inspect the existing files before editing. Follow the repository instructions in `AGENTS.md` when present, and review the resulting diff before opening a pull request.
