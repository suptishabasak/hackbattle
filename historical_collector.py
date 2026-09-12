import json
from github_client import get_github_client

def collect_historical_prs(repo_name):
    g = get_github_client()
    repo = g.get_repo(repo_name)

    # Fetch closed/merged PRs
    pulls = repo.get_pulls(state='closed', sort='created', direction='desc')

    pr_data = []
    count = 0

    for pr in pulls:
        if count >= 100:   # stop after 20 PRs for testing
            break
        count += 1

        # Get changed file names
        try:
            changed_files = [f.filename for f in pr.get_files()]
        except Exception as e:
            print(f"  PR #{pr.number}: could not fetch files ({e}), skipping files list")
            changed_files = []

        # Check pass/fail status based on whether the PR was merged
        status = "pass" if pr.merged else "fail"

        pr_data.append({
            "pr_number": pr.number,
            "title": pr.title,
            "status": status,
            "changed_files": changed_files
        })

    # Save output to JSON file
    with open("historical_data.json", "w") as f:
        json.dump(pr_data, f, indent=4)

    print("Done! Historical PR data saved to historical_data.json")

if __name__ == "__main__":
    collect_historical_prs("facebook/react")