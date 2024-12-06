# Vigil - SDK

## Overview

Welcome to the official SDK for Vigil - A comprehensive solution for all your monitoring requirements. The foxsenseinnovations.vigil PyPi package provides developers with a powerful and easy-to-use toolkit for integrating Vigil into their applications. Monitor exceptions, jobs, APIs, and website availability seamlessly with this SDK.

## Features

- Exception Monitoring: Keep track of exceptions in your application, receive detailed reports, and gain insights into potential issues.
- Job Monitoring: Monitor the status and performance of background jobs, ensuring that critical tasks are executed successfully.
- API Monitoring: Track the health and performance of your APIs, ensuring optimal functionality and responsiveness.
- Website Availability: Check the availability and responsiveness of your websites to ensure a seamless user experience.

## Installation

To get started with 'foxsenseinnovations.vigil' SDK, follow these steps:

### Install the pypi Package:

```
pip install foxsenseinnovations.vigil
```

### Initialize Vigil (Django): 

Initialize Vigil with the provided VigilOptions. This step involves setting up the necessary configurations for your Vigil instance. Define API_KEY (mandatory) , INSTANCE_URL (optional) and CLIENT_VERSION (optional) in settings.py file. Declare the below statements in main application manage.py file.

```
# import Vigil to initialize the API KEY
from foxsenseinnovations.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.vigil_options_types import VigilOptions
from django.conf import settings as django_settings

# Access the API_KEY from settings.py file
api_key = django_settings.API_KEY

# Define the VigilOptions instance with the desired values
options = VigilOptions(api_key=api_key)

# Initialize the Vigil class with the provided options
Vigil.initialize(options)
```

If optional parameters are also included in the settings.py file, then the initialization of Vigil would be as follows:

```
# import Vigil to initialize the API KEY
from foxsenseinnovations.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.vigil_options_types import VigilOptions
from django.conf import settings as django_settings

# Access the INSTANCE_URL, CLIENT_VERSION from settings.py file
instance_url = django_settings.INSTANCE_URL
client_version = django_settings.CLIENT_VERSION

# Define the VigilOptions instance with the desired values
options = VigilOptions(api_key=api_key, version=client_version, instance_url=instance_url)

# Initialize the Vigil class with the provided options
Vigil.initialize(options)
```

### Initialize Vigil (Flask): 

Initialize Vigil with the provided VigilOptions. This step involves setting up the necessary configurations for your Vigil instance. Define API_KEY (mandatory) , INSTANCE_URL (optional) and CLIENT_VERSION (optional). Declare the below statements in main application app.py file.

```
# import Vigil to initialize the API KEY
from foxsenseinnovations.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.vigil_options_types import VigilOptions

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Define the VigilOptions instance with the desired values
apikey = app.config['API_KEY']
instanceurl = app.config['INSTANCE_URL']
clientversion = app.config['CLIENT_VERSION']
options = VigilOptions(api_key=apikey, instance_url=instanceurl, client_version=clientversion)

# Initialize the Vigil class with the provided options
Vigil.initialize(options)
```

### Initialize Vigil (Fast API): 

Initialize Vigil with the provided VigilOptions. This step involves setting up the necessary configurations for your Vigil instance. Define API_KEY (mandatory) , INSTANCE_URL (optional) and CLIENT_VERSION (optional). Declare the below statements in main application app.py file.

```
# import Vigil to initialize the API KEY
from foxsenseinnovations.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.vigil_options_types import VigilOptions

app = FastAPI()

# Define the VigilOptions instance with the desired values
vigil_options = VigilOptions(
    api_key=API_KEY,
    instance_url=INSTANCE_URL,
    client_version=CLIENT_VERSION
)

# Initialize the Vigil class with the provided options
Vigil.initialize(options)
```

## API Monitoring (Django)

Declare the below statements in settings.py file

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, ExcludeOptions

# In MIDDLEWARE of settings.py file add the below line
'foxsenseinnovations.vigil.api_manager_django.ApiMonitoringMiddleware'
```

### Options

Options are not mandatory

| Options | Mandatory |     Default      |                          Values                          |
| ------- | :-------: | :--------------: | :------------------------------------------------------: |
| exclude |   FALSE   | ExcludeOptions() | ExcludeOptions(GET: [], POST: [], PATCH: [], DELETE: []) |

#### Exclude

- The exclude option allows you to specify certain API paths to be excluded from monitoring for each HTTP method. This means that requests to these excluded paths will not be tracked or analyzed by Vigil.
- It's particularly useful when there are specific endpoints that you don't want to include in your monitoring activities, perhaps because they are known to be non-critical or for internal use only.
- For each HTTP method (GET, POST, PATCH, DELETE), you can define a list of API paths to be excluded. By default, if no exclusions are provided, all API paths are monitored.

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, ExcludeOptions

# In MIDDLEWARE list of settings.py file add the below line
'foxsenseinnovations.vigil.api_manager_django.ApiMonitoringMiddleware'

# After MIDDLEWARE list add the below lines
exclude_options = ApiMonitoringOptions(exclude=ExcludeOptions(GET=['/'],POST=['/health']))

# '/' GET method and '/health' POST method APIs are not monitored
API_MONITORING_OPTIONS = exclude_options
```

## API Monitoring (Flask)

Declare the below statements in app.py file

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ExcludeOptions, ApiMonitoringOptions
from foxsenseinnovations.vigil.api_manager_flask import ApiMonitoringMiddleware

