# Master Group 63

## Intro

This project is a Flask-based platform for product price trend analysis and sharing. It aims to help users track the historical prices and trends of products from major retailers (such as Coles, Woolworths, JB Hi-Fi), and provides price forecasting. Users can register, log in, upload product price data, browse and analyze price trends, and share product information or trends with other users through the platform. The platform also supports product image uploads, data visualization, and multi-user collaboration.



## Main Features and Design

- **Data Collection & Management**: Supports batch uploading of product price data via CSV files, with automatic storage and management by the system.
- **Price Trend Analysis**: Generates historical price charts and future price forecasts for each product to help users make better purchasing decisions.
- **User Interaction**: Allows user registration, login, and sharing of products and their price trends to facilitate information exchange.
- **Multi-Retailer Support**: Integrates data from multiple retailers such as Coles, Woolworths, and JB Hi-Fi for easy comparison.
- **Extensibility**: Uses the Flask application factory pattern to facilitate future feature expansion and maintenance.

This platform is suitable for consumers and data analysis enthusiasts who want to monitor price changes, compare prices across retailers, and predict future price trends.



## Group Members

| UWA ID   | Student Name      | GitHub User Name                                             |
| -------- | ----------------- | ------------------------------------------------------------ |
| 24141207 | Kai Zheng         | [Kaichao-Zheng](https://github.com/Kaichao-Zheng)            |
| 24074951 | Tony Chu          | [TonyChyu](https://github.com/TonyChyu)                      |
| 24112359 | Chang Liu         | [ChangLiu-doc](https://github.com/ChangLiu-doc)              |
| 24205163 | Kushan Jayasekera | [kushanuwa](https://github.com/kushanuwa)<br/>[kushjayz](https://github.com/kushjayz) |



## Installation

⚠️**Please always work on `yourOwnBranch`, NOT on the `origin/main` branch, which should only be used for merging.**

**How to Run the Application**

1. **Install the required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variable Configuration**
   
   - Ensure there is a `.flaskenv` file in the project root directory, with content like:
     ```
     FLASK_APP=main.py
     FLASK_ENV=development
     FLASK_DEBUG=1
     ```
   - To customize the database path, edit the configuration in `instance/config.py`.
   
3. **Initialize the Database**
   - For first-time setup or after database schema changes, run:
     ```bash
     flask db upgrade
     ```

4. **Start the Application**
   
   - In the project root directory, run:
     ```bash
     flask run
     ```
   - The default access address is [http://127.0.0.1:5000](http://127.0.0.1:5000)
   
5. **Test Account**
   - You can register a test account on the registration page.

⚠️**If you encounter issues, please check dependencies, database configuration, and port usage.**



## How to Run Application Tests

This project includes automated unit tests based on Python's unittest framework, located in `test/unitTests.py`.

1. **Ensure Dependencies Are Installed**
   
   - All required dependencies are listed in `requirements.txt`.
   
2. **Run Test Commands**
   - To run the main test file in the project root directory:
     ```bash
     python -m unittest test/unitTests.py
     ```
     
     If the tests run successfully, you will see output similar to the following in your terminal:
     
     ```bash
     Test module initialized!
     ....
     ----------------------------------------------------------------------
     Ran 4 tests in 0.860s
     
     OK
     ```
     
   - Or to run all tests:
     ```bash
     python -m unittest discover -s test
     ```
   
3. **Test Environment Notes**
   - Tests automatically use the `TestConfig` configuration with an in-memory database, so production data is not affected.
   - Each test case automatically initializes and cleans up the database environment.

**To add more test cases, extend `test/unitTests.py` as needed.**



## Tech Stacks

* HTML
* CSS
* JavaScript
* Bootstrap
* jQuery
* Flask (SSR)
* AJAX (CSR)
* SOLite interfaced to via the SQLAlchemy package

