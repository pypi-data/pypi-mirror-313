## Ask 4x models same question 



#### Target platform, provider and model

The default platform below is `Groq (Free)` using the provider `Meta` and the model `llama3-70b-8192` , 
but you can change these values for all chatbot UIs using these select boxes:

{{render_template("llms/includes/choose-llm.html")}}

#### Chat Bot UI with 3x Board Personas

{{chatbot   name             = "Main Chat bot" 
            initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
            initial_prompt    = "what do you do?"
            system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
            edit_mode        = "false"
            platform         = "Groq (Free)"
            provider         = "Meta"
            model            = "llama3-70b-8192"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-4">
        {{chatbot   name               = "LLaMa3.0 #1"  
                    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
                    initial_prompt    = "what do you do?"
                    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-1" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "LLaMa3.0 #3"  
                    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
                    initial_prompt    = "what do you do?"
                    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-2" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "LLaMa3.0 #3"  
                    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
                    initial_prompt    = "what do you do?"
                    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-3" 
        }}
    </div>
</div>

<script>
    $('#main-wrapper').removeAttr('data-layout');
   $('aside').hide()
</script>
