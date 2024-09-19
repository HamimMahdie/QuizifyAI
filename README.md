# Gemini-AI-Quizify

This project implements a Quiz Builder using various technologies such as Google Gemini, Vertex AI API, embeddings, Google Service Account, Langchain, PDF loader, and Streamlit. The project is part of the challenges provided by Radical AI, with contributions to specific implementation steps.

## Description

The Quiz Builder generates quizzes from input documents and user-provided topics. It uses machine learning models for text embeddings, with Google's Gemini and Vertex AI API for document processing and quiz generation. The project also includes a Streamlit-based user interface for an interactive and user-friendly experience.

## Tasks

By implementing the script files, the following tasks are covered:

1. **Document Processing**: Utilizing Google Gemini for document processing.
2. **Text Embeddings**: Generating embeddings with Langchain.
3. **Authentication**: Integrating Google Service Account for secure API access.
4. **PDF Ingestion**: Loading documents using a PDF loader.
5. **User Interface**: Building an interface with Streamlit.
6. **Quiz Generation**: Creating quizzes based on user-specified topics.
7. **Answer Explanations**: Providing detailed explanations for quiz answers.
8. **Navigation Controls**: Implementing navigation within the quiz interface.
9. **Error Handling**: Ensuring robust error handling and validation.
10. **Deployment**: Considering packaging and deployment strategies.

## Installation

To set up the Quiz Builder:

1. Clone the repository:
   ```bash
   git clone <repository-url>

2. Navigate to the project directory:

3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
4. Replace Project ID with Unique Project ID from desired AI model (In this model vertex AI Google Gemini was used over google cloud server)
5. Alternatively, use the dockerfile to build and run from docker.
   
## Usage
To run the Quiz Builder:

1. Start the Streamlit application:
   ```bash
    streamlit run <your_script>.py

Replace <your_script> with the name of the Python script you want to run.

Follow the instructions in the Streamlit interface to interact with the Quiz Builder.

## Program Structure

### Embedding Client
![Screenshot 2024-07-22 042511](https://github.com/user-attachments/assets/8cb851a0-184a-4776-a4d1-1ed948a71889)

### Docoment Ingestion
![Ilustration 1](https://github.com/user-attachments/assets/f31f3173-3bd3-4783-8178-7312f7118710)

### Quiz Generation
![Quiz Generator](https://github.com/user-attachments/assets/f0febb5b-edaa-43a0-9bdc-b2fa0e60dfe3)

### Generate Quiz Algorithm
![algorithm](https://github.com/user-attachments/assets/3887aa34-312f-4cf6-8e7c-68b87bcc4b59)

### Screen State Handling
![Screen handeling](https://github.com/user-attachments/assets/ccd57932-b248-489b-b8a0-6680b501c57c)

### Questions Layout
![Tested Questions on Books](https://github.com/user-attachments/assets/3abd2f0e-742c-4056-b5eb-0ba38e462a4e)


## Example of the Program Output

![Quiz Generation 2](https://github.com/user-attachments/assets/06e28797-4804-456e-864b-5963c2b0fb67)


## Contributiions

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure your code follows the project's style and guidelines.


## Acknowledgments

This project is based on [mission-quizify](https://github.com/radicalxdev/mission-quizify), developed by [radicalxdev](https://github.com/radicalxdev). We thank them for providing the foundation for this project.

- [Radical AI](https://www.radicalai.org/) - For providing the challenges and inspiration.
- [Streamlit](https://streamlit.io/) - For the development of the user interface.
- [Google Cloud Platform](https://cloud.google.com/) - For the APIs and services used.
- [Langchain](https://langchain.com/) - For the text embeddings technology.




