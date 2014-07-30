from datetime import date, datetime


def str2date(text):
    return datetime.strptime(text, "%Y-%m-%d").date()

        
class ApiException(Exception):

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class HSApi:
    
    def __init__(self, remote_app):
        self._remapp = remote_app
        
    def get(self, *args, **kwargs):
        req = self._remapp.get(*args, **kwargs)
        if req.status == 200:
            return req.data
        else:
            raise ApiException('api call failed with status code {0}'.format(req.status))
        
    def post(self, *args, **kwargs):
        req = self._remapp.post(*args, **kwargs)
        if req.status == 200:
            return req.data
        else:
            raise ApiException('api call failed with status code {0}'.format(req.status))
    
    def batches(self):
        return self.get('batches')

    def active_batches(self):
        today = date.today()
        return [b for b in self.batches() if str2date(b['start_date']) <= today and today <= str2date(b['end_date'])]
    
    def batch_members(self, batch):
        path = 'batches/{0}/people'.format(batch['id'])
        return self.get(path)

    def active_batch_members(self):
        return [p for b in self.active_batches() for p in self.batch_members(b)]
    
    def refresh_token(self, token):
        return self.post(self._remapp.access_token_url, 
                         data={ 'grant_type':'refresh_token',
                                'refresh_token': token[1],
                                'client_id': self._remapp.consumer_key, 
                                'client_secret': self._remapp.consumer_secret },
                         token=token)
