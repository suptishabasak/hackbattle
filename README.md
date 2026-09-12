# AI-Powered Risk-Aware Predictive Test Selection

## Track
Dev Tools / AI-ML & Data

## Problem Statement

Large software projects can contain thousands of automated tests. 
Running the entire test suite for every code change makes CI 
pipelines slow and expensive.

Most code changes affect only a small portion of the test suite. 
This project aims to identify and prioritize the tests that are 
most relevant to a code change while safely avoiding unnecessary 
test execution.

## Solution

Our system analyzes code changes, identifies potentially affected 
tests using dependency analysis, and uses historical data and 
machine learning to rank tests according to their risk and 
relevance.

The system also provides confidence scores and explanations for 
test selection. When confidence is low or the change is considered 
high-risk, additional tests can be triggered as a safety mechanism.

### Core Idea

**Predict → Prioritize → Explain → Verify**

## Key Features

- Detect changed files from a GitHub Pull Request
- Analyze code dependencies using Python AST
- Identify potentially affected tests
- Use historical test and CI data for risk scoring
- Rank tests by risk and relevance
- Generate confidence scores
- Explain why a test was selected
- Safely handle low-confidence or high-risk changes
- Measure test reduction and execution-time savings
- Replay historical pull requests for validation
- Provide an interactive Streamlit dashboard

## System Architecture

The system consists of four major components:

### 1. Dependency Graph & Impact Analysis
- Parse the codebase using Python AST
- Build a dependency graph
- Identify tests potentially affected by changed files

### 2. Git/GitHub & Data Collection
- Detect changed files from Git diffs and Pull Requests
- Collect historical Pull Requests
- Collect test results and CI history

### 3. AI/ML, Risk Scoring & Validation
- Rank tests using historical data
- Generate risk and confidence scores
- Apply safety mechanisms for uncertain predictions
- Validate predictions against historical Pull Requests

### 4. Dashboard & Explainability
- Display changed files and affected tests
- Show selected tests and risk scores
- Explain why tests were selected
- Display test reduction and time savings
- Provide historical regression replay

## Technology Stack

- Python
- Python AST
- Git
- GitHub
- Machine Learning
- Streamlit
- Pandas

## Project Structure

```text
project/
│
├── README.md
├── LICENSE
├── dashboard/
├── data/
├── ...