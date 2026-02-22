# RAG-Based Website Chatbot (Day 1 Progress)

## Project Overview

This project is part of my hackathon submission where I am building a Retrieval-Augmented Generation (RAG) based chatbot. The goal is to create a system that can scrape content from a website and answer user questions strictly based on that website content using Google Gemini.

The main idea is to make the chatbot respond only using retrieved contextual information.



## What I Completed on Day 1

On Day 1, I focused on building the core pipeline of the RAG system. Below is what I implemented:

### 1. Web Scraping
- Scraped textual content from a webpage.
- Cleaned HTML and extracted meaningful text.
- Verified that the content was correctly captured.

### 2. Text Chunking
- Split the large webpage content into smaller chunks.
- This helps in better semantic search and embedding generation.
- Ensured chunks are manageable in size for the LLM.

### 3. Embedding Generation
- Used Gemini embedding model to convert each text chunk into vector representations.
- Verified embedding dimensions and number of chunks.

### 4. Vector Storage and Retrieval
- Stored embeddings using FAISS.
- Implemented similarity search.
- Retrieved top relevant chunks based on user query.

### 5. Gemini Integration
- Connected Gemini API.
- Created a structured RAG prompt.
- Ensured the model answers strictly using retrieved context.
- Successfully generated a grounded response.



## Example Flow

1. User asks a question.
2. Question is converted into embedding.
3. Most relevant chunks are retrieved.
4. Retrieved context is sent to Gemini.
5. Gemini generates an answer using only that context.



## Tech Stack Used

- Python
- Google Gemini API
- FAISS
- BeautifulSoup
- NumPy



## Current Status

Day 1: Core RAG pipeline working successfully.



## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Set Gemini API key as environment variable:
   export GOOGLE_API_KEY="your_api_key"

3. Run the notebook.




# Day 2 Progress – Structured Document-Based RAG

On Day 2, I improved and structured the system further.

Instead of only scraping websites, I added support for PDF documents. This makes the system more flexible.

###  What I Completed on Day 2:

### 1. PDF Processing
- Uploaded a research journal PDF.
- Used PyPDFLoader to extract text.
- Verified number of pages loaded.

### 2. Improved Chunking
- Used RecursiveCharacterTextSplitter.
- Added chunk overlap for better context continuity.
- Generated clean text chunks.

### 3. Updated Embedding Model
- Switched to the latest Gemini embedding model:
  `models/gemini-embedding-001`
- Generated 3072-dimensional embeddings.
- Converted them into NumPy float32 format for FAISS.

### 4. FAISS Vector Index
- Created FAISS IndexFlatL2.
- Stored all document embeddings.
- Implemented top-k semantic retrieval.

### 5. Final RAG Pipeline
- Embedded user query.
- Retrieved top relevant chunks.
- Constructed context.
- Used `models/gemini-2.5-flash` for answer generation.
- Ensured answers are strictly based on retrieved context.

Now the system works for both:
- Website content
- PDF documents

# Tech Stack Used

- Python
- Google Gemini API
- FAISS
- LangChain
- BeautifulSoup
- NumPy


# How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Set Gemini API key:
   export GOOGLE_API_KEY="your_api_key"

3. Run the notebook step by step.



# Current Status

Day 1: Website-based RAG working  
Day 2: PDF-based structured RAG working  