#Define the blueprint of your app with the configured endpoints (Optional)
from api import api_bp

```

### Options

Options are not mandatory

| Options | Mandatory |     Default      |                          Values                          |
| ------- | :-------: | :--------------: | :------------------------------------------------------: |
| exclude |   FALSE   | ExcludeOptions() | ExcludeOptions(GET: [], POST: [], PATCH: [], DELETE: []) |

#### Exclude

- The exclude option allows you to specify certain API paths to be excluded from monitoring for each HTTP method. This means that requests to these excluded paths will not be tracked or analyzed by Vigil.
- It's particularly useful when there are specific endpoints that you don't want to include in your monitoring activities, perhaps because they are known to be non-critical or for internal use only.
- For each HTTP method (GET, POST, PATCH, DELETE), you can define a list of API paths to be excluded. By default, if no exclusions are provided, all API paths are monitored.

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, ExcludeOptions



# '/' GET method and '/health' POST method APIs are not monitored
exclude_options = ApiMonitoringOptions(exclude=ExcludeOptions(GET=['/'], POST=['/health']), clientVersion=clientversion)

#Pass the app to the middleware
app.wsgi_app = ApiMonitoringMiddleware(app, options=exclude_options)

#Register the blueprint if necessary
app.register_blueprint(api_bp, url_prefix='/api')


```

## API Monitoring (Fast API)

Declare the below statements in main.py file

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ExcludeOptions, ApiMonitoringOptions
from foxsenseinnovations.vigil.api_manager_fast_api import ApiMonitoringMiddleware

```

### Options

Options are not mandatory

| Options | Mandatory |     Default      |                          Values                          |
| ------- | :-------: | :--------------: | :------------------------------------------------------: |
| exclude |   FALSE   | ExcludeOptions() | ExcludeOptions(GET: [], POST: [], PATCH: [], DELETE: []) |

#### Exclude

- The exclude option allows you to specify certain API paths to be excluded from monitoring for each HTTP method. This means that requests to these excluded paths will not be tracked or analyzed by Vigil.
- It's particularly useful when there are specific endpoints that you don't want to include in your monitoring activities, perhaps because they are known to be non-critical or for internal use only.
- For each HTTP method (GET, POST, PATCH, DELETE), you can define a list of API paths to be excluded. By default, if no exclusions are provided, all API paths are monitored.

```
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, ExcludeOptions


# Configure API Monitoring
exclude_options = ApiMonitoringOptions(exclude=ExcludeOptions(GET=['/'],POST=['/health']),clientVersion=CLIENT_VERSION)

# Add middleware
app.add_middleware(ApiMonitoringMiddleware, options=exclude_options)


```

## Job Monitoring

To ensure monitoring of jobs within the application, integrate the following code snippet wherever jobs are defined and executed:

```
# import JobManager to monitor the Jobs in the application
from foxsenseinnovations.vigil.job_manager import JobManager
from foxsenseinnovations.vigil.vigil_types.job_monitoring_types import JobDetail

# Job function
def job_func():
    try:
        // log that the job triggered with a start message
        start_job_detail = {'job_id': "<job-id>", 'message': "<job-start-message>"}
        JobManager.capture_job_start(JobDetail(**start_job_detail))
        ...
        ...
        // log that the job has completed its execution with a success message
        stop_job_detail = {'job_id': "<job-id>", 'message': "<job-end-message>"}
        JobManager.capture_job_end(JobDetail(**stop_job_detail))
    except Exception as error:
        fail_job_detail = {'job_id'="<job-id>", message=f"<job-failure-message>: {str(error)}"}
        JobManager.capture_job_failure(JobDetail(**fail_job_detail))
```

Either job_id or job_slug should be provided with values. Neither of these values should be empty inorder to pass to JobDetail.

| Options   |      Values      |
| -------   | :--------------: |
| job_id    |      String      |
| job_slug  |      String      |

Incorporating this code into job functions enables monitoring of job execution, capturing start, success, and failure events.

## Error Monitoring

To ensure monitoring of errors within the application, integrate the following code snippet wherever errors are captured:

```
# import ErrorManager to capture any exceptions/errors that occur in the application
from foxsenseinnovations.vigil.error_manager import ErrorManager

def function():
    try:
        ...
        ...
    except Exception as error:
        // capture the exception from the error object
        ErrorManager.capture_exception(error)
```

### Options

Options are not mandatory

| Options | Mandatory | Default |      Values      |
| ------- | :-------: | :-----: | :--------------: |
| tags    |   FALSE   |   []    | Array of strings |
| context |   FALSE   |   {}    |    An object     |

#### Tags and Context

- Gives extra information about the exception that occurred

```
# import ErrorManager to capture any exceptions/errors that occur in the application
from foxsenseinnovations.vigil.error_manager import ErrorManager

def function():
    try:
        ...
        ...
    except Exception as error:
        options = {
            tags: ['tag1','tag2'],
            context: {
                <key1>: <value1>,
                <key2>: <value2>
            }
        }
        // capture the exception from the error object
        // and pass extra information about the exception in options
        ErrorManager.capture_exception(error, options)
```

## Support

In case of any issues, questions or assistance needed, please feel free to reach out to our support team (support@vigilnow.freshdesk.com).

Happy Monitoring with Vigil!
