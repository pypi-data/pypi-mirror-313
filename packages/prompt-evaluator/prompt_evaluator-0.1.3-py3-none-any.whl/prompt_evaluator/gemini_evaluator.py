import google.generativeai as genai
import tiktoken

EVALUATION_CRITERIA = {
    "clarity": "How clear and unambiguous is the prompt?",
    "specificity": "Does the prompt specify what is expected in the output?",
    "relevance": "Is the prompt directly related to the intended task?",
    "completeness": "Does the prompt provide all necessary context for the task?",
    "neutrality": "Is the prompt free from bias or leading language?",
    "efficiency": "Is the prompt concise and free of unnecessary verbosity?",
}

class GeminiPromptEvaluator:
    def __init__(self, google_api_key):
        # Initialize the Google Gemini client with the provided API key
        genai.configure(api_key=google_api_key)
        #self.client = google_chat.ChatClient(api_key=google_api_key)
        self.client = genai.GenerativeModel("gemini-1.5-flash")

    def query_model(self, prompt, criterion, question):
        evaluation_question = (
            f"On a scale of 1 to 5, evaluate the following prompt based on {criterion}:\n\n"
            f"Prompt: {prompt}\n\n"
            f"Question: {question}\n\n"
            f"Provide only the numeric score (1-5) and a brief explanation."
        )

        response = self.client.generate_content(evaluation_question)

        # Extract the relevant message from the response
        return response.text

    def evaluate_prompt(self, prompt: str):
        final_response = []
        for criterion, question in EVALUATION_CRITERIA.items():
            response = self.query_model(prompt, criterion, question)
            final_response.append(response)
        return final_response

    def token_length(self, prompt: str, model: str = "gemini-1.5-flash") -> int:
        try:
            # Load the tokenizer for the specified model
            tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fall back to a generic tokenizer if the model is unknown
            tokenizer = tiktoken.get_encoding("cl100k_base")

        # Tokenize the prompt and calculate the token count
        tokens = tokenizer.encode(prompt)
        return len(tokens)

