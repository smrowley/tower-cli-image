import os
import json
import sys, getopt
from tower_cli import get_resource
from tower_cli.conf import settings

jobVars = []

try:
    opts, args = getopt.getopt(sys.argv[1:], "u:p:h:t:v:", ["username=", "password=", "hostname=", "template=", "var="])
    print("Parsing credentials from script args")

    for opt, arg in opts:
        if opt in("-u", "--username"):
            username = arg
        elif opt in("-p", "--password"):
            password = arg
        elif opt in("-h", "--hostname"):
            hostname = arg
        elif opt in("-t", "--template"):
            jobTemplateName = arg
        elif opt in("-v", "--var"):
            jobVars.append(arg)

except getopt.GetoptError as e:
    print("Failed to interpret arguments: " + str(e))
    exit(1)
    
searchParams = [("name", jobTemplateName)]

print("Attempting to execute '" + jobTemplateName + "' job template on " + hostname)
print("Passing the following extra variables to Tower job: " + str(jobVars))

with settings.runtime_values(host = hostname, username = username, password = password):
    jobTemplateResource = get_resource("job_template")
    searchResults = jobTemplateResource.list(query = searchParams)

    assert searchResults["count"] == 1, "Expected 1 search result, but got " + str(searchResults["count"])

    print("Found job: " + jobTemplateName)

    jobId = searchResults["results"][0]["id"]

    jobResource = get_resource("job")
    job = jobResource.launch(job_template = jobId, monitor = True, extra_vars = jobVars)
    
assert not job["failed"], "The job execution has failed"

print("Job execution completed")