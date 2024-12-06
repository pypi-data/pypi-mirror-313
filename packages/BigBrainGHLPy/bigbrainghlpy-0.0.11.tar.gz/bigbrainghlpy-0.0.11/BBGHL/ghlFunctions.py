"""
This is a basic wrapper for GoHighLevel V1 API, it was created for my convenience, and basic use.

Based on: https://public-api.gohighlevel.com/

"""

__author__="xtrakTD"
__status__ = "ongoing"


import requests 
from typing import Union, Optional
from datetime import datetime
from dateutil.tz import tzutc
import json 



class GHL:
    
    """
    Class for GHL wrapper 
    """


    def __init__(self, token):
        '''Call the client with V1 token'''
        self.token = token
        self.endpoint = "https://rest.gohighlevel.com/v1"
        self.headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.token)}
    
     
    '''
    Calendar Endpoints + Appointments + Contacts
    '''

    def get_calendars(self,type="services"):
        '''Get Calendars associated with your token
        type teams or services
        Default services
        '''
        try:
            url = self.endpoint+f"/calendars/{type}"
            response = requests.request("GET", url, headers=self.headers)
            return response.json() 
        except Exception as e:
            return e


    def get_calendarFreeSlots(self,calendarId,startDate, endDate):
        '''
        Get available slots in the calendar
        format for date: YYYY-MM-DD
        '''
        
        epoch1970 = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        epochStart= int((datetime.strptime(startDate, "%Y-%m-%d").replace(tzinfo=tzutc()) - epoch1970).total_seconds()*1000)
        epochEnd = int((datetime.strptime(endDate, "%Y-%m-%d").replace(tzinfo=tzutc()) - epoch1970).total_seconds()*1000)
        
        try:
        
            url = self.endpoint+f"/appointments/slots?calendarId={calendarId}&startDate={epochStart}&endDate{epochEnd}"
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e


    def get_calendarBookedSlots(self,calendarId:None,startDate, endDate, userId,teamId, includeState=True):
        '''
        Get  booked slots in the calendar
        format for date: YYYY-MM-DD
        state of include all is True by default
        '''

        epoch1970 = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        epochStart= int((datetime.strptime(startDate, "%Y-%m-%d").replace(tzinfo=tzutc()) - epoch1970).total_seconds()*1000)
        epochEnd = int((datetime.strptime(endDate, "%Y-%m-%d").replace(tzinfo=tzutc()) - epoch1970).total_seconds()*1000)
        
        try:
            url = self.endpoint+f"/appointments/startDate={epochStart}&endDate{epochEnd}&userId={userId}&calendarId={calendarId}&teamId={teamId}&includeAll={includeState}"
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e

    '''
    Appointments
    '''

    def bookAppointment(self,email,phone,selectedSlot,selectedTimeZone,
                        calendarId,firstName=None,lastName=None,
                        name=None,title=None,address1=None,
                        city=None,state=None,website=None,
                        calendarNotes=None):

        '''
        
        Book an Appointment
        '''
        url = self.endpoint+"/appointments/"

        try:
            payload = json.dumps({
                "selectedTimezone": f"{selectedTimeZone}",
                "selectedSlot": f"{selectedSlot}",
                "calendarId": f"{calendarId}",
                "email": f"{email}",
                "phone": f"{phone}",
                "firstName": f"{firstName}",
                "lastName": f"{lastName}",
                "name": f"{name}",
                "title": f"{title}",
                "address1": f"{address1}",
                "city": f"{city}",
                "state": f"{state}",
                "website": f"{website}",
                "calendarNotes": f"{calendarNotes}"   
            })
            response = requests.request("POST", url, headers=self.headers, data=payload)
            return response.json()

        except Exception as e:
            return e
    

    def get_appointmentById(self,appointmentId):
        '''
        
        Retrieve an appointment by it's ID

        '''
        url = self.endpoint+f"/appointments/{appointmentId}"
        
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json() 
        except Exception as e:
            return e


    def update_appointmentById(self, appointmentId,selectedSlot,selectedTimezone=None):
        '''
        Update an appointment by ID
        
        '''
        url = self.endpoint+f"/appointments/{appointmentId}"

        try:
            if selectedTimezone == None:
                payload = json.dumps({

                    "selectedSlot": f"{selectedSlot}"
                })
            else: 
                payload = json.dumps({

                    "selectedSlot": f"{selectedSlot}",
                    "selectedTimezone": f"{selectedTimezone}"
                })
        
            response = requests.request("PUT", url, headers=self.headers, data=payload)
            return response.json() 

        except Exception as e:
            return e

    
    def delete_appointmentById(self, appointmentId):
        '''
        Delete an appointment by it's Id
        '''

        url = self.endpoint+f"/appointments/{appointmentId}"
        
        try:
            response = requests.request("DELETE", url, headers=self.headers)
            return response.json() 
        except Exception as e:
            return e

    
    def update_appointmentStatusById(self,appointmentId,status):
        
        '''
        Update an appointment's status
        '''


        url = self.endpoint+f"/appointments/{appointmentId}/status"
        
        try:
            payload = json.dumps({
                "status": f"{status}"
            })

            response = requests.request("PUT", url, headers=self.headers, data=payload)
            return response.json() 
        except Exception as e:
            return e


    '''
    Contacts
    '''


    def create_contactByName(self,firstName,lastName,
                        email,phone,name=None):
        '''
        Create a contact
        '''
        url = self.endpoint+"/contacts/"
        try:

            payload = json.dumps({
                "firstName": f"{firstName}",
                "lastName": f"{lastName}",
                "name": f"{name}",
                "email": f"{email}",
                "phone": f"{phone}"
            })

            response = requests.request("POST", url, headers=self.headers, data=payload)
            return response.json()

        except Exception as e:
            return e


    def lookup_contactByEmail(self,email):
        '''
        find contact by email
        '''
        url = self.endpoint+f"/contacts/lookup?email={email}"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e


    def lookup_contactByEmail(self,phone):
        '''
        find contact by phone
        '''
        url = self.endpoint+f"/contacts/lookup?email={phone}"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e
    

    def lookup_contactById(self,contactId):
        '''
        find contact by phone
        '''
        url = self.endpoint+f"/contacts/{contactId}"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e


    def contact_appointments(self,contactId):
        '''
        Get contact's appointments
        '''
        url = self.endpoint+f"/contacts/{contactId}/appointments/"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json() 
        except Exception as e:
            return e 
        

    def contact_tasks(self, contactId):
        '''
        Get contact's tasks
        '''
        url = self.endpoint+f"/contacts/{contactId}/tasks/"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json() 
        except Exception as e:
            return e 
        

    def get_taskById(self, contactId, taskId):
        '''
        Get single task details
        '''
        url = self.endpoint+f"/contacts/{contactId}/tasks/{taskId}"
        try:
            response = requests.request("GET", url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e

    
    
    def add_contactTag(self,contactId,tag):
        '''
        add tag to contact
        '''
        url = self.endpoint+f"/contacts/{contactId}/tags/"
        try:
            payload = json.dumps({
                "tags": [f"{tag}"]
            })

            response = requests.request("POST", url, headers=self.headers, data=payload)
            return response.json() 

        except Exception as e:
            return e
    
    
    def remove_contactTag(self,contactId,tag):
        '''
        Remove tag from a contact
        '''
       
        url = self.endpoint+f"/contacts/{contactId}/tags/"
        try:
            payload = json.dumps({
                "tags": [f"{tag}"]
            })

            response = requests.request("DELETE", url, headers=self.headers, data=payload)
            return response.json() 

        except Exception as e:
            return e 

    
    def get_contacts(self, after: Optional[Union[int, datetime]] = None, after_id: Optional[str] = None):
        '''
        Get all contacts
        :param after: - timestamp or datetime 
        :param after_id: - str Contact ID 
        :return: - list of GHL contacts. if no params are present - all contacts will be pulled
        '''

        url = self.endpoint+f"/contacts/"
        params = {
            "limit": 100,
        }

        if after_id:
            params['startAfterId'] = after_id
        if after:
            if isinstance(after, int):
                params['startAfter'] = after * 1000
            elif isinstance(after, datetime):
                params['startAfter'] = datetime.timestamp(after) * 1000
        
        _contacts = []

        try:
            response = requests.request(method='GET', url=url, headers=self.headers, params=params)
            _contacts.extend(response.json().get('contacts'))
            
            if response.json().get('meta', {}).get('nextPageUrl', None) is not None:
                while response.json().get('meta', {}).get('nextPageUrl', None) is not None:
                    _url = (response.json()['meta']['nextPageUrl']).replace('http:', 'https:')
                    response = requests.request(method='GET', url=_url, headers=self.headers)
                    _contacts.extend(response.json().get('contacts'))
            return _contacts
        except Exception as e:
            return e


    '''
    Opportunities
    '''


    def get_pipelines(self, id_only: bool = False):
        '''
        Get all pipelines
        :param id_only: - bool if set only pipeline ID is returned
        '''

        url = self.endpoint+f'/pipelines/'

        try:
            response = requests.request(method='GET', url=url, headers=self.headers)
            return response.json() if not id_only else [x.get('id') for x in response.json().get('pipelines', {})]
        except Exception as e:
            return e
        
    def get_opportunitiesByPipelline(self, pipeline_id: str, after: Optional[Union[int, datetime]] = None, after_id: Optional[str] = None):
        '''
        Get all opportunities for a pipeline 
        :param pipeline_id: - ID of the pipeline
        :param after: - timestamp or datetime 
        :param after_id: - str Opportunity ID 
        '''

        url = self.endpoint+f'/pipelines/{pipeline_id}/opportunities/'

        params = {
            "limit": 100,
        }

        if after_id:
            params['startAfterId'] = after_id
        if after:
            if isinstance(after, int):
                params['startAfter'] = after * 1000
            elif isinstance(after, datetime):
                params['startAfter'] = datetime.timestamp(after) * 1000
        
        _opportunities = []

        try:
            response = requests.request(method='GET', url=url, headers=self.headers, params=params)
            _opportunities.extend(response.json().get('opportunities'))
            
            if response.json().get('meta', {}).get('nextPageUrl', None) is not None:
                while response.json().get('meta', {}).get('nextPageUrl', None) is not None:
                    _url = (response.json()['meta']['nextPageUrl']).replace('http:', 'https:')
                    response = requests.request(method='GET', url=_url, headers=self.headers)
                    _opportunities.extend(response.json().get('opportunities'))
            return _opportunities
        except Exception as e:
            return e

    '''
    Users
    '''

    def get_staffUsers(self):
        '''
        Get all staff users
        '''

        url = self.endpoint+f'/users/'

        try:
            response = requests.request(method='GET', url=url, headers=self.headers)
            return response.json()
        except Exception as e:
            return e
    