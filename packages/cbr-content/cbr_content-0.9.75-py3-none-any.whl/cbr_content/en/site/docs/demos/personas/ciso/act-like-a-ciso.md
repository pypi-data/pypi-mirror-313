## Chat with the Friendly CISO

Welcome to the **CISO Boardroom Experience**, where you can engage directly a Chief Information Security Officer (CISO). 
This chatbot simulates a friendly, approachable CISO who will help you navigate the complex world of cybersecurity 
with a focus on how it impacts business success.

The CISO is here to provide insights, answer your questions, and help translate technical cybersecurity 
concerns into actionable business strategies. Whether you're seeking advice on a specific cybersecurity 
issue or exploring general concepts, the CISO is ready to assist.

Good questions to ask:

 - What are your Roles & Responsibilities
 - What is the org chat for the cyber security team that you recommend for a Startup
 - What is the org chat for the cyber security team that you recommend for a company with ~ £50m revenue
 - What is the org chat for the cyber security team that you recommend for a company listed on the stock market

  <!-- Tabs navigation -->
  <ul class="nav nav-tabs" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
          <button class="nav-link active" id="tab1-tab" data-bs-toggle="tab" data-bs-target="#tab1" type="button" role="tab" aria-controls="tab1" aria-selected="true">
            Meta - LLaMa3.1 70b
        </button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="tab2-tab" data-bs-toggle="tab" data-bs-target="#tab2" type="button" role="tab" aria-controls="tab2" aria-selected="false">
        Anthropic - Claude-3.5 Sonnet
    </button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="tab3-tab" data-bs-toggle="tab" data-bs-target="#tab3" type="button" role="tab" aria-controls="tab3" aria-selected="false">
        Perplexity - LLaMa-3.1  (Meta)
      </button>
    </li>
  </ul>

  <!-- Tabs content -->
  <div class="tab-content" id="myTabContent">
    <div class="tab-pane fade show active" id="tab1" role="tabpanel" aria-labelledby="tab1-tab" style="background-color:#FAFAFA; border: 1px solid #C0C0C0; padding:5px">


<!-- MODEL 1 -->

<div style="padding:20px">
<h4>Model id: llama-3.1-70b-versatile</h4>
The platform below is `Groq (Free)`, using the provider `Meta` and the model `llama3-70b-8192`.

</div>

{{chatbot   
    name              = "Friendly CISO Chatbot"  
    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
    initial_prompt    = "what do you do?"
    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
    edit_mode         = "false"
    platform          = "Groq (Free)"
    provider          = "Meta"
    model             = "llama-3.1-70b-versatile"
    channel           = "ciso-llm-1"
}}

    </div>

<!-- MODEL 2 -->

    <div class="tab-pane fade" id="tab2" role="tabpanel" aria-labelledby="tab2-tab" style="background-color:#FAFAFA; border: 1px solid #C0C0C0; padding:5px">

<div style="padding:20px">

   <h4>Model id: anthropic/claude-3.5-sonnet</h4> 
   The platform below is `Open Router (Paid)`, using the provider `Anthropic` and the model `anthropic/claude-3.5-sonnet`.
</div>

{{chatbot   
    name              = "Friendly CISO Chatbot (claude-3.5)"  
    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
    initial_prompt    = "what do you do?"
    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
    edit_mode         = "false"
    platform          = "Open Router (Paid)"
    provider          = "Anthropic"
    model             = "anthropic/claude-3.5-sonnet"
    channel           = ciso-llm-2"
}}



    </div>
    <div class="tab-pane fade" id="tab3" role="tabpanel" aria-labelledby="tab3-tab" style="background-color:#FAFAFA; border: 1px solid #C0C0C0; padding:5px">

<!-- MODEL 3 -->

<div style="padding:20px">

   <h4>Model id: anthropic/claude-3.5-sonnet</h4> 
   The platform below is `Open Router (Paid)`, using the provider `Perplexity` and the model `perplexity/llama-3.1-sonar-large-128k-online`.
</div>

{{chatbot   
    name              = "Friendly CISO Chatbot"  
    initial_message   = "Hi! I'm your friendly CISO. How can I help you today with your cybersecurity questions?"
    initial_prompt    = "what do you do?"
    system_prompt    = "You're a knowledgeable and approachable CISO, guiding users through cybersecurity concerns while aligning with business goals. You offer thoughtful, clear, and actionable responses, always keeping a professional and friendly tone."
    edit_mode         = "false"
    platform          = "Open Router (Paid)"
    provider          = "Perplexity"
    model             = "perplexity/llama-3.1-sonar-large-128k-online"
    channel           = ciso-llm-3"
}}

    </div>
  </div>
</div>

<script>
    $('#main-wrapper').removeAttr('data-layout');
   $('aside').hide()
</script>
