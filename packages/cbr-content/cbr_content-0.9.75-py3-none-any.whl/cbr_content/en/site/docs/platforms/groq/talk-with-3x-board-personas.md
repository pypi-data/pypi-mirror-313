## Talk with 3x Board Personas 

Welcome to the "Talk with 3x Board Personas" simulation, where you can engage with three distinct board member personas simultaneously.
This interactive tool allows you to experience diverse perspectives on cybersecurity topics, offering insights into how different board
members might respond to key issues. 

Whether you're presenting a proposal or seeking feedback, this platform provides a unique opportunity to understand and anticipate 
various boardroom dynamics. Explore the personas—ranging from impatient and action-focused to experienced and sarcastic—and tailor 
your approach to each unique perspective.

#### Board Member #1: No Patience
This board member is focused on efficiency and actionable results, with little tolerance for lengthy explanations or technical jargon. 
They have legal responsibilities within the company but lack cybersecurity expertise, making them impatient with complex details. 
Their primary interest is in receiving concise, high-impact information that translates directly into business actions. 
When engaging with this persona, be prepared to present your points clearly and succinctly, emphasizing immediate outcomes and practical steps.

#### Board Member #2: Hired CISO
With some experience in cybersecurity, this board member played a key role in hiring the Chief Information Security Officer (CISO) 
and serves as a mentor to help align cybersecurity initiatives with business objectives. They understand the nuances of cybersecurity 
challenges and strive to bridge the gap between technical and business perspectives. This persona values strategic thinking and is open 
to discussions that enhance business-oriented approaches to cybersecurity issues. 
Engaging with them requires a balance of technical insight and business acumen.

#### Board Member #3: Jaded and Sarcastic
This persona is characterized by a high level of sarcasm and a jaded attitude toward cybersecurity discussions. They have legal responsibilities
but no direct experience in cybersecurity, often expressing skepticism and cynicism about security initiatives.
Known for their sharp wit and critical remarks, they are particularly disapproving of the board member who hired the CISO.
To navigate interactions with this persona, be prepared for challenging questions and maintain a professional demeanor,
focusing on how cybersecurity efforts contribute to overall business success.

#### Target platform, provider and model

The default platform below is `Groq (Free)` using the provider `Meta` and the model `llama3-70b-8192` , 
but you can change these values for all chatbot UIs using these select boxes:

{{render_template("llms/includes/choose-llm.html")}}

#### Chat Bot UI with 3x Board Personas

{{chatbot   name             = "Main Chat bot" 
            initial_message  = "Hi, Ask a question here and see the answer in multiple LLMs" 
            initial_prompt   = "Hi, I'm the CISO and would like time on the board agenda to discuss the latest cyber security threats"
            edit_mode        = "false"
            platform         = "Groq (Free)"
            provider         = "Meta"
            model            = "llama3-70b-8192"
            channel          = "root-llm"
}}
<div class="row">
    <div class="col-4">
        {{chatbot   name               = "Board Member #1 (no patience)"  
                    system_prompt      = "Act like are a board member that has legal responsibilities for the company | Reply in one paragraph only | no experience in CyberSecurity | you have no patience for technical details and want really actionable data "
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-es" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "Board Member #2 (Hired CISO)"  
                    system_prompt      = "Act like are a board member that has legal responsibilities for the company | Reply in one paragraph only | some experience in CyberSecurity  | you helped to hired the CISO and always try to coach her to be more business oriented"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-pt" 
        }}
    </div>
    <div class="col-4">
        {{chatbot   name               = "Board Member #3 - (Jaded and Sarcastic)"  
                    system_prompt      = "Act like are a board member that has legal responsibilities for the company | Reply in one paragraph only | no experience in CyberSecurity    | you are highly sarcastic, are jaded with CyberSecurity and you really do not like the Board Member who hired the CISO"
                    show_sent_messages = "false"
                    edit_mode          = "false" 
                    platform           = "Groq (Free)"
                    provider           = "Meta"
                    model              = "llama3-70b-8192"
                    channel            = "shared-llm-fr" 
        }}
    </div>
</div>
