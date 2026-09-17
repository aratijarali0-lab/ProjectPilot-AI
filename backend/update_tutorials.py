from app.database import projects_collection
import yt_dlp


def find_tutorial(title):
    """
    Find the best YouTube tutorial for a project.
    Returns a direct YouTube video URL.
    """

    search_query = f"ytsearch5:{title} project tutorial"

    options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(
                search_query,
                download=False
            )

        videos = result.get("entries", [])

        if not videos:
            return None

        # Prefer videos whose titles contain tutorial/project keywords
        best_video = videos[0]

        for video in videos:
            video_title = video.get("title", "").lower()

            if (
                "tutorial" in video_title
                or "project" in video_title
                or "complete" in video_title
                or "full" in video_title
            ):
                best_video = video
                break

        video_id = best_video.get("id")

        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    except Exception as e:
        print(f"Error searching '{title}': {e}")

    return None


# ---------------------------------------------------------
# Get all projects
# ---------------------------------------------------------

projects = list(
    projects_collection.find(
        {},
        {
            "_id": 1,
            "id": 1,
            "title": 1
        }
    )
)

print(f"Found {len(projects)} projects")
print("=" * 60)


updated = 0
failed = 0


# ---------------------------------------------------------
# Update tutorial links
# ---------------------------------------------------------

for index, project in enumerate(projects, start=1):

    project_id = project.get("id")
    title = project.get("title", "").strip()

    print()
    print(f"[{index}/{len(projects)}] {title}")

    if not title:
        print("  SKIPPED: No title")
        failed += 1
        continue

    tutorial_url = find_tutorial(title)

    if tutorial_url:

        projects_collection.update_one(
            {"_id": project["_id"]},
            {
                "$set": {
                    "resources.tutorial": tutorial_url
                }
            }
        )

        print(f"  Tutorial: {tutorial_url}")
        updated += 1

    else:
        print("  FAILED: No tutorial found")
        failed += 1


# ---------------------------------------------------------
# Final result
# ---------------------------------------------------------

print()
print("=" * 60)
print("UPDATE COMPLETE")
print("=" * 60)

print(f"Total projects : {len(projects)}")
print(f"Updated        : {updated}")
print(f"Failed         : {failed}")