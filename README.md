# Master Group 63

## Intro

This `README.md` will be replaced by another `README.md` to explain the project, as required by the project specification.

⚠️**Please always work on `yourOwnBranch`, NOT on the `origin/main` branch, which should only be used for merging.**

## Schedule

| Progress | Week        | Event                | Note                                                         |
| -------- | ----------- | -------------------- | ------------------------------------------------------------ |
|          | Week 6      | Project Release      |                                                              |
|          | Week 7      | First Meeting        | at 3pm, on 08 April                                          |
|          | Week 8      |                      |                                                              |
|          | Study Break | Second Meeting       | at 11am, on 22 April                                         |
|          | Week 9      | GUI Presentation     | [at 2:05pm, on 1st May, in MATH 123B](https://uniwa-my.sharepoint.com/:x:/g/personal/00112652_uwa_edu_au/EQXmSIthQ1FMjJQ1KADV7tUBN0DVQKh_OwTA4efE24TfrQ?e=vjnEQB) |
| ⌛        | Week 10     | Feature Presentation | [at 2:05pm, on 8st May, in MATH 123B](https://uniwa-my.sharepoint.com/:x:/g/personal/00112652_uwa_edu_au/EQXmSIthQ1FMjJQ1KADV7tUBN0DVQKh_OwTA4efE24TfrQ?e=vjnEQB) |
|          | Week 11     | Project Submission   | [at 11:59pm, on 16 May](https://lms.uwa.edu.au/webapps/blackboard/content/listContent.jsp?course_id=_101669_1&content_id=_4251653_1&mode=reset) |
|          | Week 12     | Group Presentation   |                                                              |

## Installation
Install the required dependency

```bash
pip install -r requirements.txt
```

Update `requirements.txt` file after new dependency is added

```bash
pip freeze > requirements.txt
```

## Create Test Database

💬**SQLite Viewer** is a light-weight GUI Extension in VSCode

**Dependency**

```bash
pip install flask
pip install flask_sqlalchemy
pip install python-dotenv
```

Run Flask Shell in terminal

```bash
flask shell
```

Create a new SQLite database at `instance/site.db`

```bash
>>> db.create_all()
```

Insert the first row in user table

```bash
>>> u = User(id='1', employee_id='001', merchant_id='001', user_type='Merchant', username='kai', email='CITS5505@student.uwa', password_hash='asdfghjkl')
>>> db.session.add(u)
>>> db.session.commit()
```

Query: `SELECT * FROM user;`

```bash
>>> query = sa.select(User)
>>> users = db.session.scalars(query).all()
>>> Users
[<User 1>]
```

```bash
>>> users[0].username
'kai'
```

Delete the user `where id='1'`

```bash
>>> user = User.query.get(1)
>>> db.session.delete(user)
>>> db.session.commit()
```

## High-Priority Tasks

- [x] Convert hardcoded HTML into Jinja blocks
- [ ] Design **JavaScript** to interact backend routes defined by `@app.route()` or `@api_bp.route()`
- [ ] To be continued

## Known Challenges

- [ ] Dynamic CSR in search result
- [ ] Line chart visualization
- [ ] Price prediction and visualization
- [ ] Reuse search functionality in "share user selection"
- [ ] [Optional] Real-time fuzzy search

## Tech Stacks

* HTML
* CSS + Bootstrap
* JavaScript + jQuery
* Flask (SSR)
* AJAX (CSR)
* SQL-Alchemy (ORM for application-database interaction)

## Group Members

| UWA ID   | Student Name      | GitHub User Name                                             |
| -------- | ----------------- | ------------------------------------------------------------ |
| 24141207 | Kai Zheng         | [Kaichao-Zheng](https://github.com/Kaichao-Zheng)            |
| 24074951 | Tony Chu          | [TonyChyu](https://github.com/TonyChyu)                      |
| 24112359 | Chang Liu         | [ChangLiu-doc](https://github.com/ChangLiu-doc)              |
| 24205163 | Kushan Jayasekera | [kushanuwa](https://github.com/kushanuwa)<br />[kushjayz](https://github.com/kushjayz) |
