from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="ProjectPilot AI",
    description="Engineering Project Recommendation API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# BRANCH OPTIONS
# ============================================================

BRANCH_OPTIONS = {

    "Computer Science": {
        "skills": [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "React",
            "Node.js",
            "SQL",
            "Machine Learning",
            "NLP",
            "Cybersecurity",
            "Data Analysis",
            "Cloud Computing"
        ],

        "interests": [
            "Artificial Intelligence",
            "Machine Learning",
            "Web Development",
            "Data Science",
            "Cybersecurity",
            "Software Development",
            "Cloud Computing",
            "Natural Language Processing",
            "Computer Vision",
            "Automation"
        ],

        "career_goals": [
            "Software Engineer",
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Web Developer",
            "Cybersecurity Engineer",
            "Cloud Engineer"
        ]
    },


    "Electronics and Communication": {
        "skills": [
            "Arduino",
            "Embedded C",
            "Python",
            "MATLAB",
            "IoT",
            "ESP32",
            "Microcontrollers",
            "Digital Electronics",
            "PCB Design",
            "Signal Processing",
            "Communication Systems",
            "Sensors"
        ],

        "interests": [
            "IoT",
            "Embedded Systems",
            "Robotics",
            "Communication",
            "Automation",
            "Smart Devices",
            "Signal Processing",
            "Wireless Communication",
            "Electronics",
            "Artificial Intelligence"
        ],

        "career_goals": [
            "Embedded Engineer",
            "IoT Engineer",
            "Electronics Engineer",
            "Communication Engineer",
            "Robotics Engineer",
            "VLSI Engineer"
        ]
    },


    "Electrical Engineering": {
        "skills": [
            "MATLAB",
            "Python",
            "Electrical Systems",
            "Power Electronics",
            "PLC",
            "Arduino",
            "IoT",
            "Circuit Design",
            "Control Systems",
            "Sensors",
            "Power Systems",
            "Renewable Energy"
        ],

        "interests": [
            "Power Systems",
            "Renewable Energy",
            "Electrical Automation",
            "Power Electronics",
            "Smart Grid",
            "Electric Vehicles",
            "IoT",
            "Control Systems",
            "Energy Management",
            "Automation"
        ],

        "career_goals": [
            "Electrical Engineer",
            "Power Systems Engineer",
            "Power Electronics Engineer",
            "Control Engineer",
            "Renewable Energy Engineer",
            "Electrical Automation Engineer"
        ]
    },


    "Mechanical Engineering": {
        "skills": [
            "CAD",
            "SolidWorks",
            "AutoCAD",
            "Manufacturing",
            "Python",
            "MATLAB",
            "Robotics",
            "Arduino",
            "3D Printing",
            "CNC",
            "Thermodynamics",
            "Mechanical Design"
        ],

        "interests": [
            "Robotics",
            "Manufacturing",
            "Automation",
            "Mechanical Design",
            "3D Printing",
            "Automobile",
            "Industrial Engineering",
            "Thermal Engineering",
            "CAD Design",
            "Smart Manufacturing"
        ],

        "career_goals": [
            "Mechanical Engineer",
            "Design Engineer",
            "Manufacturing Engineer",
            "Robotics Engineer",
            "Automobile Engineer",
            "Automation Engineer"
        ]
    },


    "Civil Engineering": {
        "skills": [
            "AutoCAD",
            "Structural Engineering",
            "Python",
            "MATLAB",
            "STAAD Pro",
            "Revit",
            "GIS",
            "Surveying",
            "Construction Management",
            "Data Analysis",
            "Structural Analysis",
            "Quantity Estimation"
        ],

        "interests": [
            "Construction",
            "Infrastructure",
            "Structural Engineering",
            "Smart Cities",
            "Transportation",
            "Water Management",
            "Environmental Engineering",
            "Urban Planning",
            "Building Information Modeling",
            "Project Management"
        ],

        "career_goals": [
            "Civil Engineer",
            "Structural Engineer",
            "Construction Engineer",
            "Transportation Engineer",
            "Environmental Engineer",
            "Urban Planning Engineer"
        ]
    }
}


# ============================================================
# PROJECT DATABASE
# ============================================================

