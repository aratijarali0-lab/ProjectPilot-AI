from app.database import db
from app.data.projects import PROJECTS


def seed_projects():
    print(f"Projects found in projects.py: {len(PROJECTS)}")

    if not PROJECTS:
        print("ERROR: No projects found in projects.py")
        return

    # Remove old project documents so we don't create duplicates
    db.projects.delete_many({})

    # Insert all projects
    result = db.projects.insert_many(PROJECTS)

    print("----------------------------------------")
    print("MongoDB seeding completed!")
    print(f"Inserted projects: {len(result.inserted_ids)}")
    print("----------------------------------------")


if __name__ == "__main__":
    seed_projects()