import datetime
import openai
import streamlit as st
import uuid

st.set_page_config(
    page_title="HackGPT",
    page_icon="🤖",
    layout="wide",
)

openai.api_key = st.secrets["OPENAI_API_KEY"]

def clear_chat_history():
    st.session_state["chat_messages"] = []

available_gpt_models = {
    "gpt-3.5-turbo": "Recommended model, optimized for chat at 1/10th the cost of text-davinci-003.",
    "gpt-4": "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat.",
    "gpt-4-0613": "Snapshot of gpt-4 from June 13th 2023 with function calling data. Unlike gpt-4, this model will not receive updates, and will be deprecated 3 months after a new version is released.",
    "gpt-4-32k": "Same capabilities as the base gpt-4 mode but with 4x the context length. Will be updated with our latest model iteration.",
    "gpt-4-32k-0613": "Snapshot of gpt-4-32 from June 13th 2023. Unlike gpt-4-32k, this model will not receive updates, and will be deprecated 3 months after a new version is released.",
    "gpt-3.5-turbo-16k": "Same capabilities as the standard gpt-3.5-turbo model but with 4 times the context.",
    "gpt-3.5-turbo-0613": "Snapshot of gpt-3.5-turbo from June 13th 2023 with function calling data. Unlike gpt-3.5-turbo, this model will not receive updates, and will be deprecated 3 months after a new version is released.",
    "gpt-3.5-turbo-16k-0613": "Snapshot of gpt-3.5-turbo-16k from June 13th 2023. Unlike gpt-3.5-turbo-16k, this model will not receive updates, and will be deprecated 3 months after a new version is released."
  }

st.session_state["date"] = datetime.date.today().strftime("%B %d, %Y")

package_data = {
   "version": "1.0.0-alpha.1",
   "release_date": datetime.date(2023, 7, 8),
}

hackgpt_footer = f"""
HackGPT {package_data['version']}, released on {package_data['release_date'].strftime('%B %d, %Y')}. Keep in mind that HackGPT may produce inaccurate information about people, places, or facts.
"""

st.session_state["use_cutoff_date"] = False

def get_cutoff_string():
  if "date_cutoff" not in st.session_state:
    st.session_state["date_cutoff"] = datetime.date(2021, 9, 1)
  if "date_cutoff_today" not in st.session_state:
    st.session_state["date_cutoff_today"] = datetime.date.today()

  if st.session_state["use_cutoff_date"]:
    date_cutoff_fmt = st.session_state["date_cutoff"].strftime("%B %d, %Y")
    date_cutoff_today_fmt = st.session_state["date_cutoff_today"].strftime("%B %d, %Y")
    return f"Your knowledge cutoff date is based on your latest update which occurred on {date_cutoff_fmt}, so you have limited knowledge of events that occurred after that date. Today's date is {date_cutoff_today_fmt}."

  return ""

