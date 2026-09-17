
from typing import Any, Dict, List, Optional
from pathlib import Path
from urllib.parse import quote_plus
import json
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ============================================================
# PROJECTPILOT AI
# Complete FastAPI backend
#
# Data flow:
# Branch
#   -> branch-specific skills
#   -> multiple selected skills
#   -> related interests
#   -> one selected interest
#   -> related career goals
#   -> strongest projects
#   -> project roadmap
#   -> project resources
#   -> YouTube video tutorials
#
# Projects are loaded from:
#   backend/app/project_dataset.json
# ============================================================


# ============================================================
# DATASET LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DATASET_FILE = BASE_DIR / "project_dataset.json"


def load_projects() -> List[Dict[str, Any]]:
    """Load all projects from project_dataset.json."""

    if not PROJECT_DATASET_FILE.exists():
        raise RuntimeError(
            "project_dataset.json was not found.\n"
            f"Expected location:\n{PROJECT_DATASET_FILE}"
        )

    try:
        with PROJECT_DATASET_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "project_dataset.json contains invalid JSON.\n"
            f"Line: {exc.lineno}, "
            f"Column: {exc.colno}, "
            f"Error: {exc.msg}"
        ) from exc

    if not isinstance(data, list):
        raise RuntimeError(
            "project_dataset.json must contain a JSON array."
        )

    clean_projects: List[Dict[str, Any]] = []

    for index, project in enumerate(data):
        if not isinstance(project, dict):
            continue

        # Give missing IDs a stable temporary value.
        if "id" not in project:
            project["id"] = index + 1

        clean_projects.append(project)

    return clean_projects


PROJECTS = load_projects()


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ProjectPilot AI",
    description=(
        "Personalized engineering project recommendation system "
        "based on branch, multiple skills, interest and career goal."
    ),
    version="11.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API MODELS
# ============================================================

class ProfileRequest(BaseModel):
    branch: str
    skills: List[str] = Field(
        default_factory=list
    )
    interests: List[str] = Field(
        default_factory=list
    )


class RecommendationRequest(BaseModel):
    branch: str = ""
    skills: List[str] = Field(
        default_factory=list
    )
    interests: List[str] = Field(
        default_factory=list
    )
    career_goal: str = ""

    # Backward compatibility with older frontend versions.
    skill: str = ""
    interest: str = ""
    career_goals: List[str] = Field(
        default_factory=list
    )


class ProjectRequest(BaseModel):
    project_id: int


# ============================================================
# NORMALIZATION
# ============================================================

TERM_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "cv": "computer vision",
    "nlp": "natural language processing",
    "iot": "iot",
    "cyber security": "cybersecurity",

    "manufacture": "manufacturing",
    "manufacture engg": "manufacturing engineer",
    "manufacturing engineering": "manufacturing engineer",

    "data analytics": "data analysis",

    "frontend": "frontend development",
    "frontend developer": "frontend development",

    "backend": "backend development",
    "backend developer": "backend development",

    "reactjs": "react",
    "node": "node.js",

    "ev": "electric vehicles",
}


def normalize(
    value: Any,
) -> str:
    """Normalize text for reliable matching."""

    if value is None:
        return ""

    text = str(
        value
    ).strip().lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return TERM_ALIASES.get(
        text,
        text,
    )


