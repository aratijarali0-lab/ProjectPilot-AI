import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("home");

  // ----------------------------------------------------------
  // PROFILE DATA
  // ----------------------------------------------------------

  const [branches, setBranches] = useState([]);
  const [branch, setBranch] = useState("");

  const [skills, setSkills] = useState([]);
  const [interests, setInterests] = useState([]);
  const [careerGoals, setCareerGoals] = useState([]);

  const [selectedSkills, setSelectedSkills] = useState([]);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [careerGoal, setCareerGoal] = useState("");

  // ----------------------------------------------------------
  // PROJECT DATA
  // ----------------------------------------------------------

  const [recommendations, setRecommendations] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);

  const [roadmap, setRoadmap] = useState([]);
  const [resources, setResources] = useState(null);

  // ----------------------------------------------------------
  // UI STATE
  // ----------------------------------------------------------

  const [loadingProfile, setLoadingProfile] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] =
    useState(false);
  const [loadingRoadmap, setLoadingRoadmap] = useState(false);

  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  // ----------------------------------------------------------
  // ROADMAP PROGRESS
  // ----------------------------------------------------------

  const [completedSteps, setCompletedSteps] = useState({});
  const [expandedStep, setExpandedStep] = useState(0);

  // ----------------------------------------------------------
  // LOAD BRANCHES
  // ----------------------------------------------------------

  useEffect(() => {
    fetchBranches();
  }, []);

  async function fetchBranches() {
    try {
      setError("");

      const response = await fetch(`${API}/branches`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load branches"
        );
      }

      setBranches(data.branches || []);
    } catch (err) {
      setError(
        "Backend connection failed. Start FastAPI on port 8000."
      );
    }
  }

  // ----------------------------------------------------------
  // PROFILE
  // ----------------------------------------------------------

  async function updateProfile(
    currentBranch,
    currentSkills = [],
    currentInterests = []
  ) {
    if (!currentBranch) return;

    try {
      setLoadingProfile(true);
      setError("");

      const response = await fetch(`${API}/profile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          branch: currentBranch,
          skills: currentSkills,
          interests: currentInterests,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to generate profile options"
        );
      }

      setSkills(data.skills || []);
      setInterests(data.interests || []);
      setCareerGoals(data.career_goals || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingProfile(false);
    }
  }

  // ----------------------------------------------------------
  // BRANCH
  // ----------------------------------------------------------

  function handleBranchChange(event) {
    const value = event.target.value;

    setBranch(value);

    setSelectedSkills([]);
    setSelectedInterests([]);
    setCareerGoal("");

    setRecommendations([]);
    setSelectedProject(null);
    setRoadmap([]);
    setResources(null);

    setCompletedSteps({});
    setExpandedStep(0);

    if (value) {
      updateProfile(value);
    } else {
      setSkills([]);
      setInterests([]);
      setCareerGoals([]);
    }
  }

  // ----------------------------------------------------------
  // SKILL
  // ----------------------------------------------------------

  function toggleSkill(skill) {
    const updatedSkills =
      selectedSkills.includes(skill)
        ? selectedSkills.filter(
            (item) => item !== skill
          )
        : [
            ...selectedSkills,
            skill,
          ];

    setSelectedSkills(
      updatedSkills
    );

    // Skills changed, so previous interests/career
    // no longer represent the current profile.
    setSelectedInterests([]);
    setCareerGoal("");
    setRecommendations([]);
    setSelectedProject(null);
    setRoadmap([]);
    setResources(null);

    updateProfile(
      branch,
      updatedSkills,
      []
    );
  }

  // ----------------------------------------------------------
  // INTEREST
  // ----------------------------------------------------------

  function toggleInterest(interest) {
    // One interest at a time.
    const updatedInterests =
      selectedInterests[0] === interest
        ? []
        : [interest];

    setSelectedInterests(
      updatedInterests
    );

    // Career options must be regenerated from the
    // current skills + current interest.
    setCareerGoal("");
    setRecommendations([]);
    setSelectedProject(null);
    setRoadmap([]);
    setResources(null);

    updateProfile(
      branch,
      selectedSkills,
      updatedInterests
    );
  }

  // ----------------------------------------------------------
  // RECOMMENDATIONS
  // ----------------------------------------------------------

  async function findProjects() {
    setError("");

    if (!branch) {
      setError(
        "Please select your engineering branch."
      );
      return;
    }

    if (selectedSkills.length === 0) {
      setError(
        "Select at least one technical skill."
      );
      return;
    }

    if (selectedInterests.length === 0) {
      setError(
        "Select at least one area of interest."
      );
      return;
    }

    if (!careerGoal) {
      setError(
        "Please select your career goal."
      );
      return;
    }

    try {
      setLoadingRecommendations(true);

      const response = await fetch(`${API}/recommend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          branch,
          skills: selectedSkills,
          interests: selectedInterests,
          career_goal: careerGoal,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Recommendation failed"
        );
      }

      setRecommendations(data.recommendations || []);

      setPage("recommendations");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingRecommendations(false);
    }
  }

  // ----------------------------------------------------------
  // PROJECT ROADMAP
  // ----------------------------------------------------------

  async function openProject(project) {
    setSelectedProject(project);

    setRoadmap([]);
    setResources(null);
    setError("");

    setCompletedSteps({});
    setExpandedStep(0);

    setLoadingRoadmap(true);

    try {
      // First use project roadmap if backend recommendation
      // already contains it.
      let finalRoadmap = normalizeRoadmap(
        project.roadmap
      );

      // Then try the dedicated roadmap endpoint.
      try {
        const roadmapResponse = await fetch(
          `${API}/roadmap/${project.id}`
        );

        const roadmapData =
          await roadmapResponse.json();

        if (roadmapResponse.ok) {
          const apiRoadmap = normalizeRoadmap(
            roadmapData.roadmap
          );

          if (apiRoadmap.length > 0) {
            finalRoadmap = apiRoadmap;
          }
        }
      } catch {
        // If roadmap endpoint fails, use project roadmap.
      }

      setRoadmap(finalRoadmap);

      // ------------------------------------------------------
      // RESOURCES
      // ------------------------------------------------------

      try {
        const resourceResponse = await fetch(
          `${API}/resources/${project.id}`
        );

        const resourceData =
          await resourceResponse.json();

        if (resourceResponse.ok) {
          setResources(
            resourceData.resources || null
          );
        } else {
          setResources(
            project.resources || null
          );
        }
      } catch {
        setResources(
          project.resources || null
        );
      }

      setPage("roadmap");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } catch (err) {
      setError(
        err.message ||
          "Unable to load project roadmap."
      );
    } finally {
      setLoadingRoadmap(false);
    }
  }

  // ----------------------------------------------------------
  // NORMALIZE ROADMAP
  // ----------------------------------------------------------

  function normalizeRoadmap(rawRoadmap) {
    if (!Array.isArray(rawRoadmap)) {
      return [];
    }

    return rawRoadmap.map((step, index) => {
      if (typeof step === "string") {
        return {
          id: index,
          title: step,
          description:
            "Complete this stage before moving to the next stage of the project.",
          technologies: [],
          phase: getPhase(index, rawRoadmap.length),
        };
      }

      return {
        id: step.id ?? index,
        title:
          step.title ||
          step.name ||
          step.step ||
          `Project Step ${index + 1}`,
        description:
          step.description ||
          step.details ||
          step.text ||
          "Complete this stage before moving to the next stage.",
        technologies:
          step.technologies ||
          step.tech ||
          step.tools ||
          [],
        phase:
          step.phase ||
          getPhase(index, rawRoadmap.length),
      };
    });
  }

  // ----------------------------------------------------------
  // ROADMAP PHASE
  // ----------------------------------------------------------

  function getPhase(index, total) {
    if (index === 0) return "START";

    if (index === total - 1) {
      return "DEPLOY";
    }

    if (index < Math.ceil(total * 0.25)) {
      return "PLAN";
    }

    if (index < Math.ceil(total * 0.65)) {
      return "BUILD";
    }

    return "TEST";
  }

  // ----------------------------------------------------------
  // ROADMAP PROGRESS
  // ----------------------------------------------------------

  function toggleStep(index) {
    setCompletedSteps((previous) => ({
      ...previous,
      [index]: !previous[index],
    }));

    setExpandedStep(index);
  }

  function isStepCompleted(index) {
    return completedSteps[index] === true;
  }

  const completedCount = roadmap.filter(
    (_, index) => completedSteps[index]
  ).length;

  const progressPercentage =
    roadmap.length > 0
      ? Math.round(
          (completedCount / roadmap.length) * 100
        )
      : 0;

  // ----------------------------------------------------------
  // PROJECT SEARCH
  // ----------------------------------------------------------

  const filteredProjects = useMemo(() => {
    const query = search.toLowerCase().trim();

    if (!query) {
      return recommendations;
    }

    return recommendations.filter((project) => {
      const title =
        project.title?.toLowerCase() || "";

      const description =
        project.description?.toLowerCase() || "";

      const technologies =
        project.technologies
          ?.join(" ")
          ?.toLowerCase() || "";

      return (
        title.includes(query) ||
        description.includes(query) ||
        technologies.includes(query)
      );
    });
  }, [recommendations, search]);

  // ----------------------------------------------------------
  // RESET
  // ----------------------------------------------------------

  function reset() {
    setBranch("");
    setSkills([]);
    setInterests([]);
    setCareerGoals([]);

    setSelectedSkills([]);
    setSelectedInterests([]);
    setCareerGoal("");

    setRecommendations([]);
    setSelectedProject(null);

    setRoadmap([]);
    setResources(null);

    setCompletedSteps({});
    setExpandedStep(0);

    setError("");
    setSearch("");

    setPage("home");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  // ----------------------------------------------------------
  // HOME
  // ----------------------------------------------------------

  function Home() {
    return (
      <main className="home">
        <section className="hero">
          <div className="hero-grid"></div>

          <div className="hero-orb hero-orb-one"></div>
          <div className="hero-orb hero-orb-two"></div>

          <div className="hero-content">
            <div className="hero-badge">
              <span className="live-dot"></span>
              AI-POWERED PROJECT DISCOVERY
            </div>

            <h1>
              Build something
              <br />
              <span>worth building.</span>
            </h1>

            <p className="hero-description">
              ProjectPilot connects your engineering
              branch, technical skills, interests and
              career goals with projects that actually
              fit your journey.
            </p>

            <div className="hero-actions">
              <button
                className="hero-cta"
                onClick={() =>
                  setPage("profile")
                }
              >
                <span>Build My Profile</span>
                <strong>→</strong>
              </button>

              <button
                className="hero-secondary"
                onClick={() =>
                  setPage("profile")
                }
              >
                Explore projects
              </button>
            </div>

            <div className="hero-stats">
              <div className="hero-stat">
                <strong>100+</strong>
                <span>Projects</span>
              </div>

              <div className="stat-divider"></div>

              <div className="hero-stat">
                <strong>AI</strong>
                <span>Matching</span>
              </div>

              <div className="stat-divider"></div>

              <div className="hero-stat">
                <strong>01→∞</strong>
                <span>Build Paths</span>
              </div>
            </div>
          </div>

          <div className="hero-floating-card floating-card-one">
            <span className="mini-icon">✦</span>
            <div>
              <small>SMART MATCH</small>
              <strong>96% Match</strong>
            </div>
          </div>

          <div className="hero-floating-card floating-card-two">
            <span className="mini-check">✓</span>
            <div>
              <small>BUILD PROGRESS</small>
              <strong>8 / 12 Complete</strong>
            </div>
          </div>
        </section>

        <section className="workflow-section">
          <div className="section-header">
            <div>
              <span className="section-label">
                THE PROCESS
              </span>

              <h2>
                From idea
                <br />
                <em>to execution.</em>
              </h2>
            </div>

            <p>
              No random project lists. Your profile
              determines what appears next.
            </p>
          </div>

          <div className="workflow-grid">
            <div className="workflow-card">
              <div className="workflow-number">
                01
              </div>

              <div className="workflow-card-icon">
                <span>◎</span>
              </div>

              <h3>Build your profile</h3>

              <p>
                Select your engineering branch,
                skills and areas that interest you.
              </p>

              <div className="workflow-line"></div>
            </div>

            <div className="workflow-card featured-workflow">
              <div className="workflow-number">
                02
              </div>

              <div className="workflow-card-icon">
                <span>✦</span>
              </div>

              <h3>Find your matches</h3>

              <p>
                ProjectPilot ranks projects based on
                the profile you create.
              </p>

              <div className="workflow-line"></div>
            </div>

            <div className="workflow-card">
              <div className="workflow-number">
                03
              </div>

              <div className="workflow-card-icon">
                <span>↗</span>
              </div>

              <h3>Build step by step</h3>

              <p>
                Open any project and follow its
                dedicated journey from start to deploy.
              </p>

              <div className="workflow-line"></div>
            </div>
          </div>
        </section>

        <section className="feature-strip">
          <div>
            <span>01</span>
            <strong>Personalized</strong>
            <p>Recommendations shaped around you.</p>
          </div>

          <div>
            <span>02</span>
            <strong>Project-specific</strong>
            <p>Every project has its own build plan.</p>
          </div>

          <div>
            <span>03</span>
            <strong>Interactive</strong>
            <p>Track every step as you build.</p>
          </div>

          <div>
            <span>04</span>
            <strong>Practical</strong>
            <p>Resources are available when you need them.</p>
          </div>
        </section>
      </main>
    );
  }

  // ----------------------------------------------------------
  // PROFILE
  // ----------------------------------------------------------

  function Profile() {
    const profileProgress =
      branch && selectedSkills.length > 0
        ? selectedInterests.length > 0
          ? careerGoal
            ? 100
            : 85
          : 55
        : branch
        ? 25
        : 0;

    return (
      <main className="profile-page">
        <section className="profile-hero">
          <div>
            <div className="hero-badge small-badge">
              01 / BUILD YOUR PROFILE
            </div>

            <h1>
              Tell us what
              <br />
              <span>you want to build.</span>
            </h1>

            <p>
              Your answers help us find projects that
              match what you already know and where you
              want to go.
            </p>
          </div>

          <div className="profile-progress-card">
            <div className="progress-ring">
              <svg viewBox="0 0 100 100">
                <circle
                  className="ring-bg"
                  cx="50"
                  cy="50"
                  r="42"
                />

                <circle
                  className="ring-progress"
                  cx="50"
                  cy="50"
                  r="42"
                  style={{
                    strokeDashoffset:
                      264 -
                      (264 * profileProgress) /
                        100,
                  }}
                />
              </svg>

              <strong>{profileProgress}%</strong>
            </div>

            <div>
              <span>PROFILE READY</span>
              <strong>
                {profileProgress === 100
                  ? "Ready to match"
                  : "Keep going"}
              </strong>
            </div>
          </div>
        </section>

        {error && (
          <div className="error-message">
            <span>!</span>
            <div>
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* BRANCH */}

        <section className="profile-section">
          <div className="profile-step-number">
            01
          </div>

          <div className="profile-section-content">
            <div className="section-copy">
              <span>FOUNDATION</span>

              <h2>Engineering branch</h2>

              <p>
                Choose the field you're studying or
                building your career in.
              </p>
            </div>

            <div className="select-wrapper">
              <select
                value={branch}
                onChange={handleBranchChange}
                className="select-control"
              >
                <option value="">
                  Choose your branch
                </option>

                {branches.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>

              <span className="select-arrow">
                ↓
              </span>
            </div>
          </div>
        </section>

        {/* SKILLS */}

        {branch && (
          <section className="profile-section">
            <div className="profile-step-number">
              02
            </div>

            <div className="profile-section-content">
              <div className="section-copy">
                <span>YOUR TOOLKIT</span>

                <h2>Technical skills</h2>

                <p>
                  Choose the skills you already know. You can select multiple skills.
                </p>
              </div>

              {loadingProfile ? (
                <div className="profile-loader">
                  <div className="loader-spinner"></div>
                  <div>
                    <strong>
                      Finding skills for {branch}
                    </strong>
                    <span>
                      Preparing your personalized options
                    </span>
                  </div>
                </div>
              ) : (
                <>
                  <div className="choice-list modern-choice-list">
                    {skills.map((skill) => {
                      const active =
                        selectedSkills.includes(skill);

                      return (
                        <button
                          key={skill}
                          className={
                            active
                              ? "choice-chip active"
                              : "choice-chip"
                          }
                          onClick={() =>
                            toggleSkill(skill)
                          }
                        >
                          <span className="chip-icon">
                            {active ? "✓" : "+"}
                          </span>

                          {skill}
                        </button>
                      );
                    })}
                  </div>

                  <div className="selection-footer">
                    <span>
                      {selectedSkills.length}{" "}
                      {selectedSkills.length === 1
                        ? "skill"
                        : "skills"}{" "}
                      selected
                    </span>

                    {selectedSkills.length > 0 && (
                      <div className="selection-dots">
                        {selectedSkills
                          .slice(0, 5)
                          .map((skill) => (
                            <i key={skill}></i>
                          ))}
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          </section>
        )}

        {/* INTEREST */}

        {selectedSkills.length > 0 && (
          <section className="profile-section">
            <div className="profile-step-number">
              03
            </div>

            <div className="profile-section-content">
              <div className="section-copy">
                <span>WHAT EXCITES YOU</span>

                <h2>Areas of interest</h2>

                <p>
                  Select the areas you would actually
                  enjoy working on.
                </p>
              </div>

              <div className="choice-list modern-choice-list">
                {interests.map((interest) => {
                  const active =
                    selectedInterests.includes(
                      interest
                    );

                  return (
                    <button
                      key={interest}
                      className={
                        active
                          ? "choice-chip interest-chip active"
                          : "choice-chip interest-chip"
                      }
                      onClick={() =>
                        toggleInterest(interest)
                      }
                    >
                      <span className="chip-icon">
                        {active ? "✓" : "+"}
                      </span>

                      {interest}
                    </button>
                  );
                })}
              </div>

              <div className="selection-footer">
                <span>
                  {selectedInterests.length} selected
                </span>
              </div>
            </div>
          </section>
        )}

        {/* CAREER */}

        {selectedInterests.length > 0 && careerGoals.length > 0 && (
          <section className="profile-section">
            <div className="profile-step-number">
              04
            </div>

            <div className="profile-section-content">
              <div className="section-copy">
                <span>WHERE YOU'RE HEADED</span>

                <h2>Career direction</h2>

                <p>
                  Choose the career direction that best matches
                  your selected skills and interest.
                </p>
              </div>

              <div className="select-wrapper">
                <select
                  value={careerGoal}
                  onChange={(event) =>
                    setCareerGoal(
                      event.target.value
                    )
                  }
                  className="select-control"
                >
                  <option value="">
                    Choose your career goal
                  </option>

                  {careerGoals.map((career) => (
                    <option
                      key={career}
                      value={career}
                    >
                      {career}
                    </option>
                  ))}
                </select>

                <span className="select-arrow">
                  ↓
                </span>
              </div>
            </div>
          </section>
        )}

        {/* ACTION */}

        <section className="profile-submit">
          <div>
            <span className="section-label">
              READY?
            </span>

            <h2>
              Your profile is ready.
              <br />
              <em>Find your project.</em>
            </h2>
          </div>

          <div className="profile-actions">
            <button
              className="primary-action large-action"
              disabled={
                !branch ||
                selectedSkills.length === 0 ||
                selectedInterests.length === 0 ||
                !careerGoal ||
                loadingRecommendations
              }
              onClick={findProjects}
            >
              {loadingRecommendations ? (
                <>
                  <span className="button-spinner"></span>
                  Finding your matches...
                </>
              ) : (
                <>
                  Find My Matching Projects
                  <strong>→</strong>
                </>
              )}
            </button>

            <button
              className="ghost-action"
              onClick={reset}
            >
              Reset profile
            </button>
          </div>
        </section>
      </main>
    );
  }

  // ----------------------------------------------------------
  // RECOMMENDATIONS
  // ----------------------------------------------------------

  function Recommendations() {
    return (
      <main className="results-page">
        <section className="results-hero">
          <div className="results-hero-copy">
            <div className="hero-badge small-badge">
              02 / YOUR PROJECT MATCHES
            </div>

            <h1>
              Projects that
              <br />
              <span>fit your path.</span>
            </h1>

            <p>
              These projects are ranked using your
              branch, technical skills, interests and
              career direction.
            </p>
          </div>

          <div className="match-summary">
            <div className="summary-top">
              <span>PROFILE MATCH</span>
              <strong>
                {recommendations.length}
              </strong>
            </div>

            <p>projects discovered</p>

            <div className="summary-bars">
              <i></i>
              <i></i>
              <i></i>
              <i></i>
              <i></i>
            </div>
          </div>
        </section>

        <section className="profile-summary">
          <div className="summary-item">
            <span>BRANCH</span>
            <strong>{branch}</strong>
          </div>

          <div className="summary-item">
            <span>SKILLS</span>
            <strong>
              {selectedSkills.length}
            </strong>
          </div>

          <div className="summary-item">
            <span>INTERESTS</span>
            <strong>
              {selectedInterests.length}
            </strong>
          </div>

          <div className="summary-item career-summary">
            <span>CAREER DIRECTION</span>
            <strong>
              {careerGoal || "Exploring"}
            </strong>
          </div>
        </section>

        {error && (
          <div className="error-message">
            <span>!</span>
            <div>
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        <section className="results-section">
          <div className="results-toolbar">
            <div>
              <span className="section-label">
                YOUR MATCHES
              </span>

              <h2>
                {filteredProjects.length}{" "}
                <small>projects</small>
              </h2>
            </div>

            <div className="toolbar-actions">
              <div className="search-box">
                <span>⌕</span>

                <input
                  placeholder="Search projects, skills..."
                  value={search}
                  onChange={(event) =>
                    setSearch(
                      event.target.value
                    )
                  }
                />
              </div>

              <button
                className="edit-profile-button"
                onClick={() =>
                  setPage("profile")
                }
              >
                ← Edit profile
              </button>
            </div>
          </div>

          {filteredProjects.length === 0 ? (
            <div className="no-projects">
              <div className="no-project-icon">
                ⌕
              </div>

              <h3>No projects found</h3>

              <p>
                Try searching for a different project
                or edit your profile.
              </p>

              <button
                onClick={() => {
                  setSearch("");
                  setPage("profile");
                }}
              >
                Edit my profile →
              </button>
            </div>
          ) : (
            <div className="project-grid">
              {filteredProjects.map(
                (project, index) => {
                  const score = Math.min(
                    100,
                    Math.max(
                      0,
                      Number(
                        project.recommendation_score ||
                          project.score ||
                          0
                      )
                    )
                  );

                  return (
                    <article
                      className="project-card-new"
                      key={
                        project.id ||
                        `${project.title}-${index}`
                      }
                    >
                      <div className="project-card-glow"></div>

                      <div className="project-card-header">
                        <span className="project-index">
                          {String(index + 1).padStart(
                            2,
                            "0"
                          )}
                        </span>

                        <div className="match-badge">
                          <div
                            className="mini-score-ring"
                            style={{
                              "--score":
                                `${score * 3.6}deg`,
                            }}
                          >
                            <span>
                              {score}%
                            </span>
                          </div>

                          <small>MATCH</small>
                        </div>
                      </div>

                      <div className="project-card-content">
                        <div className="project-category">
                          {project.difficulty ||
                            "INTERMEDIATE"}
                        </div>

                        <h3>{project.title}</h3>

                        <p>
                          {project.description}
                        </p>

                        {project.reason && (
                          <div className="match-reason">
                            <span>✦</span>
                            <p>
                              {project.reason}
                            </p>
                          </div>
                        )}

                        <div className="project-tech">
                          {(
                            project.technologies ||
                            []
                          )
                            .slice(0, 5)
                            .map((technology) => (
                              <span
                                key={technology}
                              >
                                {technology}
                              </span>
                            ))}
                        </div>
                      </div>

                      <div className="project-card-footer">
                        <span>
                          <i></i>
                          Project roadmap included
                        </span>

                        <button
                          onClick={() =>
                            openProject(
                              project
                            )
                          }
                        >
                          Explore
                          <strong>→</strong>
                        </button>
                      </div>
                    </article>
                  );
                }
              )}
            </div>
          )}
        </section>
      </main>
    );
  }

  // ----------------------------------------------------------
  // ROADMAP
  // ----------------------------------------------------------

  function Roadmap() {
    if (loadingRoadmap) {
      return (
        <main className="roadmap-loading-page">
          <div className="loading-orbit">
            <span></span>
            <span></span>
            <span></span>
          </div>

          <div className="roadmap-loading-copy">
            <span className="section-label">
              PROJECTPILOT AI
            </span>

            <h2>
              Building your
              <br />
              <em>project journey...</em>
            </h2>

            <p>
              Preparing the roadmap and learning
              resources for this project.
            </p>
          </div>
        </main>
      );
    }

    if (!selectedProject) {
      return null;
    }

    return (
      <main className="roadmap-page-new">
        {error && (
          <div className="error-message">
            <span>!</span>
            <div>
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* PROJECT HEADER */}

        <section className="roadmap-hero">
          <button
            className="back-project-button"
            onClick={() =>
              setPage("recommendations")
            }
          >
            <span>←</span>
            Back to projects
          </button>

          <div className="roadmap-hero-grid">
            <div className="roadmap-project-info">
              <div className="hero-badge small-badge">
                03 / PROJECT BUILD JOURNEY
              </div>

              <div className="roadmap-project-number">
                PROJECT #
                {String(
                  selectedProject.id || "01"
                ).padStart(2, "0")}
              </div>

              <h1>
                {selectedProject.title}
              </h1>

              <p>
                {selectedProject.description}
              </p>

              <div className="roadmap-badges-new">
                <span className="difficulty-badge">
                  <i></i>
                  {selectedProject.difficulty ||
                    "Intermediate"}
                </span>

                {(
                  selectedProject.technologies ||
                  []
                )
                  .slice(0, 6)
                  .map((technology) => (
                    <span key={technology}>
                      {technology}
                    </span>
                  ))}
              </div>
            </div>

            {/* PROGRESS CARD */}

            <div className="roadmap-progress-card">
              <div className="progress-card-header">
                <span>BUILD PROGRESS</span>

                <strong>
                  {progressPercentage}%
                </strong>
              </div>

              <div className="big-progress-ring">
                <svg viewBox="0 0 120 120">
                  <circle
                    cx="60"
                    cy="60"
                    r="51"
                    className="big-ring-bg"
                  />

                  <circle
                    cx="60"
                    cy="60"
                    r="51"
                    className="big-ring-progress"
                    style={{
                      strokeDashoffset:
                        320 -
                        (320 *
                          progressPercentage) /
                          100,
                    }}
                  />
                </svg>

                <div>
                  <strong>
                    {completedCount}
                  </strong>

                  <span>
                    / {roadmap.length}
                  </span>

                  <small>STEPS</small>
                </div>
              </div>

              <div className="progress-card-footer">
                {progressPercentage === 100 ? (
                  <>
                    <span className="success-dot">
                      ✓
                    </span>
                    Project journey complete
                  </>
                ) : (
                  <>
                    <span className="progress-dot"></span>
                    {roadmap.length -
                      completedCount}{" "}
                    steps remaining
                  </>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* ROADMAP BODY */}

        <section className="roadmap-content">
          <div className="roadmap-main-new">
            <div className="roadmap-section-heading">
              <div>
                <span className="section-label">
                  YOUR PROJECT PLAN
                </span>

                <h2>
                  From initial idea
                  <br />
                  <em>to final deployment.</em>
                </h2>
              </div>

              <p>
                Complete each step in order. This
                roadmap is specifically connected to{" "}
                <strong>
                  {selectedProject.title}
                </strong>
                .
              </p>
            </div>

            {roadmap.length === 0 ? (
              <div className="empty-roadmap-new">
                <div className="empty-roadmap-icon">
                  !
                </div>

                <h3>
                  Roadmap unavailable
                </h3>

                <p>
                  This project does not currently
                  contain roadmap steps in the
                  project database.
                </p>

                <button
                  onClick={() =>
                    setPage(
                      "recommendations"
                    )
                  }
                >
                  Back to projects
                </button>
              </div>
            ) : (
              <div className="interactive-timeline">
                {roadmap.map((step, index) => {
                  const completed =
                    isStepCompleted(index);

                  const expanded =
                    expandedStep === index;

                  const isLast =
                    index ===
                    roadmap.length - 1;

                  return (
                    <div
                      className={
                        completed
                          ? "roadmap-step completed"
                          : expanded
                          ? "roadmap-step expanded"
                          : "roadmap-step"
                      }
                      key={
                        step.id ??
                        index
                      }
                    >
                      <div className="step-track">
                        <button
                          className="step-number-button"
                          onClick={() =>
                            toggleStep(index)
                          }
                          aria-label={`Mark step ${
                            index + 1
                          } as complete`}
                        >
                          {completed ? (
                            <span>✓</span>
                          ) : (
                            String(
                              index + 1
                            ).padStart(
                              2,
                              "0"
                            )
                          )}
                        </button>

                        {!isLast && (
                          <div className="step-line">
                            <span
                              style={{
                                height:
                                  completed
                                    ? "100%"
                                    : "0%",
                              }}
                            ></span>
                          </div>
                        )}
                      </div>

                      <div className="step-content">
                        <div className="step-card">
                          <div className="step-card-top">
                            <div>
                              <span className="step-phase">
                                {step.phase ||
                                  "BUILD"}
                              </span>

                              <h3>
                                {step.title}
                              </h3>
                            </div>

                            <button
                              className="expand-step"
                              onClick={() =>
                                setExpandedStep(
                                  expanded
                                    ? null
                                    : index
                                )
                              }
                            >
                              {expanded
                                ? "−"
                                : "+"}
                            </button>
                          </div>

                          <div className="step-short">
                            {step.description}
                          </div>

                          {expanded && (
                            <div className="step-details">
                              <div className="detail-box">
                                <span>
                                  WHAT TO DO
                                </span>

                                <p>
                                  {step.description ||
                                    "Complete this project stage and verify that it works before moving to the next stage."}
                                </p>
                              </div>

                              {step.technologies &&
                                step.technologies
                                  .length >
                                  0 && (
                                  <div className="detail-box">
                                    <span>
                                      TOOLS FOR THIS STEP
                                    </span>

                                    <div className="step-tech-list">
                                      {step.technologies.map(
                                        (
                                          technology
                                        ) => (
                                          <span
                                            key={
                                              technology
                                            }
                                          >
                                            {technology}
                                          </span>
                                        )
                                      )}
                                    </div>
                                  </div>
                                )}

                              <button
                                className={
                                  completed
                                    ? "complete-step-button completed-button"
                                    : "complete-step-button"
                                }
                                onClick={() =>
                                  toggleStep(
                                    index
                                  )
                                }
                              >
                                {completed ? (
                                  <>
                                    <span>
                                      ✓
                                    </span>
                                    Completed
                                  </>
                                ) : (
                                  <>
                                    Mark step
                                    complete
                                    <strong>
                                      →
                                    </strong>
                                  </>
                                )}
                              </button>
                            </div>
                          )}
                        </div>

                        <div className="step-status">
                          {completed ? (
                            <>
                              <span>✓</span>
                              COMPLETE
                            </>
                          ) : expanded ? (
                            <>
                              <span>●</span>
                              IN PROGRESS
                            </>
                          ) : (
                            <>
                              <span>○</span>
                              UPCOMING
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* RESOURCES */}

          <aside className="resource-panel-new">
            <div className="resource-panel-inner">
              <div className="resource-heading-new">
                <span className="section-label">
                  KEEP BUILDING
                </span>

                <h2>
                  Project
                  <br />
                  <em>resources.</em>
                </h2>

                <p>
                  Useful references specifically for
                  this project.
                </p>
              </div>

              {resources ? (
                <div className="resource-links-new">
                  {resources.github && (
                    <ResourceLink
                      href={cleanUrl(
                        resources.github
                      )}
                      icon="⌘"
                      type="CODE"
                      title="GitHub"
                    />
                  )}

                  {resources.research_papers && (
                    <ResourceLink
                      href={cleanUrl(
                        resources.research_papers
                      )}
                      icon="◇"
                      type="RESEARCH"
                      title="Research Papers"
                    />
                  )}

                  {resources.dataset && (
                    <ResourceLink
                      href={cleanUrl(
                        resources.dataset
                      )}
                      icon="▦"
                      type="DATA"
                      title="Dataset"
                    />
                  )}

                  {getVideoTutorials(
                    resources,
                    selectedProject?.title
                  ).length > 0 && (
                    <div className="resource-video-heading">
                      <span className="section-label">
                        VIDEO
                      </span>
                      <strong>Project Tutorials</strong>
                    </div>
                  )}

                  {getVideoTutorials(
                    resources,
                    selectedProject?.title
                  ).map(
                    (
                      tutorial,
                      index
                    ) => (
                      <ResourceLink
                        key={`${tutorial.url}-${index}`}
                        href={tutorial.url}
                        icon="▶"
                        type="VIDEO TUTORIAL"
                        title={
                          tutorial.title ||
                          `Project Video ${index + 1}`
                        }
                      />
                    )
                  )}
                </div>
              ) : (
                <div className="no-resources">
                  <span>◇</span>
                  <p>
                    No external resources are
                    available for this project yet.
                  </p>
                </div>
              )}

              <button
                className="new-project-button-new"
                onClick={() =>
                  setPage(
                    "recommendations"
                  )
                }
              >
                <span>←</span>
                Choose another project
              </button>

              <button
                className="new-project-button-secondary"
                onClick={() =>
                  setPage("profile")
                }
              >
                Build a new profile
                <span>→</span>
              </button>
            </div>
          </aside>
        </section>
      </main>
    );
  }

  // ----------------------------------------------------------
  // RESOURCE LINK
  // ----------------------------------------------------------

  function getVideoTutorials(
    resourceData,
    projectTitle
  ) {
    const videos = [];
    const seen = new Set();

    const addVideo = (
      title,
      url
    ) => {
      const safeUrl = cleanUrl(
        url || ""
      );

      // ONLY YouTube is allowed in Tutorial section.
      if (
        !safeUrl.includes("youtube.com") &&
        !safeUrl.includes("youtu.be")
      ) {
        return;
      }

      if (seen.has(safeUrl)) {
        return;
      }

      seen.add(safeUrl);

      videos.push({
        title:
          title ||
          "Project Video Tutorial",
        url: safeUrl,
      });
    };

    // New backend format.
    if (
      Array.isArray(
        resourceData?.tutorials
      )
    ) {
      resourceData.tutorials.forEach(
        (tutorial) => {
          addVideo(
            tutorial?.title,
            tutorial?.url
          );
        }
      );
    }

    // Legacy format.
    addVideo(
      "Project Video Tutorial",
      resourceData?.tutorial
    );

    // Guaranteed YouTube-only fallback.
    if (
      videos.length === 0 &&
      projectTitle
    ) {
      addVideo(
        "Full Project Video",
        `https://www.youtube.com/results?search_query=${encodeURIComponent(
          `${projectTitle} full project tutorial`
        )}`
      );

      addVideo(
        "Step-by-Step Video",
        `https://www.youtube.com/results?search_query=${encodeURIComponent(
          `${projectTitle} step by step tutorial`
        )}`
      );
    }

    return videos;
  }


function ResourceLink({
    href,
    icon,
    type,
    title,
  }) {
    const safeHref = cleanUrl(href);

    if (!safeHref) return null;

    // Tutorial/resource links marked as video must be YouTube only.
    if (
      type === "VIDEO TUTORIAL" &&
      !(
        safeHref.includes("youtube.com") ||
        safeHref.includes("youtu.be")
      )
    ) {
      return null;
    }

    return (
      <a
        href={safeHref}
        target="_blank"
        rel="noreferrer"
        className="resource-link-new"
      >
        <div className="resource-link-icon">
          {icon}
        </div>

        <div className="resource-link-copy">
          <small>{type}</small>
          <strong>{title}</strong>
        </div>

        <span className="resource-arrow">
          ↗
        </span>
      </a>
    );
  }

  // ----------------------------------------------------------
  // NAVIGATION
  // ----------------------------------------------------------

  return (
    <div className="app">
      <header className="navbar-new">
        <button
          className="brand-new"
          onClick={reset}
        >
          <span className="brand-logo">
            P
          </span>

          <span className="brand-name">
            ProjectPilot
          </span>

          <span className="brand-ai">
            AI
          </span>
        </button>

        <nav className="main-nav">
          <button
            className={
              page === "home"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              setPage("home")
            }
          >
            Home
          </button>

          <button
            className={
              page === "profile"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              setPage("profile")
            }
          >
            Build Profile
          </button>

          <button
            disabled={
              recommendations.length ===
              0
            }
            className={
              page ===
              "recommendations"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              setPage(
                "recommendations"
              )
            }
          >
            Projects
          </button>
        </nav>

        <div className="nav-status">
          <span></span>
          AI MATCHING
        </div>
      </header>

      {page === "home" && <Home />}

      {page === "profile" && <Profile />}

      {page === "recommendations" && (
        <Recommendations />
      )}

      {page === "roadmap" && <Roadmap />}

      <footer className="footer-new">
        <div className="footer-brand">
          <span className="footer-logo">
            P
          </span>

          <div>
            <strong>
              ProjectPilot
              <b> AI</b>
            </strong>

            <span>
              Discover. Build. Grow.
            </span>
          </div>
        </div>

        <div className="footer-center">
          Personalized project discovery
        </div>

        <div className="footer-right">
          PROJECTPILOT © 2026
        </div>
      </footer>
    </div>
  );
}

// ------------------------------------------------------------
// CLEAN RESOURCE URL
// ------------------------------------------------------------

function cleanUrl(value) {
  if (!value || typeof value !== "string") {
    return "";
  }

  let url = value.trim();

  // Handles values accidentally returned as:
  // [https://example.com](https://example.com)
  const markdownMatch = url.match(
    /^\[.*?\]\((.*?)\)$/
  );

  if (markdownMatch) {
    url = markdownMatch[1];
  }

  url = url.replace(/\\&/g, "&");

  if (
    !url.startsWith("http://") &&
    !url.startsWith("https://")
  ) {
    url = `https://${url}`;
  }

  return url;
}

export default App;