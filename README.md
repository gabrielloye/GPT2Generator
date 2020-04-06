# GPT2 Text Generator and Spacy Named Entity Recognition

Deployed as a Microservice using Flask to host a Text Generation endpoint and Named Entity Recognition + Rule-based entity matching endpoint

## Models Used

- Text Generation - GPT2 for next token predicted by Transformers

- Named Entity Recognition - Spacys Medium English model + Custom Rules

## Areas for improvement

- Pretrain GPT2 on domain specific corpus to enhance generative abilities
- Using websocket connections to improve latency on generation
- Named Entity Recognition model fine-tuned to domain specific task