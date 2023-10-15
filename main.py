from downloadbutton import download_button
 

# Recieving Input
import time

# text_input
import streamlit as st
import pandas as pd
import openai

# import streamlit as st
st.header("Blobee: Your AI People Agent")

# fn = st.text_input("Enter your First Name", max_chars = 10)
# #Buttons
# b = st.button("Save", key)

# if b:
# 	st.success("Your submission have been saved successfully")



# fn = st.text_input("What type of companies should they be at?", max_chars = 10)
# #Buttons
# c = st.button("Save")

# if c:
# 	st.success("Your submission have been saved successfully")



st.sidebar.header("Blobee: Your AI People Agent")

job = st.sidebar.text_area("Enter who you are and what kind of person you are looking for", "")


companyTarget = st.sidebar.text_area("Enter what kind of company that person would be working at ?")

# age = st.sidebar.number_input(
#     "How many results", min_value=0, max_value=100, step=1
# )

quantity = st.sidebar.selectbox(
    'How Many Results?',
     ('Low', 'High'))


columns = st.columns((2, 1))


with columns[0]:
    st.info(f"Role : {job}")
    st.warning(f"Target Companies : {companyTarget}")
    st.info(f"Quantity : {quantity}")


def openAIcall(messages):
    import openai
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    return response
def is_string_representing_list_of_strings(data):
    # Check if data is a string
    if not isinstance(data, str):
        return False
    
    # Remove the first and last characters (assuming they are quotation marks)
    trimmed_data = data[1:-1]

    try:
        # Attempt to evaluate the string as a Python expression
        evaluated_data = eval(f"[{trimmed_data}]")
    except Exception:
        # If evaluation fails, it's not a string representing a list of strings
        return False
    
    # Check if the evaluated data is a list of strings
    return isinstance(evaluated_data, list) and all(isinstance(item, str) for item in evaluated_data)

def get_data_with_retry(messages, max_retries=5, delay_seconds=2):
    for _ in range(max_retries):
        data = openAIcall(messages)
        dataClean = data.choices[0].message['content'].strip()

        if is_string_representing_list_of_strings(dataClean):
            return dataClean  # Return the data if it is in the correct format as a string
        else:
            st.markdown(dataClean)
            st.markdown(type(dataClean))
            
            st.markdown(f"Data not in expected format. Retrying... ({_+1}/{max_retries})")
            time.sleep(delay_seconds)  # Wait for some time before retrying
    raise ValueError("Max retries reached. Data not in expected format.")


def coolest_func_ever(job, companyTarget, quantity, numPages=3):
    import pandas as pd
    content = "I am using the Apollo API to find partnerships for my role as " + job + ". The Apollo API enables me to find lots of people and their emails so I can reach out to them. However, one of their filters I can choose between is what their job titles are. please generate a list of 15 job titles that could be relevant for me to meet. I will be using your response directly as the input into the API call so I need it to be in the perfect format of an array with strings. For example, if a marketing director would be useful to me, please output:  ['marketing director', 'Director, Marketing and Communications', 'Marketing'] Make sure your output has no new lines and no slashes "

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    person_title_strings = get_data_with_retry(messages)


    st.markdown("---")
    st.subheader("Job Titles You Are Querying")
    st.markdown(person_title_strings)


    if quantity == "High": 
        numresults = 50
    else: 
        numresults = 30
    ##FOMRAT: 
    from urllib.parse import urlparse, urlunparse

    urls = []

    # Iterate through the URLs in the response object

    for i in range(len(response.results)):
        # Parse the URL
        parsed_url = urlparse(response.results[i].url)
        
        # Reconstruct the URL with just the scheme and netloc
        root_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
        
        # Append the root URL to the urls list
        urls.append(root_url)

    # Additional step to format URLs as per the previous code snippet
    formatted_urls = "\n".join(url.replace("https://", "").replace("www.", "").strip("/") for url in urls)


    st.markdown("---")
    st.subheader("Companies You Are Querying")
    st.markdown(urls)

    ##BEGIN APOLLO

    import ast
    person_title_strings = ast.literal_eval(person_title_strings)

    import requests
    import pandas as pd
    import time

    master_df = pd.DataFrame()

    # Create headers for the API request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }

    if quantity == "High": 
        page_limit = 6
    else: 
        page_limit = 4

    for page_num in range(1, page_limit):  # assuming you still want 4 pages per part
        data["page"] = page_num

        #api call
        response = requests.request("POST", url, headers=headers, json=data, timeout=10)

        #check response
        if response.status_code == 200:
            response_data = response.json()
        else:
            st.markdown("oops")
            st.markdown(response.text)

        # Check if the 'people' key exists in the response and that it's a list
        if 'people' in response_data and isinstance(response_data['people'], list):
            new_data = pd.DataFrame(response_data['people'])

            # Drop certain columns from the new data
            columns_to_drop = [
                "photo_url",
                "first_name",
                "last_name",
                "twitter_url",
                "github_url",
                "facebook_url",
                "extrapolated_email_confidence",
                "flagged_datum",
                "intent_strength",
                "show_intent",
                "revealed_for_current_team",
                "organization_id",
                "employment_history",
                "id"
            ]

            #reorder column
            for col in columns_to_drop:
                if col in new_data.columns:
                    new_data.drop(columns=[col], inplace=True)

            cols = new_data.columns.tolist()
            if 'organization' in cols: 
                new_data['organization_name'] = new_data['organization'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
                cols = new_data.columns.tolist()
                cols.insert(cols.index('email'), cols.pop(cols.index('organization_name')))
                cols.insert(cols.index('email_status'), cols.pop(cols.index('organization_name')))
                cols.insert(cols.index('email_status'), cols.pop(cols.index('email')))
                columns_to_drop.append("organization")
                    

            if 'phone_numbers' in cols: 
                new_data['phone_number'] = new_data['phone_numbers'].apply(lambda x: x[0]['sanitized_number'] if isinstance(x, list) and x else None)
                columns_to_drop.append("phone_numbers")



            for col in columns_to_drop:
                if col in new_data.columns:
                    new_data.drop(columns=[col], inplace=True)

    
            # Append the new data
            master_df = master_df.append(new_data, ignore_index=True)

        else:
            st.markdown(f"Error on page {page}: 'people' key not found or not a list in the response data.")

    # Introduce a delay of 5 seconds between requests. You can adjust this duration as needed.
        time.sleep(1)

    # MOVE LINKEDIN COLUMN BACK 
    # Get the column names
    cols = master_df.columns.tolist()
    cols = [cols[0], cols[5],  cols[2],  cols[1], cols[-1], cols[6], cols[7], cols[8], cols[13], cols[9], cols[4],cols[3] ]
    # Move the 2nd column (index 1) to be the 10th column (index 9)
    # Note: Python uses zero-based indexing, so the 2nd column is at index 1, the 10th at index 9, etc.
    # Reorder the DataFrame
    master_df = master_df[cols]
    st.markdown("---")
    st.subheader("Your Contacts")

    st.dataframe(master_df)

    csv = master_df.to_csv()

    download_button(csv, "file.csv",  "Press to Download Your CSV", pickle_it=False)

    # st.download_button(
    # "Press to Download Your CSV",
    # csv,
    # "file.csv",
    # "text/csv",
    # key='download-csv'
    # )



if st.button('Generate List'):
    if (companyTarget and quantity): 
        coolest_func_ever(job, companyTarget, quantity, 3)
    else: 
        st.error("Error: Please provide companies to target")


st.markdown(f"Please press Generate List. Your results will populate here. ")


### HI IHIHIHIH
