from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized") 
# Để headless thì ảnh đầu ra đần lắm nhen
# chrome_options.add_argument("--headless")  

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

urls = []
base_url = 'https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c={}&s={}'

#Chỗ này fill chapter và section vào
chapters_sections = {
  6:[1,2,3,4],
  7: [1,2,3,4],
}


for chapter, sections in chapters_sections.items():
  for section in sections:
    urls.append(base_url.format(chapter, section))

import os

def capture_screenshot(question_num, chapter, section):
  screenshot_name = f"chapter{chapter}_section{section}_question{question_num}.png"
  screenshot_path = os.path.join("screenshots", screenshot_name)
  driver.save_screenshot(screenshot_path)
  print(f"Captured screenshot: {screenshot_path}")

def scroll_to_element(element):
  driver.execute_script("arguments[0].scrollIntoView(true);", element)

def scroll_to_bottom():
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

for url in urls:
  chapter = url.split('c=')[1].split('&')[0]
  section = url.split('s=')[1].split('&')[0] if '&' in url.split('s=')[1] else url.split('s=')[1]
  
  print(f"\nProcessing Chapter {chapter} Section {section}")
  driver.get(url)
  wait = WebDriverWait(driver, 30)
  
  try:
    question_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#question1 > form > span')))
    question_text = question_span.text
    total_questions = int(question_text.split('/')[1])
    print(f"Found {total_questions} questions")
  except Exception as e:
    print(f"ERROR: Failed to process Chapter {chapter} Section {section}")
    print(f"Reason: {str(e)}")
    continue

  for i in range(1, total_questions + 1):
    try:
      wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#question{i}')))
    except Exception as e:
      print(f"ERROR: Failed on Chapter {chapter} Section {section} Question {i}")
      print(f"Reason: {str(e)}")
      continue

    question_element = driver.find_element(By.CSS_SELECTOR, f'#question{i}')
    scroll_to_element(question_element)

    driver.execute_script(f"""
    $(`#question{i} input[type=checkbox][data-ans='1']`).prop('checked', true);
    $(`#question{i} input[type=radio][data-ans='1']`).prop('checked', true);
    """)

    driver.execute_script(f"""
    $(`#question{i} select`).each(function () {{
      const correctAnswer = $(this).attr('data-ans');
      if (correctAnswer !== undefined) {{
        $(this).val(correctAnswer); // Select the correct answer
      }}
    }});
    """)

    driver.execute_script(f"""
    $(`#question{i} input[type=text]`).each(function () {{
      const textInputId = $(this).attr('id'); // Get the ID of the text input
      const hiddenAnswerId = `sa${{textInputId.replace('q', '')}}`; // Derive hidden answer ID
      const hiddenAnswer = $(`#${{hiddenAnswerId}}`).val(); // Get the hidden answer

      if (hiddenAnswer !== undefined) {{
        $(this).val(hiddenAnswer); // Populate the text input with the hidden answer
      }}
    }});
    """)

    driver.execute_script(f"$(`#question{i} .check-answer`).click();")
    scroll_to_bottom()
    capture_screenshot(i, chapter, section)

    if i < total_questions:
      next_button = f"#question{i} .btn-forward"
      wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button)))
      driver.execute_script(f"$('{next_button}').click();")

  driver.execute_script("$('#btn-first-question').click();")

driver.quit()
