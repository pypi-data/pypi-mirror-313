"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

AV_GET_APP_BY_NAME_API_URL = "/v1/applications?include_complete=true&sort=updatedAt,desc&org_id={}&{}&"
AV_GET_APP_BY_NAME_SEARCH_PARAM_API_URL = "search=name $in "
AV_DELETE_APP_API_URL = "/v1/applications/{}?org_id={}"
AV_GET_APPS_API_URL = "/v1/applications?{}&include_complete=true&sort=updatedAt,desc&org_id={}"
AV_IMPORT_API_URL = "v1/import/app-packages"
AV_IMPORT_STATUS_API_URL = "v1/import/app-packages/status/"
AV_CREATE_APP_ENTITLEMENT_API_URL = "v1/app-entitlements/create-bulk"
AV_GET_ENTITLEMENT_API_URL = "v1/app-entitlements"
AV_DELETE_ENTITLEMENT_API_URL = "v1/app-entitlements/delete-bulk"
AV_GET_FILESHARE_API_URL = "v1/fileshares"

AV_IMPORT_AVAILABLE = "IMPORT_AVAILABLE"
ERROR = "ERROR"
PROVISION_SUCCESS = "PROVISION_SUCCESS"
PROVISION_FAILED = "PROVISION_FAILED"
COMPLETE = "COMPLETE"
INCOMPLETE = "INCOMPLETE"
SUCCESS = "success"
START = "START"
MS_STORAGE_ACCOUNTS = "Microsoft.Storage/storageAccounts"
CONN_STR_1 = "DefaultEndpointsProtocol=https;AccountName="
CONN_STR_2 = ";AccountKey="
CONN_STR_3 = ";EndpointSuffix=core.windows.net"
FS_COPY_TRANSITION_STATUS = ["INCOMPLETE", "START"]
STATUS = "status"
FORWARD_SLASH = "/"
