from downloadbutton import download_button
import time
import streamlit as st
import pandas as pd
import openai
import ast
from urllib.parse import urlparse, urlunparse
import requests
import os

# Set up OpenAI client
openai_api_key = os.environ['OPENAI_API_KEY']
client = openai.OpenAI(api_key=openai_api_key)

st.header("Blobee: Your AI People Agent")

st.sidebar.header("Blobee: Your AI People Agent")

job = st.sidebar.text_area("Enter who you are and what kind of person you are looking for", "")
companyTarget = st.sidebar.text_area("Enter what kind of company that person would be working at ?")
quantity = st.sidebar.selectbox('How Many Results?', ('Low', 'High'))

columns = st.columns((2, 1))

with columns[0]:
    st.info(f"Role : {job}")
    st.warning(f"Target Companies : {companyTarget}")
    st.info(f"Quantity : {quantity}")

def openAIcall(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def get_data_with_retry(messages, max_retries=5, delay_seconds=2):
    for _ in range(max_retries):
        data = openAIcall(messages)
        # Split the response into lines and extract job titles
        job_titles = [line.split('. ', 1)[-1] for line in data.split('\n') if line.strip() and line[0].isdigit()]
        if job_titles:
            return job_titles
        else:
            st.markdown(data)
            st.markdown(f"Data not in expected format. Retrying... ({_+1}/{max_retries})")
            time.sleep(delay_seconds)
    raise ValueError("Max retries reached. Data not in expected format.")

def coolest_func_ever(job, companyTarget, quantity, numPages=3):
    content = f"I am using the API to find partnerships for my role as {job}. Please provide a numbered list of 5 relevant job titles, each on a new line."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    person_title_strings = get_data_with_retry(messages)

    st.markdown("---")
    st.subheader("Job Titles You Are Querying")
    for title in person_title_strings:
        st.markdown(f"- {title}")

    if quantity == "High": 
        numresults = 50
    else: 
        numresults = 30

    # Note: The following block seems to use undefined variables. 
    # You may need to implement or remove this part based on your needs.
    """
    urls = []
    for i in range(len(response.results)):
        parsed_url = urlparse(response.results[i].url)
        root_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
        urls.append(root_url)
    formatted_urls = "\n".join(url.replace("https://", "").replace("www.", "").strip("/") for url in urls)

    st.markdown("---")
    st.subheader("Companies You Are Querying")
    st.markdown(urls)
    """

    master_df = pd.DataFrame()

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }

    if quantity == "High": 
        page_limit = 6
    else: 
        page_limit = 4

    # Note: The following block uses undefined variables (url, data).
    # You'll need to define these or adjust this part based on your actual data source.
    """
    for page_num in range(1, page_limit):
        data["page"] = page_num
        response = requests.request("POST", url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
        else:
            st.markdown("oops")
            st.markdown(response.text)

        if 'people' in response_data and isinstance(response_data['people'], list):
            new_data = pd.DataFrame(response_data['people'])
            # ... (rest of your data processing logic)
            master_df = pd.concat([master_df, new_data], ignore_index=True)
        else:
            st.markdown(f"Error on page {page_num}: 'people' key not found or not a list in the response data.")
        time.sleep(1)
    """

    # For demonstration, let's create a dummy dataframe
    master_df = pd.DataFrame({
        'Name': ['John Doe', 'Jane Smith'],
        'Title': ['Software Engineer', 'Data Scientist'],
        'Company': ['Tech Corp', 'Data Inc'],
        'Email': ['john@example.com', 'jane@example.com']
    })

    st.markdown("---")
    st.subheader("Your Contacts")
    st.dataframe(master_df)

    csv = master_df.to_csv(index=False)
    download_button(csv, "file.csv",  "Press to Download Your CSV", pickle_it=False)

if st.button('Generate List'):
    if job and companyTarget and quantity: 
        coolest_func_ever(job, companyTarget, quantity, 3)
    else: 
        st.error("Error: Please provide all required information (job, companies to target, and quantity).")

st.markdown("Please press Generate List. Your results will populate here.")