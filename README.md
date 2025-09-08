# Content Generation with Multiple AI Agents 🤖✍️

![Project Demo] https://youtu.be/oXCvkkM1ots

A multi-agent content generation system combining a **writer agent**, a **content critic agent**, and an **SEO critic agent** to collaboratively create and improve text content. Powered by **OpenAI GPT** models and orchestrated with the **Autogen** framework. Interactive chat UI built with **Streamlit**.

---

## 🚀 Features

- Multi-agent AI collaboration for content creation and evaluation.
- Custom termination based on quality score thresholds.
- Real-time feedback loop with grammar, clarity, style, and SEO scoring.
- Streamlit chat interface with distinct agent avatars.
- Pydantic schemas ensure structured, validated feedback.
- Async orchestration for efficient, scalable workflows.

---

## 📂 Project Structure
```
root/
├── assets/ # Avatars and images (writer.png, content.png, seo.png)
├── src/ # Python source code
│ ├── app.py # Streamlit frontend
│ ├── agents.py # AI agent logic and orchestration
│ └── schemas.py # Pydantic models for structured feedback
├── .gitignore # Files to ignore in git
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── .env # Environment variables (OpenAI API key)

---

## 🛠️ Technologies Used

- Python 3.12
- [Autogen Framework](https://github.com/microsoft/autogen)
- OpenAI GPT models (o3-mini)
- Streamlit for UI
- Pydantic for data validation
- Asyncio for concurrency handling

---

## ⚡ Quickstart

### Installation

1. Clone the repo:
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

---

## 🛠️ Technologies Used

- Python 3.12
- [Autogen Framework](https://github.com/microsoft/autogen)
- OpenAI GPT models (o3-mini)
- Streamlit for UI
- Pydantic for data validation
- Asyncio for concurrency handling

---

## ⚡ Quickstart

### Installation

1. Clone the repo:
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

---

2. Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate # macOS/Linux
.\venv\Scripts\activate # Windows

---

3. Install dependencies:
pip install -r requirements.txt

---

4. Configure your OpenAI API key in `.env` (create this file if missing):
OPENAI_API_KEY=your_openai_api_key_here

---

5. Confirm the `assets/` folder contains all avatar images.

---

### Running the App
streamlit run src/app.py

---

Browse to http://localhost:8501 to start interacting with the AI agents.

---

## 🧑‍💻 Usage

1. Choose a minimum content quality score threshold to stop generation.
2. Enter a content generation prompt.
3. Observe the writer compose and critics provide feedback iteratively.
4. Continue refining content until termination condition is met.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo and open pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Renar Zamora — Data Scientist / AI Engineer  
[LinkedIn](https://www.linkedin.com/in/renar-arnoldo-zamora-54bb9024/)

---

Made with ❤️ and 🤖 for collaborative AI content creation.