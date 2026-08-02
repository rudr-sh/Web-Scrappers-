from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

expected_fields = ["Other Name", "Former Name", "Address", "Telephone",
                    "Facsimile", "Email", "Website", "Prefix(es)"]

all_publishers = []

start_url = (
    "https://www.collectionscanada.gc.ca/isbn-canada/app/index.php"
    "?form-action=16&prev_close_url=-1&stack-key=0&stack-overwrite="
    "&fuseaction=public.searchPublishersResult&lang=eng"
    "&publisherName=&city=&province=&select_isbn_keyword=ISBN_PREFIX"
    "&search_isbn_keyword=&page-size=100&submitBtn=Submit"
)

driver.get(start_url)
sleep(3)

page_num = 1

while True:
    print(f"Scraping page {page_num}...")

    try:
        names = driver.find_elements(By.CSS_SELECTOR, ".table section h3")
        labels = driver.find_elements(By.CSS_SELECTOR, ".table-display-publisher dt")
        values = driver.find_elements(By.CSS_SELECTOR, ".table-display-publisher dd")
    except NoSuchElementException:
        print(f"Could not find data on page {page_num}, stopping.")
        break

    if not names:
        print(f"No results found on page {page_num}, stopping.")
        break

    names_text = [n.text for n in names]
    labels_text = [l.text.strip(":") for l in labels]
    values_text = [v.text for v in values]

    page_publishers = []
    current = {field: "" for field in expected_fields}
    started = False

    for label, value in zip(labels_text, values_text):
        if label == "Address":
            if started:
                page_publishers.append(current)
            current = {field: "" for field in expected_fields}
            started = True
        if label in expected_fields:
            current[label] = value

    if started:
        page_publishers.append(current)

    # ---- Attach names (matched by order) ----
    for name, pub in zip(names_text, page_publishers):
        pub["Name"] = name

    all_publishers.extend(page_publishers)
    print(f"  -> {len(page_publishers)} publishers (total so far: {len(all_publishers)})")

    try:
        next_link = driver.find_element(By.LINK_TEXT, "Next")
        next_link.click()
        sleep(3)
        page_num += 1
    except NoSuchElementException:
        print("No more pages. Done scraping.")
        break

driver.quit()

fieldnames = ["Name"] + expected_fields
with open("isbn_publishers.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for pub in all_publishers:
        writer.writerow(pub)

print(f"Done. {len(all_publishers)} publishers written to isbn_publishers.csv")
