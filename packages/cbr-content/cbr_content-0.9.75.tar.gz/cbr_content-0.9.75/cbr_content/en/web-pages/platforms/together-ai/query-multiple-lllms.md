## Together AI : Query multiple LLMs 

At the same time



{{chatbot   name             = "Main Chat bot" 
            initial_message  = "Hi, Ask a question here and see the answer in multiple LLMs" 
            initial_prompt   = "Hi"
            edit_mode        = "false"
            platform         = "Together AI (Paid)"
            provider         = "Meta"
            model            = "meta-llama/Llama-3-70b-chat-hf"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-4">
        {{chatbot   name               = "in Qwen 72B (Spanish)"  
                    system_prompt      = "Only reply in Spanish"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Qwen"
                    model              = "Qwen/Qwen2-72B-Instruct"
                    channel            = "shared-llm-es" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Qwen 110B (Portuguese)"  
                    system_prompt      = "Only reply in Portuguese"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Qwen"
                    model              = "Qwen/Qwen1.5-110B-Chat"
                    channel            = "shared-llm-pt" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Mistral AI 7B (French)"  
                    system_prompt      = "Only reply in French"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Mistral AI"
                    model              = "mistralai/Mistral-7B-Instruct-v0.3"
                    channel            = "shared-llm-fr" 
        }}
    </div>
</div>  

<div class="row">
    <div class="col-4">
        {{chatbot   name               = "in Deepseek AI (Japanese)"  
                    system_prompt      = "Only reply in Japanese"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Deepseek AI"
                    model              = "deepseek-ai/deepseek-llm-67b-chat"
                    channel            = "shared-llm-jp" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Snowflake (Emojis)"  
                    system_prompt      = "Only reply in Emojis"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Snowflake"
                    model              = "Snowflake/snowflake-arctic-instruct"
                    channel            = "shared-llm-emj" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Snowflake (klingon)"  
                    system_prompt      = "Only reply in klingon"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Together AI (Paid)"
                    provider           = "Snowflake"
                    model              = "databricks/dbrx-instruct"
                    channel            = "shared-llm-kl" 
        }}
    </div>
</div>  