def unique_strings(
    values: Any,
) -> List[str]:
    """Remove empty and duplicate strings while preserving order."""

    if values is None:
        return []

    if isinstance(
        values,
        str,
    ):
        values = [values]

    result: List[str] = []
    seen = set()

    for value in values:

        if value is None:
            continue

        item = str(
            value
        ).strip()

        if not item:
            continue

        key = normalize(
            item
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        result.append(
            item
        )

    return result


def values_match(
    first: Any,
    second: Any,
) -> bool:
    """
    Match exact/alias/domain-related terms.

    This is intentionally conservative enough to prevent
    unrelated engineering domains from leaking into the
    progressive profile flow.
    """

    a = normalize(
        first
    )

    b = normalize(
        second
    )

    if not a or not b:
        return False

    if a == b:
        return True

    # Specific compatible pairs/families.
    families = [
        {
            "machine learning",
            "artificial intelligence",
        },
        {
            "deep learning",
            "machine learning",
            "artificial intelligence",
        },
        {
            "computer vision",
            "deep learning",
            "artificial intelligence",
        },
        {
            "natural language processing",
            "nlp",
            "artificial intelligence",
        },
        {
            "manufacturing",
            "manufacturing engineer",
            "production",
        },
        {
            "industrial automation",
            "automation",
        },
        {
            "iot",
            "internet of things",
        },
        {
            "frontend development",
            "web development",
        },
        {
            "backend development",
            "web development",
        },
        {
            "data analysis",
            "data analytics",
        },
    ]

    if any(
        a in family
        and b in family
        for family in families
    ):
        return True

    # Only use substring matching for reasonably specific terms.
    if (
        len(a) >= 4
        and (
            a in b
            or b in a
        )
    ):
        return True

    return False


def matching_values(
    selected: List[str],
    available: List[str],
) -> List[str]:

    result: List[str] = []

    for selected_value in unique_strings(
        selected
    ):

        for available_value in unique_strings(
            available
        ):

            if values_match(
                selected_value,
                available_value,
            ):

                result.append(
                    available_value
                )

                break

    return unique_strings(
        result
    )


# ============================================================
# BRANCH ALIASES
# ============================================================

BRANCH_ALIASES = {
    "computer science": "Computer Science",
    "cse": "Computer Science",
    "cs": "Computer Science",

    "information technology": "Information Technology",
    "it": "Information Technology",

    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",

    "ece": "ECE",
    "electronics and communication": "ECE",
    "electronics & communication": "ECE",
    "electronics communication": "ECE",

    "electrical engineering": "Electrical Engineering",
    "electrical": "Electrical Engineering",
    "ee": "Electrical Engineering",

    "mechanical engineering": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",
    "me": "Mechanical Engineering",

    "civil engineering": "Civil Engineering",
    "civil": "Civil Engineering",

    "agricultural engineering": "Agricultural Engineering",
    "agriculture engineering": "Agricultural Engineering",
    "agri": "Agricultural Engineering",

    "biomedical engineering": "Biomedical Engineering",
    "biomedical": "Biomedical Engineering",

    "chemical engineering": "Chemical Engineering",
    "chemical": "Chemical Engineering",
}


def canonical_branch(
    branch: str,
) -> str:
    raw = str(
        branch or ""
    ).strip()

    return BRANCH_ALIASES.get(
        normalize(raw),
        raw,
    )


# ============================================================
# PROJECT FIELD HELPERS
# ============================================================

def get_list(
    project: Dict[str, Any],
    *names: str,
) -> List[str]:

    for name in names:

        value = project.get(
            name
        )

        if isinstance(
            value,
            list,
        ):
            return unique_strings(
                value
            )

        if isinstance(
            value,
            str,
        ):
            return unique_strings(
                value
            )

    return []


def get_project_branches(
    project: Dict[str, Any],
) -> List[str]:

    return get_list(
        project,
        "branches",
        "branch",
    )


def get_project_skills(
    project: Dict[str, Any],
) -> List[str]:

    return get_list(
        project,
        "skills",
    )


def get_project_interests(
    project: Dict[str, Any],
) -> List[str]:

    return get_list(
        project,
        "interests",
    )


def get_project_careers(
    project: Dict[str, Any],
) -> List[str]:

    return get_list(
        project,
        "career_goals",
        "career",
        "careers",
    )


def get_project_technologies(
    project: Dict[str, Any],
) -> List[str]:

    return get_list(
        project,
        "technologies",
    )


# ============================================================
# BRANCH PROJECT FILTER
# ============================================================

def branch_projects(
    branch: str,
) -> List[Dict[str, Any]]:

    wanted = canonical_branch(
        branch
    )

    result: List[Dict[str, Any]] = []

    for project in PROJECTS:

        for project_branch in get_project_branches(
            project
        ):

            project_canonical = canonical_branch(
                project_branch
            )

            if (
                project_canonical == wanted
                or values_match(
                    project_canonical,
                    wanted,
                )
            ):
                result.append(
                    project
                )
                break

    return result


# ============================================================
# BRANCH SKILLS
# ============================================================

BRANCH_SKILLS = {
    "Computer Science": [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "SQL",
        "MongoDB",
        "Web Development",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Natural Language Processing",
        "Computer Vision",
        "Data Science",
        "Data Analysis",
        "Cloud Computing",
        "Cybersecurity",
        "Networking",
        "DevOps",
        "Git",
        "Docker",
        "API Development",
    ],

    "Information Technology": [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "SQL",
        "MongoDB",
        "Web Development",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Computer Vision",
        "Data Science",
        "Data Analysis",
        "Cloud Computing",
        "Cybersecurity",
        "Networking",
        "DevOps",
        "Git",
        "Docker",
        "API Development",
    ],

    "Artificial Intelligence": [
        "Python",
        "C++",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Natural Language Processing",
        "Computer Vision",
        "Data Science",
        "Data Analysis",
        "TensorFlow",
        "PyTorch",
        "Generative AI",
        "Transformers",
        "Audio Processing",
        "Speech Processing",
        "Reinforcement Learning",
        "MLOps",
        "SQL",
    ],

    "ECE": [
        "C",
        "C++",
        "Python",
        "MATLAB",
        "Arduino",
        "ESP32",
        "Embedded Systems",
        "IoT",
        "Sensors",
        "Networking",
        "Microcontrollers",
        "Signal Processing",
        "VLSI",
        "Digital Electronics",
        "Analog Electronics",
        "RFID",
        "Robotics",
        "Computer Vision",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "PCB Design",
    ],

    "Electrical Engineering": [
        "C",
        "C++",
        "Python",
        "MATLAB",
        "Arduino",
        "ESP32",
        "Embedded Systems",
        "IoT",
        "Sensors",
        "Power Systems",
        "Electrical Systems",
        "Control Systems",
        "Circuit Design",
        "PLC",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Analysis",
        "Data Science",
        "Signal Processing",
    ],

    "Mechanical Engineering": [
        "AutoCAD",
        "SolidWorks",
        "CAD",
        "CAM",
        "3D Modeling",
        "MATLAB",
        "Python",
        "C++",
        "Robotics",
        "IoT",
        "Sensors",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Analysis",
        "Data Science",
        "Computer Vision",
        "Simulation",
        "ANSYS",
        "Manufacturing",
        "PLC",
        "Industrial Automation",
    ],

    "Civil Engineering": [
        "AutoCAD",
        "Revit",
        "STAAD Pro",
        "ETABS",
        "Primavera",
        "GIS",
        "Python",
        "MATLAB",
        "C++",
        "SQL",
        "Structural Analysis",
        "3D Modeling",
        "BIM",
        "Data Analysis",
        "Data Science",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Computer Vision",
        "Image Processing",
        "IoT",
        "Sensors",
        "Remote Sensing",
        "Time Series",
        "Cloud Computing",
    ],

    "Agricultural Engineering": [
        "Python",
        "C",
        "C++",
        "MATLAB",
        "Arduino",
        "ESP32",
        "IoT",
        "Sensors",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Computer Vision",
        "Data Science",
        "Data Analysis",
        "GIS",
        "Remote Sensing",
        "Embedded Systems",
        "Robotics",
        "Image Processing",
    ],

    "Biomedical Engineering": [
        "Python",
        "C++",
        "MATLAB",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Computer Vision",
        "NLP",
        "Data Science",
        "Data Analysis",
        "Signal Processing",
        "Audio Processing",
        "IoT",
        "Sensors",
        "Medical Imaging",
        "Image Processing",
    ],

    "Chemical Engineering": [
        "Python",
        "MATLAB",
        "C++",
        "Data Science",
        "Data Analysis",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Process Simulation",
        "Process Control",
        "Optimization",
        "IoT",
        "Sensors",
        "Time Series",
    ],
}


# ============================================================
# SKILL -> INTEREST
# ============================================================

SKILL_TO_INTERESTS = {
    "python": [
        "Data Science",
        "Data Analysis",
        "Machine Learning",
        "Automation",
    ],
    "java": [
        "Software Development",
        "Web Development",
    ],
    "javascript": [
        "Web Development",
        "Frontend Development",
        "Software Development",
    ],
    "html": [
        "Web Development",
        "Frontend Development",
    ],
    "css": [
        "Web Development",
        "Frontend Development",
    ],
    "react": [
        "Web Development",
        "Frontend Development",
    ],
    "node.js": [
        "Web Development",
        "Backend Development",
    ],
    "sql": [
        "Database",
        "Web Development",
        "Data Analysis",
    ],
    "web development": [
        "Web Development",
        "Software Development",
    ],
    "machine learning": [
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Predictive Maintenance",
    ],
    "deep learning": [
        "Deep Learning",
        "Artificial Intelligence",
        "Computer Vision",
        "Generative AI",
    ],
    "artificial intelligence": [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "Computer Vision",
        "Generative AI",
    ],
    "computer vision": [
        "Computer Vision",
        "Artificial Intelligence",
        "Deep Learning",
        "Quality Control",
    ],
    "nlp": [
        "Natural Language Processing",
        "Artificial Intelligence",
        "Generative AI",
    ],
    "natural language processing": [
        "Natural Language Processing",
        "Artificial Intelligence",
        "Generative AI",
    ],
    "data science": [
        "Data Science",
        "Machine Learning",
        "Analytics",
    ],
    "data analysis": [
        "Data Analysis",
        "Data Science",
        "Forecasting",
    ],
    "cloud computing": [
        "Cloud Computing",
        "DevOps",
        "Software Development",
    ],
    "networking": [
        "Networking",
        "Cybersecurity",
    ],
    "cybersecurity": [
        "Cybersecurity",
        "Networking",
    ],
    "embedded systems": [
        "Embedded Systems",
        "IoT",
        "Automation",
    ],
    "iot": [
        "IoT",
        "Industrial Automation",
        "Automation",
        "Smart Systems",
    ],
    "sensors": [
        "IoT",
        "Machine Monitoring",
        "Automation",
    ],
    "robotics": [
        "Robotics",
        "Automation",
        "Manufacturing",
    ],
    "autocad": [
        "CAD Design",
        "Construction Technology",
        "Structural Engineering",
    ],
    "revit": [
        "BIM",
        "Construction Technology",
    ],
    "gis": [
        "GIS",
        "Smart Cities",
        "Urban Planning",
        "Transportation",
    ],
    "manufacturing": [
        "Manufacturing",
        "Industrial Automation",
        "Production",
        "Machine Monitoring",
        "Predictive Maintenance",
        "Quality Control",
        "Digital Twin",
    ],
    "industrial automation": [
        "Industrial Automation",
        "Automation",
        "Manufacturing",
        "Production",
        "Robotics",
    ],
    "power systems": [
        "Power Systems",
        "Energy Management",
        "Smart Grid",
    ],
    "electrical systems": [
        "Electrical Systems",
        "Energy Management",
        "Power Systems",
    ],
    "control systems": [
        "Control Systems",
        "Automation",
        "Industrial Automation",
    ],
    "time series": [
        "Forecasting",
        "Data Science",
        "Energy Management",
    ],
}


# ============================================================
# INTEREST -> CAREER
# ============================================================

INTEREST_TO_CAREERS = {
    "Deep Learning": [
        "Deep Learning Engineer",
        "AI Engineer",
        "Machine Learning Engineer",
    ],

    "Artificial Intelligence": [
        "AI Engineer",
        "Machine Learning Engineer",
        "ML Engineer",
        "Deep Learning Engineer",
    ],

    "Computer Vision": [
        "Computer Vision Engineer",
        "AI Engineer",
        "Deep Learning Engineer",
    ],

    "Machine Learning": [
        "Machine Learning Engineer",
        "ML Engineer",
        "Data Scientist",
    ],

    "Natural Language Processing": [
        "NLP Engineer",
        "AI Engineer",
    ],

    "NLP": [
        "NLP Engineer",
        "AI Engineer",
    ],

    "Generative AI": [
        "AI Engineer",
        "Generative AI Engineer",
        "Deep Learning Engineer",
    ],

    "Data Science": [
        "Data Scientist",
        "Machine Learning Engineer",
        "ML Engineer",
    ],

    "Data Analysis": [
        "Data Analyst",
        "Data Scientist",
    ],

    "Web Development": [
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Software Engineer",
    ],

    "Frontend Development": [
        "Frontend Developer",
        "Full Stack Developer",
        "UI Developer",
    ],

    "Backend Development": [
        "Backend Developer",
        "Full Stack Developer",
        "Software Engineer",
    ],

    "Database": [
        "Database Engineer",
        "Backend Developer",
        "Software Engineer",
    ],

    "Software Development": [
        "Software Engineer",
        "Backend Developer",
        "Full Stack Developer",
    ],

    "Manufacturing": [
        "Manufacturing Engineer",
        "Production Engineer",
        "Automation Engineer",
    ],

    "Industrial Automation": [
        "Automation Engineer",
        "Manufacturing Engineer",
        "Robotics Engineer",
    ],

    "Production": [
        "Production Engineer",
        "Manufacturing Engineer",
    ],

    "Machine Monitoring": [
        "Maintenance Engineer",
        "Manufacturing Engineer",
    ],

    "Predictive Maintenance": [
        "Maintenance Engineer",
        "Reliability Engineer",
        "Manufacturing Engineer",
    ],

    "Quality Control": [
        "Quality Engineer",
        "Manufacturing Engineer",
    ],

    "Digital Twin": [
        "Digital Twin Engineer",
        "Manufacturing Engineer",
    ],

    "Robotics": [
        "Robotics Engineer",
        "Automation Engineer",
    ],

    "Automation": [
        "Automation Engineer",
        "Robotics Engineer",
    ],

    "IoT": [
        "IoT Engineer",
        "Embedded Engineer",
        "Automation Engineer",
    ],

    "Embedded Systems": [
        "Embedded Engineer",
        "Embedded Systems Engineer",
    ],

    "CAD Design": [
        "CAD Engineer",
        "Design Engineer",
    ],

    "BIM": [
        "BIM Engineer",
        "Civil Engineer",
    ],

    "Construction Technology": [
        "Construction Engineer",
        "Civil Engineer",
    ],

    "Structural Engineering": [
        "Structural Engineer",
        "Civil Engineer",
    ],

    "GIS": [
        "GIS Engineer",
        "Urban Planner",
    ],

    "Smart Cities": [
        "Urban Planner",
        "Civil Engineer",
    ],

    "Transportation": [
        "Transportation Engineer",
        "Civil Engineer",
    ],

    "Power Systems": [
        "Power Systems Engineer",
        "Electrical Engineer",
    ],

    "Energy Management": [
        "Energy Systems Engineer",
        "Electrical Engineer",
        "Energy Analyst",
    ],

    "Renewable Energy": [
        "Renewable Energy Engineer",
        "Energy Systems Engineer",
    ],

    "Smart Grid": [
        "Smart Grid Engineer",
        "Power Systems Engineer",
    ],

    "Control Systems": [
        "Control Systems Engineer",
        "Automation Engineer",
    ],

    "Cybersecurity": [
        "Cybersecurity Engineer",
        "Security Analyst",
    ],

    "Networking": [
        "Network Engineer",
        "Cybersecurity Engineer",
    ],

    "Cloud Computing": [
        "Cloud Engineer",
        "DevOps Engineer",
    ],

    "DevOps": [
        "DevOps Engineer",
        "Cloud Engineer",
    ],
}


# ============================================================
# PROGRESSIVE FLOW
# ============================================================

def get_branch_skill_options(
    branch: str,
) -> List[str]:

    canonical = canonical_branch(
        branch
    )

    configured = BRANCH_SKILLS.get(
        canonical,
        [],
    )

    # Always start from the branch's allowed catalog.
    if not configured:
        configured = []

    # Keep branch-specific skills, but include dataset skills that
    # clearly belong to the selected branch.
    projects = branch_projects(
        canonical
    )

    dataset_context: List[str] = []

    for project in projects:
        dataset_context.extend(
            get_project_skills(project)
        )

        dataset_context.extend(
            get_project_technologies(project)
        )

    if not dataset_context:
        return unique_strings(
            configured
        )

    result = []

    for skill in configured:
        if any(
            values_match(
                skill,
                value,
            )
            for value in dataset_context
        ):
            result.append(
                skill
            )

    # Add project-defined skills where they are not redundant.
    for project in projects:
        for skill in get_project_skills(
            project
        ):

            if not any(
                values_match(
                    skill,
                    current,
                )
                for current in result
            ):
                result.append(
                    skill
                )

    return unique_strings(
        result
    )


def project_skill_hits(
    project: Dict[str, Any],
    selected_skills: List[str],
) -> int:

    skills = unique_strings(
        selected_skills
    )

    if not skills:
        return 0

    context = (
        get_project_skills(project)
        + get_project_technologies(project)
    )

    return sum(
        1
        for skill in skills
        if any(
            values_match(
                skill,
                value,
            )
            for value in context
        )
    )


def generate_interests(
    branch: str,
    selected_skills: List[str],
) -> List[str]:
    """
    Branch + selected multiple skills -> related interests.

    IMPORTANT:
    We never collect every interest from every branch project.
    The selected skills control the allowed interest set.
    """

    skills = unique_strings(
        selected_skills
    )

    if not skills:
        return []

    projects = branch_projects(
        branch
    )

    if not projects:
        return []

    # --------------------------------------------------------
    # Semantic intersection:
    # For multiple selected skills, take interests that are
    # explicitly related to the selected skills.
    # --------------------------------------------------------

    mapped_sets: List[set] = []

    for skill in skills:

        mapped = SKILL_TO_INTERESTS.get(
            normalize(skill),
            [],
        )

        if mapped:
            mapped_sets.append(
                {
                    normalize(item)
                    for item in mapped
                }
            )

    if mapped_sets:

        allowed = set(
            mapped_sets[0]
        )

        for mapped_set in mapped_sets[1:]:
            allowed.intersection_update(
                mapped_set
            )

    else:
        allowed = set()

    # If no exact common semantic interest exists,
    # allow the union of interests from the selected skill mappings.
    if not allowed:

        for mapped_set in mapped_sets:
            allowed.update(
                mapped_set
            )

    # --------------------------------------------------------
    # Project-backed validation.
    # --------------------------------------------------------

    result = []

    for project in projects:

        hits = project_skill_hits(
            project,
            skills,
        )

        if hits <= 0:
            continue

        project_interests = get_project_interests(
            project
        )

        for interest in project_interests:

            normalized_interest = normalize(
                interest
            )

            # The interest must be directly related to at least
            # one semantic selected-skill mapping OR be explicitly
            # represented by the selected-skill context.
            if (
                normalized_interest in allowed
                or any(
                    values_match(
                        interest,
                        candidate,
                    )
                    for candidate
                    in [
                        item
                        for skill in skills
                        for item in SKILL_TO_INTERESTS.get(
                            normalize(skill),
                            [],
                        )
                    ]
                )
            ):
                result.append(
                    interest
                )

    # --------------------------------------------------------
    # If the project dataset doesn't explicitly repeat the
    # semantic interest, use the selected-skill mapping itself.
    # --------------------------------------------------------

    semantic_display = []

    for skill in skills:

        for interest in SKILL_TO_INTERESTS.get(
            normalize(skill),
            [],
        ):

            semantic_display.append(
                interest
            )

    # Only return the semantic interest if it is relevant to
    # the selected branch's actual project set.
    branch_interest_context = [
        interest
        for project in projects
        for interest in (
            get_project_interests(project)
            + get_project_skills(project)
            + get_project_technologies(project)
        )
    ]

    for semantic_interest in semantic_display:

        if any(
            values_match(
                semantic_interest,
                candidate,
            )
            for candidate
            in branch_interest_context
        ):
            result.append(
                next(
                    (
                        candidate
                        for candidate
                        in branch_interest_context
                        if values_match(
                            semantic_interest,
                            candidate,
                        )
                    ),
                    semantic_interest,
                )
            )

    return unique_strings(
        result
    )


def generate_career_goals(
    branch: str,
    selected_skills: List[str],
    selected_interest: str,
) -> List[str]:
    """
    Branch + selected multiple skills + ONE selected interest
    -> related career goals.

    No selected interest means no career goals.
    """

    interest = str(
        selected_interest or ""
    ).strip()

    skills = unique_strings(
        selected_skills
    )

    if not interest:
        return []

    projects = branch_projects(
        branch
    )

    if not projects:
        return []

    # --------------------------------------------------------
    # Find projects connected to the complete current profile.
    # --------------------------------------------------------

    relevant_projects = []

    for project in projects:

        skill_hits = project_skill_hits(
            project,
            skills,
        )

        context = (
            get_project_interests(project)
            + get_project_skills(project)
            + get_project_technologies(project)
        )

        interest_match = any(
            values_match(
                interest,
                value,
            )
            for value in context
        )

        if (
            skill_hits == len(skills)
            and interest_match
        ):
            relevant_projects.append(
                project
            )

    # Fallback to closest projects when exact intersection
    # is sparse in the dataset.
    if not relevant_projects:

        scored = []

        for project in projects:

            skill_hits = project_skill_hits(
                project,
                skills,
            )

            context = (
                get_project_interests(project)
                + get_project_skills(project)
                + get_project_technologies(project)
            )

            interest_match = any(
                values_match(
                    interest,
                    value,
                )
                for value in context
            )

            score = (
                skill_hits * 2
                + (
                    3
                    if interest_match
                    else 0
                )
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        project,
                    )
                )

        best = max(
            (
                score
                for score, _
                in scored
            ),
            default=0,
        )

        relevant_projects = [
            project
            for score, project
            in scored
            if score == best
        ]

    careers = []

    for project in relevant_projects:
        careers.extend(
            get_project_careers(
                project
            )
        )

    # Add only careers semantically connected to the selected
    # interest and supported by relevant project careers.
    mapped_careers = []

    for interest_name, interest_careers in INTEREST_TO_CAREERS.items():

        if values_match(
            interest,
            interest_name,
        ):
            mapped_careers.extend(
                interest_careers
            )

    for career in mapped_careers:

        if any(
            values_match(
                career,
                existing,
            )
            for existing
            in careers
        ):
            careers.append(
                next(
                    (
                        existing
                        for existing
                        in careers
                        if values_match(
                            career,
                            existing,
                        )
                    ),
                    career,
                )
            )

    return unique_strings(
        careers
    )