PROJECTS = [

    # ========================================================
    # COMPUTER SCIENCE PROJECTS
    # ========================================================

    {
        "id": 1,
        "title": "AI College Chatbot",
        "branches": ["Computer Science"],
        "skills": ["Python", "NLP", "Machine Learning"],
        "interests": [
            "Artificial Intelligence",
            "Natural Language Processing",
            "Software Development"
        ],
        "career_goals": [
            "AI Engineer",
            "Software Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "An AI chatbot that answers common college-related questions.",
        "technologies": [
            "Python",
            "NLP",
            "FastAPI",
            "React",
            "MySQL"
        ],
        "roadmap": [
            "Identify frequently asked questions",
            "Create question-answer dataset",
            "Clean and preprocess text",
            "Create intent categories",
            "Train an NLP model",
            "Build chatbot response system",
            "Create FastAPI backend",
            "Connect database",
            "Build React chat interface",
            "Test chatbot accuracy",
            "Deploy the application"
        ],
        "resources": {
            "github": "https://github.com/search?q=college+chatbot+NLP&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=educational+chatbot+NLP",
            "dataset": "https://www.kaggle.com/search?q=chatbot+dataset",
            "tutorial": "https://www.google.com/search?q=Python+NLP+chatbot+tutorial"
        }
    },


    {
        "id": 2,
        "title": "Smart Attendance System",
        "branches": ["Computer Science"],
        "skills": ["Python", "Machine Learning", "SQL"],
        "interests": [
            "Artificial Intelligence",
            "Computer Vision",
            "Automation"
        ],
        "career_goals": [
            "AI Engineer",
            "Software Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "An automated attendance system using face recognition.",
        "technologies": [
            "Python",
            "OpenCV",
            "Face Recognition",
            "FastAPI",
            "MySQL"
        ],
        "roadmap": [
            "Understand face recognition",
            "Collect student images",
            "Prepare image dataset",
            "Detect faces",
            "Generate face embeddings",
            "Configure recognition model",
            "Identify students",
            "Create attendance database",
            "Build backend API",
            "Create attendance dashboard",
            "Test recognition accuracy",
            "Deploy the system"
        ],
        "resources": {
            "github": "https://github.com/search?q=face+recognition+attendance&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=face+recognition+attendance+system",
            "dataset": "https://www.kaggle.com/search?q=face+recognition+dataset",
            "tutorial": "https://www.google.com/search?q=python+face+recognition+attendance+tutorial"
        }
    },


    {
        "id": 3,
        "title": "E-Learning Recommendation System",
        "branches": ["Computer Science"],
        "skills": ["Python", "Machine Learning", "SQL"],
        "interests": [
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science"
        ],
        "career_goals": [
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Scientist"
        ],
        "difficulty": "Advanced",
        "description": "Recommend learning resources based on student interests and skills.",
        "technologies": [
            "Python",
            "Pandas",
            "Scikit-learn",
            "FastAPI",
            "React",
            "MySQL"
        ],
        "roadmap": [
            "Collect learning resource data",
            "Create student profile structure",
            "Clean the dataset",
            "Extract important features",
            "Build recommendation logic",
            "Implement similarity calculation",
            "Rank learning resources",
            "Create backend API",
            "Build user interface",
            "Test recommendations",
            "Deploy the system"
        ],
        "resources": {
            "github": "https://github.com/search?q=learning+recommendation+system&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=educational+recommendation+system",
            "dataset": "https://www.kaggle.com/search?q=course+recommendation+dataset",
            "tutorial": "https://www.google.com/search?q=Python+recommendation+system+tutorial"
        }
    },


    {
        "id": 4,
        "title": "Cybersecurity Threat Detection",
        "branches": ["Computer Science"],
        "skills": ["Python", "Cybersecurity", "Machine Learning"],
        "interests": [
            "Cybersecurity",
            "Artificial Intelligence"
        ],
        "career_goals": [
            "Cybersecurity Engineer",
            "AI Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Detect suspicious network activities using machine learning.",
        "technologies": [
            "Python",
            "Scikit-learn",
            "Pandas",
            "FastAPI"
        ],
        "roadmap": [
            "Study common cyber threats",
            "Collect network traffic dataset",
            "Clean network data",
            "Extract network features",
            "Train classification model",
            "Evaluate threat detection",
            "Create detection API",
            "Build security dashboard",
            "Test attack scenarios",
            "Deploy monitoring system"
        ],
        "resources": {
            "github": "https://github.com/search?q=machine+learning+intrusion+detection&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=machine+learning+intrusion+detection",
            "dataset": "https://www.kaggle.com/search?q=intrusion+detection+dataset",
            "tutorial": "https://www.google.com/search?q=machine+learning+cybersecurity+tutorial"
        }
    },


    {
        "id": 5,
        "title": "Web-Based Student Management System",
        "branches": ["Computer Science"],
        "skills": ["JavaScript", "React", "Node.js", "SQL"],
        "interests": [
            "Web Development",
            "Software Development"
        ],
        "career_goals": [
            "Software Engineer",
            "Web Developer"
        ],
        "difficulty": "Intermediate",
        "description": "A web application for managing student records, courses and academic information.",
        "technologies": [
            "React",
            "Node.js",
            "Express",
            "MySQL",
            "JavaScript"
        ],
        "roadmap": [
            "Identify student management requirements",
            "Design database tables",
            "Create user interface",
            "Build React components",
            "Create Node.js backend",
            "Connect MySQL database",
            "Implement student registration",
            "Implement course management",
            "Add search and filtering",
            "Add authentication",
            "Test the application",
            "Deploy the system"
        ],
        "resources": {
            "github": "https://github.com/search?q=student+management+system+react+nodejs&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=student+management+system",
            "dataset": "https://www.kaggle.com/search?q=student+dataset",
            "tutorial": "https://www.google.com/search?q=React+Node.js+student+management+system+tutorial"
        }
    },


    # ========================================================
    # ECE PROJECTS
    # ========================================================

    {
        "id": 11,
        "title": "Smart Health Monitoring System",
        "branches": [
            "Electronics and Communication"
        ],
        "skills": [
            "Arduino",
            "IoT",
            "Sensors",
            "Python"
        ],
        "interests": [
            "IoT",
            "Smart Devices",
            "Embedded Systems"
        ],
        "career_goals": [
            "IoT Engineer",
            "Embedded Engineer",
            "Electronics Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Monitor health parameters using sensors and an IoT platform.",
        "technologies": [
            "Arduino",
            "ESP32",
            "Sensors",
            "Python",
            "IoT"
        ],
        "roadmap": [
            "Study health monitoring parameters",
            "Select suitable sensors",
            "Connect sensors to microcontroller",
            "Read sensor measurements",
            "Filter sensor data",
            "Connect ESP32 to Wi-Fi",
            "Send data to backend",
            "Store health measurements",
            "Create monitoring dashboard",
            "Test sensor accuracy",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=IoT+health+monitoring+Arduino&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=IoT+health+monitoring",
            "dataset": "https://www.kaggle.com/search?q=health+monitoring+dataset",
            "tutorial": "https://www.google.com/search?q=Arduino+IoT+health+monitoring+tutorial"
        }
    },


    {
        "id": 12,
        "title": "Fire and Gas Detection System",
        "branches": [
            "Electronics and Communication"
        ],
        "skills": [
            "Arduino",
            "Sensors",
            "Embedded C"
        ],
        "interests": [
            "Embedded Systems",
            "Smart Devices",
            "Automation"
        ],
        "career_goals": [
            "Embedded Engineer",
            "Electronics Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Detect fire and hazardous gases using sensors and provide alerts.",
        "technologies": [
            "Arduino",
            "Gas Sensor",
            "Flame Sensor",
            "Buzzer",
            "Embedded C"
        ],
        "roadmap": [
            "Study fire and gas detection",
            "Select gas and flame sensors",
            "Connect sensors to Arduino",
            "Read sensor values",
            "Set threshold levels",
            "Implement warning logic",
            "Connect buzzer and indicators",
            "Add mobile notification",
            "Test different conditions",
            "Improve detection accuracy",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=Arduino+fire+gas+detection&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=IoT+fire+gas+detection",
            "dataset": "https://www.kaggle.com/search?q=gas+detection+dataset",
            "tutorial": "https://www.google.com/search?q=Arduino+fire+gas+detection+tutorial"
        }
    },


    {
        "id": 13,
        "title": "IoT Smart Home Automation",
        "branches": [
            "Electronics and Communication"
        ],
        "skills": [
            "ESP32",
            "IoT",
            "Arduino",
            "Python"
        ],
        "interests": [
            "IoT",
            "Automation",
            "Smart Devices"
        ],
        "career_goals": [
            "IoT Engineer",
            "Embedded Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Control and monitor home appliances through an IoT platform.",
        "technologies": [
            "ESP32",
            "Arduino",
            "IoT",
            "Python",
            "Sensors"
        ],
        "roadmap": [
            "Study smart home architecture",
            "Select appliances and sensors",
            "Connect relay modules",
            "Program ESP32",
            "Connect device to Wi-Fi",
            "Build IoT communication",
            "Create appliance control logic",
            "Build monitoring dashboard",
            "Add automation rules",
            "Test remote control",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=ESP32+smart+home+automation&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=IoT+smart+home+automation",
            "dataset": "https://www.kaggle.com/search?q=smart+home+dataset",
            "tutorial": "https://www.google.com/search?q=ESP32+smart+home+automation+tutorial"
        }
    },


    {
        "id": 14,
        "title": "Wireless Communication Monitoring System",
        "branches": [
            "Electronics and Communication"
        ],
        "skills": [
            "MATLAB",
            "Signal Processing",
            "Communication Systems"
        ],
        "interests": [
            "Communication",
            "Wireless Communication",
            "Signal Processing"
        ],
        "career_goals": [
            "Communication Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Analyze and visualize wireless communication signals.",
        "technologies": [
            "MATLAB",
            "Signal Processing",
            "Communication Systems"
        ],
        "roadmap": [
            "Study wireless communication basics",
            "Understand signal characteristics",
            "Generate sample signals",
            "Apply signal filtering",
            "Analyze frequency spectrum",
            "Implement modulation techniques",
            "Compare communication methods",
            "Measure signal quality",
            "Build visualization interface",
            "Test different signal conditions",
            "Document results"
        ],
        "resources": {
            "github": "https://github.com/search?q=MATLAB+wireless+communication&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=wireless+communication+signal+processing",
            "dataset": "https://www.kaggle.com/search?q=signal+processing+dataset",
            "tutorial": "https://www.google.com/search?q=MATLAB+wireless+communication+tutorial"
        }
    },


    # ========================================================
    # ELECTRICAL PROJECTS
    # ========================================================

    {
        "id": 21,
        "title": "Renewable Energy Management System",
        "branches": [
            "Electrical Engineering"
        ],
        "skills": [
            "IoT",
            "Python",
            "Electrical Systems"
        ],
        "interests": [
            "Renewable Energy",
            "IoT",
            "Energy Management"
        ],
        "career_goals": [
            "Electrical Engineer",
            "Renewable Energy Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Monitor and manage renewable energy generation and consumption.",
        "technologies": [
            "ESP32",
            "Python",
            "IoT",
            "Sensors",
            "FastAPI"
        ],
        "roadmap": [
            "Study renewable energy systems",
            "Identify energy parameters",
            "Connect measurement sensors",
            "Collect generation data",
            "Collect consumption data",
            "Build IoT communication",
            "Store energy measurements",
            "Analyze generation and demand",
            "Develop energy management logic",
            "Create dashboard",
            "Test system",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=renewable+energy+management+IoT&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=renewable+energy+management+IoT",
            "dataset": "https://www.kaggle.com/search?q=renewable+energy+dataset",
            "tutorial": "https://www.google.com/search?q=renewable+energy+IoT+monitoring+tutorial"
        }
    },


    {
        "id": 22,
        "title": "Smart Grid Energy Monitoring",
        "branches": [
            "Electrical Engineering"
        ],
        "skills": [
            "MATLAB",
            "Power Systems",
            "Python"
        ],
        "interests": [
            "Power Systems",
            "Smart Grid",
            "Energy Management"
        ],
        "career_goals": [
            "Power Systems Engineer",
            "Electrical Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Monitor electrical energy consumption and analyze smart grid parameters.",
        "technologies": [
            "MATLAB",
            "Python",
            "IoT",
            "Power Systems"
        ],
        "roadmap": [
            "Study smart grid architecture",
            "Identify power parameters",
            "Collect energy consumption data",
            "Process measurement data",
            "Analyze load patterns",
            "Identify peak demand",
            "Develop monitoring algorithm",
            "Create visualization dashboard",
            "Test different load conditions",
            "Evaluate system performance",
            "Deploy monitoring prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=smart+grid+energy+monitoring&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=smart+grid+energy+monitoring",
            "dataset": "https://www.kaggle.com/search?q=smart+grid+dataset",
            "tutorial": "https://www.google.com/search?q=MATLAB+smart+grid+tutorial"
        }
    },


    {
        "id": 23,
        "title": "Solar Power Prediction System",
        "branches": [
            "Electrical Engineering"
        ],
        "skills": [
            "Python",
            "MATLAB",
            "Data Analysis"
        ],
        "interests": [
            "Renewable Energy",
            "Power Systems",
            "Artificial Intelligence"
        ],
        "career_goals": [
            "Renewable Energy Engineer",
            "Electrical Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Predict solar power generation using weather and historical energy data.",
        "technologies": [
            "Python",
            "Pandas",
            "Scikit-learn",
            "MATLAB"
        ],
        "roadmap": [
            "Study solar power generation",
            "Collect solar generation data",
            "Collect weather data",
            "Clean the dataset",
            "Analyze important parameters",
            "Create input features",
            "Train prediction model",
            "Evaluate prediction accuracy",
            "Build prediction API",
            "Create dashboard",
            "Test with new data"
        ],
        "resources": {
            "github": "https://github.com/search?q=solar+power+prediction+machine+learning&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=solar+power+prediction+machine+learning",
            "dataset": "https://www.kaggle.com/search?q=solar+power+dataset",
            "tutorial": "https://www.google.com/search?q=solar+power+prediction+Python+tutorial"
        }
    },


    {
        "id": 24,
        "title": "Electric Vehicle Charging Monitor",
        "branches": [
            "Electrical Engineering"
        ],
        "skills": [
            "IoT",
            "Python",
            "Electrical Systems"
        ],
        "interests": [
            "Electric Vehicles",
            "Energy Management",
            "IoT"
        ],
        "career_goals": [
            "Electrical Engineer",
            "Power Electronics Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Monitor EV charging parameters and energy consumption.",
        "technologies": [
            "ESP32",
            "Python",
            "IoT",
            "Sensors"
        ],
        "roadmap": [
            "Study EV charging systems",
            "Identify charging parameters",
            "Connect voltage and current sensors",
            "Collect charging measurements",
            "Calculate power consumption",
            "Store charging data",
            "Build monitoring API",
            "Create dashboard",
            "Add charging alerts",
            "Test different charging conditions",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=EV+charging+monitor+IoT&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=electric+vehicle+charging+monitoring",
            "dataset": "https://www.kaggle.com/search?q=electric+vehicle+dataset",
            "tutorial": "https://www.google.com/search?q=ESP32+EV+charging+monitor+tutorial"
        }
    },


    # ========================================================
    # MECHANICAL PROJECTS
    # ========================================================

    {
        "id": 31,
        "title": "Robotic Arm Control System",
        "branches": [
            "Mechanical Engineering"
        ],
        "skills": [
            "Arduino",
            "Robotics",
            "Python"
        ],
        "interests": [
            "Robotics",
            "Automation",
            "Manufacturing"
        ],
        "career_goals": [
            "Robotics Engineer",
            "Mechanical Engineer",
            "Automation Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Design and control a robotic arm for automated object handling.",
        "technologies": [
            "Arduino",
            "Servo Motors",
            "Python",
            "OpenCV",
            "Robotics"
        ],
        "roadmap": [
            "Study robotic arm concepts",
            "Design mechanical structure",
            "Select motors",
            "Build arm mechanism",
            "Connect motor controllers",
            "Program basic movement",
            "Implement inverse kinematics",
            "Add object detection",
            "Implement automated picking",
            "Build control interface",
            "Test precision",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=Arduino+robotic+arm&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=robotic+arm+control+system",
            "dataset": "https://www.kaggle.com/search?q=robotic+arm",
            "tutorial": "https://www.google.com/search?q=Arduino+robotic+arm+tutorial"
        }
    },


    {
        "id": 32,
        "title": "Smart Manufacturing Monitoring System",
        "branches": [
            "Mechanical Engineering"
        ],
        "skills": [
            "IoT",
            "Python",
            "Manufacturing"
        ],
        "interests": [
            "Manufacturing",
            "Automation",
            "Smart Manufacturing"
        ],
        "career_goals": [
            "Manufacturing Engineer",
            "Automation Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Monitor manufacturing machines and production parameters using IoT.",
        "technologies": [
            "ESP32",
            "Python",
            "IoT",
            "Sensors"
        ],
        "roadmap": [
            "Study manufacturing processes",
            "Identify machine parameters",
            "Select industrial sensors",
            "Install sensors",
            "Collect machine data",
            "Connect IoT device",
            "Store production data",
            "Analyze machine performance",
            "Create monitoring dashboard",
            "Add machine alerts",
            "Test the system",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=IoT+smart+manufacturing&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=smart+manufacturing+IoT",
            "dataset": "https://www.kaggle.com/search?q=manufacturing+dataset",
            "tutorial": "https://www.google.com/search?q=IoT+smart+manufacturing+tutorial"
        }
    },


    {
        "id": 33,
        "title": "3D Printed Mechanical Component Design",
        "branches": [
            "Mechanical Engineering"
        ],
        "skills": [
            "CAD",
            "SolidWorks",
            "3D Printing"
        ],
        "interests": [
            "3D Printing",
            "Mechanical Design",
            "CAD Design"
        ],
        "career_goals": [
            "Design Engineer",
            "Mechanical Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Design, simulate and 3D print a functional mechanical component.",
        "technologies": [
            "SolidWorks",
            "CAD",
            "3D Printing"
        ],
        "roadmap": [
            "Identify component requirements",
            "Create initial concept",
            "Create CAD model",
            "Apply dimensions",
            "Perform mechanical analysis",
            "Optimize component design",
            "Prepare 3D printing model",
            "Select printing material",
            "Print prototype",
            "Test component strength",
            "Improve final design"
        ],
        "resources": {
            "github": "https://github.com/search?q=3D+printed+mechanical+design&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=3D+printing+mechanical+design",
            "dataset": "https://www.kaggle.com/search?q=3D+printing+dataset",
            "tutorial": "https://www.google.com/search?q=SolidWorks+3D+printing+mechanical+design+tutorial"
        }
    },


    {
        "id": 34,
        "title": "Predictive Maintenance System",
        "branches": [
            "Mechanical Engineering"
        ],
        "skills": [
            "Python",
            "Machine Learning",
            "Data Analysis"
        ],
        "interests": [
            "Manufacturing",
            "Automation",
            "Industrial Engineering"
        ],
        "career_goals": [
            "Manufacturing Engineer",
            "Mechanical Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Predict possible machine failures using sensor and maintenance data.",
        "technologies": [
            "Python",
            "Pandas",
            "Scikit-learn",
            "Machine Learning"
        ],
        "roadmap": [
            "Study machine failure patterns",
            "Collect machine sensor data",
            "Clean the dataset",
            "Analyze machine parameters",
            "Create predictive features",
            "Train machine learning model",
            "Evaluate failure prediction",
            "Create prediction API",
            "Build monitoring dashboard",
            "Test with new data",
            "Deploy the system"
        ],
        "resources": {
            "github": "https://github.com/search?q=predictive+maintenance+machine+learning&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=predictive+maintenance+machine+learning",
            "dataset": "https://www.kaggle.com/search?q=predictive+maintenance+dataset",
            "tutorial": "https://www.google.com/search?q=Python+predictive+maintenance+tutorial"
        }
    },


    # ========================================================
    # CIVIL PROJECTS
    # ========================================================

    {
        "id": 41,
        "title": "Construction Cost Prediction",
        "branches": [
            "Civil Engineering"
        ],
        "skills": [
            "Python",
            "Machine Learning",
            "Data Analysis"
        ],
        "interests": [
            "Construction",
            "Machine Learning",
            "Project Management"
        ],
        "career_goals": [
            "Civil Engineer",
            "Construction Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Estimate construction costs using historical project data.",
        "technologies": [
            "Python",
            "Pandas",
            "Scikit-learn",
            "FastAPI",
            "React"
        ],
        "roadmap": [
            "Study construction cost estimation",
            "Collect historical project data",
            "Identify cost factors",
            "Clean dataset",
            "Analyze project parameters",
            "Select important features",
            "Train regression models",
            "Evaluate cost prediction",
            "Build prediction API",
            "Create estimation interface",
            "Test with sample projects",
            "Deploy system"
        ],
        "resources": {
            "github": "https://github.com/search?q=construction+cost+prediction+machine+learning&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=construction+cost+prediction+machine+learning",
            "dataset": "https://www.kaggle.com/search?q=construction+cost+dataset",
            "tutorial": "https://www.google.com/search?q=construction+cost+prediction+python+tutorial"
        }
    },


    {
        "id": 42,
        "title": "Smart Traffic Management System",
        "branches": [
            "Civil Engineering"
        ],
        "skills": [
            "Python",
            "Data Analysis",
            "GIS"
        ],
        "interests": [
            "Transportation",
            "Smart Cities",
            "Infrastructure"
        ],
        "career_goals": [
            "Transportation Engineer",
            "Civil Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Analyze traffic data and develop a smart traffic management solution.",
        "technologies": [
            "Python",
            "Pandas",
            "GIS",
            "Machine Learning"
        ],
        "roadmap": [
            "Study traffic flow concepts",
            "Collect traffic data",
            "Clean traffic dataset",
            "Analyze traffic patterns",
            "Identify congestion points",
            "Create traffic prediction model",
            "Develop traffic optimization logic",
            "Visualize traffic conditions",
            "Create monitoring dashboard",
            "Test different traffic scenarios",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=smart+traffic+management+python&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=smart+traffic+management+system",
            "dataset": "https://www.kaggle.com/search?q=traffic+dataset",
            "tutorial": "https://www.google.com/search?q=Python+traffic+management+project+tutorial"
        }
    },


    {
        "id": 43,
        "title": "Structural Health Monitoring System",
        "branches": [
            "Civil Engineering"
        ],
        "skills": [
            "MATLAB",
            "Structural Engineering",
            "Sensors"
        ],
        "interests": [
            "Structural Engineering",
            "Infrastructure",
            "Smart Cities"
        ],
        "career_goals": [
            "Structural Engineer",
            "Civil Engineer"
        ],
        "difficulty": "Advanced",
        "description": "Monitor structural conditions using sensors and data analysis.",
        "technologies": [
            "MATLAB",
            "Sensors",
            "Python",
            "Data Analysis"
        ],
        "roadmap": [
            "Study structural health monitoring",
            "Identify structural parameters",
            "Select sensors",
            "Install measurement system",
            "Collect structural data",
            "Filter sensor measurements",
            "Analyze structural behavior",
            "Identify abnormal conditions",
            "Create monitoring dashboard",
            "Test system",
            "Prepare structural report"
        ],
        "resources": {
            "github": "https://github.com/search?q=structural+health+monitoring&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=structural+health+monitoring",
            "dataset": "https://www.kaggle.com/search?q=structural+health+dataset",
            "tutorial": "https://www.google.com/search?q=structural+health+monitoring+MATLAB+tutorial"
        }
    },


    {
        "id": 44,
        "title": "Water Quality Monitoring System",
        "branches": [
            "Civil Engineering"
        ],
        "skills": [
            "IoT",
            "Python",
            "Sensors"
        ],
        "interests": [
            "Water Management",
            "Environmental Engineering",
            "IoT"
        ],
        "career_goals": [
            "Environmental Engineer",
            "Civil Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Monitor water quality parameters using IoT sensors.",
        "technologies": [
            "ESP32",
            "IoT",
            "Sensors",
            "Python"
        ],
        "roadmap": [
            "Study water quality parameters",
            "Select water quality sensors",
            "Connect sensors to microcontroller",
            "Collect pH and other measurements",
            "Calibrate sensors",
            "Transmit sensor data",
            "Store measurements",
            "Analyze water quality",
            "Create monitoring dashboard",
            "Add quality alerts",
            "Test the system",
            "Deploy prototype"
        ],
        "resources": {
            "github": "https://github.com/search?q=IoT+water+quality+monitoring&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=IoT+water+quality+monitoring",
            "dataset": "https://www.kaggle.com/search?q=water+quality+dataset",
            "tutorial": "https://www.google.com/search?q=ESP32+water+quality+monitoring+tutorial"
        }
    },


    {
        "id": 45,
        "title": "BIM-Based Construction Management",
        "branches": [
            "Civil Engineering"
        ],
        "skills": [
            "Revit",
            "AutoCAD",
            "Construction Management"
        ],
        "interests": [
            "Building Information Modeling",
            "Construction",
            "Project Management"
        ],
        "career_goals": [
            "Construction Engineer",
            "Civil Engineer"
        ],
        "difficulty": "Intermediate",
        "description": "Use BIM concepts to improve construction planning and project management.",
        "technologies": [
            "Revit",
            "AutoCAD",
            "BIM",
            "Project Management"
        ],
        "roadmap": [
            "Study BIM concepts",
            "Define construction project requirements",
            "Create building model",
            "Add structural components",
            "Add construction information",
            "Create project schedule",
            "Link construction activities",
            "Analyze project progress",
            "Identify construction conflicts",
            "Create project dashboard",
            "Prepare final BIM report"
        ],
        "resources": {
            "github": "https://github.com/search?q=BIM+construction+management&type=repositories",
            "research_papers": "https://scholar.google.com/scholar?q=BIM+construction+management",
            "dataset": "https://www.kaggle.com/search?q=construction+dataset",
            "tutorial": "https://www.google.com/search?q=Revit+BIM+construction+management+tutorial"
        }
    }
]


# ============================================================
# REQUEST MODEL
# ============================================================

class RecommendationRequest(BaseModel):
    branch: str
    skill: str
    interest: str
    career_goal: Optional[str] = None


# ============================================================
# HELPER
# ============================================================

def normalize(value: str) -> str:
    return value.strip().lower()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "ProjectPilot AI backend is running",
        "docs": "/docs"
    }


# ============================================================
# GET ALL BRANCHES
# ============================================================

@app.get("/branches")
def get_branches():
    return {
        "status": "success",
        "branches": list(BRANCH_OPTIONS.keys())
    }


# ============================================================
# GET BRANCH-SPECIFIC OPTIONS
# ============================================================

@app.get("/branch-options/{branch}")
def get_branch_options(branch: str):

    # Decode URL value naturally
    selected_branch = branch.strip()

    if selected_branch not in BRANCH_OPTIONS:
        return {
            "status": "error",
            "message": "Branch not found",
            "skills": [],
            "interests": [],
            "career_goals": []
        }

    options = BRANCH_OPTIONS[selected_branch]

    return {
        "status": "success",
        "branch": selected_branch,
        "skills": options["skills"],
        "interests": options["interests"],
        "career_goals": options["career_goals"]
    }


# ============================================================
# RECOMMEND PROJECTS
# ============================================================

@app.post("/recommend")
def recommend_projects(request: RecommendationRequest):

    branch = request.branch.strip()
    skill = request.skill.strip()
    interest = request.interest.strip()
    career_goal = (
        request.career_goal.strip()
        if request.career_goal
        else ""
    )

    # --------------------------------------------------------
    # Validate branch
    # --------------------------------------------------------

    if branch not in BRANCH_OPTIONS:
        return {
            "status": "error",
            "message": "Invalid engineering branch.",
            "recommendations": []
        }

    # --------------------------------------------------------
    # Validate skill
    # --------------------------------------------------------

    branch_skills = BRANCH_OPTIONS[branch]["skills"]

    if skill not in branch_skills:
        return {
            "status": "error",
            "message": "Selected skill does not belong to this branch.",
            "recommendations": []
        }

    # --------------------------------------------------------
    # Validate interest
    # --------------------------------------------------------

    branch_interests = BRANCH_OPTIONS[branch]["interests"]

    if interest not in branch_interests:
        return {
            "status": "error",
            "message": "Selected interest does not belong to this branch.",
            "recommendations": []
        }

    # --------------------------------------------------------
    # Validate career goal if selected
    # --------------------------------------------------------

    branch_career_goals = BRANCH_OPTIONS[branch]["career_goals"]

    if career_goal and career_goal not in branch_career_goals:
        return {
            "status": "error",
            "message": "Selected career goal does not belong to this branch.",
            "recommendations": []
        }

    # --------------------------------------------------------
    # Normalize input
    # --------------------------------------------------------

    selected_branch = normalize(branch)
    selected_skill = normalize(skill)
    selected_interest = normalize(interest)
    selected_career = normalize(career_goal)

    scored_projects = []

    # --------------------------------------------------------
    # Score every project
    # --------------------------------------------------------

    for project in PROJECTS:

        score = 0

        matched_skills = []
        matched_interests = []
        matched_career_goals = []
        matched_branches = []

        project_branches = [
            normalize(x)
            for x in project["branches"]
        ]

        project_skills = [
            normalize(x)
            for x in project["skills"]
        ]

        project_interests = [
            normalize(x)
            for x in project["interests"]
        ]

        project_career_goals = [
            normalize(x)
            for x in project.get("career_goals", [])
        ]

        # ----------------------------------------------------
        # BRANCH MATCH
        # ----------------------------------------------------

        if selected_branch in project_branches:

            score += 40
            matched_branches.append(branch)

        else:
            # Do not recommend unrelated branch projects
            continue

        # ----------------------------------------------------
        # SKILL MATCH
        # ----------------------------------------------------

        if selected_skill in project_skills:

            score += 30
            matched_skills.append(skill)

        # ----------------------------------------------------
        # INTEREST MATCH
        # ----------------------------------------------------

        if selected_interest in project_interests:

            score += 30
            matched_interests.append(interest)

        # ----------------------------------------------------
        # CAREER GOAL MATCH
        # ----------------------------------------------------

        if selected_career:

            if selected_career in project_career_goals:

                score += 20
                matched_career_goals.append(career_goal)

        # ----------------------------------------------------
        # Only keep projects that have at least branch match
        # plus skill or interest match.
        # ----------------------------------------------------

        if (
            matched_skills
            or matched_interests
            or matched_career_goals
        ):

            reasons = []

            if matched_skills:
                reasons.append(
                    "Matches your selected skill"
                )

            if matched_interests:
                reasons.append(
                    "Matches your selected interest"
                )

            if matched_career_goals:
                reasons.append(
                    "Matches your career goal"
                )

            if matched_branches:
                reasons.append(
                    "Matches your engineering branch"
                )

            result = {
                "id": project["id"],
                "title": project["title"],
                "branches": project["branches"],
                "skills": project["skills"],
                "interests": project["interests"],
                "career_goals": project.get(
                    "career_goals",
                    []
                ),
                "difficulty": project["difficulty"],
                "description": project["description"],
                "technologies": project["technologies"],
                "roadmap": project["roadmap"],
                "resources": project["resources"],

                "match_score": score,
                "recommendation_score": score,

                "matched_skills": matched_skills,
                "matched_interests": matched_interests,
                "matched_career_goals": matched_career_goals,
                "matched_branches": matched_branches,

                "reason": ", ".join(reasons)
            }

            scored_projects.append(result)

    # --------------------------------------------------------
    # SORT BY SCORE
    # --------------------------------------------------------

    scored_projects.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # RETURN ALL MATCHING PROJECTS
    # --------------------------------------------------------

    return {
        "status": "success",
        "branch": branch,
        "skill": skill,
        "interest": interest,
        "career_goal": career_goal if career_goal else None,
        "total_recommendations": len(scored_projects),
        "recommendations": scored_projects
    }