from bs4 import BeautifulSoup
import os
import helpers.utils as utils



if __name__ == '__main__':

    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(current_dir, 'html_samples/index.html'), encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    jobs_list = soup.find('div', {'class': 'job-listing'})
    # exclude sponsored jobs
    jobs_html = jobs_list.find_all(utils.is_valid_job)

    jobs = utils.extract_jobs(jobs_html)

    # save to json file
    print(utils.save_to_json(jobs, current_dir))

    # save to csv file
    print(utils.save_to_csv(jobs, current_dir))