# ============================================================
# ROADMAP
# ============================================================

def normalize_roadmap(
    roadmap: Any,
) -> List[Dict[str, Any]]:

    if not isinstance(
        roadmap,
        list,
    ):
        return []

    result = []

    for index, step in enumerate(
        roadmap,
        start=1,
    ):

        if isinstance(
            step,
            str,
        ):
            result.append({
                "phase": index,
                "title": step,
                "description": (
                    f"Complete this project stage: {step}."
                ),
                "technologies": [],
            })

        elif isinstance(
            step,
            dict,
        ):
            result.append({
                "phase": step.get(
                    "phase",
                    index,
                ),
                "title": (
                    step.get(
                        "title"
                    )
                    or step.get(
                        "name"
                    )
                    or f"Project Step {index}"
                ),
                "description": (
                    step.get(
                        "description"
                    )
                    or step.get(
                        "details"
                    )
                    or step.get(
                        "text"
                    )
                    or ""
                ),
                "technologies": unique_strings(
                    step.get(
                        "technologies",
                        [],
                    )
                ),
            })

    return result


def generate_project_roadmap(
    branch: str,
    skills: List[str],
    interest: str,
    career_goal: str,
    technologies: List[str],
) -> List[Dict[str, Any]]:

    technologies = unique_strings(
        technologies
    )

    if not technologies:
        technologies = unique_strings(
            skills
        )

    steps = [
        (
            "Understand the problem",
            (
                f"Study the {interest} problem in {branch} "
                "and define the expected outcome."
            ),
        ),
        (
            "Define requirements",
            (
                "Identify inputs, outputs, features, constraints "
                "and success criteria."
            ),
        ),
        (
            "Prepare the data",
            (
                f"Collect, clean and prepare the data required "
                f"for the {interest} use case."
            ),
        ),
        (
            "Design the system",
            (
                "Create the system architecture, modules, "
                "data flow and processing pipeline."
            ),
        ),
        (
            "Build the core",
            (
                "Implement the main project functionality using "
                + ", ".join(skills)
                + "."
            ),
        ),
        (
            "Implement the domain feature",
            (
                f"Implement features specifically required for "
                f"{interest}."
            ),
        ),
        (
            "Align with the career goal",
            (
                f"Refine the solution around real "
                f"{career_goal} responsibilities."
            ),
        ),
        (
            "Test and evaluate",
            (
                "Test functionality, quality, accuracy, "
                "performance and edge cases."
            ),
        ),
        (
            "Document",
            (
                "Prepare README, architecture, implementation "
                "details and results."
            ),
        ),
        (
            "Deploy and demonstrate",
            (
                "Deploy the completed project and prepare a "
                "final demonstration."
            ),
        ),
    ]

    return [
        {
            "phase": index,
            "title": title,
            "description": description,
            "technologies": technologies[:6],
        }
        for index, (
            title,
            description,
        ) in enumerate(
            steps,
            start=1,
        )
    ]


