from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import time
from datetime import datetime


FILE_MODE = True
SAVE_TRANSCRIPT = False
file_input_path = "./input.txt"
file_output_path = f"./outputs/output-{datetime.now().strftime('%m-%d_%H%M%S')}.txt"
key_questions_answers_output_path = "./outputs/key_questions_answers.txt"
key_questions_output_path = "./outputs/key_questions.txt"


# Initialize the WebDriver (replace 'Chrome' with your browser of choice)
driver = webdriver.Chrome()

def chat_with_bot(question, child_num):
    # Find the chat input element and send the question
    input_element = driver.find_element(
        "xpath",
        '//*[@id="GeckoChatWidget"]/div[1]/div/div[3]/div[1]/textarea')
    input_element.send_keys(question)
    input_element.send_keys(Keys.RETURN)  # Press Enter to send the question

    # Wait for the bot to respond (adjust sleep time as needed)
    reply_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 
             f"#GeckoChatWidget > div.GeckoChatWidget > div > div.Conversation > div:nth-child({child_num}) > div.Message-content"
             ))
             )
    response_text_1 = "123"
    response_text_2 = "456"
    while (not response_text_1 == response_text_2):
        time.sleep(1)
        response_text_1 = reply_box.text
        time.sleep(1)
        response_text_2 = reply_box.text
    return response_text_2

try:
    # Open the website with the chatbot
    driver.get("https://widget-assets.geckochat.io/widget.html?widget=s6uMmAyXZPK0ytv")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#GeckoChatWidget > div.GeckoChatWidget > button"))
             ).click()
    
    time.sleep(2)

    # Interact with the chatbot
    if FILE_MODE and not file_input_path == None:
        # Open the file in read mode
        with open(file_input_path, 'r') as file:
            # Read lines from the file and remove newline characters
            questions = [line.strip() for line in file.readlines()]
    else:
        questions = ["What is your name?", "What is your name?", "What is your name?", "What is your name?"]

    responses = []
    key_questions_responses = []
    key_questions = []
    for num, question in enumerate(questions, start=1):
        response = chat_with_bot(question, num*2)
        if FILE_MODE:
            if "sorry" in response.lower():
                key_questions.append(question)
                key_questions_responses.append(f"Question: {question}\nResponse: {response}\n")
            responses.append(f"Question: {question}\nResponse: {response}\n")
        else:
            print(f"Question: {question}\nResponse: {response}\n")
finally:
    if SAVE_TRANSCRIPT:
        driver.find_element(
            "xpath",
            '//*[@id="GeckoChatWidget"]/div[1]/div/div[1]/div[2]').click()
    # Close the browser window
    time.sleep(2)
    driver.quit()

    if FILE_MODE and not file_output_path == None:
        with open(file_output_path, 'w') as file:
            # Write each line to the file
            for line in responses:
                file.write(unidecode(line) + '\n')
        with open(key_questions_output_path, 'a') as file:
            # Write each line to the file
            for line in key_questions:
                file.write(unidecode(line) + '\n')
        with open(key_questions_answers_output_path, 'a') as file:
            # Write each line to the file
            for line in key_questions_responses:
                file.write(unidecode(line) + '\n')