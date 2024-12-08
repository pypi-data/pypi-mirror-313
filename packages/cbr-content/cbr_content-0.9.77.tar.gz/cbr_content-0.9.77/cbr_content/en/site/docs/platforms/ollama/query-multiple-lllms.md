## Query multiple LLMs (Ollama) 

In this UI you can ask the same question to the multiple supported Ollama models 



{{chatbot   name             = "Meta (LLaMA3 8b)" 
            initial_message  = "Hi, Ask a question to 5 Ollama LLMs" 
            initial_prompt   = "Hi"
            edit_mode        = "false"
            platform         = "Ollama (Local)"
            provider         = "Meta"
            model            = "llama3"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-6">
        {{chatbot   name               = "Meta (Code LLaMa)"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Ollama (Local)"
                    provider           = "Code LLaMa"
                    model              = "codellama"
                    channel            = "shared-llm-codellama" 
        }}
    </div>
    <div class="col-6">
        {{chatbot   name               = "Mistral"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Ollama (Local)"
                    provider           = "Mistral"
                    model              = "mistral"
                    channel            = "shared-llm-shared" 
        }}
    </div>
</div>  

<div class="row">
    <div class="col-6">
        {{chatbot   name               = "Google (Gemma 7b)"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Ollama (Local)"
                    provider           = "Gemma 7b"
                    model              = "gemma"
                    channel            = "shared-llm-gemma" 
        }}
    </div>
    <div class="col-6">
        {{chatbot   name               = "Microsoft (Phi 3b (Mini))"   
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Ollama (Local)"
                    provider           = "Phi 3b (Mini)"
                    model              = "phi3"
                    channel            = "shared-llm-phi3" 
        }}
    </div> 
</div>  