# ============================================================
# RESOURCES
# ============================================================

def clean_url(
    value: Any,
) -> str:

    if not value:
        return ""

    url = str(
        value
    ).strip()

    if (
        url.startswith("[")
        and "](" in url
        and url.endswith(")")
    ):
        url = url.split(
            "](",
            1,
        )[1][:-1]

    return url.replace(
        "\\&",
        "&",
    )


def build_resources(
    project: Dict[str, Any],
) -> Dict[str, Any]:

    title = str(
        project.get(
            "title",
            "Project",
        )
    )

    query = quote_plus(
        title
    )

    raw = project.get(
        "resources",
        {},
    )

    if not isinstance(
        raw,
        dict,
    ):
        raw = {}

    tutorials = []

    def add_youtube(
        tutorial_title: str,
        value: Any,
    ) -> None:

        url = clean_url(
            value
        )

        # Tutorials are YouTube-only.
        if (
            "youtube.com" not in url
            and "youtu.be" not in url
        ):
            return

        tutorials.append({
            "title": tutorial_title,
            "platform": "YouTube",
            "type": "video",
            "url": url,
        })

    raw_tutorials = raw.get(
        "tutorials",
        [],
    )

    if isinstance(
        raw_tutorials,
        list,
    ):

        for item in raw_tutorials:

            if not isinstance(
                item,
                dict,
            ):
                continue

            add_youtube(
                str(
                    item.get(
                        "title",
                        f"{title} Video Tutorial",
                    )
                ),
                item.get(
                    "url"
                ),
            )

    add_youtube(
        f"{title} Video Tutorial",
        raw.get(
            "tutorial"
        ),
    )

    add_youtube(
        f"{title} Video Tutorial",
        project.get(
            "tutorial"
        ),
    )

    # Guaranteed fallback: YouTube search pages only.
    if not tutorials:

        tutorials = [
            {
                "title": f"{title} Full Project Video",
                "platform": "YouTube",
                "type": "video",
                "url": (
                    "https://www.youtube.com/results?search_query="
                    + quote_plus(
                        title
                        + " full project tutorial"
                    )
                ),
            },
            {
                "title": f"{title} Step-by-Step Video",
                "platform": "YouTube",
                "type": "video",
                "url": (
                    "https://www.youtube.com/results?search_query="
                    + quote_plus(
                        title
                        + " step by step tutorial"
                    )
                ),
            },
        ]

    unique_tutorials = []
    seen_urls = set()

    for tutorial in tutorials:

        if tutorial["url"] in seen_urls:
            continue

        seen_urls.add(
            tutorial["url"]
        )

        unique_tutorials.append(
            tutorial
        )

    return {
        "github": clean_url(
            raw.get(
                "github"
            )
            or project.get(
                "github"
            )
            or (
                "https://github.com/search?q="
                + query
                + "&type=repositories"
            )
        ),
        "research_papers": clean_url(
            raw.get(
                "research_papers"
            )
            or raw.get(
                "research"
            )
            or project.get(
                "research_papers"
            )
            or project.get(
                "research"
            )
            or (
                "https://scholar.google.com/scholar?q="
                + query
            )
        ),
        "dataset": clean_url(
            raw.get(
                "dataset"
            )
            or project.get(
                "dataset"
            )
            or (
                "https://www.kaggle.com/search?q="
                + query
            )
        ),
        "tutorials": unique_tutorials,
    }


