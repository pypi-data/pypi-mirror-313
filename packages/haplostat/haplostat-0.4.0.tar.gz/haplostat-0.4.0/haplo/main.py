from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from flask import Flask, request, jsonify
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import os
import platform
app = Flask(__name__)

def get_driver_path():
    """
    Locate the correct WebDriver binary based on the user's platform.
    """
    base_dir = os.path.dirname(__file__)  # Directory of the current script
    driver_dir = os.path.join(base_dir, "drivers")

    os_name = platform.system()
    if os_name == "Windows":
        return os.path.join(driver_dir, "chromedriver_win.exe")
    elif os_name == "Darwin":  # macOS
        return os.path.join(driver_dir, "chromedriver_mac")
    elif os_name == "Linux":
        return os.path.join(driver_dir, "chromedriver_linux")
    else:
        raise EnvironmentError(f"Unsupported OS: {os_name}")
    
def map_populations(user_selected_populations):
    population_mapping = {
        "African American": "AFA",
        "Asian or Pacific Islander": "API",
        "Caucasian": "CAU",
        "Hispanic": "HIS",
        "Native American": "NAM",
    }
    return population_mapping.get(user_selected_populations, "CAU")

def parse_top_hla_group(soup):
    table = soup.find("table", {"class": "compact"})
    if not table:
        return {"error"}

    tbody = table.find("tbody")
    if not tbody:
        return {"error"}

    results = [[],[]]
    rows = tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            hla_right = cols[0].text.strip()
            hla_left = cols[1].text.strip()
            results[0].append(hla_right)
            results[1].append(hla_left)

    return results

def run_convert_hla(population_1, hla_a="", hla_a1="", hla_b="", hla_b1="", hla_c="", hla_c1="", 
                    hla_drb1="", hla_drb2="", hla_dqb1="", hla_dqb2=""):
    driver_path = get_driver_path()    
    driver = None  
    print(f"Driver path: {driver_path}")

    try:
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver initialized successfully.")

        driver.get("https://www.haplostats.org/haplostats")
        print("Navigated to haplostats.org.")

        clear_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "popButton2"))
        )
        clear_button.click()
        pop_val = map_populations(population_1)
        if pop_val:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//fieldset[@class='criteria']//input[@type='checkbox' and @value='{pop_val}']"))
            )
            checkbox.click()
        try:
            dropdown = driver.find_element(By.NAME, "haplotypeLoci")
            select = Select(dropdown)
            select.select_by_visible_text("A~C~B~DRBX~DRB1~DQB1")
            print("Selected option 'A~C~B~DRBX~DRB1~DQB1' from dropdown.")
        except Exception as e:
            print(f"Error selecting option from dropdown: {e}")
            raise
        payload = {
            "a1": hla_a,
            "b1": hla_b,
            "c1": hla_c,
            "drb11": hla_drb1,
            "dqb11": hla_dqb1,
            "a2": hla_a1,
            "b2": hla_b1,
            "c2": hla_c1,
            "drb12": hla_drb2,
            "dqb12": hla_dqb2
        }

        for field_name, value in payload.items():
            if value:
                print(f"Filling field {field_name} with value {value}")
                field = driver.find_element(By.NAME, field_name)
                field.clear()
                field.send_keys(value)

        submit_button = driver.find_element(By.NAME, "_eventId_success")
        submit_button.click()
        print("Form submitted.")

        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        print("Switched to results tab.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "_title_A-C-B-DRBX-DRB1-DQB1_mug_id"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print("Results page loaded successfully.")
        return parse_top_hla_group(soup)

    except Exception as e:
        print(f"Error during run_convert_hla: {e}")
        raise

    finally:
        if driver is not None:
            driver.quit()

@app.route('/convert_hla', methods=['POST'])
def convert_hla():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        population_1 = data.get('population_1', "")
        hla_a = data.get('hla_a', "")
        hla_a1 = data.get('hla_a1', "")
        hla_b = data.get('hla_b', "")
        hla_b1 = data.get('hla_b1', "")
        hla_c = data.get('hla_c', "")
        hla_c1 = data.get('hla_c1', "")
        hla_drb1 = data.get('hla_drb1', "")
        hla_drb2 = data.get('hla_drb2', "")
        hla_dqb1 = data.get('hla_dqb1', "")
        hla_dqb2 = data.get('hla_dqb2', "")

        results = run_convert_hla(
            population_1, hla_a, hla_a1, hla_b, hla_b1, hla_c, hla_c1,
            hla_drb1, hla_drb2, hla_dqb1, hla_dqb2
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
