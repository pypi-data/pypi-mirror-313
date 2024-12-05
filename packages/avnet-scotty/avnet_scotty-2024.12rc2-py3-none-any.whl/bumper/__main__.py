"""Bumper: assistance tool to bump a recipe's SRCREV."""
# SPDX-FileCopyrightText: (C) 2022 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import os
import re
import textwrap

import git


def get_args():
    """Parse command-line arguments."""
    description = "Bumper tool helps to create recipe SRCREV bumps"
    parser = argparse.ArgumentParser(prog="bumper",
                                     description=description)
    parser.add_argument('--autopush', action="store_true",
                        help="Automatically push changes to remote")
    parser.add_argument('repo_path',
                        help="Path to the recipe's code repository")
    parser.add_argument('branch_name',
                        help="Branch name to query")
    parser.add_argument('recipe',
                        help="Path to the recipe")
    return parser.parse_args()


def get_srcrev(recipe_filename):
    """Get SRCREV from the recipe, as a string, but without its quotes."""
    with open(recipe_filename) as recipe:
        lines = [line for line in recipe]
        for line in lines:
            if re.match("^SRCREV\\s+.*=", line):
                return line.split()[-1].strip('\"')


def generate_change_log(commits, path_to_recipe):
    """Generate a string containing the commit's title and body."""
    recipe_name = path_to_recipe.split('/')[-1]
    authors = []
    titles = []
    message = ["{}: bump SRCREV\n".format(recipe_name)]

    for c in commits:
        author = "{} <{}>".format(c.author.name, c.author.email)
        if author not in authors:
            authors.append(author)

        title = c.message.split("\n")[0]
        titles.append(title)

    message.append('Changes:\n')
    for t in titles:
        message.append('\n'.join(textwrap.wrap(t, 72)))

    message.append('\nAuthors:\n')
    for a in authors:
        message.append('\n'.join(textwrap.wrap(a, 72)))

    return '\n'.join(message)


def set_srcrev(path_to_recipe, new_srcrev):
    """Write the new SRCREV to the recipe."""
    new_line = ""
    with open(path_to_recipe) as recipe:
        lines = [line for line in recipe]
        for line in lines:
            if re.match("^SRCREV\\s+.*=", line):
                tmp = line.split()
                tmp[-1] = '\"{}\"'.format(new_srcrev)
                new_line = ' '.join(tmp) + "\n"

    with open(path_to_recipe, "w") as new:
        for line in lines:
            if re.match("^SRCREV\\s+.*=", line):
                new.write(new_line)
                continue
            else:
                new.write(line)


def get_repo_from_recipe(path_to_recipe):
    """Return the Repo object corresponding to the recipe's repository."""
    path = os.path.dirname(os.path.abspath(path_to_recipe))
    try:
        return git.Repo(path, search_parent_directories=True)
    except Exception:
        raise Exception(f'Can\'t find repository root for {path_to_recipe}')


def submit_changes(path_to_recipe, change_log, autopush=False):
    """Add, commit and push."""
    repo = get_repo_from_recipe(path_to_recipe)
    repo.git.add(path_to_recipe)
    repo.index.commit(change_log)
    if autopush:
        repo.git.push(repo.remote().name, "HEAD")


def main():
    """Usage: bumper ~/my-repo repo-branch-name ~/meta-x/recipe.bb ."""
    args = get_args()
    path_to_repo = args.repo_path
    branch_name = args.branch_name
    path_to_recipe = args.recipe
    commits = []

    srcrev = get_srcrev(path_to_recipe)

    print(f'Base rev is {srcrev}')
    repo = git.Repo(path_to_repo)
    repo.git.checkout(branch_name)
    commits = [repo.commit(x) for x in repo.git.rev_list(
        '--ancestry-path',  f'{srcrev}..{branch_name}').split('\n')]
    print(f'{len(commits)} new commit(s)')

    if any(commits):
        set_srcrev(path_to_recipe, commits[0])
        message = generate_change_log(commits, path_to_recipe)
        submit_changes(path_to_recipe, message, args.autopush)


if __name__ == '__main__':
    main()
