import requests
from typing import List, Dict, Optional

from lms_hub.controllers.learning_env import LearningEnv
from lms_hub.models.deadline import Deadline
from lms_hub.models.credentials import UVLeCredentials
from lms_hub.models.learning_env_class import LearningEnvClass, Platform

@LearningEnv.register
class UVLeClient:
    def __init__(self, creds: UVLeCredentials):
        self.credentials = creds
        self._user_id = None
    
    @property
    def user_id(self) -> str:
        if self._user_id is None:
            # Cache user ID from server response
            response = self.uvle_request("core_webservice_get_site_info")
            self._user_id = response.json()["userid"]
        return self._user_id

    def uvle_request(
        self,
        func: str,
        id_required: bool = False,
        params:Optional[Dict[str, any]] = None
    ) -> requests.Response:
        if params is None:
            params = {}
        
        request_params = {
            "wstoken": self.credentials.token,
            "wsfunction": func,
            "moodlewsrestformat": "json",
        }

        if id_required:
            request_params["userid"] = self.user_id
        
        # Update params with any additional parameters
        request_params.update(params)

        # Create request and send it to the remote server
        return requests.get(
            f"https://{self.credentials.server}/webservice/rest/server.php",
            params=request_params,
        )

    def _get_category_name(self, category_id: int) -> Optional[str]:
        response = self.uvle_request(
            "core_course_get_categories",
            params={"criteria[0][key]": "id", "criteria[0][value]": category_id},
        )

        # We should never get more than one matching category per ID,
        # but just in case...
        for category in response.json():
            if category["id"] == category_id:
                return category["name"]
        return None

    def get_classes(self) -> List[LearningEnvClass]:
        classes = []

        # Construct MoodleClass instances from server response
        response = self.uvle_request(
            "core_enrol_get_users_courses", id_required=True
        )
        courses = response.json()
        for course in courses:
            classes.append(
                LearningEnvClass(
                    class_id=course["id"],
                    platform=Platform.UVLE,
                    name=course["fullname"],
                    # The Moodle API (if you can call it that) does not return the URL to the
                    # course, so we just construct it using the course ID.
                    url=f'https://{self.credentials.server}/course/view.php?id={course["id"]}',
                    # The 'description' in Moodle is actually
                    # the name of the category that the course belongs to.
                    description=self._get_category_name(course["category"]),
                )
            )

        return classes

    def get_deadlines(self) -> List[Deadline]:
        raw_deadlines = []

        # timesortfrom and aftereventid lets us not repeat requests for
        # the same deadlines
        timesortfrom = 0
        aftereventid = 0
        limitnum = 20
        while True:
            # Request next 20 deadlines
            r = self.uvle_request(
                'core_calendar_get_action_events_by_timesort',
                id_required=True,
                params={
                    'timesortfrom' : timesortfrom,
                    'aftereventid' : aftereventid,
                    'limitnum' : limitnum
            }).json()
            new_deadlines = r['events']
            raw_deadlines.extend(new_deadlines)

            # If it returns less than 20 deadlines, then there are no more
            # deadlines to request. 
            if len(new_deadlines) < limitnum:
                break
            timesortfrom = new_deadlines[-1]['timesort']
            aftereventid = r['lastid']
        
        deadlines = []
        for raw_deadline in raw_deadlines:
            name = raw_deadline['name']
            if name.endswith(' is due'):
                name = name[:-7]

            deadlines.append(Deadline(
                course_name=raw_deadline['course']['fullname'],
                course_url=raw_deadline['course']['viewurl'],
                name=name,
                url=raw_deadline['viewurl'],
                timestamp=raw_deadline['timesort'],
                description=raw_deadline['description'],
                platform=Platform.UVLE,
                moduletype=raw_deadline['modulename']
            ))

        return deadlines