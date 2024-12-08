## Together AI

[Together AI](https://www.together.ai/) is a cloud platform for building and running generative AI. 

You can see the list of Together AI 100x+ in their [models available](https://api.together.ai/models) page, usually hosted at Hugging Face

The Cyber Boardroom has native support for using Together AI serverless models, 
and you can easily integrate them into your workflows. Just set the `TOGETHER_AI_API_KEY` environment variable. 

Here are the models currently wired in the UI (if you want to add more, just let us know):


| **Company**     | **Model**          | **Identifier**                      |
|-----------------|--------------------|-------------------------------------|
| **Meta**        | LLaMA3 70b HF      | meta-llama/Llama-3-70b-chat-hf      |
| **Qwen**        | Qwen2 72B          | Qwen/Qwen2-72B-Instruct             |
| **Qwen**        | Qwen1.5 110B       | Qwen/Qwen1.5-110B-Chat              |
| **Mistral AI**  | Mistral-7B         | mistralai/Mistral-7B-Instruct-v0.3  |
| **Deepseek AI** | Deepseek LLM 67b   | deepseek-ai/deepseek-llm-67b-chat   |
| **Snowflake**   | Arctic Instruct    | Snowflake/snowflake-arctic-instruct |
| **Databricks**  | DBRX Instruct      | databricks/dbrx-instruct            |

----

You can give these models a test drive in the [chat-with-llms](chat-with-llms) page or use one of the chatbots UI below.


<div class="row">
    <div class="col-6"> 
        {{chatbot name="Meta (Llama3)" 
                  initial_message = "Hi, I'm llama-3-70b-chat-hf, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "Meta" 
                  model           = "meta-llama/Llama-3-70b-chat-hf" 
                  edit_mode       = "false" 
                  channel         = "Meta" }}
    </div>
    <div class="col-6"> 
        {{chatbot name="Qwen"  
                  initial_message = "Hi, I'm qwen2-72b-instruct, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "Qwen" 
                  model           = "Qwen/Qwen2-72B-Instruct" 
                  edit_mode       = "false" 
                  channel         = "Qwen" }}
    </div>
</div>
<div class="row">
    <div class="col-6"> 
        {{chatbot name="Mistral AI"  
                  initial_message = "Hi, I'm mistral-7B-Instruct-v0.3, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "Mistral AI" 
                  model           = "mistralai/Mistral-7B-Instruct-v0.3" 
                  edit_mode       = "false" 
                  channel         = "Mistral" }}
    </div>
    <div class="col-6"> 
        {{chatbot name="Deepseek AI"  
                  initial_message = "Hi, I'm deepseek-llm-67b-chat, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "Deepseek AI"
                  model           = "deepseek-ai/deepseek-llm-67b-chat" 
                  edit_mode       = "false" 
                  channel         = "Deepseek" }}
    </div>
</div>
<div class="row">
    <div class="col-6"> 
        {{chatbot name="Snowflake"  
                  initial_message = "Hi, I'm snowflake-arctic-instruct, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "Snowflake" 
                  model           = "snowflake/snowflake-arctic-instruct" 
                  edit_mode       = "false" 
                  channel         = "Snowflake" }}
    </div>
    <div class="col-6"> 
        {{chatbot name="Databricks"  
                  initial_message = "Hi, I'm deepseek-llm-67b-chat, how can I help you?"
                  initial_prompt  = "Hello, who created you and what is your model?"
                  platform        = "Together AI (Paid)"
                  provider        = "DBRX Instruct"
                  model           = "databricks/dbrx-instruct" 
                  edit_mode       = "false" 
                  channel         = "databricks" }}
    </div>
</div>



<style>
    table { width:100%; border:1px solid black  }
    td    { padding:10px}
    th    { padding:10px; background-color: #0a3069 ; color:white}
</style>


