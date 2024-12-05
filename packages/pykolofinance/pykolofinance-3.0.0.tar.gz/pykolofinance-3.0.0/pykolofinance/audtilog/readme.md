# Usage Guide for Activity Log Utility Function (Python Version)

## This utility function allows you to send activity logs to a designated endpoint for logging and auditing purposes. It is particularly useful in scenarios where you need to log user actions, system events, or any other relevant activities within your microservice.


## Calling the Function
To create a log entry, call the create_log function with the appropriate parameters

# Example usage within a Django view function

```json
def my_view(request):
    # Perform some actions
    
    # Prepare activity log data
    activity_data = {
        "request": request,
        "action_type": "CREATE",
        "action": "User registration",
        "microservice_name": "Authentication Service",
        "module": "User Management",
        "module_id": "1",
        "oldvaluejson": None,
        "newvaluejson": {"username": "john_doe", "email": "john@example.com"},
        "affected_columns": ["username", "email"]
    }
    
    # Send activity log asynchronously
    send_activity_log.delay(activity_data)
    
    # Continue with view logic
In the example above, send_activity_log.delay() is used to send the activity log asynchronously using a task queue (e.g., Celery). This ensures that logging does not block the main request-response cycle.


## Environment Variables
Ensure that the LOGGER_URL environment variable is set to the URL of your logging endpoint.


The function payloads are: 

```json
{
  "auditID": "uuid",
  "action": "string",
  "sourceIP": "string",
  "roleId": "string",
  "fullName": "string",
  "userActivityType": "string",
  "microserviceName": "string",
  "endpointName": "string",
  "oldValuesJson": "string",
  "payloadCreatedDate": "string",
  "newValuesJson": "string",
  "affectedColumns": "string",
  "role": "string",
  "userName": "string",
  "userID": "string",
  "createdDate": "string",
  "ipAddress": "string",
  "startDate": "string",
  "endDate": "string",
  "branchCode": "string",
  "location": "string",
  "branchName": "string",
  "clientInfo": "string",
  "actionStatus": "string",
  "lastLogin": "string",
  "sessionID": "string",
  "module": "string",
  "moduleID": "string",
  "timestamp": "string"
}
```