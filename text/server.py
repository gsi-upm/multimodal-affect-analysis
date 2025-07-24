import torch
import litserve as ls
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class HuggingFaceLitAPI(ls.LitAPI):
    def setup(self, device):
        # Load the model and tokenizer from Hugging Face Hub
        self.model_name = "roblesadrian/llama-3b-emotion-classifier"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=5)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def decode_request(self, request):
        # Extract text from request
        # This assumes the request payload is of the form: {'text': 'Your input text here'}
        return request["text"]

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.sigmoid(logits)
        return probs

    def encode_response(self, output):
        labels = ['anger', 'fear', 'joy', 'sadness', 'surprise']

        results = {label: float(prob) for label, prob in zip(labels, output[0])}
        return results

if __name__ == "__main__":
    # Create an instance of your API
    api = HuggingFaceLitAPI()
    # Start the server, specifying the port
    server = ls.LitServer(
        HuggingFaceLitAPI(),
        accelerator='cuda' if torch.cuda.is_available() else 'cpu',
        devices=1
    )
    server.run(port=8000)