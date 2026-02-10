
import json
import os
import re
import time
from urllib import response

from admin_app.models import Creadentials as Credentials
import requests

from organization.models import Organization, Project, Service

try:
    RAILWAY_AUTH_TOKEN =Credentials.objects.first().railway_auth_token
    RAILWAY_TEMPLATE_ID = Credentials.objects.first().raiway_template_id
    WORKSPACE_ID = Credentials.objects.first().railway_workspace_id
except Exception as e:
    print("Error loading environment variables:", e)
    RAILWAY_AUTH_TOKEN = None
    RAILWAY_TEMPLATE_ID = None
    WORKSPACE_ID = None

def sanitize_project_name(name):
    name = name.strip().lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name)
    return name[:60]

def send_request_to_railway(data):
    
    url = "https://backboard.railway.com/graphql/v2"

    headers = {
        "Authorization": f"Bearer {RAILWAY_AUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=data   # use json= if data is a dict
    )
    # print("Request data:", data)
    # print("Response status:", response.status_code)
    
    print("RAILWAY_AUTH_TOKEN:", RAILWAY_AUTH_TOKEN)
    print("RAILWAY_TEMPLATE_ID:", RAILWAY_TEMPLATE_ID)
    print("WORKSPACE_ID:", WORKSPACE_ID)
    print("Response data:", response.json())
    return response.json()



def project_create(service_name):

    mutation = f"""
    mutation {{
        projectCreate(input: {{ name: "{service_name}", workspaceId: "{WORKSPACE_ID}" }}) {{
            id
            name
            environments {{
                edges {{
                    node {{
                        id
                        name
                    }}
                }}
            }}
        }}
    }}
    """
    data = {

        "query": mutation,
    }

    response = send_request_to_railway(data)
    if response is None:
        return None
    project_data = response['data']['projectCreate']
    environment_data = project_data['environments']['edges'][0]['node']

    project_id = Project.objects.create(
        project_id=project_data['id'],
        environment_id=environment_data['id'],
    )
    return project_id

def deploy_to_railway(service_name,service_image,project_id,environment_id):
    CSRF_TRUSTED_ORIGINS = f"https://{service_name}-opensaas-production.up.railway.app"
    postgres_ref=f"Postgres-{service_name}"
    mutation = """
    mutation templateDeployV2($input: TemplateDeployV2Input!) {
        templateDeployV2(input: $input) {
            projectId
            workflowId
        }
    }
    """

    variables = {
        "input": {
            "serializedConfig": {
                "services": {
                    # -------------------------
                    # HORILLA SERVICE
                    # -------------------------
                    "fjlkasdfjalskdjfalksjdfkjadskf": {
                        "name": service_name,
                        "source": {"image": service_image},
                        "variables": {
                            "DATABASE_URL": {"value": f"${{{{{postgres_ref}.DATABASE_URL}}}}"},
                            "CSRF_TRUSTED_ORIGINS": {"value": CSRF_TRUSTED_ORIGINS},
                        },
                        "networking": {
                            "tcpProxies": {"8000": {}},
                            "serviceDomains": {
                                "0": {} 
                            }
                        }
                    },

                    # -------------------------
                    # POSTGRES SERVICE
                    # -------------------------
                    "jfdajfkasjdflkjsadflkjasd": {
                        "icon": "https://devicons.railway.app/i/postgresql.svg",
                        "name": f"Postgres-{service_name}",
                        "build": {},
                        "source": {
                            "image": "ghcr.io/railwayapp-templates/postgres-ssl:17"
                        },
                        "variables": {
                            "PGDATA": {"value": "/var/lib/postgresql/data/pgdata"},
                            "PGHOST": {"value": "${{RAILWAY_PRIVATE_DOMAIN}}"},
                            "PGPORT": {"value": "5432"},
                            "PGUSER": {"value": "${{ POSTGRES_USER }}"},
                            "PGDATABASE": {"value": "${{POSTGRES_DB}}"},
                            "PGPASSWORD": {"value": "${{POSTGRES_PASSWORD}}"},
                            "POSTGRES_DB": {"value": "railway"},
                            "DATABASE_URL": {
                                "value": "postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}"
                            },
                            "POSTGRES_USER": {"value": "postgres"},
                            "SSL_CERT_DAYS": {"value": "820"},
                            "POSTGRES_PASSWORD": {
                                "value": "${{ secret(32, \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\") }}"
                            },
                            "DATABASE_PUBLIC_URL": {
                                "value": "postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_TCP_PROXY_DOMAIN}}:${{RAILWAY_TCP_PROXY_PORT}}/${{PGDATABASE}}"
                            },
                            "RAILWAY_DEPLOYMENT_DRAINING_SECONDS": {"value": "60"}
                        },
                        "networking": {
                            "tcpProxies": {"5432": {}},
                            "serviceDomains": {}
                        },
                        "volumeMounts": {
                            "fdsakfjlasdlkfjalksdfj": {"mountPath": "/var/lib/postgresql/data"}
                        }
                    }
                }
            },
            "workspaceId": WORKSPACE_ID,
            "templateId": RAILWAY_TEMPLATE_ID,
            "environmentId":environment_id,
            "projectId": project_id
        }
    }

    data = {
        "query": mutation,
        "variables": variables,
        "operationName": "templateDeployV2"
    }

    deploy = send_request_to_railway(data)
    workflow_id = deploy['data']['templateDeployV2']['workflowId']
    
    if deploy is None:
        return None
    return workflow_id


