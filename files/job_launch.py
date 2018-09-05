import os
import json
from tower_cli import get_resource
from tower_cli.conf import settings

host = os.environ["TOWER_HOST"]
username = os.environ["TOWER_USERNAME"]
password = os.environ["TOWER_PASSWORD"]
jobVars = ["deploy_group: " + os.environ["DEPLOY_GROUP"]]
jobTemplateName = os.environ["JOB_NAME"]
searchParams = [("name", jobTemplateName)]

print("Attempting to execute '" + jobTemplateName + "' job template on " + host)

with settings.runtime_values(host = host, username = username, password = password):
    jobTemplateResource = get_resource("job_template")
    searchResults = jobTemplateResource.list(query = searchParams)

    assert searchResults["count"] == 1, "Expected 1 search result, but got " + str(searchResults["count"])

    print("Found job: " + jobTemplateName)

    jobId = searchResults["results"][0]["id"]

    jobResource = get_resource("job")
    job = jobResource.launch(job_template = jobId, monitor = True, extra_vars = jobVars)
    
assert not job["failed"], "The job execution has failed"

print("Job execution completed")