# ============================================================
# RECOMMENDATION SCORING
# ============================================================

CAREER_FAMILIES = {
    "deep learning engineer": [
        "deep learning",
        "machine learning",
        "artificial intelligence",
        "computer vision",
    ],
    "ai engineer": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "computer vision",
        "natural language processing",
    ],
    "machine learning engineer": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "data science",
    ],
    "ml engineer": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "data science",
    ],
    "computer vision engineer": [
        "computer vision",
        "deep learning",
        "artificial intelligence",
    ],
    "nlp engineer": [
        "natural language processing",
        "nlp",
        "machine learning",
        "artificial intelligence",
    ],
    "frontend developer": [
        "web development",
        "frontend development",
        "html",
        "css",
        "javascript",
        "react",
    ],
    "backend developer": [
        "web development",
        "backend development",
        "node.js",
        "python",
        "sql",
    ],
    "full stack developer": [
        "web development",
        "frontend development",
        "backend development",
        "react",
        "node.js",
        "javascript",
    ],
    "software engineer": [
        "software development",
        "web development",
        "python",
        "java",
        "javascript",
        "database",
    ],
    "manufacturing engineer": [
        "manufacturing",
        "production",
        "industrial automation",
        "automation",
        "machine monitoring",
        "predictive maintenance",
        "quality control",
        "digital twin",
    ],
    "production engineer": [
        "production",
        "manufacturing",
        "industrial automation",
        "automation",
    ],
    "automation engineer": [
        "automation",
        "industrial automation",
        "robotics",
        "manufacturing",
        "iot",
    ],
    "robotics engineer": [
        "robotics",
        "automation",
        "manufacturing",
        "computer vision",
    ],
    "iot engineer": [
        "iot",
        "internet of things",
        "embedded systems",
        "automation",
    ],
}


