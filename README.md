# AI Model Match

AI Model Match is an open-source service that helps product teams release, test, and optimize prompt configurations for AI-powered applications. It transforms the traditionally manual, trial-and-error process into an automated system that continuously identifies the best-performing configurations for each use case.

By organizing AI experimentation into use cases, flows, and steps, AI Model Match allows product teams to rapidly test different strategies, collect real feedback, and deliver AI experiences that continuously improve.

## 🚀 Overview

AI Model Match enables teams to:

- Define **use cases** as product goals, such as providing recommendations, generating content, or planning a trip.
- Create **flows**, representing multiple candidate strategies to achieve each goal.
- Organize flows into **steps**, precise configurations that guide AI behavior at each stage of the interaction.
- Intelligently distribute traffic across flows to maintain consistency while optimizing performance.
- Collect and use feedback from both end users and product teams to automatically improve AI performance.

This system empowers product managers to iterate independently, accelerate release cycles, and minimize risk, while end users benefit from AI interactions that steadily improve.

## 📐 Core Concepts

1. **Use Case**

   - Represents a specific product goal or objective.
   - Defines the scope of experimentation and the metrics for success.

2. **Flow**

   - A candidate configuration or strategy to achieve a use case.
   - Multiple flows can be defined to explore different approaches.

3. **Step**

   - Each flow is composed of steps, with each step defining a precise prompt configuration.
   - Steps allow fine-grained control of AI behavior at each stage of interaction.

4. **Session & Correlation ID**

   - Each user session is tied to a unique correlation ID.
   - Once a flow is selected for a correlation ID, all subsequent steps in that session use the same flow, ensuring predictable and coherent experiences.

5. **Feedback**
   - Ratings (1–5) and optional notes can be submitted for each session.
   - Feedback is aggregated per flow to guide automated flow selection and optimization.

## ⚙️ Rollout Strategy

AI Model Match automates the rollout of flows using a controlled, multi-phase approach:

1. **Warmup**

   - New flows are gradually introduced until they reach a target traffic percentage.

2. **Adaptive**

   - Traffic is automatically shifted toward higher-performing flows based on feedback.
   - Flows that receive positive feedback gain more traffic until one flow converges to 100%.

3. **Escape**
   - Configurable rollback conditions trigger automatic reversion if a flow underperforms (e.g., ≥10 evaluations with an average score < 2/5).
   - Protects user experience while minimizing risks.

## 💡 Benefits

**For Product Managers**

- Accelerates iteration cycles without heavy engineering dependency.
- Provides a data-driven approach to evaluating AI strategies.
- Enables safe experimentation with automated traffic distribution and rollback.

**For End Users**

- Consistent, high-quality AI experiences.
- Interactions improve over time based on real-world feedback.

**Business Value**

- Reduces time and cost of AI experimentation.
- Identifies the best-performing strategies quickly.
- Lowers risk while scaling successful configurations.

## 🛠️ Technical Details

- AI Model Match is implemented as an open-source **microservice**.
- Provides APIs to external systems for runtime prompt configuration.
- Supports fine-grained control over AI interactions through use cases, flows, and steps.
- Correlation IDs ensure consistent execution across multi-step flows.
- Feedback collection APIs enable automated performance evaluation and optimization.
- Can be deployed standalone or integrated with existing production environments.
- Future plans may include a **SaaS version** to abstract deployment and infrastructure management.

## 📈 How It Works

1. Define a **use case** representing a product goal.
2. Create one or more **flows** with structured **steps** for AI behavior.
3. Release the flows and let AI Model Match manage traffic distribution and feedback collection.
4. Monitor performance as the system automatically optimizes flow selection based on real-world data.

## 🎯 Target Audience

- **Product Managers** looking to test AI strategies quickly and independently.
- **Development Teams** integrating AI-driven workflows into their applications.
- **End Users** who benefit from AI interactions that are consistent, coherent, and continuously improving.

## 💻 How to use

### Installation

```bash
pip install ai-model-match
```

### In action

Below is an example of how to use this SDK in your project:

```python
import uuid
from ai_model_match.aimm_client import AIMMClient

# Initialize the client (provide your API base URL and credentials if needed)
client = AIMMClient(base_url="https://your-aimm-server.com", api_key="YOUR_API_KEY")

# Generate a unique correlation ID for the session
correlation_id = uuid.uuid4()

# Pick a prompt configuration for a use case and step
use_case_code = "content_generation"
step_code = "extract_transcript"
picker_response = client.Pick(use_case_code, step_code, correlation_id)
print("Prompt modality:", picker_response.output_message.modality)
print("Prompt configuration:", picker_response.output_message.parameters)

# ... Use the prompt configuration in your AI workflow ...

# After the session, send feedback (score can be a combination of relevance, quality, speed, etc.)
score = 4.5  # Example: weighted average based on your own criteria
comment = "Prompt was relevant and fast, but could be more creative."
feedback_response = client.SendFeedback(correlation_id, score, comment)
print("Feedback submitted:", feedback_response.status)
```

## 🗂️ Internal Documentation: Build & Deploy SDK to PyPI

### Prerequisites

Before building and publishing the SDK, you need to install the required packaging tools.  
**`build`** is used to create distribution archives, and **`twine`** is a utility for securely uploading those archives to PyPI.  
Install both with:

```bash
python3 -m pip install --upgrade build twine
```

And activate the Virtual ENV:

```bash
source venv/bin/activate
```

Once done, you can deactivate it with:

```bash
deactivate
```

Before building and deploy a new version, ensure to run unit tests:

```bash
PYTHONPATH=src pytest
```

### Build & Deploy

To release a new version of the SDK to PyPI, follow these steps:

1. **Update Version**

   - Increment the version number in `pyproject.toml` as appropriate.

2. **Build Distribution**

   ```bash
   python3 -m build
   ```

3. **Verify Build**

   - Check the `dist/` directory for `.tar.gz` and `.whl` files.

4. **Upload to PyPI**

   ```bash
   twine upload dist/*
   ```

5. **Confirm Release**
   - Visit [PyPI](https://pypi.org/project/ai-model-match/) to verify the new version is published.

**Note:** Ensure your PyPI credentials are configured (`~/.pypirc`). For test uploads, use `twine upload --repository testpypi dist/*`.

## 🔗 Contributing

AI Model Match is open-source and welcomes contributions from the community.

- To report bugs or request features, open an **issue**.
- To contribute code or documentation, submit a **pull request**.
- Feedback and suggestions are always appreciated!

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

## 🫶 Support Us

If you find this project useful, please consider supporting us on [**Open Collective**](https://opencollective.com/ai-model-match)
