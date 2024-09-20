## **MovieLens Data Analysis with Docker, PostgreSQL, and Python**

### **Overview**

<div style="text-align: justify">

This project simulates a data analysis environment where the dataset is stored in a relational database (<code>PostgreSQL</code>) within one Docker container, and the analytical scripts run in a separate container. The MovieLens dataset is used for the analysis, and queries are performed using both <code>psycopg2</code> (for raw SQL) and <code>SQLAlchemy</code> ORM (for an ORM approach).

</div>

### **Project Structure**

    Docker_App/
    │
    ├── Database/
    │   ├── ml-latest-small/
    │   │   ├── movies.csv
    │   │   └── ratings.csv
    │   │
    │   ├── Dockerfile
    │   └── init.sql
    │
    ├── Analytics/
    │   ├── Dockerfile
    │   ├── requirements.txt 
    │   └── script.py
    │
    └── docker-compose.yml

### **Requirements**

* Docker
* Docker Compose
* Python 3.x
* PostgreSQL
* WSL (if running on Windows) with Ubuntu
* Docker Desktop (with WSL2 backend)

### **Setup process**

**1. Preparation of general structure of project.**

<div style="text-align: justify">

A folder called <code>Docker_App</code> has been created in the system with two subfolders named <code>Database</code> and <code>Analytics</code>.

The ml-latest-small.zip dataset was then downloaded from: https://grouplens.org/datasets/movielens/latest/ and unzipped into the <code>Database/ml-latest-small/</code> directory.

</div>

**2. Creation of the <code>Dockerfile</code> and <code>docker-compose.yaml</code> file.**

A <code>docker-compose.yml</code> file has been created in the <code>Docker_App</code> root directory, that defines two services:

* A PostgreSQL database (<code>db</code> service)
* A Python analytics service (<code>analytics</code> service)

        services:
        db:
            build: ./Database
            container_name: postgres_db
            environment:
                - POSTGRES_USER=postgres
                - POSTGRES_PASSWORD=postgres
                - POSTGRES_DB=movielens_db
            ports:
                - 5432:5432
            volumes:
                - ./Database/ml-latest-small:/mnt/data

        analytics:
            build: ./Analytics
            container_name: analytics_container
            ports:
                - 8888:8888
            depends_on:
                - db
            links:
                - db
            volumes:
                - ./Analytics:/Analytics

<div style="text-align: justify">

A <code>Dockerfile</code> has been created in the <code>Docker_App/Analytics</code> directory for the Python container, where the analytics script will run. The container allows to run an interactive <code>JupyterLab</code> notebook session in the browser:

</div>

    FROM python:3.9

    WORKDIR /Analytics

    COPY requirements.txt requirements.txt

    RUN pip install --no-cache-dir -r requirements.txt

    EXPOSE 8888

    ENTRYPOINT [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser" ]

<div style="text-align: justify">

A <code>Dockerfile</code> has been created in the <code>Docker_App/Database</code> directory for the <code>PostgreSQL</code> database container. The <code>init.sql</code> file defines database schema and data migrations:

</div>

    FROM postgres:16

    ENV POSTGRES_DB=movielens_db
    ENV POSTGRES_USER=postgres
    ENV POSTGRES_PASSWORD=postgres

    COPY init.sql /docker-entrypoint-initdb.d/

**3. Database initialization script.**

<div style="text-align: justify">

In the <code>Docker_App/Database</code> directory <code>init.sql</code> file has been created to define the database schema and load the <code>CSV</code> data into the tables.

</div>

    CREATE TABLE movies (
        movieId INT PRIMARY KEY,
        title TEXT,
        genres TEXT
    );

    CREATE TABLE ratings (
        ratingId SERIAL PRIMARY KEY,
        userId INT,
        movieId INT,
        rating FLOAT,
        timestamp BIGINT
    );

    COPY movies(movieId, title, genres)
    FROM '/mnt/data/movies.csv'
    DELIMITER ',' CSV HEADER;

    COPY ratings(userId, movieId, rating, timestamp)
    FROM '/mnt/data/ratings.csv'
    DELIMITER ',' CSV HEADER;

**4. Python dependencies.**

<div style="text-align: justify">

Inside the <code>Docker_App/Analytics</code> directory the <code>requirements.txt</code> file has been created, listing the required Python packages:

</div>
    
    sqlalchemy
    psycopg2-binary
    pandas
    jupyterlab

**5. Python analytics script.**

<div style="text-align: justify">

In the <code>Docker_App/Analytics</code> directory the <code>script.ipynb</code> file has been created. This script performs the analysis using both <code>psycopg2</code> and <code>SQLAlchemy</code> ORM.

</div>

**6. Building and runninng the Docker containers.**

<div style="text-align: justify">

To build and run Docker containers, the following command was run in the terminal in the <code>Docker_App</code> directory:

</div>

    docker-compose up

### **Analytical Script**

The <code>script.ipynb</code> was written to answer the followng questions:

1. How many movies are in data set ?
2. What is the most common genre of movie?
3. What are top 10 movies with highest rate ?
4. What are 5 most often rating users ?
5. When was done first and last rate included in data set and what was the rated movie tittle?
6. Find all movies released in 1990.

<div style="text-align: justify">

The first step was to check whether the environment configuration was successful. To do this, the <code>psycopg2</code> library was used to connect to the database, and then 6 <code>SQL</code> queries were executed to get the answers to the previously mentioned questions.

</div>

* Database connection:

        import psycopg2

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="movielens_db",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )

* First SQL query:

        # Create a cursor object
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM movies;")
        movie_count = cur.fetchone()[0]
        print(f"Total number of movies: {movie_count}")

    Obtained Answer:

        Total number of movies: 9742

The remaining queries and answers are presented in the <code>script.ipynb</code> file.

<div style="text-align: justify">

To improve the quality of the code, a second approach was proposed, involving the use of the ORM library <code>SQLAlchemy</code>.

</div>

* Dependencies:

        from sqlalchemy import create_engine, func, desc
        from sqlalchemy.orm import declarative_base, sessionmaker, Session
        from sqlalchemy import BigInteger, Column, ForeignKey, Float, Integer, String

* Database connection:

        # DB connection
        DB_URL = "postgresql://postgres:postgres@db:5432/movielens_db"

        Engine = create_engine(url = DB_URL)

        DB_session = sessionmaker(
            autoflush = False,
            autocommit = False,
            bind = Engine
        )

        Base = declarative_base()
        Base.metadata.create_all(bind = Engine)

* Database objects mapping to Python classes:

        # DB object mapping
        class Movie(Base):
            __tablename__ = 'movies'

            movieid = Column(Integer, primary_key = True, autoincrement = True)
            title = Column(String)
            genres = Column(String)

        class Rating(Base):
            __tablename__ = 'ratings'

            ratingid = Column(Integer, primary_key = True, autoincrement = True)
            userid = Column(Integer)
            movieid = Column(Integer, ForeignKey('movies.movieid'))
            rating = Column(Float)
            timestamp = Column(BigInteger)

* Function that returns the answer to the first question:

        def get_movies_count(db : Session):
            return db.query(func.count(Movie.movieid)).scalar()


        movie_count = get_movies_count(db = DB_session())
        print(f"Total number of movies: [{movie_count}]")

    Obtained Answer:

        Total number of movies: [9742]

The remaining queries and answers are presented in the <code>script.ipynb</code> file.