def score_project(
    project: Dict[str, Any],
    branch: str,
    selected_skills: List[str],
    selected_interest: str,
    career_goal: str,
) -> Dict[str, Any]:

    if not any(
        canonical_branch(project_branch)
        == canonical_branch(branch)
        or values_match(
            project_branch,
            branch,
        )
        for project_branch
        in get_project_branches(
            project
        )
    ):
        return {
            "branch_match": False,
            "score": 0,
            "dimensions": 0,
            "matched_skills": [],
            "matched_interests": [],
            "matched_career_goals": [],
            "branch_score": 0,
            "skill_score": 0,
            "interest_score": 0,
            "career_score": 0,
        }

    pskills = get_project_skills(
        project
    )

    pinterests = get_project_interests(
        project
    )

    ptech = get_project_technologies(
        project
    )

    pcareers = get_project_careers(
        project
    )

    technical_context = (
        pskills
        + ptech
        + pinterests
    )

    matched_skills = [
        skill
        for skill in selected_skills
        if any(
            values_match(
                skill,
                value,
            )
            for value in technical_context
        )
    ]

    matched_interest = []

    if selected_interest:

        interest_context = (
            pinterests
            + pskills
            + ptech
        )

        if any(
            values_match(
                selected_interest,
                value,
            )
            for value in interest_context
        ):
            matched_interest = [
                selected_interest
            ]

    matched_career = []

    if career_goal:

        # Explicit metadata match.
        matched_career = matching_values(
            [career_goal],
            pcareers,
        )

        # Career-family compatibility.
        if not matched_career:

            family = CAREER_FAMILIES.get(
                normalize(
                    career_goal
                ),
                [],
            )

            career_context = (
                pcareers
                + pinterests
                + pskills
                + ptech
            )

            if any(
                any(
                    values_match(
                        domain,
                        value,
                    )
                    for value
                    in career_context
                )
                for domain in family
            ):
                matched_career = [
                    career_goal
                ]

    matched_skills = unique_strings(
        matched_skills
    )

    matched_interest = unique_strings(
        matched_interest
    )

    matched_career = unique_strings(
        matched_career
    )

    skill_coverage = (
        len(matched_skills)
        / len(selected_skills)
        if selected_skills
        else 0
    )

    branch_score = 25

    skill_score = round(
        skill_coverage
        * 35
    )

    interest_score = (
        25
        if matched_interest
        else 0
    )

    career_score = (
        15
        if matched_career
        else 0
    )

    total = (
        branch_score
        + skill_score
        + interest_score
        + career_score
    )

    # Bonus when every selected skill matched.
    if (
        selected_skills
        and len(matched_skills)
        == len(selected_skills)
    ):
        total += 5

    dimensions = sum([
        bool(matched_skills),
        bool(matched_interest),
        bool(matched_career),
    ])

    return {
        "branch_match": True,
        "score": min(
            total,
            100,
        ),
        "dimensions": dimensions,
        "matched_skills": matched_skills,
        "matched_interests": matched_interest,
        "matched_career_goals": matched_career,
        "branch_score": branch_score,
        "skill_score": skill_score,
        "interest_score": interest_score,
        "career_score": career_score,
    }


# ============================================================
# ROOT / HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": (
            "ProjectPilot AI backend is running."
        ),
        "projects_loaded": len(
            PROJECTS
        ),
        "dataset": "project_dataset.json",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy",
        "projects_loaded": len(
            PROJECTS
        ),
    }


# ============================================================
# BRANCHES
# ============================================================