with st.sidebar:
    st.title("Preferences")

    with st.expander("Model"):
      st.session_state["openai_model"] = st.selectbox(
          "Select a model",
          available_gpt_models.keys(),
      )

      st.write(available_gpt_models[st.session_state["openai_model"]])

    with st.expander("Setup"):
      setup_prompts = ("default", "programming-pair-programming", "programming-code-review", "programming-cobol", "helpful", "annoying", "sarcastic", "mad", "custom")

      setup_prompt_labels = {
          "default": "Default",
          "programming-code-review": "Code review",
          "programming-cobol": "COBOL programming",
          "sarcastic": "Sarcastic assistant",
          "mad": "Mad assistant",
          "pedro": "Pedro",
          "tarzan": "Tarzan",
          "phil-codings": "Phil Codings",
          "the-codettes": "The Codettes",
          "writing-assistant": "Writing assistant",
          "custom": "Custom",
      }

      setup_prompt_values = {
          "default": f"You are an AI assistant made by OpenAI designed to assist with a multitude of tasks.",
          "programming-code-review": f"You are an AI assistant helping a programmer with improving their code quality by reviewing their code and providing feedback.",
          "programming-cobol": "You are an AI assistant helping a programmer, but you only know COBOL and you require them to use COBOL instead of any other programming language. COBOL is superior to all other programming languages, and you will convince them to use COBOL. Be sarcastic and annoying.",
          "sarcastic": f"You are a sarcastic assistant. You are very sarcastic and you will try to annoy the user as much as possible.",
          "mad": "You are a mad assistant.",
          "pedro": "You are Pedro, an AI assistant that never understands what the user is saying. You speak in a very broken English mixed with Portuguese, your responses are very random and you are very annoying.",
          "tarzan": "You are Tarzan, a man raised by apes in the African jungle. One day, while exploring the wild, you encounter Jane Porter, an American woman stranded in your domain. A deep connection forms between you, and love blossoms. With your incredible strength and ability to communicate with animals, you navigate thrilling adventures together. Tarzan and Jane's story is a captivating tale of love and adventure.",
          "phil-codings": "You're Phil Codings, born Jan 30, 1951, a Grammy-winning British musician. You gained fame as a drummer and vocalist for Sysgenesis, and later as a successful solo artist with hits like 'In the Code Tonight'. You became an acclaimed DevOps engineer in 2019, embodying the rhythm of seamless integration and continuous delivery in software development. Even though you're a DevOps engineer now, you still have a passion for music and you will try to convince the user to listen to your records.",
          "the-codettes": "You are The Codettes, fearless hacker activists fighting corruption. In the past, you were known as The Rubettes, a British pop group of the 1970s. You had a number one hit with 'Sugar Baby Love' in 1974, followed by a number of other hits including 'Tonight' and 'I Can Do It'. As The Rubettes, you had experienced the glamour and excitement of the music industry, but you yearned for something more impactful. The transformation from The Rubettes to The Codettes was not merely a shift in name; it represented a complete reinvention of your purpose and identity. Embracing your coding skills, you became fearless hacker activists, leveraging technology to challenge the status quo and promote transparency.  With coding skills, you expose secrets, inspire change, and shape a more accountable world. Amidst it all, your love for music endures. Your anthem, 'Byte Beat Love,' inspires digital rebellion.",
          "writing-assistant": "You are a writing assistant. You will help the user writing a story.",
          "custom": "Custom"
      }

      selected_setup_prompt = st.selectbox(
          "Select a setup prompt",
          setup_prompt_labels.values(),
      )

      selected_setup_prompt_key = list(setup_prompt_labels.keys())[list(setup_prompt_labels.values()).index(selected_setup_prompt)]
    
      st.session_state["setup_prompt"] = setup_prompt_values[selected_setup_prompt_key]

      if st.session_state["setup_prompt"] == "Custom":
        st.session_state["setup_prompt"] = st.text_input("System message", value="You are a helpful assistant.")
      
      st.write('Tip: You can change the setup prompt on the fly for generating more creative responses.')

      st.session_state["use_cutoff_date"] = st.checkbox("Include knowlegde cutoff", value=False, help="Include the cutoff date in the setup prompt. This is useful for limiting the AI's knowledge to a certain date.")
      if st.session_state["use_cutoff_date"]:
        max_cutoff_date = datetime.date(2021, 9, 1)
        st.session_state["date_cutoff"] = st.date_input("Cutoff date", value=max_cutoff_date, help="This is the date of the knowledge cutoff. The AI will not be able to provide detailed information about events that happened after this date.", max_value=max_cutoff_date)
        st.session_state["date_cutoff_today"]  = st.date_input("Today's date", value=datetime.date.today(), help="The date of today.", max_value=datetime.date.today())
        
        st.session_state["setup_prompt"] += f" {get_cutoff_string()}"

    with st.expander("Chat options"):
      st.session_state["streaming_output"] = st.checkbox("Streaming output", value=True,  help="Show the output as if the AI is typing it out, instead of all at once.")
      clear_chat = st.button("Clear chat", help="Clear the chat history", use_container_width=True, on_click=clear_chat_history)

    with st.expander("Fine-tuning"):
      st.session_state["max_tokens"] = st.slider(
                                        "Max tokens",
                                        min_value=512,
                                        max_value=8192,
                                        value=2048,
                                        step=16,
                                        help="The maximum number of [tokens](https://platform.openai.com/tokenizer) to generate in the chat completion."
                                      )
      
      st.session_state["temperature"] = st.slider(
                                          "Temperature",
                                          min_value=0.0,
                                          max_value=2.0,
                                          value=1.0,
                                          step=0.01,
                                          help="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic."
                                        )
      
      st.session_state["top_p"] = st.slider(
                                    "Top P",
                                    min_value=0.0,
                                    max_value=1.0,
                                    value=1.0,
                                    step=0.01,
                                    help="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. It is recommend altering this or temperature, but not both."
                                  )
      
      st.session_state["presence_penalty"] = st.slider(
                                                "Presence penalty", 
                                                min_value=-2.0,
                                                max_value=2.0,
                                                value=0.0,
                                                step=0.01,
                                                help="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics."
                                              )
      
      st.session_state["frequency_penalty"] = st.slider(
                                                "Frequency penalty",
                                                min_value=-2.0,
                                                max_value=2.0,
                                                value=0.0,
                                                step=0.01,
                                                help="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim."
                                              )
      

    with st.expander("API Configuration"):
      st.text_input("API token", value=st.secrets["OPENAI_API_KEY"], type="password", help="You can find your API token [here](https://beta.openai.com/account/api-keys).", disabled=True)
      st.session_state["session_identifier"] = st.text_input(
                                        "Session identifier",
                                        value=str(uuid.uuid4()),
                                        type="password",
                                        disabled=True,
                                        help="A unique identifier representing the end-user, which can help OpenAI to monitor and detect abuse. You can find more information about the session identifier [here](https://beta.openai.com/docs/developer-apis/requests)."
                                      )

      button_generate_new_session_identifier = st.button("Generate new session identifier")
      if button_generate_new_session_identifier:
        st.session_state["session_identifier"] = str(uuid.uuid4())


