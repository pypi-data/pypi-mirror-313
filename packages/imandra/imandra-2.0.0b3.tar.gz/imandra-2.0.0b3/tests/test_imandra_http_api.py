import unittest
import imandra
import imandra.auth
import imandra.instance
import time
import imandra_http_api_client
from imandra_http_api_client.rest import ApiException
from pprint import pprint
import subprocess
import time

def run_verify_for(config):
    # Enter a context with an instance of the API client
    with imandra_http_api_client.ApiClient(config) as api_client:
        # Create an instance of the API class
        api_instance = imandra_http_api_client.DefaultApi(api_client)
        req = {
            "src": "fun x -> List.rev (List.rev x) = x",
            "syntax": "iml",
            "hints": {
                "method": {
                    "type": "auto"
                }
            }
        }
        print("Request: ")
        print(req)
        verify_request_src = imandra_http_api_client.VerifyRequestSrc.from_dict(req)

        try:
            # Verify a string of source code
            api_response = api_instance.verify_by_src(verify_request_src)
            print("The response of DefaultApi->verify:\n")
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling DefaultApi->verify: %s\n" % e)


class TestImandraHttpApiCloudHosted(unittest.TestCase):
    def setUp(self):
        self.auth = imandra.auth.Auth()
        self.instance = imandra.instance.create(self.auth, None, "imandra-http-api")

    def tearDown(self):
        imandra.instance.delete(self.auth, self.instance['new_pod']['id'])

    def test(self):
        cloud_api_config = imandra_http_api_client.Configuration(
            host = self.instance['new_pod']['url'],
            access_token =  self.instance['new_pod']['exchange_token'],
        )
        run_verify_for(cloud_api_config)

class TestImandraHttpApiLocal(unittest.TestCase):
    def setUp(self):
        self.auth = imandra.auth.Auth()
        self.instance = subprocess.Popen("/usr/local/bin/imandra-http-api --skip-update", shell=True)
        time.sleep(10)

    def tearDown(self):
        self.instance.terminate()
        try:
            self.instance.wait(timeout=5)
        except TimeoutExpired as e:
            self.instance.kill()

    def test(self):
        local_api_config = imandra_http_api_client.Configuration(
            host = 'http://localhost:3000',
        )
        run_verify_for(local_api_config)



if __name__ == '__main__':

    unittest.main()
