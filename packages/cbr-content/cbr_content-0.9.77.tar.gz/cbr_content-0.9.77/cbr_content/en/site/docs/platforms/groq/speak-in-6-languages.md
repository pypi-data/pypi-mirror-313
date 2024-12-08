## Speak in 6x languages 

Here is an example of sending the same query to 7 different Chat Bots UIs,each with a 
different system prompt:

1. Only reply in English (this is the main Chat Bot)
2. Only reply in Spanish (1st row)
3. Only reply in Portuguese
4. Only reply in French
5. Only reply in German (2nd row)
6. Only reply in Emojis
7. Only reply in Leetspeak

#### Target platform, provider and model

The default platform below is `Groq (Free)` using the provider `Meta` and the model `llama3-70b-8192` , 
but you can change these values for all chatbot UIs using these select boxes:

{{render_template("llms/includes/choose-llm.html")}}

#### Get answers in 7 languages

{{chatbot   name             = "Main Chat bot" 
            initial_message  = "Instructions: Ask a question here and see the answer in multiple LLMs" 
            initial_prompt   = "Hi, in one paragraph explain what is Cyber Security"
            system_prompt    = "Only reply in English"
            edit_mode        = "false"
            platform         = "Groq (Free)"
            provider         = "Meta"
            model            = "llama3-70b-8192"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-4">
        {{chatbot   name               = "in Meta (Spanish)"  
                    system_prompt      = "Only reply in Spanish"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-es" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Meta (Portuguese)"  
                    system_prompt      = "Only reply in Portuguese"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-pt" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Meta (French)"  
                    system_prompt      = "Only reply in French"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-fr" 
        }}
    </div>
</div>  

<div class="row">
    <div class="col-4">
        {{chatbot   name               = "in Meta (German)"  
                    system_prompt      = "Only reply in German"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-jp" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Meta (Emojis)"  
                    system_prompt      = "Only reply in Emojis"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-emj" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "in Meta (Leetspeak)"  
                    system_prompt      = "Only reply in Leetspeak"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-kl" 
        }}
    </div>
</div>  
