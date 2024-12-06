## Latest changes

### v0.173.0
  - Major backend features with much better workflow to create backend FastAPI and
    show them in the UI (using Markdown)

### v0.163.1 
 - Added major improvement to the ChatBot UI, where now there is support text wrapping and multiple lines auto expand
   There were also major refactoring done in the ChatBot UI, with improved support to the event driven architecture
 - Added support for: GPT-4o (2024-08-06) on OpenRouter and OpenAI platforms

### v0.163.0
 - Improved multiple documentation pages
 - Added support for new Open Router Perplexity models that are connected Online
    - [Perplexity: Llama 3.1 Sonar 70B Online](https://openrouter.ai/models/perplexity/llama-3.1-sonar-large-128k-online)
    - [Perplexity: Llama 3.1 Sonar 8B Online](https://openrouter.ai/models/perplexity/llama-3.1-sonar-small-128k-online)

#### v0.158.10
 - Added support for new Open Router models 
    - [Llama 3.1 405B Instruct](https://openrouter.ai/models/meta-llama/llama-3.1-405b-instruct)
    - [Llama 3.1 70B Instruct](https://openrouter.ai/models/meta-llama/llama-3.1-70b-instruct)
    - [Llama 3.1 8B Instruct](https://openrouter.ai/models/meta-llama/llama-3.1-8b-instruct)
    - [Qwen 2 7B Instruct](https://openrouter.ai/models/qwen/qwen-2-7b-instruct)
    - [Gemma 2 27B](https://openrouter.ai/models/google/gemma-2-27b-it)
    - [Mistral Nemo](https://openrouter.ai/models/mistralai/mistral-nemo)
    - [Codestral Mamba](https://openrouter.ai/models/mistralai/codestral-mamba)
    - [Dolphin Llama 3 70B](https://openrouter.ai/models/cognitivecomputations/dolphin-llama-3-70b)
    - [Mistral Large](https://openrouter.ai/models/mistralai/mistral-large)

#### v0.158.9
 - Added support for new Groq models: `LLaMA3 Groq 8b Tool` and `LLaMA3 Groq 70b Tool`
 
#### v0.158.8
 - Added support for Open AI's new model [GPT-4o-mini](https://www.linkedin.com/feed/update/urn:li:activity:7219804219246051328)
 - Added API method to download sqlite DB with all static content (i.e. all markdown pages)
 - 
#### v0.156.3
 - Added new MVP tool [Helper - GitHub](docs/personas/github-helper)
 - Added new MVP tool [Topic : Portuguese as a Programming language](docs/personas/portuguese-journalist)

#### v0.156.4
 - Added new MVP tool [Helper - Grammar and Spelling](docs/personas/spelling-grammar-helper)
 - Added support (via OpenRouter) to the paid model [Anthropic: Claude Instant v1](https://openrouter.ai/models/anthropic/claude-instant-1:beta) , 
   cheaper than Claude 3.5
 - Added support (via OpenRouter) to the paid model [Nous: Hermes 2 Theta 8B](https://openrouter.ai/models/nousresearch/hermes-2-theta-llama-3-8b) , 
   claims to support json outputs better