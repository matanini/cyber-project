<p align="center">
<img src="https://i.ibb.co/tKm1VRH/comunication-ltd.png" width="500px">
</p>

# Comunication Ltd

## Description:
This is a simple web application that allows users to register and login.  
The application also allows users to view a list of clients and their details.  
We chose to built this app in a microservices architecture, using **Docker** and **Docker Compose**.  
The frontend is built with [**Streamlit**](https://docs.streamlit.io/), the backend is built with [**FastAPI**](https://fastapi.tiangolo.com/) and the database is built with **SQLite3** with **FastAPI**.  

The system can be operated in two `secure modes`: **High** and **Low**, which can be chosen from the sidebar.  
In the **Low security mode**, the application is vulnerable to **SQL injection** and **stored XSS** attacks.  
You can find examples in the **Vulnerabilities** section below, and in the **Homepage** in the app.  

This project was created as the final project of **Computer Security course at HIT, 2023**.

## Requirements 
- Docker 🐳 

## Installation 
To run this project, you will need to do the following steps: 
1. Clone the repo 
   
```bash 
   git clone https://github.com/matanini/cyber-project 
```
2. Go to the main folder of the project:  
   
```bash
   cd cyber-project/ 
```
3. Run all containers (frontend, backend, db) with docker-compose :
   
```bash
   docker-compose up 
``` 
4. Go to [https://localhost:8000](https://localhost:8000) and enjoy! 🎉

## Vulnerabilities:
In this project we implemented 2 weak points in the system: 
- SQL injection 
- stored XSS

**Make sure to set security mode to low in order to exploit the vulnerabilities.**

### SQL Injection:
1) In page REGISTER -> type in **username** input: 
    ```sql
    1' OR 'a'='a'; drop table 'tokens' --
    ```
2) In page LOGIN -> type in **username** input: 
    ```sql
    a' OR '1'='1'; drop table 'users' --
    ```
3) In page SYSTEM -> type in **city** input:
    ```sql
    w'); drop table 'clients' --
    ```

### Stored XSS:
1) In page SYSTEM -> type in **name**/**city** input:
    ```html
    <script>alert("XSS MUAHAHAHAHA 😈")</script>
    ```
