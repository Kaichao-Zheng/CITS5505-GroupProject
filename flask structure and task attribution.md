# Project Development Task Breakdown – Price Prediction Website
## Phase 1: Setup & Environment Configuration
- Initialize Flask project structure.
- Create `.env` file and load environment variables securely.
- Setup private GitHub repository and add a basic README.
## Phase 2: User System & Database Design
- Implement user registration/login system with password hashing and role selection (merchant/consumer).
- Design database schema using SQLAlchemy: `users`, `products`, `price_data`, `shared_data`.
- Setup access control based on user roles.
## Phase 3: Server-side Rendering (SSR) Pages
- Develop intro page with project introduction and login/register options.
- Develop basic product search page (returns first 10 matches using SSR).
- Setup initial price chart visualisation template using server-rendered data.
## Phase 4: CSV Upload & Data Management
- Implement merchant CSV upload interface with validation and preview.
- Parse and validate CSV (product ID, date, price).
- Insert validated data into database.
- Allow merchants to manage (update/delete) their uploaded data.
## Phase 5: Price Prediction Module (Analysis)
- Retrieve historical price data for a selected product.
- Implement basic prediction model (e.g., linear regression or moving average).
- Return predictions via Flask API in JSON format.
- Support predictions for multiple ranges (e.g., next 7/30 days).
## Phase 6: Client-side Rendering (CSR) & AJAX
- Implement AJAX-based dynamic product loading (e.g., ‘Load More’).
- Use Chart.js or similar to fetch and display chart data asynchronously.
- Implement interactive data sharing (via POST + modal confirmations).
## Phase 7: Data Sharing & Access Control
- Allow users to share specific chart data with other users.
- Setup proper access control so only permitted users can view shared charts.
- Allow cancellation or revocation of previously shared data.
## Phase 8: Testing & Finalization
- Write unit tests for backend logic and data analysis.
- Perform full walkthrough testing of all user workflows.
- Finalize README with project purpose, member list, setup & test instructions.

# One possible Flask structure:
price_predictor/  
│  
├── app/                        # Main application package  
│   ├── __init__.py             # App factory and blueprint registration  
│   ├── models.py               # SQLAlchemy models (User, Product, Price, Share)  
│   ├── forms.py                # Flask-WTF forms (login, register, upload)  
│   ├── utils.py                # Utility functions (e.g., prediction models)  
│   ├── routes/                 # Modular route blueprints  
│   │   ├── auth.py             # Authentication routes (login, register)  
│   │   ├── upload.py           # Data upload and management  
│   │   ├── visualise.py        # Data visualisation and prediction  
│   │   ├── share.py            # Data sharing logic  
│  
├── static/                    # Static files (JS, CSS, icons)  
│   ├── css/  
│   ├── js/  
│  
├── templates/                 # HTML templates (Jinja2)  
│   ├── layout.html            # Base layout template  
│   ├── intro.html             # Homepage  
│   ├── login.html             # Login form  
│   ├── register.html          # Registration form  
│   ├── upload.html            # Upload page for merchants  
│   ├── visualise.html         # Visualisation page with chart  
│   ├── share.html             # Sharing interface  
│  
├── instance/                  # Configuration files and secrets  
│   ├── config.py  
│  
├── migrations/                # (Optional) Flask-Migrate folder  
│  
├── tests/                     # Unit tests folder  
│  
├── run.py                     # Application entry point  
├── requirements.txt           # Project dependencies  
└── README.md

# Here’s a possible task distribution plan for a team of 4 like us:
## Member A – Backend Core & Database Management
- Set up Flask project structure and `.env` configuration.
- Define SQLAlchemy models: User, Product, Price, Share.
- Implement user registration/login with role-based access.
- Develop upload and share-related backend APIs.
## Member B – Prediction Algorithms & Backend API
- Choose and implement price forecasting models (e.g., moving average, linear regression).
- Build reusable prediction functions and expose them via Flask APIs.
- Format output for frontend (JSON).
- Support forecast range options (e.g., 7/30 days).
- Write unit tests for prediction logic.
## Member C – Frontend Structure & User Interaction
- Build static and SSR pages using Jinja2 templates.
- Design and implement form submissions (login, register, upload).
- Use AJAX to fetch and render product/forecast data.
- Integrate Chart.js for dynamic and interactive graphs.
- Implement user-friendly feedback and error handling.
##Member D – UI Styling, Visualisation & Documentation
- Style pages using TailwindCSS or Bootstrap.
- Enhance chart visual quality (legends, tooltips, colors).
- Manage the share view UI and modal dialogs.
- Write and maintain README.md including member list, setup instructions, and testing steps.
- Coordinate final testing and project delivery.
