import pytest
from unittest.mock import MagicMock, patch
import torch

# Assume this imports your API class
from server import HuggingFaceLitAPI

@pytest.fixture
def api():
    # Patch the model and tokenizer before instantiating the API
    with patch('server.AutoTokenizer'), patch('server.AutoModelForSequenceClassification'):
        api = HuggingFaceLitAPI()
        # Manually set up model/tokenizer mocks since .setup() is called on server load
        api.model = MagicMock()
        api.tokenizer = MagicMock()
        return api

def test_decode_request(api):
    request = {"text": "I am happy."}
    text = api.decode_request(request)
    assert text == "I am happy."

def test_predict(api):
    # Mock tokenizer's return
    api.tokenizer.return_value = {'input_ids': torch.tensor([[1, 2, 3]])}
    # Mock model's return (logits)
    mock_logits = torch.tensor([[0.1, 0.2, 0.3, 0.4, 0.5]])
    api.model.return_value = MagicMock(logits=mock_logits)

    # The method may expect a dict of tensors; be sure the structure matches what your model expects
    inputs = {'input_ids': torch.tensor([[1, 2, 3]])}
    with patch.object(api.tokenizer, '__call__', return_value=inputs):
        probs = api.predict("test sentence")
        assert isinstance(probs, torch.Tensor)
        # Should have 1 row and 5 columns (for the 5 emotions)
        assert probs.shape == (1, 5)
        # Value check: sigmoid should be in (0, 1)
        assert torch.all((probs >= 0) & (probs <= 1))

def test_encode_response(api):
    # Provide mock output matching output shape [1, 5]
    probs = torch.tensor([[0.8, 0.1, 0.6, 0.05, 0.3]])
    # Patch the function to not rely on any external variables
    labels = ['anger', 'fear', 'joy', 'sadness', 'surprise']
    results = {label: float(prob) for label, prob in zip(labels, probs[0])}
    # Manually set .encode_response to use the local results computation
    output = api.encode_response.__func__(api, probs)
    assert isinstance(output, dict)
    assert set(output.keys()) == set(labels)
    for val in output.values():
        assert isinstance(val, float)

def test_full_inference_cycle(api):
    # Combine all steps: decode, predict, encode
    input_text = "I feel joy!"
    api.tokenizer.return_value = {'input_ids': torch.tensor([[1,2,3]])}
    mock_logits = torch.tensor([[0.2, 0.1, 3.0, 0.01, 0.7]])
    api.model.return_value = MagicMock(logits=mock_logits)
    with patch.object(api.tokenizer, '__call__', return_value={'input_ids': torch.tensor([[1,2,3]])}):
        text = api.decode_request({"text": input_text})
        probs = api.predict(text)
        output = api.encode_response(probs)
        # 'joy' should have the highest score
        assert output['joy'] == max(output.values())
