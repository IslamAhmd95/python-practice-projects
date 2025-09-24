import re
import os
import json
import csv


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA70-\U0001FAFF"  # Symbols for UI
        "\U00002600-\U000026FF"  # Misc symbols
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


def save_to_json(jobs, current_dir):

    json_file_name = "data/jobs.json"
    json_file_path = os.path.join(current_dir, json_file_name)

    with open(json_file_path, 'w', encoding='utf-8') as f:
    # ensure_ascii=False → tells json.dump() not to escape Arabic or other non-ASCII characters.
    # encoding='utf-8' → ensures the file saves Arabic properly.
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    return f"Saved {len(jobs)} jobs to jobs.json successfully"


def save_to_csv(jobs, current_dir):

    csv_file_name = "data/jobs.csv"
    csv_file_path = os.path.join(current_dir, csv_file_name)

    with open(csv_file_path, 'w', newline="", encoding="utf-8") as f:
        csv_writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        csv_writer.writeheader()

        for job in jobs:
            csv_writer.writerow({
                **job,
                'tags': ", ".join(job['tags'])
            })


    return f"Saved {len(jobs)} jobs to jobs.csv successfully"


def is_valid_job(tag):
    return (
        tag.name == 'div'
        and tag.has_attr('class') 
        and 'job' in tag['class'] 
        and 'sponsored' not in tag['class']
    )


def extract_jobs(jobs_html):
    jobs = []
    for job_html in jobs_html:

        location = job_html.find(class_="location").get_text(strip=True)
        if 'Germany' in location:
            continue

        job = {}

        job['title'] = remove_emojis(job_html.select_one('h2.title').text).strip()
        job['company'] = job_html.select_one("div.company").get_text(strip=True)
        job['location'] = location

        tags_list = job_html.select_one('.tags').select('span.tag')
        job['tags'] = [tag.get_text(strip=True) for tag in tags_list]
        
        meta_div = job_html.find(class_='meta')
        job['date_posted'] = meta_div.find(class_='date').get_text(strip=True).replace('Posted: ', '')
        job['apply_link'] = meta_div.find(class_='apply-btn').get('href')

        jobs.append(job)

    print(f"Extracted {len(jobs)} jobs successfully")
    return jobs

