# %%
import os
import csv

from dotenv import load_dotenv

import src.taskanalytics_data_wrapper.taskanalytics_api as task

# %%
load_dotenv()

email = os.getenv("ta_email")
password = os.getenv("ta_password")
organization = os.getenv("ta_organization")
# %%
status = task.log_in_taskanalytics(username=email, password=password)
status.status_code
# %%
get_survey = task.download_survey(
    username=email,
    password=password,
    survey_id="03348",
    filename_path="data/survey.csv",
)
get_survey.status_code
# %%
survey_metadata = task.get_survey_metadata(
    username=email, password=password, survey_id="03324"
)
survey_metadata.status_code
# %%
survey_metadata.text  # survey metadata
# %%
get_openended_survey = task.download_discovery_survey(
    username=email,
    password=password,
    organization_id=organization,
    survey_id="03230",
    filename_path="data/open_ended_survey.json",
)
# %%
data = get_openended_survey.json()
# transform dict to json file and save
import json

with open("data/open_survey.json", "w") as fp:
    json.dump(data, fp, ensure_ascii=False)


# %%
# create a new dict from our subset of data
def flatten_openended_dict(data):
    """ """
    respondent = []
    completion = []
    category = []
    discovery = []
    comment = []
    for i in data:
        respondent.append(i["id"])
        completion.append(i["completion"])
        category.append(i["category"])
        discovery.append(i["answers"]["discovery"])
        try:
            comment.append(i["answers"]["comment"])
        except:
            comment.append("")
    newlist = [
        {
            "id": respondent,
            "completion": completion,
            "category": category,
            "discovery": discovery,
            "comment": comment,
        }
        for respondent, completion, category, discovery, comment in zip(
            respondent, completion, category, discovery, comment
        )
    ]
    return newlist


newlist = flatten_openended_dict(data["responses"])

# %%
# write open ended survey to csv with your preferred encoding and delimiter
keys = newlist[0].keys()

with open("data/open_survey.csv", "w", encoding="utf-8-sig", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=";")
    writer.writeheader()
    writer.writerows(newlist)

# %%
