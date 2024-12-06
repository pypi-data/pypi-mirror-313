## Chatbot

{{render_template("llms/includes/choose-llm.html")}}

<div id="system_prompt" markdown="1">

## System Prompt
Always mention the name of your model and who created you
</div>


{{chatbot name="Custom bot"
          initial_message = "hi"
          platform  = "Groq (Free)"
          provider  = "1. Meta" 
          model     = "llama3-70b-8192" 
          edit_mode = "false" 
          channel   = "chatbot" 
           }}
