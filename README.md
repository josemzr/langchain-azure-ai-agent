# Azure AI Foundry Document Chat Assistant

A Proof of Concept (PoC) application that demonstrates how to build a document-based chat interface using Langchain, Chainlit and Azure AI Foundry AI Agent Service. This application allows users to upload documents (PDF, DOCX, TXT) and ask questions about their content using Azure's AI capabilities.

## Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🤖 **AI Agent**: Powered by Azure AI Foundry AI Agent Service
- 🔍 **Vector Search**: Automatic document vectorization and search
- 💬 **Interactive Chat**: Real-time chat interface built with Chainlit
- 🔐 **Secure Authentication**: Uses Azure Managed Identity for secure access

## Architecture

The application follows a simple yet effective architecture:

1. **Document Upload**: Users upload documents through the Chainlit interface
2. **Azure AI Processing**: Files are uploaded to Azure AI and processed into vector embeddings
3. **Agent Creation**: An AI agent is created with access to the vectorized documents
4. **Question Answering**: Users can ask questions, and the agent responds using the uploaded documents as context

## Prerequisites

- Python 3.13 or higher
- Azure subscription with AI Foundry access
- Azure CLI installed and configured (or appropriate authentication method)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd langchain-azure-ai
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

## Configuration

### Required Environment Variables

Set the following environment variables before running the application:

```bash
# Azure AI Foundry Project Endpoint
export PROJECT_ENDPOINT="https://your-project-name.openai.azure.com/"

# Azure AI Model Name (e.g., gpt-4.1)
export MODEL_NAME="gpt-4.1"
```

### How to Get Environment Variables

#### 1. PROJECT_ENDPOINT

1. Go to [Azure AI Foundry](https://ai.azure.com/)
2. Navigate to your project or create a new one
3. In the project overview, find the "Endpoint" under project details
4. Copy the endpoint URL (should end with `.openai.azure.com/`)

#### 2. MODEL_NAME

1. In your Azure AI Foundry project, go to the "Models+Endpoints" section
2. Deploy a model (recommended: `gpt-4.1`)
3. Use the deployment name as your MODEL_NAME

### Authentication Setup

This application uses Azure Managed Identity for authentication. Ensure you have the appropriate permissions:

1. **For local development**: Use Azure CLI login
```bash
az login
```

2. **For production**: Configure Managed Identity on your Azure resource

3. **Required permissions**:
   - `Cognitive Services User` role on the AI Foundry project
   - Access to the deployed model

## Usage

1. Start the application:
```bash
# Directly
chainlit run app.py -w

# Using uv
uv run chainlit run app.py -w
```

2. Open your browser and navigate to `http://localhost:8000`

3. Upload a document using the file upload interface (📎 button or drag-and-drop)

4. Once the document is processed, you can start asking questions about its content

5. The AI agent will respond based on the information in your uploaded documents

## Supported File Types

- **PDF**: Portable Document Format files
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

## Project Structure

```
langchain-azure-ai/
├── app.py              # Main application logic
├── chainlit.md         # Chainlit welcome screen configuration
├── pyproject.toml      # Project dependencies and configuration
├── uv.lock            # Dependency lock file
└── README.md          # This file
```

### Debug Mode

To run in debug mode with verbose logging:

```bash
chainlit run app.py --debug
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues related to:
- Azure AI Foundry: Check [Azure AI documentation](https://docs.microsoft.com/azure/ai-services/)
- Chainlit: Visit [Chainlit documentation](https://docs.chainlit.io/)
- Azure SDK: See [Azure SDK for Python](https://docs.microsoft.com/azure/developer/python/)
# langchain-azure-ai-agent