def update_service_id(org_id):
    if Service.objects.filter(organization_id=org_id).exists():
        if Service.objects.filter(organization_id=org_id).first().service_id:
            return
    project_id = org_id.project_id

    query = """
        query project($id: String!) {
            project(id: $id) {
                services {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
                volumes {
                    edges {
                        node {
                            id
                            name
                            volumeInstances {
                                edges {
                                    node {
                                        id
                                        environmentId
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """

    data = {
        "query": query,
        "variables": {"id": project_id.project_id}
    }

    result = send_request_to_railway(data)
    service_name =org_id.name
    project_data = result['data']['project']
    services = project_data.get('services', {}).get('edges', [])
    volumes = project_data.get('volumes', {}).get('edges', [])
    s = Service.objects.create(organization_id=org_id)
    for service in services:
        name = service['node']['name']
        sid = service['node']['id']
        if name == service_name:
            print('updating service id')
            s.service_id = sid
            s.organization_id=org_id
            s.save()
        elif name == f"Postgres-{service_name}":
            s.postgres_service_id = sid
    for volume in volumes:
        if volume['node']['name'] == f"postgres-{service_name.lower()}-volume":
            s.volume_id = volume['node']['id']

            # Check for volume instances
            for vol_instance in volume['node']['volumeInstances']['edges']:
                if vol_instance['node']['environmentId'] == project_id.environment_id:
                    # project_id.volume_instance_id = vol_instance['node']['id']
                    break
    s.save()
        


def update_service_variable(org,service_id,variable_name,variable_value):
    """Update or create an environment variable for a service"""
    mutation = """
    mutation variableUpsert($input: VariableUpsertInput!) {
        variableUpsert(input: $input)
    }
    """

    environment_id = org.project_id.environment_id

    data = {
        "query": mutation,
        "variables": {
            "input": {
                "projectId": org.project_id.project_id,
                "environmentId": environment_id,
                "serviceId": service_id,
                "name": variable_name,
                "value": variable_value
            }
        }
    }

    try:
        response = send_request_to_railway(data)
        return True
    except Exception as e:
        print(f"Error updating variable: {e}")
        return False
    

def delete_organization(org):
    delete_services(org)
    delete_volume(org)

def delete_services(org):
    """Delete Railway services and volume for an instance"""
    services = Service.objects.filter(organization_id=org)
    services_to_delete  = []
    for service in services:
        service_id = service.service_id
        services_to_delete.append({
            'alias': f"svc_{service.id}",
            'id': service.service_id
        })
        services_to_delete.append({
            'alias': f"svc_postgres_{service.id}",
            'id': service.postgres_service_id
        })
        
    
    
    # Build mutation for deleting multiple services
    mutations = []
    for service in services_to_delete:
        mutations.append(f'{service["alias"]}: serviceDelete(id: "{service["id"]}")')
    
    mutation_query = f"""
    mutation deleteServices {{
        {' '.join(mutations)}
    }}
    """
    
    data = {
        "query": mutation_query
    }
    
    result = send_request_to_railway(data)
   
def delete_volume(org):
    """Delete Railway volume for an instance"""
    service = Service.objects.filter(organization_id=org).first()
    mutation_query = """
    mutation volumeDelete($volumeId: String!) {
        volumeDelete(volumeId: $volumeId)
    }
    """
    
    data = json.dumps({
        "query": mutation_query,
        "variables": {"volumeId": service.volume_id}
    })
    result = send_request_to_railway(data)
    
def deployment_status(service):

    query = """
    query GetDeployments($serviceId: String!) {
      service(id: $serviceId) {
        deployments(first: 1) {
          edges {
            node {
              status
            }
          }
        }
      }
    }
    """

    data = {
        "query": query,
        "variables": {
            "serviceId": service.service_id
        }
    }

    response = send_request_to_railway(data)

    return response["data"]["service"]["deployments"]["edges"][0]["node"]["status"]