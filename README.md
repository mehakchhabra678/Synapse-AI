\# Synapse-AI



\## Enterprise Agentic Decision Intelligence Engine



Synapse-AI is a multi-agent enterprise decision intelligence system designed to transform business data and organizational knowledge into actionable, risk-aware management recommendations.



The system combines:



\- Multi-agent orchestration

\- Business data analysis

\- Retrieval-Augmented Generation (RAG)

\- Risk assessment

\- Strategy and action generation

\- Human-in-the-loop decision governance

\- LangGraph workflow orchestration

\- Streamlit-based enterprise dashboard



\---



\## 1. Business Problem



Organizations often have business data, operational policies, and management decisions distributed across different systems.



Traditional analytics can identify what happened, but decision-makers still need to determine:



1\. What is changing?

2\. Why does it matter?

3\. What level of business risk does it represent?

4\. What action should management take?

5\. Does the proposed action comply with organizational policies?

6\. Should a human approve, reject, or modify the recommendation?



Synapse-AI addresses this decision gap by combining data-driven analysis with enterprise knowledge and human governance.



\---



\## 2. Solution Overview



The system follows a decision intelligence workflow:



```text

Business Question

&#x20;      |

&#x20;      v

Supervisor Agent

&#x20;      |

&#x20;      +--------------------+

&#x20;      |                    |

&#x20;      v                    v

&#x20;Data Agent             RAG Agent

&#x20;      |                    |

&#x20;      v                    v

&#x20;Business Insights     Policy Evidence

&#x20;      |                    |

&#x20;      +---------+----------+

&#x20;                |

&#x20;                v

&#x20;           Risk Agent

&#x20;                |

&#x20;                v

&#x20;         Strategy Agent

&#x20;                |

&#x20;                v

&#x20;       Human Review Gate

&#x20;                |

&#x20;       +--------+--------+

&#x20;       |        |        |

&#x20;     Accept   Reject   Modify

&#x20;       |

&#x20;       v

&#x20;    Final Decision



3\. Multi-Agent Architecture

Supervisor Agent

The Supervisor Agent determines which specialized agents should participate in answering a business question.

Available agents:

\- DATA\_AGENT

\- RAG\_AGENT

\- RISK\_AGENT

\- STRATEGY\_AGENT

The project currently supports a deterministic development-mode routing mechanism and a Gemini-powered supervisor path for production use.

Data Agent

The Data Agent analyzes uploaded business datasets.

Responsibilities include:

\- Dataset structure analysis

\- Numeric metric identification

\- Descriptive statistics

\- Business trend identification

\- Generation of data-driven insights

The current application primarily supports CSV business datasets.

RAG Agent

The RAG Agent provides enterprise knowledge grounding.

It:

1\. Receives the business question

2\. Generates an embedding

3\. Searches the ChromaDB knowledge base

4\. Retrieves relevant policy content

5\. Returns policy context and source information

The current demonstration uses an enterprise delivery operations policy.

Risk Agent

The Risk Agent evaluates the business insights and determines:

\- Risk score

\- Risk level

\- Risk drivers

\- Recommended management response

Risk levels currently include:

\- LOW

\- MEDIUM

\- HIGH

Strategy Agent

The Strategy Agent converts identified risks into prioritized business actions.

Actions include:

\- Operational investigation

\- Cost and expense review

\- Negative performance investigation

\- Customer/workforce indicator review

\- Continued monitoring

Human-in-the-Loop

Synapse-AI does not make the final business decision autonomously.

The system pauses at a human review checkpoint and allows the decision-maker to:

\- Accept the proposed actions

\- Reject the proposed actions

\- Modify the proposed actions

This provides governance and human accountability before recommendations proceed toward execution.

4\. Retrieval-Augmented Generation

Synapse-AI uses RAG to ground recommendations in enterprise knowledge.

Knowledge Flow

Enterprise Policy

&#x20;      |

&#x20;      v

Document Ingestion

&#x20;      |

&#x20;      v

Text Chunking

&#x20;      |

&#x20;      v

Sentence Transformer Embeddings

&#x20;      |

&#x20;      v

ChromaDB Vector Store

&#x20;      |

&#x20;      v

Semantic Retrieval

&#x20;      |

&#x20;      v

Policy Evidence



Current embedding model:

all-MiniLM-L6-v2



Current vector database:

ChromaDB



5\. Technology Stack

Component	Technology

Programming Language	Python

Agent Orchestration	LangGraph

LLM Integration	Google Gemini

RAG	ChromaDB

Embeddings	Sentence Transformers

Data Analysis	Pandas

Frontend	Streamlit

Environment Management	Python virtual environment

Version Control	Git / GitHub



6\. Project Structure
Synapse-AI/

│

├── app/

│   ├── agents/

│   │   ├── data\_agent.py

│   │   ├── rag\_agent.py

│   │   ├── risk\_agent.py

│   │   ├── strategy\_agent.py

│   │   ├── supervisor\_agent.py

│   │   └── orchestrator.py

│   │

│   ├── data/

│   │   ├── business\_data.csv

│   │   └── documents/

│   │       └── delivery\_policy.txt

│   │

│   ├── graph/

│   │   ├── state.py

│   │   └── workflow.py

│   │

│   ├── rag/

│   │   ├── ingest.py

│   │   └── retriever.py

│   │

│   ├── tools/

│   │   ├── action\_engine.py

│   │   ├── data\_analyzer.py

│   │   ├── decision\_engine.py

│   │   ├── human\_review.py

│   │   └── insight\_engine.py

│   │

│   └── main.py

│

├── frontend/

│   └── app.py

│

├── requirements.txt

├── .gitignore

└── README.md



7\. Running the Application

1\. Clone the repository

git clone https://github.com/mehakchhabra678/Synapse-AI.git

cd Synapse-AI



2\. Create a virtual environment

python -m venv venv



3\. Activate the environment

Windows PowerShell:

.\\venv\\Scripts\\Activate.ps1



4\. Install dependencies

pip install -r requirements.txt



5\. Configure environment variables

Create a .env file in the project root:

APP\_MODE=development

GEMINI\_API\_KEY=your\_api\_key\_here



Never commit the .env file or expose API keys publicly.

6\. Start the Streamlit application

streamlit run frontend/app.py



The application will open in the browser.

8\. Example Business Workflow

A user can upload a business CSV and ask:

Analyze the uploaded dataset, identify the most significant business trends and risk indicators, assess their severity, and recommend prioritized management actions.



Synapse-AI then performs:

Upload Dataset

&#x20;     ↓

Data Analysis

&#x20;     ↓

Business Insights

&#x20;     ↓

Enterprise Policy Retrieval

&#x20;     ↓

Risk Assessment

&#x20;     ↓

Recommended Actions

&#x20;     ↓

Human Review

&#x20;     ↓

Final Decision



9\. Sample Enterprise Knowledge

The demonstration includes:

app/data/documents/delivery\_policy.txt



The policy provides guidance regarding:

\- Late-order thresholds

\- Operational escalation

\- Delivery capacity

\- Route planning

\- Driver availability

\- Warehouse delays

\- Corrective actions

\- Management review

\- Issue documentation

This allows Synapse-AI to combine quantitative business evidence with organizational policy.

10\. Governance and Safety

Human oversight is intentionally incorporated into the decision workflow.

The system separates:

AI-generated recommendation

from

Human-approved business decision

This design helps reduce the risk of blindly executing automated recommendations and provides an explicit governance checkpoint.

Sensitive configuration such as API keys is excluded from version control through .gitignore.

11\. Current Capabilities

The current implementation supports:

\- CSV business dataset analysis

\- Dynamic business metric detection

\- Business insight generation

\- Policy retrieval using RAG

\- Risk scoring

\- Risk classification

\- Recommended action generation

\- Human approval/rejection/modification

\- Streamlit dashboard

\- LangGraph workflow orchestration

\- Gemini-based supervisor integration

12\. Current Limitations

The current demonstration is intentionally focused on enterprise CSV datasets and text-based enterprise policies.

Current limitations include:

\- CSV is the primary business-data upload format

\- Enterprise knowledge is currently demonstrated using text documents

\- The development environment uses deterministic supervisor routing to avoid unnecessary LLM/API calls

\- Generated actions are recommendations and require human validation

\- The current demonstration does not directly execute business actions in external enterprise systems

13\. Future Enhancements

Potential extensions include:

\- Excel, JSON, PDF and DOCX ingestion

\- Additional enterprise knowledge sources

\- More advanced agent collaboration

\- Real-time enterprise data connectors

\- Predictive risk models

\- Automated root-cause analysis

\- Integration with ERP/CRM systems

\- Role-based access control

\- Audit logging

\- Decision history and analytics

\- Production-grade model monitoring

\- Automated action execution with approval controls

14\. Project Objective

Synapse-AI demonstrates how Agentic AI can move beyond simple question answering toward enterprise decision support by combining:

Data + Knowledge + Risk Intelligence + Strategy + Human Governance

The goal is not to replace decision-makers, but to provide them with a structured, evidence-based decision layer that improves the speed, consistency, and transparency of business decision-making.





Then:



\*\*Ctrl + S → close Notepad.\*\*



\### Stop here.



Don't run Git commands yet. Once you've saved `README.md`, tell me \*\*“README done”\*\* and I'll give you the next command to add it to the existing GitHub repository.