@app.get("/branches")
def get_branches():
    return {
        "success": True,
        "branches": list(
            BRANCH_SKILLS.keys()
        ),
    }


# ============================================================
# PROFILE
# ============================================================

@app.post("/profile")
def get_profile(
    request: ProfileRequest,
):

    branch = canonical_branch(
        request.branch
    )

    if branch not in BRANCH_SKILLS:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Branch '{request.branch}' is not supported."
            ),
        )

    selected_skills = unique_strings(
        request.skills
    )

    selected_interests = unique_strings(
        request.interests
    )

    # STEP 1:
    # Branch -> branch-specific skills only.
    skills = get_branch_skill_options(
        branch
    )

    # STEP 2:
    # Selected skills -> related interests.
    interests = generate_interests(
        branch,
        selected_skills,
    )

    # IMPORTANT:
    # Careers stay empty until the user actually selects
    # one of the interests.
    selected_interest = (
        selected_interests[0]
        if selected_interests
        else ""
    )

    career_goals = []

    if selected_interest:
        career_goals = generate_career_goals(
            branch,
            selected_skills,
            selected_interest,
        )

    return {
        "success": True,
        "branch": branch,
        "skills": skills,
        "interests": interests,
        "career_goals": career_goals,
        "project_count_for_branch": len(
            branch_projects(
                branch
            )
        ),
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

@app.post("/recommend")
def recommend(
    request: RecommendationRequest,
):

    branch = canonical_branch(
        request.branch
    )

    skills = unique_strings(
        request.skills
    )

    interests = unique_strings(
        request.interests
    )

    # Backward compatibility.
    if request.skill:
        skills.append(
            request.skill
        )

    if request.interest:
        interests.append(
            request.interest
        )

    skills = unique_strings(
        skills
    )

    interests = unique_strings(
        interests
    )

    career_goal = str(
        request.career_goal
        or ""
    ).strip()

    if (
        not career_goal
        and request.career_goals
    ):
        career_goal = str(
            request.career_goals[0]
        ).strip()

    if not branch:
        raise HTTPException(
            status_code=400,
            detail="Please select a branch.",
        )

    if not skills:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one skill.",
        )

    if not interests:
        raise HTTPException(
            status_code=400,
            detail="Please select an interest.",
        )

    if not career_goal:
        raise HTTPException(
            status_code=400,
            detail="Please select a career goal.",
        )

    selected_interest = interests[0]

    branch_project_list = branch_projects(
        branch
    )

    if not branch_project_list:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No projects are available for {branch}."
            ),
        )

    complete_matches = []
    partial_matches = []

    # Analyze ALL projects in project_dataset.json.
    for project in PROJECTS:

        scored = score_project(
            project,
            branch,
            skills,
            selected_interest,
            career_goal,
        )

        if not scored["branch_match"]:
            continue

        item = dict(
            project
        )

        item["recommendation_score"] = (
            scored["score"]
        )

        item["matched_skills"] = (
            scored["matched_skills"]
        )

        item["matched_interests"] = (
            scored["matched_interests"]
        )

        item["matched_career_goals"] = (
            scored["matched_career_goals"]
        )

        item["profile_dimensions_matched"] = (
            scored["dimensions"]
        )

        if (
            scored["dimensions"] == 3
            and scored["score"] >= 80
        ):
            item["match_level"] = (
                "Strong Match"
            )

        elif scored["dimensions"] >= 2:
            item["match_level"] = (
                "Good Match"
            )

        else:
            item["match_level"] = (
                "Partial Match"
            )

        item["match_breakdown"] = {
            "branch": scored["branch_score"],
            "skills": scored["skill_score"],
            "interests": scored["interest_score"],
            "career_goal": scored["career_score"],
        }

        item["match_coverage"] = {
            "skills": (
                round(
                    len(
                        scored[
                            "matched_skills"
                        ]
                    )
                    / len(skills)
                    * 100,
                    1,
                )
                if skills
                else 0
            ),
            "interest": (
                100
                if scored[
                    "matched_interests"
                ]
                else 0
            ),
            "career_goal": (
                100
                if scored[
                    "matched_career_goals"
                ]
                else 0
            ),
        }

        item["reason"] = (
            "Matched your selected profile: "
            + ", ".join(skills)
            + " | "
            + selected_interest
            + " | "
            + career_goal
        )

        # Use project roadmap when present.
        roadmap = normalize_roadmap(
            project.get(
                "roadmap",
                [],
            )
        )

        # Otherwise generate a roadmap specifically for this
        # selected project and profile.
        if not roadmap:
            roadmap = generate_project_roadmap(
                branch,
                skills,
                selected_interest,
                career_goal,
                get_project_technologies(
                    project
                ),
            )

        item["roadmap"] = roadmap

        item["resources"] = build_resources(
            project
        )

        if (
            scored["dimensions"] == 3
        ):
            complete_matches.append(
                item
            )

        else:
            partial_matches.append(
                item
            )

    def sort_key(
        item: Dict[str, Any],
    ):
        return (
            -item[
                "profile_dimensions_matched"
            ],
            -item[
                "recommendation_score"
            ],
            -item[
                "match_breakdown"
            ][
                "career_goal"
            ],
            -item[
                "match_breakdown"
            ][
                "interests"
            ],
            -item[
                "match_breakdown"
            ][
                "skills"
            ],
        )

    complete_matches.sort(
        key=sort_key
    )

    partial_matches.sort(
        key=sort_key
    )

    # --------------------------------------------------------
    # MUST NOT SHOW AN EMPTY PROJECT PAGE
    #
    # If an exact complete project is unavailable in the dataset,
    # create a personalized project from the full profile.
    # --------------------------------------------------------

    if complete_matches:

        recommendations = (
            complete_matches
            + partial_matches
        )

    else:

        generated_title = (
            f"{career_goal} - "
            f"{selected_interest} Project"
        )

        generated_technologies = unique_strings(
            skills
        )[:8]

        generated_project = {
            "id": 100000,
            "title": generated_title,
            "branches": [
                branch
            ],
            "skills": list(
                skills
            ),
            "interests": [
                selected_interest
            ],
            "career_goals": [
                career_goal
            ],
            "difficulty": "Advanced",
            "description": (
                "Personalized project generated from the complete "
                f"profile: {branch}, "
                + ", ".join(skills)
                + f", {selected_interest}, {career_goal}."
            ),
            "technologies": generated_technologies,
            "roadmap": generate_project_roadmap(
                branch,
                skills,
                selected_interest,
                career_goal,
                generated_technologies,
            ),
            "resources": {
                "github": (
                    "https://github.com/search?q="
                    + quote_plus(
                        generated_title
                    )
                    + "&type=repositories"
                ),
                "research_papers": (
                    "https://scholar.google.com/scholar?q="
                    + quote_plus(
                        generated_title
                    )
                ),
                "dataset": (
                    "https://www.kaggle.com/search?q="
                    + quote_plus(
                        generated_title
                    )
                ),
                "tutorials": [
                    {
                        "title": "Full Project Video",
                        "platform": "YouTube",
                        "type": "video",
                        "url": (
                            "https://www.youtube.com/results?search_query="
                            + quote_plus(
                                generated_title
                                + " full project tutorial"
                            )
                        ),
                    },
                    {
                        "title": "Step-by-Step Video",
                        "platform": "YouTube",
                        "type": "video",
                        "url": (
                            "https://www.youtube.com/results?search_query="
                            + quote_plus(
                                generated_title
                                + " step by step tutorial"
                            )
                        ),
                    },
                ],
            },
            "recommendation_score": 100,
            "match_level": "Personalized Match",
            "matched_skills": list(skills),
            "matched_interests": [
                selected_interest
            ],
            "matched_career_goals": [
                career_goal
            ],
            "profile_dimensions_matched": 3,
            "match_breakdown": {
                "branch": 25,
                "skills": 35,
                "interests": 25,
                "career_goal": 15,
            },
            "match_coverage": {
                "skills": 100,
                "interest": 100,
                "career_goal": 100,
            },
            "reason": (
                "Personalized from your complete profile."
            ),
        }

        recommendations = [
            generated_project
        ]

        # Add the closest real projects beneath the personalized one.
        recommendations.extend(
            partial_matches[:9]
        )

    return {
        "success": True,
        "branch": branch,
        "skills": skills,
        "interests": interests,
        "career_goal": career_goal,
        "total_projects_checked": len(
            PROJECTS
        ),
        "branch_projects_checked": len(
            branch_project_list
        ),
        "matching_projects": len(
            recommendations
        ),
        "strong_matches": len(
            complete_matches
        ),
        "recommendations": recommendations,
    }


