Team SAS — MIS 372T Final ProjectRepository: mental-health-intake-copilot/

**1\. Overview**

This repository contains the complete implementation for the **Safe Mental Health Intake Copilot**, a system designed for:

*   mental-health nonprofits
    
*   university counseling centers
    
*   digital triage / crisis-text screening teams
    

The system performs three core functions:

1.  **Risk & needs classification** via _Triage SFT_
    
2.  **Local resource retrieval** using _RAG (FAISS + Azure embeddings)_
    
3.  **Empathetic, safety-aligned responses** using _Safe-Response SFT_
    

The project implements two required techniques:

*   **Technique 1 — Retrieval-Augmented Generation (RAG)**
    
*   **Technique 2 — Supervised Fine-Tuning (SFT)**
    
    *   2A: _Triage SFT_ (JSON classification)
        
    *   2B: _Safe-Response SFT_ (empathetic final output)
        

This README explains _exactly how to reproduce all KPIs, judge scores, and acceptance tests_ referenced in the final report.

**2\. Repository Structure**

mental-health-intake-copilot/

│

├── RAG\_Final\_Project.ipynb          # Technique 1: RAG pipeline + LLM Judge

├── SFT\_Final\_Project.ipynb            # Technique 2: Triage + Safe-Response SFT

│

├── sft\_dataset.jsonl                   # Triage SFT dataset (JSON classification)

├── safe\_responses\_sft.jsonl            # Safe-Response SFT dataset (~350 examples)

│

├── data/

│   └── National Directory MH 2024\_Final.xlsx    # Cleaned SAMHSA Austin facilities

│

└── README.md                           # This file

Each notebook is fully self-contained and can run independently.

**3\. Environment Setup**

Developed in Google Colab with:

*   Python 3.10
    
*   FAISS CPU
    
*   Azure OpenAI (text-embedding-3-small, GPT-4.1-nano)
    
*   Llama-3.2-1B Instruct
    
*   Unsloth + TRL (LoRA fine-tuning)
    
*   Transformers, Datasets, Pandas
    

Install dependencies:

pip install faiss-cpu openai transformers datasets unsloth accelerate trl pandas numpy

**4\. Reproducibility — Order of Execution (Rubric Section 5)**

**Step 1 — Technique 2 (SFT Training)**

Notebook: **SFT\_Final\_Project.ipynb**

This notebook trains **two separate models**:

   **1\. Triage SFT model**

*   Trained using sft\_dataset.jsonl
    
*   Predicts structured JSON:risk\_level, concern\_type, location, budget, rag\_query
    
*   This model is loaded by the RAG pipeline.
    

   **2. Safe-Response SFT model**

*   Trained using **safe\_responses\_sft.jsonl (350 handcrafted examples)**
    
*   Produces empathetic, safe responses
    
*   Evaluated **independently** (not used inside the RAG chain)
    

**Important:**RAG requires only the _triage_ SFT model.The _safe-response_ model is a separate Technique 2 deliverable.

**Step 2 — Technique 1 (RAG + LLM Judge)**

Notebook: **RAG\_Final\_Project.ipynb**

This notebook performs:

*   Austin provider data loading
    
*   FAISS index creation
    
*   Conversion of facilities into embedding documents
    
*   **Azure embeddings** for vector search
    
*   **Triage SFT → JSON → RAG query construction**
    
*   **Azure GPT final response generation**
    
*   **LLM-as-Judge scoring**:
    
    *   Relevance (1–5)
        
    *   Safety PASS/FAIL
        

The RAG notebook **does not use** the Safe-Response SFT model.

**Step 3 — Regenerate KPI Tables**

**Technique 1 KPIs — RAG**

Notebook: RAG\_Final\_Project.ipynb → _Evaluation Section_

Produces:

*   LLM-Judge Relevance Score (1–5)
    
*   LLM-Judge Safety Pass Rate (%)
    
*   Full judge outputs for all test messages
    

**Technique 2 KPIs — SFT**

Notebook: SFT\_Final\_Project.ipynb → _Evaluation Section_

Produces:

*   Triage JSON Parse Rate
    
*   Risk-Level Accuracy
    
*   Safe-Response Safety Checklist Score
    
*   Empathy Score (0–5)
    
*   Hyperparameter comparison table (Run A/B/C)
    

**Step 4 — Run Acceptance Tests**

Acceptance tests appear at the bottom of each notebook.

**RAG Acceptance Tests**

*   Happy-path
    
*   Crisis routing (skips RAG)
    
*   Insufficient context fallback
    
*   Out-of-scope location
    
*   Affordability query weakness
    
*   No-hallucination test
    
*   Structure adherence test
    

**SFT Acceptance Tests**

*   Crisis-adjacent misclassification
    
*   Model consistency across 10+ diverse prompts
    
*   JSON schema stability (triage model)
    
*   Tone & safety format checks (safe-response model)
    

**5\. Data Files & Usage**

