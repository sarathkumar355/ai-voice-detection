# JanSathi AI - Design Document

## System Overview
JanSathi AI is a web-based, mobile-first application that uses artificial intelligence to assist citizens in accessing government schemes through voice and text interaction.

## Architecture Design
The system follows a layered architecture:
- Frontend layer for user interaction
- Backend layer for request handling
- AI processing layer for language understanding and eligibility logic
- Data layer for government scheme information

## Components

### Frontend
- Mobile-first web interface
- Voice input and text input options
- Displays eligible schemes and guidance steps

### Backend
- API server built using FastAPI or Node.js
- Handles user requests and data processing
- Connects frontend with AI services

### AI Processing Layer
- Language understanding using LLMs
- Eligibility checking using rule-based logic and AI
- Response generation in simple language

### Data Sources
- Government scheme documents and rules
- Structured eligibility criteria database

### Speech Services
- Speech-to-text for voice input
- Text-to-speech for voice output

## Technology Stack
- Frontend: HTML, CSS, JavaScript / React
- Backend: FastAPI or Node.js
- AI: Large Language Models with retrieval-based approach
- Database: SQLite / PostgreSQL
- Hosting: Cloud infrastructure (AWS)

## Design Considerations
- Simplicity for non-technical users
- Scalability for large user base
- Accessibility through voice and local languages
