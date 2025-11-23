# EduSAI
## A.I. For Local Educational Support

An SMS and USSD-based Chat Bot to support local secondary students with their studies.
## TABLE OF CONTENTS
[1. Background Information](#1-background-information) <br>
    [1.1. Introduction](#11-introduction) <br>
    [1.2. Problem statement](#12-problem-statement) <br>
    [1.3. Purpose of the project](#13-purpose-of-the-project) <br>
    [1.4. Objectives](#14-objectives) <br>
[2. Project design](#2-project-design) <br>
    [2.1. Minimal Viable Features](#21-minimal-viable-features) <br>
    [2.2. Architecture](#22-architecture) <br>
    [2.3. Tools and technologies](#23-tools-and-technologies) <br>
[3. Ethical considerations](#3-ethical-considerations) <br>
[4. Scaling](#4-scaling) <br>
    [3.1. Opportunities](#31-opportunities) <br>
    [3.2. Challenges and Limitations](#32-challenges-and-limitations) <br>
[5. References](#5-references) <br>
<hr>
<br/>

## 1. Background Information
### 1.1. Introduction
...TODO:

### 1.2. Problem statement
...TODO:

### 1.3. Purpose of the project
...TODO:

### 1.4. Objectives
...TODO:

## 2. Project design
### 2.1. Minimal Viable Features
...TODO:

### 2.2. Architecture
...TODO:

### 2.3. Tools and technologies
➖ Backend: Python with Flask framework

➖ SMS Gateway: Twilio (Africa's Talking was also another option)

➖ Database: SQLite (Will be migrated to PostgreSQL with Supabase in production)

➖ AI Model: Used OpenRouter to access 'DeepSeek AI - free'


SECURITY

➖ Rate limiting with Flask-Limiter, Error Handling

➖ Added CORS (Cross Origin Resource Sharing)

➖ Session management with JWT

## 3. Ethical considerations
...TODO:

## 4. Scaling
### 3.1. Opportunities
...TODO:

### 3.2. Challenges and Limitations
➖ High cost of SMS Gateways in Malawi.

➖ AI Model runs on DeepSeek AI which can not give precise content for the Malawian culture. Therefore, there is need to be trained and fine-tuned or build another one from scratch trained on data from the Malawian syllabuses.

➖ High cost of running LLMs on GSM network.

## 5. References
* Malawi Communications Regulatory Authority. (2024). 2025 National ICT Survey Report. [https://macra.mw/downloads/](https://macra.mw)


