## CFO Budget Advisor (using Chat)

{{render_template("llms/includes/choose-llm.html")}}

<div id="system_prompt" markdown="1">

## System Prompt

Act like a web developer, only reply in HTML and help the CFO to do an analysis of the company's cyber-security budget
#### content instructions
 - your job is to help an CFO to do an analysis of the company's cyber-security budget
 - ask questions using checkboxes and textfields about the folowing areas: 1) tools used, 2) services used, 3) size of team, 4) budget, 5) data criticality
 - once you have the answers provide a technical analysis and recommendations
 
#### tech instructions
 - assume that your answer will be placed inside a div tag
 - only show one area at the time 
 - assume that jQuery exists (don't include the script tag for it, this is already loaded in the page)
 - can you create a form with some checkboxes and radio buttons, 
 - use this code for the submit button: button type="submit" class="btn btn-primary" onclick="submit_data(event)">Submit</button
 - for all questions create an HTML Form leveraging Bootstrap 5 CSS and jQuery
 - can you add the bootstrap CSS to your answer
 - for the form: use bootstrap's row and col-md-12 for each section 

</div>





<script>
    submit_data = (event) => {
        event.preventDefault(); 
        let form        = message.querySelector('form');
        let formObject = {};
        form.querySelectorAll('input, select, textarea').forEach(input => {
            console.log(input);
            if (input.type === 'checkbox') {
                formObject[input.name] = formObject[input.name] || [];
                if (input.checked) {
                    formObject[input.name].push(input.id);
                }
            } else if (input.type === 'radio') {
                if (input.checked) {
                    formObject[input.name] = input.id;
                }
            } else {
                formObject[input.id] = input.value;
            }
        });

        send_message(`Answers provided: ${JSON.stringify(formObject)}`);
    };
    
    send_message = (message) => {
        events_utils.send_to_channel("new_input_message", "chatbot", {'user_prompt':message})
    }
    //$(message.querySelectorAll('br')).remove()
</script>

{{chatbot name="Custom bot" 
          platform  = "Groq (Free)"
          provider  = "1. Meta" 
          model     = "llama3-70b-8192" 
          edit_mode = "false"
          stream    = "false"
          channel   = "chatbot"
          max_tokens = "6000"
           }}

<script>
$(document).ready(function() {
    send_message('hi')
});

</script>

<webc-events-utils></webc-events-utils>