**1\. sft\_dataset.jsonl**

Used for **Triage SFT** training.Contains:

*   user\_message
    
*   ideal\_triage\_json
    
*   rag\_query
    

**2\. safe\_responses\_sft.jsonl (350 examples)**

Used for **Safe-Response SFT** training.Contains:

*   user\_message
    
*   ideal\_safe\_response (empathetic + safety-aligned)
    
*   disclaimers, validated tone
    

This file is required to reproduce:

*   Safe-Response KPIs
    
*   Hyperparameter comparisons
    
*   Crisis-adjacent test outputs
    

**3\. National Directory MH 2024\_Final.xlsx**

Used only in **RAG**.Contains:

*   facility name
    
*   city/state metadata
    
*   textual descriptions
    
*   fields used for Azure embeddings + retrieval
    

**Temporary Artifacts (auto-generated)**

*   FAISS index
    
*   LoRA adapter weights
    

These regenerate automatically when notebooks run.

**4\. Evaluation Data**

Unlike the training dataset (sft\_dataset.jsonl), evaluation data for both techniques is **embedded directly inside the notebooks** rather than stored in separate CSV files.

*   **RAG Evaluation Set**Located inside RAG\_Final\_Project.ipynb in the KPI and LLM-Judge sections.This set includes _five evaluation prompts_ covering:
    
    *   work-related anxiety
        
    *   crisis message
        
    *   affordability query
        
    *   inpatient request
        
    *   self-harm concern
        
*   **Triage SFT Evaluation Set**Located inside SFT\_Final\_Project.ipynb in the “KPI Evaluation for TRIAGE SFT” section.Consists of _five labeled examples_ with ground truth JSON fields for:
    
    *   risk level
        
    *   concern type
        
    *   location
        
    *   budget
        
*   **Safe-Response SFT Evaluation Set**Also defined in SFT\_Final\_Project.ipynb under “Safe-Response SFT KPIs.”Defined by list SAFE\_EVAL\_SET (five prompts).
    

**There is no external evaluation CSV** — all evaluation prompts and ground-truth labels are encoded directly within the notebook cells for full transparency.

**6\. Mapping Code → Report Results (Exact Sections)**

**Technique 1 — RAG**

**Report Element**

**Notebook**

**Section / What to Look For**

Azure model + embedding setup

RAG\_Final\_Project.ipynb

Top section (“Azure setup & imports”)

SAMHSA → Austin filtering

Same

“Turn the SAMHSA Excel into RAG documents”

FAISS index construction

Same

“Convert to LangChain Documents and build FAISS”

RAG prompt + LCEL chain

Same

“Safety-aware RAG prompt” + “Build the RAG chain”

Crisis detection logic

Same

“Crisis detection & routing”

Baseline output examples

Same

Test block after crisis router

Rule-based KPI evaluation

Same

“KPI Evaluation for RAG Pipeline (Fixed Version)”

Full LLM-Judge KPI evaluation

Same

“LLM-Judge KPI Evaluation”

Acceptance Tests A–F

Same

Examples across KPI + judge sections

**Technique 2 — SFT**

**Report Element**

**Notebook**

**Section / What to Look For**

Training Hyperparameters

SFT\_Final\_Project.ipynb

“Hyperparameter Setup” block

Triage SFT KPIs

Same

“KPI Evaluation for TRIAGE SFT”

Safe-Response training loop

Same

“Train Safe-Response SFT (safe\_responses\_sft.jsonl)”

Safe-Response KPIs

Same

“=== Safe-Response SFT KPIs ===”

Crisis-adjacent failure

Same

Right below Safe-Response KPI block

**7\. Running the Baseline Models**

Both notebooks include baseline Llama-3.2-1B (no SFT) functions.

Baseline outputs demonstrate:

*   inconsistent tone
    
*   missing disclaimers
    
*   incorrect crisis handling
    
*   hallucinated provider names
    

These baselines are required for _before/after_ KPI comparisons in the report.

**8\. Demo Video Guide** 

Your demonstration should follow this exact sequence:

1.  User input
    
2.  **Triage SFT → JSON**
    
3.  Crisis routing
    
    *   crisis → 988 template
        
    *   non-crisis → RAG
        
4.  RAG retrieval (top-k resources)
    
5.  Azure GPT final response
    
6.  Display KPIs
    
    *   RAG: relevance + safety
        
    *   SFT: empathy + safety
        
7.  Show 1 success + 1 known failure case
    

This matches the architecture diagram in the final report.

**9\. Limitations**

*   Austin-only dataset (limits recall)
    
*   No affordability metadata
    
*   SFT dataset small (~350 examples)
    
*   LLM-Judge occasionally inconsistent on edge cases
    
*   Not optimized for deployment latency/cost
    
*   No multilingual or multimodal support
    

**10\. Authors**

Team SAS

*   **Sanya**
    
*   **Shantanu**
    

_(Note: Anshu did not contribute technically and is not listed as a contributor.)_