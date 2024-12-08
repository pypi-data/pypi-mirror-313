## Mistral

Mistral is a small, creative team with high scientific standards. They make open, efficient, helpful and trustworthy AI models through ground-breaking innovations (from their [https://mistral.ai/company/](mistral about page) page).

- [Mistral - Introducing a free API](https://mistral.ai/news/september-24-release/)
- [Mistral - getting started docs](https://docs.mistral.ai/getting-started/models/)
- [Mistral launches a free tier for developers to test its AI models](https://techcrunch.com/2024/09/17/mistral-launches-a-free-tier-for-developers-to-test-its-ai-models/)

Currently, The Cyber Boardroom supports the 3 FREE mistral models:
 
 - **Pixtral** - A 12B model with image understanding capabilities in addition to text. Learn more on this [blog post](https://mistral.ai/news/pixtral-12b/)
 - **Mistral Nemo** - Mistral's best multilingual open source model released July 2024. Learn more on this [blog post](https://mistral.ai/news/mistral-nemo/)
 - **Codestral Mamba** - Mistral's first mamba 2 open source model released July 2024. Learn more on this [blog post](https://mistral.ai/news/codestral-mamba/)

Good examples queries:

- What is the name of your model , who created you and what is your knowledge cut off date?
- What is CyberSecurity?
- How many letters R exist in the word Strawberry?

### Query LLMs 

Below you can ask the same question to the 3 supported Mistral models


{{chatbot   name             = "Pixtral" 
            initial_message  = "Hi, Ask a question to 3x Free Mistral models" 
            initial_prompt   = "What is the name of your model , who created you and what is your knowledge cut off date?"
            edit_mode        = "false"
            platform         = "Mistral (Free)"
            provider         = "Mistral"
            model            = "pixtral-12b-2409"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-6">
        {{chatbot   name               = "Mistral Nemo"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Mistral (Free)"
                    provider           = "Mistral"
                    model              = "open-codestral-mamba"
                    channel            = "shared-llm-nemo" 
        }}
    </div>
    <div class="col-6">
        {{chatbot   name               = "Codestral Mamba"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Mistral (Free)"
                    provider           = "Mistral"
                    model              = "open-codestral-mamba"
                    channel            = "shared-llm-mamba" 
        }}
    </div>
</div>  

