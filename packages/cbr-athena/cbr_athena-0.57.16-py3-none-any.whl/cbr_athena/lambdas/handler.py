import sys

sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers
sys.path.append('/var/task'  )          # path to lambda function code

from osbot_aws.Dependencies import load_dependencies
load_dependencies(['openai','fastapi', 'mangum', 'uvicorn','requests','PyGithub'])

from cbr_athena.athena__fastapi.FastAPI_Athena import FastAPI_Athena

def run():
    fastapi_athena = FastAPI_Athena()
    fastapi_athena.run_in_lambda()

if __name__ == '__main__':
     run()                                  # to be triggered from run.sh