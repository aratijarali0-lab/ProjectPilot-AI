from app.database import db


def get_career_goals(project):
    """
    Generate career goals from the existing project data.
    """

    title = str(project.get("title", "")).lower()
    description = str(project.get("description", "")).lower()

    skills = [
        str(x).lower()
        for x in project.get("skills", [])
    ]

    interests = [
        str(x).lower()
        for x in project.get("interests", [])
    ]

    technologies = [
        str(x).lower()
        for x in project.get("technologies", [])
    ]

    branches = [
        str(x).lower()
        for x in project.get("branches", [])
    ]

    text = " ".join(
        [
            title,
            description,
            *skills,
            *interests,
            *technologies
        ]
    )

    goals = []

    # ---------------------------------------------------------
    # AI / MACHINE LEARNING
    # ---------------------------------------------------------

    if any(word in text for word in [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",
        "prediction",
        "classification",
        "regression",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ]):
        goals.append("AI Engineer")
        goals.append("Machine Learning Engineer")

    # ---------------------------------------------------------
    # COMPUTER VISION
    # ---------------------------------------------------------

    if any(word in text for word in [
        "computer vision",
        "opencv",
        "face recognition",
        "image processing",
        "object detection",
        "image classification"
    ]):
        goals.append("Computer Vision Engineer")

    # ---------------------------------------------------------
    # NLP
    # ---------------------------------------------------------

    if any(word in text for word in [
        "nlp",
        "natural language processing",
        "text classification",
        "sentiment analysis",
        "chatbot",
        "language model"
    ]):
        goals.append("NLP Engineer")
        goals.append("AI Engineer")

    # ---------------------------------------------------------
    # DATA SCIENCE
    # ---------------------------------------------------------

    if any(word in text for word in [
        "data science",
        "data analysis",
        "analytics",
        "pandas",
        "numpy",
        "visualization",
        "statistics"
    ]):
        goals.append("Data Scientist")
        goals.append("Data Analyst")

    # ---------------------------------------------------------
    # WEB / FULL STACK
    # ---------------------------------------------------------

    if any(word in text for word in [
        "web development",
        "frontend",
        "backend",
        "full stack",
        "react",
        "html",
        "css",
        "javascript",
        "fastapi",
        "django",
        "flask",
        "node",
        "nodejs"
    ]):
        goals.append("Software Engineer")
        goals.append("Full Stack Developer")

    # ---------------------------------------------------------
    # BACKEND
    # ---------------------------------------------------------

    if any(word in text for word in [
        "backend",
        "fastapi",
        "django",
        "flask",
        "api",
        "rest api",
        "server"
    ]):
        goals.append("Backend Developer")

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------

    if any(word in text for word in [
        "database",
        "mysql",
        "mongodb",
        "sql",
        "postgresql",
        "database management"
    ]):
        goals.append("Database Developer")

    # ---------------------------------------------------------
    # CYBER SECURITY
    # ---------------------------------------------------------

    if any(word in text for word in [
        "cyber security",
        "cybersecurity",
        "security",
        "encryption",
        "cryptography",
        "network security",
        "authentication"
    ]):
        goals.append("Cybersecurity Engineer")

    # ---------------------------------------------------------
    # CLOUD / DEVOPS
    # ---------------------------------------------------------

    if any(word in text for word in [
        "cloud",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "devops",
        "deployment"
    ]):
        goals.append("Cloud Engineer")
        goals.append("DevOps Engineer")

    # ---------------------------------------------------------
    # IOT
    # ---------------------------------------------------------

    if any(word in text for word in [
        "iot",
        "internet of things",
        "sensor",
        "arduino",
        "raspberry pi",
        "embedded"
    ]):
        goals.append("IoT Engineer")
        goals.append("Embedded Systems Engineer")

    # ---------------------------------------------------------
    # ECE / ELECTRONICS
    # ---------------------------------------------------------

    if any(word in text for word in [
        "electronics",
        "microcontroller",
        "embedded systems",
        "vlsi",
        "verilog",
        "fpga",
        "digital electronics"
    ]) or "ece" in branches:
        goals.append("Embedded Systems Engineer")
        goals.append("Electronics Engineer")

    # ---------------------------------------------------------
    # ELECTRICAL
    # ---------------------------------------------------------

    if any(word in text for word in [
        "electrical",
        "power system",
        "power electronics",
        "renewable energy",
        "solar",
        "motor",
        "electric vehicle"
    ]) or "electrical engineering" in branches:
        goals.append("Electrical Engineer")

    # ---------------------------------------------------------
    # MECHANICAL
    # ---------------------------------------------------------

    if any(word in text for word in [
        "mechanical",
        "cad",
        "solidworks",
        "manufacturing",
        "robotics",
        "automation",
        "3d printing"
    ]) or "mechanical engineering" in branches:
        goals.append("Mechanical Engineer")

    # ---------------------------------------------------------
    # CIVIL
    # ---------------------------------------------------------

    if any(word in text for word in [
        "civil",
        "construction",
        "structural",
        "building",
        "architecture",
        "autocad"
    ]) or "civil engineering" in branches:
        goals.append("Civil Engineer")

    # ---------------------------------------------------------
    # AGRICULTURAL
    # ---------------------------------------------------------

    if any(word in text for word in [
        "agriculture",
        "agricultural",
        "crop",
        "farming",
        "soil",
        "irrigation",
        "smart farming"
    ]) or "agricultural engineering" in branches:
        goals.append("Agricultural Engineer")

    # ---------------------------------------------------------
    # GENERAL SOFTWARE ENGINEERING
    # ---------------------------------------------------------

    if any(word in text for word in [
        "python",
        "java",
        "c++",
        "software",
        "application",
        "system"
    ]):
        goals.append("Software Engineer")

    # ---------------------------------------------------------
    # DEFAULT
    # ---------------------------------------------------------

    if not goals:
        goals.append("Software Engineer")

    # Remove duplicates while preserving order
    unique_goals = []

    for goal in goals:
        if goal not in unique_goals:
            unique_goals.append(goal)

    return unique_goals


# ============================================================
# UPDATE ALL PROJECTS
# ============================================================

projects = db.projects.find()

updated = 0

for project in projects:

    career_goals = get_career_goals(project)

    db.projects.update_one(
        {"_id": project["_id"]},
        {
            "$set": {
                "career_goals": career_goals
            }
        }
    )

    updated += 1

    print(
        f"{updated}. {project.get('title')} "
        f"-> {career_goals}"
    )


print()
print("=" * 60)
print(f"Updated projects: {updated}")
print("=" * 60)