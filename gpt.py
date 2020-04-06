from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import numpy as np
from torch.nn import functional as F

def get_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    return tokenizer, model

def generate_text(seed, tokenizer, model):
    encoded_prompt = tokenizer.encode(seed, add_special_tokens=False, return_tensors="pt")
    model_inputs = prepare_inputs_for_generation(encoded_prompt, pasts=None)
    outputs = model(**model_inputs)
    next_token_logits = outputs[0][:, -1, :]
    next_token_logits = top_k_top_p_filtering(next_token_logits, top_k=1, top_p=0.9, min_tokens_to_keep=3)
    next_token = torch.multinomial(F.softmax(next_token_logits, dim=-1), num_samples=3)[0]
    result = {}
    for token in next_token:
        score = F.softmax(next_token_logits, dim=-1)[0][token].item()
        result[tokenizer.decode([token], clean_up_tokenization_spaces=True)] = score
    for pair in sorted(result.items(), key=lambda x:x[1], reverse=True):
        if pair[0].strip() not in list(string.punctuation)+["for","or"]:
            return jsonify({
                "seed_text": seed,
                "next_token": pair[0],
                "time_taken": time.time() - start_time
            })
    return sorted(result.items(), key=lambda x:x[1], reverse=True)[0][0]

def prepare_inputs_for_generation(input_ids, **kwargs):
    return {"input_ids": input_ids}

def top_k_top_p_filtering(logits, top_k=0, top_p=1.0, filter_value=-float("Inf"), min_tokens_to_keep=1):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (batch size, vocabulary size)
            if top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            if top_p < 1.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
            Make sure we keep at least min_tokens_to_keep per batch example in the output
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    if top_k > 0:
        top_k = min(max(top_k, min_tokens_to_keep), logits.size(-1))  # Safety check
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold (token with 0 are kept)
        sorted_indices_to_remove = cumulative_probs > top_p
        if min_tokens_to_keep > 1:
            # Keep at least min_tokens_to_keep (set to min_tokens_to_keep-1 because we add the first one below)
            sorted_indices_to_remove[..., :min_tokens_to_keep] = 0
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        # scatter sorted tensors to original indexing
        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
        logits[indices_to_remove] = filter_value
    return logits