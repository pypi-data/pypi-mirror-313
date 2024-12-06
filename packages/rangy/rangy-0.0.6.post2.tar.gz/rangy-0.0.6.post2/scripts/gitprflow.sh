#! /usr/bin/env sh

# This script executes my git pr flow.

# Call it with the new branch name as the first argument.
# Example: gitprflow.sh create my-new-feature
# it will then :
# 1. git checkout -b my-new-feature
# 2. ask you for a description for the branch
# 3. Create a faux commit with the description as the branch's description
# 4. git push origin my-new-feature
# 5. git push --set-upstream origin my-new-feature
# 6. Open a PR on github with the branch's description as the PR's description

create() {
  branch_name="$2"
  if [ -z "$branch_name" ]; then
    echo "Please provide a branch name:"
    read -r branch_name
    if [ -z "$branch_name" ]; then
      echo "Branch name cannot be empty."
      exit 1
    fi
  fi

  description_file="docs/branches.txt"
  temp_file=$(mktemp)

  # Ensure the description file exists
  touch "$description_file"

  # Extract the repository name from the origin remote URL
  repo_url=$(git config --get remote.origin.url)
  repo_name=$(basename -s .git "$repo_url")
  repo_owner=$(basename -s /"$repo_name".git "$(dirname "$repo_url")")

  # Step 1: Checkout branch
  if (! git rev-parse --verify "$branch_name" >/dev/null 2>&1); then
    git checkout -b "$branch_name"
  else
    echo "Branch already exists. Checking out."
    git checkout "$branch_name"
  fi

  # Step 2: Ask for description if not already provided
  if (! grep -q "^$branch_name:" "$description_file"); then
    echo "Please enter a title for the branch"
    read -r title
    echo "Please enter a description for the branch (leave blank to open editor)"
    read -r body

    if [ -z "$body" ]; then
      echo "$title" > "$temp_file"
      echo "" >> "$temp_file"
      ${EDITOR:-vi} "$temp_file"
      body=$(tail -n +2 "$temp_file")
    fi

    echo "$branch_name: $title" >> "$description_file"
    echo "$body" >> "$description_file"
    echo "" >> "$description_file"
 else
    echo "Title and body for branch created. Continuing."
    title=$(grep "^$branch_name:" "$description_file" | cut -d ':' -f 2-)
    body=$(grep -A 1 "^$branch_name:" "$description_file" | tail -n 1)
  fi

  echo "Title: $title"
  echo "Body: $body"

  # Step 3: Create a faux commit if not already committed
  # Add the description file to the staging area before checking for changes
  git add "$description_file"
  if (! git diff --cached --quiet || git ls-files --others --exclude-standard | grep -q "$description_file"); then
    description=$(grep -A 1 "^$branch_name:" "$description_file")
    echo "$description" > "$temp_file"
    git commit -F "$temp_file"
 else
    echo "No changes to commit. Continuing."

  fi

  # Step 4: Push branch to origin if not already pushed
  if (! git ls-remote --exit-code --heads origin "$branch_name" >/dev/null 2>&1); then
    git push origin "$branch_name"
 else
    echo "The branch has already been pushed to origin. Continuing."
  fi

  # Step 5: Set upstream if not already set
  if (! git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1); then
    git push --set-upstream origin "$branch_name"
   else
    echo "The upstream has already been set. Continuing."
  fi

  # Step 6: Open a PR on GitHub if not already opened
  if ! gh pr list --head "$branch_name" -s all | grep -q "$branch_name"; then
    if gh pr create --repo "$repo_owner/$repo_name" --title "$title" --body "$body"; then
      echo "Pull request created."
    else
      echo "Failed to create pull request."
    fi
   else
    echo "The PR has already been opened."
  fi

  rm "$temp_file"
}

close() {
  current_branch=$(git symbolic-ref --short HEAD)

  if [ "$current_branch" = "main" ]; then
    echo "You are on the main branch. Exiting."
    exit 1
  fi

  # Step 1: Capture the list of commits and merge stats
  commit_log=$(git log --oneline main.."$current_branch")
  merge_stats=$(git diff --stat main.."$current_branch")

  # Step 2: Merge current branch to main
  git checkout main
  git pull origin main
  if ! git merge --no-ff "$current_branch"; then
    echo "Merge failed. Exiting."
    exit 1
  fi

  # Step 3: Add separator, commit log, and merge stats to docs/branches.txt
  {
    echo "**********************************************************************"
    echo "Commits in this PR:"
    echo "$commit_log"
    echo ""
    echo "Merge stats:"
    echo "$merge_stats"
    echo "**********************************************************************"
  } >> docs/branches.txt

  # Step 4: Commit the changes to docs/branches.txt
  git add docs/branches.txt
  git commit -m "Add PR commit log and merge stats for $current_branch"
  git push origin main

  # Step 5: Rename the branch locally
  git branch -m "$current_branch" "deleted/$current_branch"

  # Step 6: Delete the branch remotely
  git push origin --delete "$current_branch"

  # Step 7: Prune deleted branches
  git fetch -p
}

# if the first argument is "create", call the create function
if [ "$1" = "create" ]; then
  create "$@"
elif [ "$1" = "close" ]; then
  close "$@"
else
  echo "Invalid command. Please use 'create' or 'close'."
  exit 1
fi