# ============================================================
# PROJECT DETAILS
# ============================================================

def find_project(
    project_id: int,
) -> Optional[Dict[str, Any]]:
    """Find a project safely even when JSON stores IDs as strings."""

    for project in PROJECTS:
        value = project.get("id")

        try:
            if int(value) == int(project_id):
                return project
        except (TypeError, ValueError):
            continue

    return None


@app.post("/project")
def get_project(
    request: ProjectRequest,
):

    project = find_project(
        request.project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    item = dict(
        project
    )

    roadmap = normalize_roadmap(
        project.get(
            "roadmap",
            [],
        )
    )

    if not roadmap:

        project_branches = get_project_branches(
            project
        )

        project_skills = get_project_skills(
            project
        )

        project_interests = get_project_interests(
            project
        )

        project_careers = get_project_careers(
            project
        )

        roadmap = generate_project_roadmap(
            (
                project_branches[0]
                if project_branches
                else ""
            ),
            project_skills,
            (
                project_interests[0]
                if project_interests
                else "Project Development"
            ),
            (
                project_careers[0]
                if project_careers
                else "Engineer"
            ),
            get_project_technologies(
                project
            ),
        )

    item["roadmap"] = roadmap

    item["resources"] = build_resources(
        project
    )

    return {
        "success": True,
        "project": item,
    }


# ============================================================
# ROADMAP
# ============================================================

@app.get("/roadmap/{project_id}")
def get_roadmap(
    project_id: int,
):

    project = find_project(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    roadmap = normalize_roadmap(
        project.get(
            "roadmap",
            [],
        )
    )

    if not roadmap:

        project_branches = get_project_branches(
            project
        )

        roadmap = generate_project_roadmap(
            (
                project_branches[0]
                if project_branches
                else ""
            ),
            get_project_skills(
                project
            ),
            (
                get_project_interests(
                    project
                )[0]
                if get_project_interests(
                    project
                )
                else "Project Development"
            ),
            (
                get_project_careers(
                    project
                )[0]
                if get_project_careers(
                    project
                )
                else "Engineer"
            ),
            get_project_technologies(
                project
            ),
        )

    return {
        "success": True,
        "project_id": project_id,
        "title": project.get(
            "title",
            "",
        ),
        "description": project.get(
            "description",
            "",
        ),
        "difficulty": project.get(
            "difficulty",
            "Intermediate",
        ),
        "technologies": get_project_technologies(
            project
        ),
        "roadmap": roadmap,
    }


@app.post("/roadmap")
def roadmap_post(
    request: ProjectRequest,
):
    return get_roadmap(
        request.project_id
    )


# ============================================================
# RESOURCES
# ============================================================

@app.get("/resources/{project_id}")
def get_resources(
    project_id: int,
):

    project = find_project(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return {
        "success": True,
        "project_id": project_id,
        "project_title": project.get(
            "title",
            "",
        ),
        "resources": build_resources(
            project
        ),
    }


@app.post("/resources")
def resources_post(
    request: ProjectRequest,
):
    return get_resources(
        request.project_id
    )


# ============================================================
# RELATED DATASETS
# ============================================================

@app.post("/datasets")
def datasets_endpoint(
    request: ProfileRequest,
):

    try:
        from project_datasets import get_datasets

        datasets = get_datasets(
            skills=request.skills,
            interests=request.interests,
            limit=10,
        )

    except Exception:
        datasets = []

    return {
        "success": True,
        "datasets": datasets,
    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    print("=" * 72)
    print("PROJECTPILOT AI BACKEND")
    print("=" * 72)

    print(
        "Projects loaded from JSON:",
        len(PROJECTS),
    )

    print(
        "Profile flow: Branch -> Skills -> Interests -> Career"
    )

    print(
        "Recommendation flow: Branch + Skills + Interest + Career"
    )

    print(
        "Roadmaps: Project-specific"
    )

    print(
        "Resources: Project-specific"
    )

    print(
        "Tutorials: YouTube videos only"
    )

    print(
        "API: http://127.0.0.1:8000"
    )

    print(
        "Docs: http://127.0.0.1:8000/docs"
    )

    print("=" * 72)


if __name__ == "__main__":

    print(
        "ProjectPilot AI contains",
        len(PROJECTS),
        "projects.",
    )
