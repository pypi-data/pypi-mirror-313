import json
import os
import os.path
import urllib
import urllib.parse
import urllib.request
import urllib.error
import time


def status(auth, job_id):
    path = "api/ipl/jobs/{}/status".format(job_id)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = {"X-Auth": auth.token}

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    return json.loads(resp)["status"]


def wait(auth, job_id, interval=10):
    time.sleep(interval)
    s = status(auth, job_id)
    if s in ["queued", "processing"]:
        return wait(auth, job_id)
    else:
        return s


def decompose(auth, file, testgen_lang, organization, callback, doc_gen, parent_job_id):
    path = "api/ipl/jobs"

    params_dict = {"lang": "ipl"}
    if parent_job_id is not None:
        params_dict["parent-job-id"] = parent_job_id

    if file is not None:
        filename = os.path.basename(file)
        params_dict["filename"] = filename
        with open(file, "r") as ipl_file:
            content = ipl_file.read()
        data = content.encode("utf-8")
    else:
        data = b""

    if testgen_lang is not None:
        params_dict["testgen-lang"] = testgen_lang

    if doc_gen is not None:
        params_dict["doc-gen"] = doc_gen

    if organization is not None:
        params_dict["organization-id"] = organization

    if callback is not None:
        params_dict["callback"] = callback

    params = urllib.parse.urlencode(params_dict)
    url = "{}/{}?{}".format(auth.imandra_web_host, path, params)
    headers = {"X-Auth": auth.token}
    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    job_id = response.read().decode("utf-8")
    return job_id


def data(auth, job_id, file=None):
    params = f"file={file}" if file is not None else ""
    path = "api/ipl/jobs/{}/data?{}".format(job_id, params)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = {"X-Auth": auth.token}

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
        content = response.read()
        content_type = response.headers.get("Content-Type")
        return {
            "content_type": content_type,
            "content": content,
        }
    except urllib.error.HTTPError as e:
        if e.code == 302:
            content = e.read()
            content_type = e.headers.get("Content-Type")
            return {
                "content_type": content_type,
                "content": content,
            }
        else:
            raise ValueError(e.read().decode("utf-8"))


def simulator(auth, file):
    path = "simulator/create"
    with open(file, "r") as ipl_file:
        content = ipl_file.read()
    url = "{}/{}".format(auth.imandra_web_host, path)

    req = {"payload": content, "cluster": auth.zone, "version": "latest"}

    data = json.dumps(req)
    clen = len(data)
    data = data.encode("utf-8")
    headers = {
        "X-Auth": auth.token,
        "Content-Type": "application/json",
        "Content-Length": clen,
    }

    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    resp = json.loads(response.read())
    return resp


def list_jobs(auth, limit=10, job_type=None):
    path = f"api/ipl/jobs?limit={limit}"
    if job_type:
        path = f"{path}&job-type={job_type}"
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = {"X-Auth": auth.token}

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    resp = json.loads(response.read())
    return resp


def unsat_analysis(auth, file, organization, callback):
    path = "api/ipl-unsat-analysis/jobs"

    params_dict = {"lang": "ipl"}

    if file is not None:
        filename = os.path.basename(file)
        params_dict["filename"] = filename
        with open(file, "r") as ipl_file:
            content = ipl_file.read()
        data = content.encode("utf-8")
    else:
        data = b""

    if organization is not None:
        params_dict["organization-id"] = organization

    if callback is not None:
        params_dict["callback"] = callback

    params = urllib.parse.urlencode(params_dict)
    url = "{}/{}?{}".format(auth.imandra_web_host, path, params)
    headers = {"X-Auth": auth.token}
    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    job_id = response.read().decode("utf-8")
    return job_id


def log_analysis_builder(
    auth, file, organization=None, callback=None, decomp_job_id=None
):
    path = "api/ipl-log-analysis-builder/jobs"

    filename = os.path.basename(file)
    params_dict = {"filename": filename}
    with open(file, "r") as ipl_file:
        content = ipl_file.read()
        file_contents = content.encode("utf-8")

    if organization is not None:
        params_dict["organization-id"] = organization

    if callback is not None:
        params_dict["callback"] = callback

    if decomp_job_id is not None:
        params_dict["decomp-job-id"] = decomp_job_id

    params = urllib.parse.urlencode(params_dict)
    url = "{}/{}?{}".format(auth.imandra_web_host, path, params)
    headers = {"X-Auth": auth.token}
    request = urllib.request.Request(url, file_contents, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    job_id = response.read().decode("utf-8")
    return job_id


def cancel(auth, job_id):
    path = "api/ipl/jobs/{}/cancel".format(job_id)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = {"X-Auth": auth.token}

    request = urllib.request.Request(url, headers=headers, method="POST", data=None)

    try:
        response = urllib.request.urlopen(request)
        content = response.read()
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))