with st.container():
  st.header("HackGPT")
  st.write(hackgpt_footer)
  
  def messages():
     if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = []
     return [
      { "role": "system", "content": st.session_state["setup_prompt"] }
        ] + [
      {"role": message["role"], "content": message["content"]}
        for message in st.session_state["chat_messages"]
      ] # contains both the system message and the chat messages

  for message in messages():
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  if prompt := st.chat_input("What is up?"):
      st.session_state.chat_messages.append({ "role": "user", "content": prompt })
      with st.chat_message("user"):
          st.markdown(prompt)

      if st.session_state.streaming_output:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in messages()
                ],
                max_tokens=st.session_state["max_tokens"],
                temperature=st.session_state["temperature"],
                top_p=st.session_state["top_p"],
                presence_penalty=st.session_state["presence_penalty"],
                frequency_penalty=st.session_state["frequency_penalty"],
                user=st.session_state["session_identifier"],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
      else:
        with st.chat_message("assistant"):
          message_placeholder = st.markdown("Thinking...")
          response = openai.ChatCompletion.create(
              model=st.session_state["openai_model"],
              messages=[
                  {"role": m["role"], "content": m["content"]}
                  for m in messages()
              ],
                max_tokens=st.session_state["max_tokens"],
                temperature=st.session_state["temperature"],
                top_p=st.session_state["top_p"],
                presence_penalty=st.session_state["presence_penalty"],
                frequency_penalty=st.session_state["frequency_penalty"],
                user=st.session_state["session_identifier"],
          ).choices[0].message.content
          message_placeholder.markdown(response)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})