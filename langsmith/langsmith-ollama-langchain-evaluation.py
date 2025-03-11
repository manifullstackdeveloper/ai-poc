from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langsmith import traceable
from pydantic import BaseModel, Field
from langsmith import wrappers, Client

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_PROJECT"] = "ollama-test"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Load local model using Ollama
########################################################################################################
llm = Ollama(model="llama2")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################


client = Client()


# For other dataset creation methods, see:
# https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_programmatically
# https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application

# Create inputs and reference outputs
examples = [
  (
      "Which country is Mount Kilimanjaro located in?",
      "Mount Kilimanjaro is located in Tanzania.",
  ),
  (
      "What is Earth's lowest point?",
      "Earth's lowest point is The Dead Sea.",
  ),
]

inputs = [{"question": input_prompt} for input_prompt, _ in examples]
outputs = [{"answer": output_answer} for _, output_answer in examples]

# Programmatically create a dataset in LangSmith
dataset = client.create_dataset(
  dataset_name="Sample dataset-1", description="A sample dataset in LangSmith-1."
)

# Add examples to the dataset
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)

# Define the application logic you want to evaluate inside a target function
# The SDK will automatically send the inputs from the dataset to your target function
def target(inputs: dict) -> dict:
  response = llm.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          { "role": "system", "content": "Answer the following question accurately" },
          { "role": "user", "content": inputs["question"] },
      ],
  )
  return { "response": response.choices[0].message.content.strip() }


# Define instructions for the LLM judge evaluator
instructions = """Evaluate Student Answer against Ground Truth for conceptual similarity and classify true or false: 
- False: No conceptual match and similarity
- True: Most or full conceptual match and similarity
- Key criteria: Concept should match, not exact wording.
"""

# Define output schema for the LLM judge
class Grade(BaseModel):
  score: bool = Field(
      description="Boolean that indicates whether the response is accurate relative to the reference answer"
  )

# Define LLM judge that grades the accuracy of the response relative to reference output
def accuracy(outputs: dict, reference_outputs: dict) -> bool:
  response = llm.beta.chat.completions.parse(
      model="gpt-4o-mini",
      messages=[
          { "role": "system", "content": instructions },
          {
              "role": "user",
              "content": f"""Ground Truth answer: {reference_outputs["answer"]}; 
              Student's Answer: {outputs["response"]}"""
          },
      ],
      response_format=Grade,
  )
  return response.choices[0].message.parsed.score


# After running the evaluation, a link will be provided to view the results in langsmith
experiment_results = client.evaluate(
  target,
  data="Sample dataset-1",
  evaluators=[
      accuracy,
      # can add multiple evaluators here
  ],
  experiment_prefix="first-eval-in-langsmith",
  max_concurrency=2,
)

