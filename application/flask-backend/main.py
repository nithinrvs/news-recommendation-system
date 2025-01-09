from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import PlainTextResponse
import os
import asyncpg
import psycopg2
import pandas as pd
from psycopg2 import OperationalError
from predict import recommend_articles, recommend_news_for_coldstart


app = FastAPI()

# Enable CORS for all origins (you can customize this if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    user_id: str
    favorite_categories: List[str]

class NewsItem(BaseModel):
    news_id: str
    category: str
    subcategory: str
    title: str
    abstract: str
    url: str

# Database connection details
DB_HOST = "localhost"
DB_NAME = "mindnews"
DB_USER = "nithinrvs"  # Replace with your DB user
DB_PASSWORD = "nithinrvs"  # Replace with your DB password
DB_PORT = "5432"

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed {str(e)}")

global_user_id = None

# Login endpoint
@app.post("/login")
def login(login_data: LoginRequest):
    global global_user_id

    username = login_data.username
    password = login_data.password

    global_user_id = username
    print("in login")
    print(global_user_id)

    # Connect to the database
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            # Check if the username exists in the user_id column
            cur.execute("SELECT user_id FROM behaviors WHERE user_id = %s", (username,))
            result = cur.fetchone()

        if result:
            # Assuming password is the same as username for demo purposes
            if username == password:
                return {"message": "Login successful"}
            else:
                raise HTTPException(status_code=400, detail="Invaliddd password")
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        print(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
    finally:
        conn.close()  # Ensure the connection is closed after the query

fav_categories = None
@app.post("/signup")
async def signup(signup_data: SignupRequest):
    global fav_categories
    user_id = signup_data.user_id
    favorite_categories = signup_data.favorite_categories
 
    fav_categories = favorite_categories
    '''
    # Connect to the database
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            # Check if the user_id already exists in the database
            cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            result = cur.fetchone()

            if result:
                raise HTTPException(status_code=400, detail="User already exists")
            
            # Insert the new user into the database
            cur.execute(
                "INSERT INTO users (user_id, favorite_categories) VALUES (%s, %s)",
                (user_id, favorite_categories)
            )
            conn.commit()

            # Fetch the saved user data (user_id and favorite categories)
            cur.execute("SELECT user_id, favorite_categories FROM users WHERE user_id = %s", (user_id,))
            saved_user_data = cur.fetchone()

        # Return the saved user information as a response
        return {
            "message": "User registered successfully",
            "user_id": saved_user_data[0],
            "favorite_categories": saved_user_data[1]
        }

    except Exception as e:
        print(f"Database insert error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()
    '''
    
    if fav_categories:
        return {"message": "Sign up successful"}
    else:
        raise HTTPException(status_code=404, detail="Sign Up not possible")
    
@app.get("/newss",response_model=List[NewsItem])
async def get_new_news():
    print(fav_categories)
    recieved_articles = recommend_news_for_coldstart(fav_categories)
    print("got artciles")
    print(recieved_articles)
    conn = connect_db()

    try:
        news_list = []
        with conn.cursor() as cur:
            # Loop through each news_id in recommendations_for_user
            for news_id in recieved_articles:
                # Fetch news details for each news_id
                query = """
                    SELECT news_id, category, subcategory, title, abstract, url
                    FROM news
                    WHERE news_id = %s;
                """
                print(f"Querying for news_id: {news_id}")
                cur.execute(query, (news_id,))
                news_item = cur.fetchone()
                
                if news_item:
                    # Append the fetched news item to the list
                    news_list.append({
                        "news_id": news_item[0],
                        "category": news_item[1],
                        "subcategory": news_item[2],
                        "title": news_item[3],
                        "abstract": news_item[4] if news_item[4] is not None else " ",
                        "url": news_item[5]
                    })

        return news_list

    except Exception as e:
        print(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()


# News endpoint
@app.get("/news", response_model=List[NewsItem])
async def get_news():
    print("hi") 
    print(global_user_id)

    if not global_user_id:
        raise HTTPException(status_code=401, detail="User not logged in")

    # Use the global_user_id in recommend_articles to get the list of news IDs
    recommendations_for_user = recommend_articles(global_user_id, top_n=50)  # This returns a set of news_ids
    print(recommendations_for_user)

    conn = connect_db()
    try:
        with conn.cursor() as cur:
            # Sample insert query
            insert_query = """
                INSERT INTO predictions (user_id, predicted_articles)
                VALUES (%s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET predicted_articles = EXCLUDED.predicted_articles;
            """
            predicted_articles = list(recommendations_for_user)
            cur.execute(insert_query, (global_user_id, predicted_articles))
            conn.commit()  
            print("Data inserted successfully.")

    except Exception as e:
        print(f"Database insert error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

    # Connect to the database
    conn = connect_db()
    try:
        news_list = []
        with conn.cursor() as cur:
            # Loop through each news_id in recommendations_for_user
            for news_id in recommendations_for_user:
                # Fetch news details for each news_id
                query = """
                    SELECT news_id, category, subcategory, title, abstract, url
                    FROM news
                    WHERE news_id = %s;
                """
                print(f"Querying for news_id: {news_id}")
                cur.execute(query, (news_id,))
                news_item = cur.fetchone()
                
                if news_item:
                    # Append the fetched news item to the list
                    news_list.append({
                        "news_id": news_item[0],
                        "category": news_item[1],
                        "subcategory": news_item[2],
                        "title": news_item[3],
                        "abstract": news_item[4] if news_item[4] is not None else " ",
                        "url": news_item[5]
                    })
        print(news_list)
        return news_list

    except Exception as e:
        print(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()
    
# To run the FastAPI app, use `uvicorn`:
# uvicorn main:app --reload

