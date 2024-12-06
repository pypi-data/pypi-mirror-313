"""
The HEA Server Buckets Microservice provides ...
"""
import logging

from heaobject.data import AWSS3FileObject
from heaserver.service import response, client, appproperty
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, aws
from heaserver.service.wstl import builder_factory, action
from heaobject.folder import AWSS3BucketItem, Folder, AWSS3Folder
from heaobject.project import AWSS3Project
from heaobject.keychain import AWSCredentials
from heaobject.bucket import AWSBucket
from heaobject.error import DeserializeException
from heaobject.root import Tag, ViewerPermissionContext, Permission, ShareImpl, DesktopObjectDict
from heaobject.activity import Status
from heaobject.user import NONE_USER, AWS_USER, CREDENTIALS_MANAGER_USER
from heaobject.util import parse_bool
from heaobject.person import Role, Group, Person, AddingCollaborator, RemovingCollaborator, encode_group, encode_role
from heaobject.account import AWSAccount
from heaobject.volume import Volume, AWSFileSystem
from heaobject.organization import Organization
from heaserver.service.appproperty import HEA_CACHE, HEA_DB
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.heaobjectsupport import new_heaobject_from_type, type_to_resource_url
from heaserver.service.sources import AWS_S3
from heaserver.service.messagebroker import publish_desktop_object, publisher_cleanup_context_factory
from heaserver.service.activity import DesktopObjectActionLifecycle
from botocore.exceptions import ClientError as BotoClientError
import asyncio
from typing import Any, Coroutine, cast
from yarl import URL
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.type_defs import ObjectIdentifierTypeDef, DeleteTypeDef, PublicAccessBlockConfigurationTypeDef, VersioningConfigurationTypeDef, TagTypeDef
from mypy_boto3_iam.client import IAMClient
from mypy_boto3_iam.type_defs import PolicyDocumentTypeDef, PolicyDocumentDictTypeDef, PolicyTypeDef
from functools import partial
from aiohttp.client_exceptions import ClientError, ClientResponseError
from datetime import datetime
from .context import S3BucketPermissionsContext
import orjson
from collections.abc import Collection, AsyncGenerator
from itertools import chain
import re
from dataclasses import dataclass

MONGODB_BUCKET_COLLECTION = 'buckets'

ISS = 'OIDC_CLAIM_iss'
AZP = 'OIDC_CLAIM_azp'

_update_collaborators_lock = asyncio.Lock()


@routes.get('/volumes/{volume_id}/buckets/{id}')
@action('heaserver-buckets-bucket-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{id}/opener')
@action(name='heaserver-buckets-bucket-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-buckets-bucket-get-create-choices', rel='hea-creator-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{id}/creator')
@action(name='heaserver-buckets-bucket-get-trash', rel='hea-trash hea-context-menu', path='volumes/{volume_id}/awss3trash')
@action(name='heaserver-buckets-bucket-get-self', rel='self', path='volumes/{volume_id}/buckets/{id}')
@action(name='heaserver-buckets-bucket-get-volume', rel='hea-volume', path='volumes/{volume_id}')
@action(name='heaserver-buckets-bucket-get-awsaccount', rel='hea-account', path='volumes/{volume_id}/awsaccounts/me')
@action(name='heaserver-buckets-bucket-get-uploader', rel='hea-uploader', path='volumes/{volume_id}/buckets/{id}/uploader')
async def get_bucket(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified id.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_bucket(request=request)


@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}')
@action(name='heaserver-buckets-bucket-get-self', rel='self', path='volumes/{volume_id}/buckets/{id}')
@action(name='heaserver-buckets-bucket-get-volume', rel='hea-volume', path='volumes/{volume_id}')
@action(name='heaserver-buckets-bucket-get-awsaccount', rel='hea-account', path='volumes/{volume_id}/awsaccounts/me')
async def get_bucket_by_name(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified name.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - heaserver-buckets
    parameters:
        - name: bucket_name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: Name of the bucket
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_bucket(request=request)


@routes.get('/volumes/{volume_id}/buckets/{id}/opener')
@action('heaserver-buckets-bucket-open-content', rel=f'hea-opener hea-context-aws hea-default {Folder.get_mime_type()}',
        path='volumes/{volume_id}/buckets/{id}/awss3folders/root/items/')
async def get_bucket_opener(request: web.Request) -> web.Response:
    """
    Gets bucket opener choices.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Bucket opener choices
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _bucket_opener(request)


@routes.get('/volumes/{volume_id}/buckets/{id}/creator')
@action('heaserver-buckets-bucket-create-folder', rel='hea-creator hea-default application/x.folder',
        path='volumes/{volume_id}/buckets/{id}/newfolder')
@action('heaserver-buckets-bucket-create-project', rel='hea-creator hea-default application/x.project',
        path='volumes/{volume_id}/buckets/{id}/newproject')
async def get_bucket_creator(request: web.Request) -> web.Response:
    """
    Gets bucket creator choices.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Bucket creator choices
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _bucket_opener(request)

@routes.get('/volumes/{volume_id}/buckets/{id}/uploader')
@routes.get('/volumes/{volume_id}/buckets/{id}/uploader/')
@action('heaserver-buckets-bucket-get-upload-form')
async def get_folder_uploader_form(request: web.Request) -> web.Response:
    """
    Gets blank form for uploading to Bucket

    :param request: the HTTP request. Required.
    :return: a blank form for uploading a Bucket item or Not Found if the requested item does not
    exist.
    """
    return await _get_bucket(request)


@routes.get('/volumes/{volume_id}/buckets/{id}/newfolder')
@routes.get('/volumes/{volume_id}/buckets/{id}/newfolder/')
@action('heaserver-buckets-bucket-new-folder-form')
async def get_new_folder_form(request: web.Request) -> web.Response:
    """
    Gets form for creating a new folder within this bucket.

    :param request: the HTTP request. Required.
    :return: the current folder, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: A folder.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_bucket(request)

@routes.get('/volumes/{volume_id}/buckets/{id}/newproject')
@routes.get('/volumes/{volume_id}/buckets/{id}/newproject/')
@action('heaserver-buckets-bucket-new-project-form')
async def get_new_project_form(request: web.Request) -> web.Response:
    """
    Gets form for creating a new project within this bucket.

    :param request: the HTTP request. Required.
    :return: the current project, with a template for creating a child project or Not Found if the requested item does not
    exist.
    ---
    summary: A folder.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_bucket(request)


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/newfolder')
@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/newfolder/')
async def post_new_folder(request: web.Request) -> web.Response:
    """
    Gets form for creating a new folder within this bucket.

    :param request: the HTTP request. Required.
    :return: the current folder, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: A folder.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    requestBody:
        description: A new folder.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.folder.AWSS3Folder"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "Joe",
                    "type": "heaobject.folder.AWSS3Folder"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info['bucket_id']
    folder_url = await type_to_resource_url(request, AWSS3Folder)
    if folder_url is None:
        raise ValueError('No AWSS3Folder service registered')
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    resource_base = str(URL(folder_url) / volume_id / 'buckets' / bucket_id / 'awss3folders' / 'root' / 'newfolder')
    folder = await new_heaobject_from_type(request, type_=AWSS3Folder)
    try:
        id_ = await client.post(request.app, resource_base, data=folder, headers=headers)
        return await response.post(request, id_, resource_base)
    except ClientResponseError as e:
        return response.status_generic_error(status=e.status, body=e.message)
    except ClientError as e:
        return response.status_generic(status=500, body=str(e))

@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/newproject')
@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/newproject/')
async def post_new_project(request: web.Request) -> web.Response:
    """
    Gets form for creating a new project within this bucket.

    :param request: the HTTP request. Required.
    :return: the current project, with a template for creating a child project or Not Found if the requested item does not
    exist.
    ---
    summary: A project.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    requestBody:
        description: A new project.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Project example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.project.AWSS3Project"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "Joe",
                    "type": "heaobject.project.AWSS3Project"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info['bucket_id']
    project_url = await type_to_resource_url(request, AWSS3Project)
    if project_url is None:
        raise ValueError('No AWSS3Project service registered')
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    resource_base = str(URL(project_url) / volume_id / 'buckets' / bucket_id / 'awss3projects')
    project = await new_heaobject_from_type(request, type_=AWSS3Project)
    try:
        id_ = await client.post(request.app, resource_base, data=project, headers=headers)
        return await response.post(request, id_, resource_base)
    except ClientResponseError as e:
        return response.status_generic_error(status=e.status, body=e.message)
    except ClientError as e:
        return response.status_generic(status=500, body=str(e))


@routes.post('/volumes/{volume_id}/buckets/{id}/uploader')
@routes.post('/volumes/{volume_id}/buckets/{id}/uploader/')
async def post_bucket_uploader(request: web.Request) -> web.Response:
    """
    :param request:
    :return:
    ---
    summary: A folder.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    requestBody:
        description: Upload file to bucket.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.folder.AWSS3ItemInFolder"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "Joe",
                    "type": "heaobject.folder.AWSS3ItemInFolder",
                    "folder_id": "root"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info['id']

    folder_url = await type_to_resource_url(request, AWSS3Folder)
    if folder_url is None:
        raise ValueError('No AWSS3Folder service registered')
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None

    resource_base = str(URL(folder_url) / volume_id / 'buckets' / bucket_id / 'awss3folders' / 'root' / 'uploader')
    logging.info(f"This is the url to reach the folder service from the bucket\n{resource_base}")
    # posting to root of bucket with file template
    file = await new_heaobject_from_type(request, type_=AWSS3FileObject)
    try:
        location_url = await client.post(request.app, resource_base, data=file, headers=headers)
        content_rb = location_url.removeprefix(request.app[appproperty.HEA_COMPONENT] + "/")\
            .removesuffix("/content") if location_url else ""
        content_id = "content" if content_rb else None
        return await response.post(request=request, result=content_id, resource_base=content_rb)
    except ClientResponseError as e:
        return response.status_generic(status=e.status, body=str(e))
    except ClientError as e:
        return response.status_generic(status=500, body=str(e))



@routes.get('/volumes/{volume_id}/buckets')
@routes.get('/volumes/{volume_id}/buckets/')
@action('heaserver-buckets-bucket-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{id}/opener')
@action(name='heaserver-buckets-bucket-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-buckets-bucket-get-create-choices', rel='hea-creator-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{id}/creator')
@action(name='heaserver-buckets-bucket-get-trash', rel='hea-trash hea-context-menu', path='volumes/{volume_id}/awss3trash')
@action(name='heaserver-buckets-bucket-get-self', rel='self', path='volumes/{volume_id}/buckets/{id}')
@action(name='heaserver-buckets-bucket-get-uploader', rel='hea-uploader', path='volumes/{volume_id}/buckets/{id}/uploader')
async def get_all_buckets(request: web.Request) -> web.Response:
    """
    Gets all buckets.
    :param request: the HTTP request.
    :return: all buckets.
    ---
    summary: get all buckets for a hea-volume associate with account.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    volume_id = request.match_info.get("volume_id", None)
    if not volume_id:
        return web.HTTPBadRequest(body="volume_id is required")
    loop = asyncio.get_running_loop()
    cache_key = (sub, volume_id, None, 'actual')
    cache_value = request.app[HEA_CACHE].get(cache_key)
    context = S3BucketPermissionsContext(request, volume_id)
    if cache_value is not None:
        bucket_dict_list: list[DesktopObjectDict] = cache_value[0]
        perms: list[list[Permission]] =  cache_value[1]
        attribute_perms: list[dict[str, list[Permission]]] = cache_value[2]
    else:
        async with DesktopObjectActionLifecycle(request=request,
                                                    code='hea-get',
                                                    description=f'Getting all buckets',
                                                    activity_cb=publish_desktop_object) as activity:
            try:
                credentials = await request.app[HEA_DB].get_credentials_from_volume(request, volume_id)
            except ValueError:
                return web.HTTPBadRequest(body=f'No volume with id {volume_id} exists')
            async with aws.S3ClientContext(request=request, credentials=credentials) as s3_client:
                try:
                    resp = await loop.run_in_executor(None, s3_client.list_buckets)
                    bucket_coros: list[Coroutine[Any, Any, tuple[AWSBucket, dict[str, list[Permission]]]]] = []
                    for bucket in resp['Buckets']:
                        bucket_coro = __get_bucket(request, volume_id, s3_client, request.app[HEA_CACHE],
                                                   context,
                                                   bucket_name=bucket["Name"],
                                                   creation_date=bucket['CreationDate'],
                                                   sub=request.headers.get(SUB, NONE_USER),
                                                   credentials=credentials)
                        if bucket_coro is not None:
                            bucket_coros.append(bucket_coro)

                    buck_list = await asyncio.gather(*bucket_coros)
                    activity.new_object_uri = f'volumes/{volume_id}/buckets/'
                    activity.new_object_type_name = AWSBucket.get_type_name()
                    activity.new_volume_id = volume_id
                except BotoClientError as e:
                    activity.status = Status.FAILED
                    return awsservicelib.handle_client_error(e)
                else:
                    perms = []
                    attribute_perms = []
                    bucket_dict_list = []
                    for buck, attr_perms in buck_list:
                        perms.append(buck.shares[0].permissions)
                        attribute_perms.append(attr_perms)
                        bucket_dict_list.append(buck.to_dict())
                    request.app[HEA_CACHE][cache_key] = (bucket_dict_list, perms, attribute_perms)
                    for buck_dict in bucket_dict_list:
                        request.app[HEA_CACHE][(sub, volume_id, buck_dict['id'], 'head')] = buck_dict['id']
                        request.app[HEA_CACHE][(sub, volume_id, buck_dict['id'], 'actual')] = (buck_dict, perms, attribute_perms)
    return await response.get_all(request, bucket_dict_list,
                                  permissions=perms,
                                  attribute_permissions=attribute_perms)


@routes.get('/volumes/{volume_id}/bucketitems')
@routes.get('/volumes/{volume_id}/bucketitems/')
@action(name='heaserver-buckets-item-get-actual', rel='hea-actual', path='{+actual_object_uri}')
@action(name='heaserver-buckets-item-get-volume', rel='hea-volume', path='volumes/{volume_id}')
async def get_all_bucketitems(request: web.Request) -> web.Response:
    """
    Gets all buckets.
    :param request: the HTTP request.
    :return: all buckets.
    ---
    summary: get all bucket items for a hea-volume associate with account.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info["volume_id"]
    sub = request.headers.get(SUB, NONE_USER)

    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting all buckets',
                                                activity_cb=publish_desktop_object) as activity:
        cache_key = (sub, volume_id, None, 'items')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            result: list[dict[str, Any]] = cached_value[0]
            permissions: list[list[Permission]] = cached_value[1]
            attribute_permissions: list[dict[str, list[Permission]]] = cached_value[2]
        else:
            async with aws.S3ClientContext(request=request, volume_id=volume_id) as s3_client:
                try:
                    resp = await asyncio.get_running_loop().run_in_executor(None, s3_client.list_buckets)

                    bucket_url = URL('volumes') / volume_id / 'buckets'
                    bucket_type = AWSBucket.get_type_name()
                    context: ViewerPermissionContext[AWSS3BucketItem] = ViewerPermissionContext(sub)
                    result = []
                    permissions = []
                    attribute_permissions = []
                    for bucket in resp['Buckets']:
                        bucket_item = AWSS3BucketItem()
                        bucket_name = bucket['Name']
                        bucket_item.bucket_id = bucket_name
                        creation_date = bucket['CreationDate']
                        bucket_item.modified = creation_date
                        bucket_item.created = creation_date
                        bucket_item.actual_object_type_name = bucket_type
                        bucket_item.actual_object_id = bucket_name
                        bucket_item.actual_object_uri = str(bucket_url / bucket_name)
                        bucket_item.source = AWS_S3
                        bucket_item.source_detail = AWS_S3
                        share = await bucket_item.get_permissions_as_share(context)
                        bucket_item.shares = [share]
                        permissions.append(share.permissions)
                        attribute_permissions.append(await bucket_item.get_all_attribute_permissions(context))
                        result.append(bucket_item.to_dict())
                    activity.new_object_uri = f'volumes/{volume_id}/bucketitems/'
                    activity.new_object_type_name = AWSS3BucketItem.get_type_name()
                    activity.new_volume_id = volume_id
                    request.app[HEA_CACHE][cache_key] = (result, permissions, attribute_permissions)
                    for buck in result:
                        request.app[HEA_CACHE][(sub, volume_id, buck['id'], 'head')] = buck['id']
                except BotoClientError as e:
                    activity.status = Status.FAILED
                    return awsservicelib.handle_client_error(e)
        return await response.get_all(request, result, permissions=permissions,
                                      attribute_permissions=attribute_permissions)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{id}')
async def get_bucket_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'DELETE', 'HEAD', 'OPTIONS', 'PUT'])


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/')
async def get_buckets_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'HEAD', 'POST', 'OPTIONS'])


@routes.route('OPTIONS', '/volumes/{volume_id}/bucketitems')
@routes.route('OPTIONS', '/volumes/{volume_id}/bucketitems/')
async def get_bucketitems_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'HEAD', 'OPTIONS'])


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.post('/volumes/{volume_id}/buckets')
@routes.post('/volumes/{volume_id}/buckets/')
async def post_bucket(request: web.Request) -> web.Response:
    """
    Posts the provided bucket.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    ---
    summary: Bucket Creation
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    requestBody:
      description: Attributes of new Bucket.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "template": {
                  "data": [{
                    "name": "created",
                    "value": null
                  },
                  {
                    "name": "derived_by",
                    "value": null
                  },
                  {
                    "name": "derived_from",
                    "value": []
                  },
                  {
                    "name": "description",
                    "value": null
                  },
                  {
                    "name": "display_name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "invited",
                    "value": []
                  },
                  {
                    "name": "modified",
                    "value": null
                  },
                  {
                    "name": "name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "owner",
                    "value": "system|none"
                  },
                  {
                    "name": "shared_with",
                    "value": []
                  },
                  {
                    "name": "source",
                    "value": null
                  },
                  {
                    "name": "version",
                    "value": null
                  },
                  {
                    "name": "encrypted",
                    "value": true
                  },
                  {
                    "name": "versioned",
                    "value": false
                  },
                  {
                    "name": "locked",
                    "value": false
                  },
                  {
                    "name": "tags",
                    "value": []
                  },
                  {
                    "name": "region",
                    "value": us-west-2
                  },
                  {
                    "name": "permission_policy",
                    "value": null
                  },
                  {
                    "name": "type",
                    "value": "heaobject.bucket.AWSBucket"
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": "This is a description",
                "display_name": "hci-test-bucket",
                "invited": [],
                "modified": null,
                "name": "hci-test-bucket",
                "owner": "system|none",
                "shared_with": [],
                "source": null,
                "type": "heaobject.bucket.AWSBucket",
                "version": null,
                encrypted: true,
                versioned: false,
                locked: false,
                tags: [],
                region: "us-west-2",
                permission_policy: null
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _post_bucket(request=request)


@routes.put('/volumes/{volume_id}/buckets/{id}')
async def put_bucket(request: web.Request) -> web.Response:
    """
    Updates the provided bucket. Only the tags may be updated.

    :param request: the HTTP request.
    :return: a Response object with a status of No Content, or Not Found if no
    bucket exists with that name, or Bad Request if there is a problem with the
    request.
    ---
    summary: Bucket update.
    tags:
        - heaserver-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    requestBody:
      description: Attributes of the bucket.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "template": {
                  "data": [
                  {
                    "name": "id",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "created",
                    "value": null
                  },
                  {
                    "name": "derived_by",
                    "value": null
                  },
                  {
                    "name": "derived_from",
                    "value": []
                  },
                  {
                    "name": "description",
                    "value": null
                  },
                  {
                    "name": "display_name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "invited",
                    "value": []
                  },
                  {
                    "name": "modified",
                    "value": null
                  },
                  {
                    "name": "name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "owner",
                    "value": "system|none"
                  },
                  {
                    "name": "shared_with",
                    "value": []
                  },
                  {
                    "name": "source",
                    "value": null
                  },
                  {
                    "name": "version",
                    "value": null
                  },
                  {
                    "name": "encrypted",
                    "value": true
                  },
                  {
                    "name": "versioned",
                    "value": false
                  },
                  {
                    "name": "locked",
                    "value": false
                  },
                  {
                    "name": "tags",
                    "value": []
                  },
                  {
                    "name": "region",
                    "value": us-west-2
                  },
                  {
                    "name": "permission_policy",
                    "value": null
                  },
                  {
                    "name": "type",
                    "value": "heaobject.bucket.AWSBucket"
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": "This is a description",
                "display_name": "hci-test-bucket",
                "invited": [],
                "modified": null,
                "name": "hci-test-bucket",
                "owner": "system|none",
                "shared_with": [],
                "source": null,
                "type": "heaobject.bucket.AWSBucket",
                "version": null,
                encrypted: true,
                versioned: false,
                locked: false,
                tags: [],
                region: "us-west-2",
                permission_policy: null
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['id']
    credentials = await request.app[HEA_DB].get_credentials_from_volume(request, volume_id)
    async with aws.S3ClientContext(request, credentials=credentials) as s3_client:
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_name))
        except BotoClientError as e:
            return awsservicelib.handle_client_error(e);

        try:
            b = await new_heaobject_from_type(request=request, type_=AWSBucket)
            if not b:
                return web.HTTPBadRequest(body=f"Put body is not a {AWSBucket.get_type_name()}")
            if not b.name:
                return web.HTTPBadRequest(body="Bucket name is required in the body")
            if b.name != bucket_name:
                return web.HTTPBadRequest(body='Bucket name in URL does not match bucket in body')
        except DeserializeException as e:
            return web.HTTPBadRequest(body=str(e))

        async with DesktopObjectActionLifecycle(request=request,
                                                    code='hea-update',
                                                    description=f'Updating {bucket_name}',
                                                    activity_cb=publish_desktop_object) as activity:
            activity.old_object_id = bucket_name
            activity.old_object_uri = f'volumes/{volume_id}/buckets/{bucket_name}'
            activity.old_object_type_name = AWSBucket.get_type_name()
            activity.old_volume_id = volume_id
            # We only support changing the bucket tags and collaborators.
            try:
                await _put_bucket_tags(s3_client, request, volume_id, bucket_name, b.tags)
            except BotoClientError as e:
                activity.status = Status.FAILED
                return awsservicelib.handle_client_error(e)
            activity.new_object_id = bucket_name
            activity.new_object_uri = f'volumes/{volume_id}/buckets/{bucket_name}'
            activity.new_object_type_name = AWSBucket.get_type_name()
            activity.new_volume_id = volume_id
            request.app[HEA_CACHE].pop((sub, volume_id, None, 'items'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, None, 'actual'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_name, 'head'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_name, 'actual'), None)

            elevated_credentials = await request.app[HEA_DB].elevate_privileges(request, credentials)
            async with aws.IAMClientContext(request=request, credentials=elevated_credentials) as iam_client:
                old_collaborator_id_to_collaborator = {old_collaborator.collaborator_id: old_collaborator for old_collaborator in await _get_collaborators(b.name, iam_client)}
                new_collaborator_ids = b.collaborator_ids
                coros: list[Coroutine[Any, Any, None]] = []
                for collaborator_id in set(old_collaborator_id_to_collaborator.keys()).difference(new_collaborator_ids):
                    coros.append(_delete_collaborator(request, b.name, old_collaborator_id_to_collaborator[collaborator_id], iam_client))
                await asyncio.gather(*coros)
                coros.clear()
                for collaborator_id in set(new_collaborator_ids).difference(old_collaborator_id_to_collaborator.keys()):
                    coros.append(_put_collaborator(request, volume_id, b.name, collaborator_id, iam_client))
                await asyncio.gather(*coros)
            return await response.put(True)




@routes.delete('/volumes/{volume_id}/buckets/{id}')
async def delete_bucket(request: web.Request) -> web.Response:
    """
    Deletes the bucket with the specified id. The bucket must be empty. If the bucket is versioned, then there can be
    no objects with delete markers in the bucket either. Setting the deletecontents query parameter to y, yes, or true
    will delete the bucket's contents, including any deleted versions, and then delete the bucket.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - heaserver-buckets
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the bucket to delete.
          schema:
            type: string
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: deletecontents
          in: query
          description: flag whether to delete the bucket's contents before deleting the bucket.
          schema:
            type: boolean
          examples:
            example:
              summary: The default value
              value: false
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    volume_id = request.match_info.get("volume_id", None)
    bucket_id = request.match_info.get("id", None)
    delete_contents = parse_bool(request.query.get('deletecontents', 'no'))
    if not volume_id:
        return web.HTTPBadRequest(body="volume_id is required")
    if not bucket_id:
        return web.HTTPBadRequest(body="bucket_id is required")
    loop = asyncio.get_running_loop()
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-delete',
                                                description=f'Deleting {bucket_id}',
                                                activity_cb=publish_desktop_object) as activity:
        activity.old_object_id = bucket_id
        activity.old_object_uri = f'volumes/{volume_id}/buckets/{bucket_id}'
        activity.old_object_type_name = AWSBucket.get_type_name()
        activity.old_volume_id = volume_id
        try:
            credentials = await request.app[HEA_DB].get_credentials_from_volume(request, volume_id)
        except ValueError as e:
            return web.HTTPBadRequest(body=f'No volume with id {volume_id} exists')
        async with aws.S3ClientContext(request=request, credentials=credentials) as s3_client:
            try:
                if delete_contents:
                    await _delete_bucket_objects(s3_client, bucket_id, delete_versions=True)
                await loop.run_in_executor(None, partial(s3_client.delete_bucket, Bucket=bucket_id))
                request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, 'head'), None)
                request.app[HEA_CACHE].pop((sub, volume_id, None, 'items'), None)
                request.app[HEA_CACHE].pop((sub, volume_id, None, 'actual'), None)
                request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, 'actual'), None)
                return web.HTTPNoContent()
            except BotoClientError as e:
                activity.status = Status.FAILED
                return awsservicelib.handle_client_error(e)
        elevated_credentials = await request.app[HEA_DB].elevate_privileges(request, credentials)
        async with aws.IAMClientContext(request=request, credentials=elevated_credentials) as iam_client:
            coros: list[Coroutine[Any, Any, None]] = []
            for retval in await _get_collaborators(request, bucket_id, iam_client):
                coros.append(_delete_collaborator(request, bucket_id, retval, iam_client))
            await asyncio.gather(*coros)


def main() -> None:
    config = init_cmd_line(description='a service for managing buckets and their data within the cloud',
                           default_port=8080)
    start(package_name='heaserver-buckets', db=aws.S3Manager,
          wstl_builder_factory=builder_factory(__package__),
          cleanup_ctx=[publisher_cleanup_context_factory(config)],
          config=config)


async def _delete_bucket_objects(s3_client: S3Client, bucket_name: str, delete_versions=False, fail_if_not_empty=False) -> None:
    """
    Deletes all objects inside a bucket, assuming the bucket exists.

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param bucket_name: Bucket to delete
    :param delete_versions: Boolean indicating if the versioning should be deleted as well, defaults to False. For
    versioned buckets, this flag must be set to True or subsequently attempting to delete the bucket will fail.
    :raises BotoClientError: if the bucket does not exist, or another error occurred while deleting the bucket's
    contents.
    """
    loop = asyncio.get_running_loop()
    if delete_versions:
        bucket_versioning = await loop.run_in_executor(None, partial(s3_client.get_bucket_versioning, Bucket=bucket_name))
        if bucket_versioning['Status'] == 'Enabled':
            delete_marker_list: list[ObjectIdentifierTypeDef] = []
            version_list: list[ObjectIdentifierTypeDef] = []
            async for page in awsservicelib.list_object_versions(s3_client, bucket_name):
                if 'DeleteMarkers' in page:
                    for delete_marker in page['DeleteMarkers']:
                        delete_marker_list.append({'Key': delete_marker['Key'], 'VersionId': delete_marker['VersionId']})

                if 'Versions' in page:
                    for version in page['Versions']:
                        version_list.append({'Key': version['Key'], 'VersionId': version['VersionId']})

            for i in range(0, len(delete_marker_list), 1000):
                await loop.run_in_executor(None, partial(s3_client.delete_objects,
                    Bucket=bucket_name,
                    Delete={
                        'Objects': delete_marker_list[i:i+1000],
                        'Quiet': True
                    }
                ))

            for i in range(0, len(version_list), 1000):
                await loop.run_in_executor(None, partial(s3_client.delete_objects,
                    Bucket=bucket_name,
                    Delete={
                        'Objects': version_list[i:i+1000],
                        'Quiet': True
                    }
                ))
        else:
            object_list: list[ObjectIdentifierTypeDef] = []
            async for object in awsservicelib.list_objects(s3_client, bucket_name):
                object_list.append({'Key': object['Key']})
            for i in range(0, len(object_list), 1000):
                delete_: DeleteTypeDef = {
                    'Objects': object_list[i:i+1000],
                    'Quiet': True
                }
                await loop.run_in_executor(None, partial(s3_client.delete_objects, Bucket=bucket_name, Delete=delete_))
    else:
        object_list = []
        async for object in awsservicelib.list_objects(s3_client, bucket_name):
            object_list.append({'Key': object['Key']})
        for i in range(0, len(object_list), 1000):
            delete_ = {
                'Objects': object_list[i:i+1000],
                'Quiet': True
            }
            await loop.run_in_executor(None, partial(s3_client.delete_objects, Bucket=bucket_name, Delete=delete_))


async def _get_bucket(request: web.Request) -> web.Response:
    """
    List a single bucket's attributes

    :param request: the aiohttp Request (required).
    :return:  return the single bucket object requested or HTTP Error Response
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    try:
        volume_id = request.match_info['volume_id']
        bucket_name = request.match_info.get('id')
        if bucket_name is None:
            bucket_name = request.match_info['bucket_name']
    except KeyError as e:
        raise ValueError(str(e))

    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting {bucket_name}',
                                                activity_cb=publish_desktop_object) as activity:
        cache_key = (sub, volume_id, bucket_name, 'actual')
        cache_value = request.app[HEA_CACHE].get(cache_key)
        include_data = parse_bool(request.query.get('data') or 'true')
        if cache_value:
            bucket_dict, perms, attribute_perms = cache_value
            return await response.get(request=request, data=bucket_dict,
                                      permissions=perms, attribute_permissions=attribute_perms,
                                      include_data=include_data)
        else:
            try:
                credentials = await request.app[HEA_DB].get_credentials_from_volume(request, volume_id)
            except ValueError:
                raise web.HTTPBadRequest(body=f'No volume with id {volume_id} exists')

            async with aws.S3ClientContext(request=request, credentials=credentials) as s3_client:
                if include_data:
                    try:
                        bucket_result, attribute_perms = await __get_bucket(request, volume_id, s3_client, request.app[HEA_CACHE],
                                                        S3BucketPermissionsContext(request, volume_id),
                                                        bucket_name=bucket_name, bucket_id=bucket_name,
                                                        sub=request.headers.get(SUB, NONE_USER),
                                                        credentials=credentials)
                        if bucket_result is not None:
                            activity.new_object_id = bucket_name
                            activity.new_object_uri = f'volumes/{volume_id}/buckets/{bucket_name}'
                            activity.new_object_type_name = AWSBucket.get_type_name()
                            activity.new_volume_id = volume_id
                            perms = bucket_result.shares[0].permissions
                            bucket_dict = bucket_result.to_dict()
                            request.app[HEA_CACHE][(sub, volume_id, bucket_dict['id'], 'actual')] = (bucket_dict, perms, attribute_perms)
                            return await response.get(request=request, data=bucket_dict,
                                                    permissions=bucket_result.shares[0].permissions,
                                                    attribute_permissions=attribute_perms, include_data=True)
                        activity.status = Status.FAILED
                        return await response.get(request, data=None)
                    except BotoClientError as e:
                        activity.status = Status.FAILED
                        return awsservicelib.http_error_message(awsservicelib.handle_client_error(e), bucket_name, None)
                else:
                    loop = asyncio.get_running_loop()
                    try:
                        await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_name))
                        bucket_dict_: DesktopObjectDict | None = {'id': bucket_name, 'type': AWSBucket.get_type_name()}
                    except BotoClientError as e:
                        code, _ = aws.client_error_status(e)
                        if code == 404:
                            bucket_dict_ = None
                        else:
                            return awsservicelib.http_error_message(awsservicelib.handle_client_error(e), bucket_name, None)
                    return await response.get(request=request, data=bucket_dict_, include_data=False)


async def __get_bucket(request: web.Request, volume_id: str, s3_client: S3Client, cache,
                       context: S3BucketPermissionsContext,
                       bucket_name: str | None = None, bucket_id: str | None = None,
                       creation_date: datetime | None = None,
                       sub: str | None = None, credentials: AWSCredentials | None = None) -> tuple[AWSBucket, dict[str, list[Permission]]]:
    """
    :param volume_id: the volume id
    :param s3_client:  the boto3 client
    :param bucket_name: str the bucket name (optional)
    :param bucket_id: str the bucket id (optional)
    :param creation_date: str the bucket creation date (optional)
    :return: Returns either the AWSBucket or None for Not Found or Forbidden, else raises ClientError
    """
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    if not volume_id or (not bucket_id and not bucket_name):
        raise ValueError("volume_id is required and either bucket_name or bucket_id")

    b = AWSBucket()
    b.name = bucket_id if bucket_id else bucket_name
    b.id = bucket_id if bucket_id else bucket_name
    if bucket_id is not None:
        b.display_name = bucket_id
    elif bucket_name is not None:
        b.display_name = bucket_name
    async_bucket_methods: list[Coroutine[Any, Any, None]] = []
    b.bucket_id = b.name
    b.source = AWS_S3
    b.source_detail = AWS_S3
    b.arn = f'arn:aws:s3::{b.id}'
    b.owner = AWS_USER
    attr_perms: dict[str, list[Permission]] = {}

    if creation_date:
        b.created = creation_date
    elif cached_value := cache.get((sub, volume_id, None, 'items')):
        bucket, _, _ = cached_value
        b.created = next((bucket_['created'] for bucket_ in bucket if bucket_['name'] == b.name), None)
    else:
        async def _get_creation_date(b: AWSBucket):
            logger.debug('Getting creation date of bucket %s', b.name)
            try:
                creation_date = next((bucket_['CreationDate'] for bucket_ in (await loop.run_in_executor(None, s3_client.list_buckets))['Buckets'] if bucket_['Name'] == b.name), None)
                b.created = creation_date
            except BotoClientError as ce:
                logger.exception('Error getting the creation date of bucket %s', b.name)
                raise ce

        async_bucket_methods.append(_get_creation_date(b))

    async def _get_perms(b: AWSBucket):
        share = await b.get_permissions_as_share(context)
        b.shares = [share]
    async_bucket_methods.append(_get_perms(b))

    async def _get_version_status(b: AWSBucket):
        logger.debug('Getting version status of bucket %s', b.name)
        try:
            assert b.name is not None, 'b.name cannot be None'
            bucket_versioning = await loop.run_in_executor(None,
                                                            partial(s3_client.get_bucket_versioning, Bucket=b.name))
            logger.debug('bucket_versioning=%s', bucket_versioning)
            if 'Status' in bucket_versioning:
                b.versioned = bucket_versioning['Status'] == 'Enabled'
                logger.debug('Got version status of bucket %s successfully', b.name)
            else:
                logger.debug('No version status information for bucket %s', b.name)
        except BotoClientError as ce:
            logger.exception('Error getting the version status of bucket %s', b.name)
            raise ce

    async_bucket_methods.append(_get_version_status(b))

    async def _get_region(b: AWSBucket):
        logger.debug('Getting region of bucket %s', b.name)
        try:
            assert b.name is not None, 'b.name cannot be None'
            loc = await loop.run_in_executor(None, partial(s3_client.get_bucket_location, Bucket=b.name))
            b.region = loc['LocationConstraint'] or 'us-east-1'
        except BotoClientError as ce:
            logging.exception('Error getting the region of bucket %s', b.name)
            raise ce
        logger.debug('Got region of bucket %s successfully', b.name)

    async_bucket_methods.append(_get_region(b))

    # todo how to find partition dynamically. The format is arn:PARTITION:s3:::NAME-OF-YOUR-BUCKET
    # b.arn = "arn:"+"aws:"+":s3:::"

    async def _get_tags(b: AWSBucket):
        logger.debug('Getting tags of bucket %s', b.name)
        try:
            assert b.name is not None, 'b.name cannot be None'
            tagging = await loop.run_in_executor(None, partial(s3_client.get_bucket_tagging, Bucket=b.name))
            b.tags = _from_aws_tags(aws_tags=tagging['TagSet'])
        except BotoClientError as ce:
            if ce.response['Error']['Code'] != 'NoSuchTagSet':
                logging.exception('Error getting the tags of bucket %s', b.name)
                raise ce
        logger.debug('Got tags of bucket %s successfully', b.name)

    async_bucket_methods.append(_get_tags(b))

    async def _get_all_attribute_permissions(b: AWSBucket):
        nonlocal attr_perms
        attr_perms = await b.get_all_attribute_permissions(context)

    async_bucket_methods.append(_get_all_attribute_permissions(b))

    async def _get_encryption_status(b: AWSBucket):
        logger.debug('Getting encryption status of bucket %s', b.name)
        try:
            assert b.name is not None, 'b.name cannot be None'
            encrypt = await loop.run_in_executor(None, partial(s3_client.get_bucket_encryption, Bucket=b.name))
            rules: list = encrypt['ServerSideEncryptionConfiguration']['Rules']
            b.encrypted = len(rules) > 0
        except BotoClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                b.encrypted = False
            else:
                logger.exception('Error getting the encryption status of bucket %s', b.name)
                raise e
        logger.debug('Got encryption status of bucket %s successfully', b.name)

    async_bucket_methods.append(_get_encryption_status(b))

    async def _get_collaborators_for_bucket(b: AWSBucket):
        assert b.name is not None, 'b.name cannot be None'
        elevated_credentials = await request.app[HEA_DB].elevate_privileges(request, credentials) if credentials is not None else None
        async with aws.IAMClientContext(request, credentials=elevated_credentials) as iam_client:
            b.collaborator_ids = [r.collaborator_id for r in await _get_collaborators(b.name, iam_client)]
    async_bucket_methods.append(_get_collaborators_for_bucket(b))

    async def _get_bucket_lock_status(b: AWSBucket):
        logger.debug('Getting bucket lock status of bucket %s', b.name)
        try:
            assert b.name is not None, 'b.name cannot be None'
            lock_config = await loop.run_in_executor(None, partial(s3_client.get_object_lock_configuration,
                                                                    Bucket=b.name))
            b.locked = lock_config['ObjectLockConfiguration']['ObjectLockEnabled'] == 'Enabled'
        except BotoClientError as e:
            if e.response['Error']['Code'] != 'ObjectLockConfigurationNotFoundError':
                logger.exception('Error getting the lock status of bucket %s', b.name)
                raise e
            b.locked = False
        logger.debug('Got bucket lock status of bucket %s successfully', b.name)

    async_bucket_methods.append(_get_bucket_lock_status(b))

    # todo need to lazy load this these metrics
    total_size = None
    obj_count = None
    mod_date = None
    # FIXME need to calculate this metric data in a separate call. Too slow
    # s3bucket = s3_resource.Bucket(b.name)
    # for obj in s3bucket.objects.all():
    #     total_size += obj.size
    #     obj_count += 1
    #     mod_date = obj.last_modified if mod_date is None or obj.last_modified > mod_date else mod_date
    b.size = total_size
    b.object_count = obj_count
    b.modified = mod_date
    await asyncio.gather(*async_bucket_methods)
    return b, attr_perms


@dataclass
class _GetCollaboratorRetval:
    collaborator_id: str
    other_bucket_names: list[str]


async def _get_collaborators(bucket_name: str, iam_client: IAMClient) -> list[_GetCollaboratorRetval]:
    logger = logging.getLogger(__name__)
    logger.debug('Getting collaborators for bucket %s', bucket_name)
    try:
        assert bucket_name is not None, 'bucket_name cannot be None'
        return [_GetCollaboratorRetval(collaborator_id=policy_info.user_id, other_bucket_names=list(policy_info.bucket_names - set([bucket_name]))) \
                async for policy_info in _all_collaborator_policies_gen(iam_client) if bucket_name in policy_info.bucket_names]
    except BotoClientError as e:
        if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
            logging.exception('Error getting collaborators for bucket %s', bucket_name)
            raise e
        return []



def _from_aws_tags(aws_tags: list[TagTypeDef]) -> list[Tag]:
    """
    :param aws_tags: Tags obtained from boto3 Tags api
    :return: List of HEA Tags
    """
    hea_tags = []
    for t in aws_tags:
        tag = Tag()
        tag.key = t['Key']
        tag.value = t['Value']
        hea_tags.append(tag)
    return hea_tags


async def _bucket_opener(request: web.Request) -> web.Response:
    """
    Returns links for opening the bucket. The volume id must be in the volume_id entry of the request's
    match_info dictionary. The bucket id must be in the id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and a Collection+JSON document in the body
    containing an heaobject.bucket.AWSBucket object and links, 403 if access was denied, 404 if the bucket
    was not found, or 500 if an internal error occurred.
    """
    try:
        volume_id = request.match_info['volume_id']
        bucket_id = request.match_info['id']
    except KeyError as e:
        return response.status_bad_request(str(e))
    sub = request.headers.get(SUB, NONE_USER)
    loop = asyncio.get_running_loop()

    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-get',
                                            description=f'Accessing bucket {bucket_id}',
                                            activity_cb=publish_desktop_object) as activity:
        head_cache_key = (sub, volume_id, bucket_id, 'head')
        actual_cache_key = (sub, volume_id, bucket_id, 'actual')
        if head_cache_key not in request.app[HEA_CACHE] and actual_cache_key not in request.app[HEA_CACHE]:
            async with aws.S3ClientContext(request, volume_id) as s3_client:
                try:
                    await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_id))
                    activity.new_object_id = bucket_id
                    activity.new_object_type_name = AWSBucket.get_type_name()
                    activity.new_object_uri = f'volumes/{volume_id}/buckets/{bucket_id}'
                    activity.new_volume_id = volume_id
                    request.app[HEA_CACHE][head_cache_key] = bucket_id
                except BotoClientError as e:
                    raise awsservicelib.handle_client_error(e)
        return await response.get_multiple_choices(request)


async def _post_bucket(request: web.Request):
    """
    Create an S3 bucket in a specified region. Will fail if the bucket with the given name already exists.
    If a region is not specified, the bucket is created in the S3 default region (us-east-1).

    The request must have either a volume id, which is the id string of the volume representing the user's AWS account,
    or an id, which is the account id.

    :param request: the aiohttp Request (required). A volume_id must be specified in its match info. The AWSBucket
    in the body of the request must have a name.
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    bucket_already_exists_msg = "A bucket named {} already exists"

    volume_id = request.match_info.get('volume_id', None)
    if not volume_id:
        volume_id = await awsservicelib.get_volume_id_for_account_id(request)
        if not volume_id:
            return web.HTTPBadRequest(body="either id or volume_id is required")
    try:
        b = await new_heaobject_from_type(request=request, type_=AWSBucket)
        if not b:
            return web.HTTPBadRequest(body="Post body is not an HEAObject AWSBUCKET")
        if not b.name:
            return web.HTTPBadRequest(body="Bucket name is required")
    except DeserializeException as e:
        return response.status_bad_request(str(e))

    loop = asyncio.get_running_loop()
    credentials = await request.app[HEA_DB].get_credentials_from_volume(request, volume_id)
    async with aws.S3ClientContext(request, credentials=credentials) as s3_client:
        try:
            await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=b.name))  # check if bucket exists, if not throws an exception
            return web.HTTPConflict(body=bucket_already_exists_msg.format(b.display_name))
        except BotoClientError as e:
            loop = asyncio.get_running_loop()
            try:
                # todo this is a privileged actions need to check if authorized
                error_code = e.response['Error']['Code']

                if error_code == '404':  # bucket doesn't exist
                    create_bucket_params: dict[str, Any] = {'Bucket': b.name}
                    put_bucket_policy_params: PublicAccessBlockConfigurationTypeDef = {
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                    if b.region and b.region != 'us-east-1':
                        create_bucket_params['CreateBucketConfiguration'] = {'LocationConstraint': b.region}
                    if b.locked:
                        create_bucket_params['ObjectLockEnabledForBucket'] = True

                    await loop.run_in_executor(None, partial(s3_client.create_bucket, **create_bucket_params))
                    # make private bucket
                    await loop.run_in_executor(None, partial(s3_client.put_public_access_block, Bucket=b.name,
                                                            PublicAccessBlockConfiguration=put_bucket_policy_params))

                    await _put_bucket_encryption(b, loop, s3_client)
                    # todo this is a privileged action need to check if authorized ( may only be performed by bucket owner)

                    await _put_bucket_versioning(bucket_name=b.name, s3_client=s3_client, is_versioned=b.versioned)

                    await _put_bucket_tags(s3_client, request=request, volume_id=volume_id,
                                        bucket_name=b.name, new_tags=b.tags)
                    elevated_credentials = await request.app[HEA_DB].elevate_privileges(request, credentials) if credentials is not None else None
                    async with aws.IAMClientContext(request=request, credentials=elevated_credentials) as iam_client:
                        coros: list[Coroutine[Any, Any, None]] = []
                        for collaborator_id in b.collaborator_ids:
                            coros.append(_put_collaborator(request=request, volume_id=volume_id, bucket_name=b.name,
                                                           collaborator_id=collaborator_id, iam_client=iam_client))
                        await asyncio.gather(*coros)
                elif error_code == '403':  # already exists but the user doesn't have access to it
                    logger.exception(bucket_already_exists_msg, b.display_name)
                    return response.status_bad_request(bucket_already_exists_msg.format(b.display_name))
                else:
                    logger.exception(str(e))
                    return response.status_bad_request(str(e))
            except BotoClientError as e2:
                logger.exception(str(e2))
                try:
                    await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=b.name))
                    del_bucket_result = await loop.run_in_executor(None, partial(s3_client.delete_bucket, Bucket=b.name))
                    logging.info(f"deleted failed bucket {b.name} details: \n{del_bucket_result}")
                except BotoClientError:  # bucket doesn't exist so no clean up needed
                    pass
                return web.HTTPBadRequest(body=e2.response['Error'].get('Message'))
            request.app[HEA_CACHE].pop((sub, volume_id, None, 'items'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, None, 'actual'), None)
            return await response.post(request, b.name, f'volumes/{volume_id}/buckets')


async def _put_bucket_encryption(b, loop, s3_client):
    if b.encrypted:
        SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'
        try:
            await loop.run_in_executor(None, partial(s3_client.get_bucket_encryption, Bucket=b.name))
        except BotoClientError as e:
            if e.response['Error']['Code'] == SSECNF:
                config = \
                    {'Rules': [{'ApplyServerSideEncryptionByDefault':
                                    {'SSEAlgorithm': 'AES256'}, 'BucketKeyEnabled': False}]}
                await loop.run_in_executor(None, partial(s3_client.put_bucket_encryption, Bucket=b.name,
                                                         ServerSideEncryptionConfiguration=config))
            else:
                logging.error(e.response['Error']['Code'])
                raise e


async def _put_bucket_versioning(bucket_name: str, is_versioned: bool | None, s3_client: S3Client):
    """
    Use To change turn on or off bucket versioning settings. Note that if the Object Lock
    is turned on for the bucket you can't change these settings.

    :param bucket_name: The bucket name
    :param is_versioned: For toggling on or off the versioning
    :param s3_client: Pass the active client if exists (optional)
    :raises BotoClientError: if an error occurred setting version information.
    """
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    vconfig: VersioningConfigurationTypeDef = {
        'MFADelete': 'Disabled',
        'Status': 'Enabled' if is_versioned else 'Suspended',
    }
    vresp = await loop.run_in_executor(None, partial(s3_client.put_bucket_versioning, Bucket=bucket_name,
                                                     VersioningConfiguration=vconfig))
    logger.debug(vresp)


async def _put_bucket_tags(s3_client: S3Client, request: web.Request, volume_id: str, bucket_name: str,
                           new_tags: list[Tag] | None):
    """
    Creates or adds to a tag list for bucket

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account (required).
    :param bucket_name: The bucket (required).
    :param new_tags: new tags to be added tag list on specified bucket. Pass in the empty list or None to clear out
    the bucket's tags.
    :raises BotoClientError: if an error occurs interacting with S3.
    """
    if request is None:
        raise ValueError('request is required')
    if volume_id is None:
        raise ValueError('volume_id is required')
    if bucket_name is None:
        raise ValueError('bucket_name is required')

    loop = asyncio.get_running_loop()
    def delete_and_put():
        s3_client.delete_bucket_tagging(Bucket=bucket_name)
        s3_client.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': _to_aws_tags(new_tags or [])})
    await loop.run_in_executor(None, delete_and_put)


async def _delete_collaborator(request: web.Request, bucket_name: str, collaborator: _GetCollaboratorRetval, iam_client: IAMClient):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    sub = request.headers.get(SUB, NONE_USER)
    sub_headers = {SUB: sub}
    collaborator_id = collaborator.collaborator_id
    collab_sub_headers = {SUB: collaborator_id}
    cred_man_sub_headers = {SUB: CREDENTIALS_MANAGER_USER}
    policy_arn, policy = await _get_policy_by(iam_client, collaborator_id)
    policy_stmts = policy['Statement']
    assert not isinstance(policy_stmts, str), 'policy_stmt must not be a string'
    role_name = _role_template.format(user_id=collaborator_id)
    await _remove_bucket_from_policy_or_delete_policy(bucket_name, collaborator_id, iam_client, role_name)
    if collaborator.other_bucket_names:
        logger.debug('User %s has access to other buckets in this account, so not deleting Keycloak groups and role', collaborator_id)
        return

    account_id = _extract_account_id_from(policy_arn)
    # Delete group and role from keycloak (may need to detach group from user first)
    group_url = await type_to_resource_url(request, Group)
    group_name = f'/Collaborators/AWS Accounts/{account_id}/{collaborator_id}'
    try:
        await client.delete(request.app, URL(group_url) / 'internal' / 'byname' / encode_group(group_name))
        logger.debug('Group %s successfully deleted', group_name)
    except ClientResponseError as e:
        if e.status == 404:
            logger.debug('Group %s already deleted from people service', group_name)
        else:
            raise e

    role_arn = _role_arn_template.format(account_id=account_id, user_id=collaborator_id)
    role_url = await type_to_resource_url(request, Role)
    try:
        await client.delete(request.app, URL(role_url) / 'internal' / 'byname' / encode_role(role_arn))
        logger.debug('Role %s successfully deleted', role_name)
    except ClientResponseError as e:
        if e.status == 404:
            logger.debug('Role %s already deleted from people service', role_name)
        else:
            raise e

    def role_deleter():
        try:
            logger.debug(f'Deleting role %s', role_name)
            iam_client.delete_role(RoleName=role_name)
            logger.debug('Role deletion successful')
        except BotoClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                logger.debug(f'Role {role_name} already deleted from AWS')
            else:
                raise e
    await loop.run_in_executor(None, role_deleter)

    person_url = await type_to_resource_url(request, Person)
    person = await client.get(request.app, URL(person_url) / collaborator_id, Person, headers=sub_headers)
    assert person is not None, f'Person {collaborator_id} disappeared'
    logger.debug('Person %s retrieved successfully', collaborator_id)

    volume_url = await type_to_resource_url(request, Volume)
    volume_name = f'{account_id}_Collaborator_{collaborator_id}'
    logger.debug('Getting volume %s', volume_name)
    volume = await client.get(request.app, URL(volume_url) / 'byname' / volume_name, Volume, headers=collab_sub_headers)
    logger.debug('Got volume %r', volume)
    if volume is not None:
        credential_id = volume.credential_id
        assert volume.id is not None, 'volume.id cannot be None'
        try:
            logger.debug('Deleting volume %s', volume.id)
            await client.delete(request.app, URL(volume_url) / volume.id, headers=cred_man_sub_headers)
            logger.debug('Volume %s deleted successfully', volume.id)
        except ClientResponseError as e:
            if e.status == 404:
                logger.debug('Volume %s not found', volume.id)
            else:
                raise e
        if credential_id is not None:
            credential_url = await type_to_resource_url(request, AWSCredentials)
            try:
                logger.debug('Deleting credentials %s', credential_id)
                await client.delete(request.app, URL(credential_url) / credential_id, headers=cred_man_sub_headers)
                logger.debug('Credentials %s deleted successfully')
            except ClientResponseError as e:
                if e.status == 404:
                    logger.debug('Credentials %s not found', credential_id)
                else:
                    raise e

    logger.debug('Getting AWS account %s', account_id)
    aws_account_url = await type_to_resource_url(request, AWSAccount)
    aws_account = await client.get(request.app, URL(aws_account_url) / account_id, AWSAccount, headers=sub_headers)
    assert aws_account is not None, f'AWS account {account_id} disappeared'
    logger.debug('AWS account %r retrieved successfully', aws_account)

    organization_url = await type_to_resource_url(request, Organization)
    assert aws_account.instance_id is not None, 'aws_account.instance_id must not be None'
    async with _update_collaborators_lock:
        organization = await client.get(request.app, URL(organization_url) / 'byaccountid' / aws_account.instance_id,
                                        Organization, headers=sub_headers)
        logger.debug('Found organization %r', organization)
        if organization is not None:
            removing_collaborator = RemovingCollaborator()
            removing_collaborator.collaborator_id = person.id
            removing_collaborator.first_name = person.first_name
            removing_collaborator.last_name = person.last_name
            removing_collaborator.preferred_name = person.preferred_name
            removing_collaborator.name = person.name
            removing_collaborator.actual_object_id = person.id
            removing_collaborator.actual_object_type_name = Person.get_type_name()
            removing_collaborator.actual_object_uri = f'people/{person.id}'
            removing_collaborator.from_organization_id = organization.id
            logger.debug('Preparing to publish desktop object %r successfully', removing_collaborator)
            await publish_desktop_object(request.app, removing_collaborator)
            logger.debug('Published desktop object %r successfully', removing_collaborator)

async def _detach_and_delete_policy(iam_client: IAMClient, policy_arn: str):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    def policy_detacher():
        policy_attachments = iam_client.list_entities_for_policy(PolicyArn=policy_arn)
        for policy_role in policy_attachments['PolicyRoles']:
            logger.debug('Detaching policy %s from role %s', policy_arn, policy_role['RoleName'])
            iam_client.detach_role_policy(RoleName=policy_role['RoleName'], PolicyArn=policy_arn)
            logger.debug('Detachment successful')
    def policy_deleter():
        try:
            logger.debug(f'Deleting policy %s', policy_arn)
            iam_client.delete_policy(PolicyArn=policy_arn)
            logger.debug('Policy deletion successful')
        except BotoClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                logger.debug(f'Policy {policy_arn} already deleted')
            elif e.response['Error']['Code'] == 'DeleteConflict':
                logger.debug('Policy is still attached to %s', iam_client.list_entities_for_policy(PolicyArn=policy_arn))
                raise e
            else:
                raise e
    logger.debug('Detaching and deleting policy %s', policy_arn)
    await loop.run_in_executor(None, policy_detacher)
    await loop.run_in_executor(None, policy_deleter)

def _extract_account_id_from(arn: str) -> str:
    return arn.split(':')[4]

async def _get_policy_by(iam_client: IAMClient, user_id: str) -> tuple[str, PolicyDocumentDictTypeDef]:
    logger = logging.getLogger(__name__)
    logger.debug('Getting collaborator policy for user %s', user_id)
    loop = asyncio.get_running_loop()
    response_ = (await loop.run_in_executor(None, partial(iam_client.get_account_authorization_details,
                                                                     Filter=['LocalManagedPolicy'])))
    logger.debug('Account authorization details: %s', response_)
    for policy in response_['Policies']:
        logger.debug('Policy detail: %s', policy)
        if policy['PolicyName'] == _collaborator_policy_name_template.format(user_id=user_id):
            for version in policy['PolicyVersionList']:
                if version['IsDefaultVersion']:
                    pol_doc = version['Document']
                    logger.debug('Returning policy doc from policy %s for user %s: %s', policy, user_id, pol_doc)
                    assert not isinstance(pol_doc, str), 'pol_doc unexpected type'
                    return policy['Arn'], pol_doc
    raise ValueError(f'Policy for user {user_id} not found')

@dataclass
class _PolicyInfo:
    user_id: str
    policy_arn: str
    bucket_names: set[str]
    policy_doc: PolicyDocumentDictTypeDef


async def _all_collaborator_policies_gen(iam_client: IAMClient) -> AsyncGenerator[_PolicyInfo, None]:
    logger = logging.getLogger(__name__)
    logger.debug('Getting collaborator policy')
    loop = asyncio.get_running_loop()
    response_ = (await loop.run_in_executor(None, partial(iam_client.get_account_authorization_details,
                                                                     Filter=['LocalManagedPolicy'])))
    logger.debug('Account authorization details: %s', response_)
    for policy in response_['Policies']:
        logger.debug('Policy detail: %s', policy)
        if policy['PolicyName'].startswith(_collaborator_policy_name_prefix):
            user_id = policy['PolicyName'].removeprefix(_collaborator_policy_name_prefix)
            logger.debug('User id %s', user_id)
            for version in policy['PolicyVersionList']:
                if version['IsDefaultVersion']:
                    pol_doc = version['Document']
                    assert not isinstance(pol_doc, str), 'Unexpected policy document type'
                    pol_doc_stmt = pol_doc['Statement']
                    assert not isinstance(pol_doc_stmt, str), 'Unexpected policy document statement type'
                    assert len(pol_doc_stmt) == 2, 'Unexpected number of policy statements'
                    bucket_names: set[str] = set()
                    for resource in pol_doc_stmt[0]['Resource']:
                        bucket_names.add(_arn_pattern.split(resource)[5])
                    logger.debug('Returning policy doc from policy %s for user %s with buckets %s', policy, pol_doc, bucket_names)
                    assert not isinstance(pol_doc, str), 'pol_doc unexpected type'
                    yield _PolicyInfo(user_id=user_id, policy_arn=policy['Arn'], bucket_names=bucket_names, policy_doc=pol_doc)

async def _put_collaborator(request: web.Request, volume_id: str, bucket_name: str, collaborator_id: str, iam_client: IAMClient):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    sub = request.headers.get(SUB, NONE_USER)
    sub_headers = {SUB: sub}
    collab_sub_headers = {SUB: collaborator_id}
    cred_man_sub_headers = {SUB: CREDENTIALS_MANAGER_USER}
    person_url = await type_to_resource_url(request, Person)

    logger.debug('Getting person %s', collaborator_id)
    person_url = await type_to_resource_url(request, Person)
    person = await client.get(request.app, URL(person_url) / collaborator_id, Person, headers=sub_headers)
    assert person is not None, f'Person {collaborator_id} disappeared'
    logger.debug('Person %s retrieved successfully', collaborator_id)

    logger.debug('Getting AWS account for volume %s', volume_id)
    aws_account = cast(AWSAccount, await request.app[HEA_DB].get_account(request, volume_id))
    assert aws_account is not None, f'AWS account for volume {volume_id} disappeared'
    account_id = aws_account.id
    assert account_id is not None, f'aws_account.account_id cannot be None for account {aws_account}'
    logger.debug('AWS account %r retrieved successfully', aws_account)

    volume_url = await type_to_resource_url(request, Volume)
    volume_name = f'{aws_account.id}_Collaborator_{collaborator_id}'
    async def get_volume() -> Volume | None:
        assert aws_account.instance_id is not None, 'aws_account.instance_id cannot be None'
        assert person is not None, 'person cannot be None'
        logger.debug('Checking if user %s already has access to account %s', collaborator_id, aws_account.id)
        user_volumes_gen = client.get_all(request.app, URL(volume_url).with_query([('account_id', aws_account.instance_id)]), Volume, headers=collab_sub_headers)
        volume_: Volume | None = None
        async for volume in user_volumes_gen:
            logger.debug('Checking volume %r', volume)
            if volume.owner == CREDENTIALS_MANAGER_USER:
                if volume.name != f'{aws_account.id}_Collaborator_{person.id}':
                    raise response.status_conflict(f'{person.display_name} already has access to this AWS account')
                elif volume.name == volume_name:
                    volume_ = volume
        return volume_
    volume_ = await get_volume()

    policy = await _add_bucket_to_policy(bucket_name, collaborator_id, iam_client)
    policy_arn = policy['Arn']
    logger.debug("Created policy %s", policy)
    oidc_provider_url = request.headers[ISS].removeprefix('https://')
    logger.debug('OIDC provider URL is %s', oidc_provider_url)
    id_provider_arn = f"arn:aws:iam::{account_id}:oidc-provider/{oidc_provider_url}"
    # AWS seems to use the azp claim (client id) rather than the actual aud claim (intended user).
    oidc_aud = request.headers.get(AZP, 'hea')
    assume_role_policy_doc = orjson.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": id_provider_arn
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                    "StringEquals": {
                        f"{oidc_provider_url}:aud": oidc_aud
                    }
                }
            }
        ]
    }).decode('utf-8')
    logger.debug('Assume role policy document is %s', assume_role_policy_doc)
    role_name = _role_template.format(user_id=collaborator_id)
    role_arn = _role_arn_template.format(account_id=account_id, user_id=collaborator_id)

    # Create role in keycloak, create group in keycloak with role, and add user to group.
    role = Role()
    role.role = role_arn
    role_url = await type_to_resource_url(request, Role)
    try:
        logger.debug('Creating role %r', role)
        try:
            role_location_url = await client.post(request.app, URL(role_url) / 'internal', role)
            role.id = role_location_url.rsplit('/', maxsplit=1)[1]
            logger.debug('Role created successfully')
        except ClientResponseError as e:
            if e.status == 409:
                logger.debug('Role %r already exists', role)
                role_from_server = await client.get(request.app, URL(role_url) / 'byname' / encode_role(role_arn), Role)
                assert role_from_server is not None, 'role_from_server is not None'
                role = role_from_server
            else:
                raise e
        assert role.id is not None, 'role.id cannot be None'
        group_url_ = await type_to_resource_url(request, Group)
        group = Group()
        group.group = f'/Collaborators/AWS Accounts/{account_id}/{collaborator_id}'
        group.role_ids = [role.id]
        logger.debug('Creating group %r', group)
        try:
            group_url = await client.post(request.app, URL(group_url_) / 'internal', group)
            group.id = group_url.rsplit('/', maxsplit=1)[1]
            group_id: str | None = group.id
            logger.debug('Group %s created successfully', group)
        except ClientResponseError as e:
            if e.status == 409:
                logger.debug('Group %r already exists', group)
                group_ = await client.get(request.app, URL(group_url_) / 'byname' / encode_group(group.group), Group)
                assert group_ is not None, 'group cannot be None'
                group = group_
                group_id = group.id
            else:
                raise e
        assert group_id is not None, 'group.id cannot be None'
        logger.debug('Adding user %s to group %r', collaborator_id, group)
        await client.post(request.app, URL(person_url) / 'internal' / collaborator_id / 'groups', data=group)
        logger.debug('User added successfully, creating role %s in AWS', role_name)
        try:
            await loop.run_in_executor(None, partial(iam_client.create_role, RoleName=role_name, Path='/',
                                                     AssumeRolePolicyDocument=assume_role_policy_doc,
                                                     MaxSessionDuration=aws.S3.MAX_DURATION_SECONDS))
            logger.debug('AWS role created successfully, attaching policy %s to role %s', policy_arn, role_name)
        except BotoClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                logger.debug('AWS role %s already exists', role_name)
            else:
                raise e
        await loop.run_in_executor(None, partial(iam_client.attach_role_policy, RoleName=role_name, PolicyArn=policy_arn))
        logger.debug('AWS role attached successfully')

        # Create and post AWSCredentials object, then create and post Volume object.
        person.add_group_id(group_id)
        logger.debug('Creating new credentials for account %r, person %r, and group %r', aws_account, person, group)
        new_credentials = aws_account.new_credentials(person, [group])
        assert new_credentials is not None, 'AWS credentials is unexpectedly None'
        new_credentials.display_name = f'Collaborator on AWS account {account_id}'
        new_credentials.owner = CREDENTIALS_MANAGER_USER
        new_credentials.temporary = True
        new_credentials.managed = True
        share = ShareImpl()
        share.user = collaborator_id
        share.permissions = [Permission.VIEWER]
        new_credentials.add_share(share)

        # Get volume for account, and if there is a volume that isn't a collaborator volume, error out.
        # The organizations microservice just overwrites the volume info since it's by definition higher access.
        logger.debug('User %s can be a collaborator', collaborator_id)
        if volume_ is not None:
            logger.debug('Volume %s found', volume_name)
            volume = volume_
        else:
            logger.debug('Volume %s not found, so creating a new volume', volume_name)
            volume = Volume()
            volume.name = volume_name
            volume.file_system_type = AWSFileSystem.get_type_name()
        volume.account_id = aws_account.instance_id
        volume.credential_type_name = AWSCredentials.get_type_name()
        volume.owner = CREDENTIALS_MANAGER_USER
        volume.add_share(share)

        aws_credentials_url = await type_to_resource_url(request, AWSCredentials)
        try:
            logger.debug('Trying to post a credentials object: %r', new_credentials)
            new_credentials_url = await client.post(request.app, aws_credentials_url, new_credentials,
                                                    headers=cred_man_sub_headers)
            credential_id = new_credentials_url[new_credentials_url.rindex('/') + 1:]
        except ClientResponseError as e:
            if e.status == 409:
                logger.debug('Existing credentials object %r; getting existing one', new_credentials)
                assert new_credentials.name is not None, 'new_credentials.name cannot be None'
                credentials_by_name = await client.get(request.app,
                                                    URL(aws_credentials_url) / 'byname' / new_credentials.name,
                                                    AWSCredentials, headers=collab_sub_headers)
                logger.debug('Got existing credentials %r', credentials_by_name)
                assert credentials_by_name is not None, 'credentials_by_name cannot be None'
                assert credentials_by_name.id is not None, 'credentials_by_name.id cannot be None'
                credentials_by_name.expiration = None  # force existing temporary credentials to refresh.
                logger.debug('Updating existing credentials %r', credentials_by_name)
                await client.put(request.app, URL(aws_credentials_url) / credentials_by_name.id, credentials_by_name,
                                 headers=cred_man_sub_headers)
                logger.debug('Updating existing credentials successfully')
                credential_id = credentials_by_name.id
            else:
                raise e
        volume.credential_id = credential_id

        if volume_ is not None:
            logger.debug('Updating volume %r', volume)
            assert volume.id is not None, 'volume.id cannot be None'
            await client.put(request.app, URL(volume_url) / volume.id, volume, headers=cred_man_sub_headers)
            logger.debug('Updated volume successfully')
        else:
            logger.debug('Creating volume %r', volume)
            await client.post(request.app, volume_url, volume, headers=cred_man_sub_headers)
            logger.debug('Created volume successfully')

        organization_url = await type_to_resource_url(request, Organization)
        assert aws_account.instance_id is not None, 'aws_account.instance_id cannot be None'

        async with _update_collaborators_lock:
            organization = await client.get(request.app, URL(organization_url) / 'byaccountid' / aws_account.instance_id,
                                            Organization, headers=sub_headers)
            logger.debug('Found organization %r', organization)
            if organization is not None and person.id not in organization.collaborator_ids:
                collaborator = AddingCollaborator()
                collaborator.collaborator_id = person.id
                collaborator.first_name = person.first_name
                collaborator.last_name = person.last_name
                collaborator.preferred_name = person.preferred_name
                collaborator.actual_object_id = person.id
                collaborator.actual_object_type_name = Person.get_type_name()
                collaborator.actual_object_uri = f'people/{person.id}'
                collaborator.to_organization_id = organization.id
                logger.debug('Preparing to publish desktop object %r successfully', collaborator)
                await publish_desktop_object(request.app, collaborator)
                logger.debug('Published desktop object %r successfully', collaborator)
    except ClientResponseError as e:
        if e.status == 409:
            raise response.status_conflict()
        else:
            raise response.status_internal_error()

async def _add_bucket_to_policy(bucket_name: str, collaborator_id: str, iam_client: IAMClient) -> PolicyTypeDef:
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    policy_name = _collaborator_policy_name_template.format(user_id=collaborator_id)
    try:
        policy_arn, policy_doc = await _get_policy_by(iam_client, collaborator_id)
        await _detach_and_delete_policy(iam_client, policy_arn)
        policy_doc = _new_policy_doc(set(_get_buckets_from(policy_doc) + [bucket_name]))
    except ValueError:
        policy_doc = _new_policy_doc([bucket_name])
    logger.debug('Creating policy with policy document %s', policy_doc)
    return (await loop.run_in_executor(None, partial(iam_client.create_policy,
                                                       PolicyName=policy_name,
                                                       Path=_collab_policy_path, PolicyDocument=orjson.dumps(policy_doc).decode('utf-8'))))['Policy']


async def _remove_bucket_from_policy_or_delete_policy(bucket_name: str, collaborator_id: str, iam_client: IAMClient, role_name: str):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    policy_name = _collaborator_policy_name_template.format(user_id=collaborator_id)
    try:
        policy_arn, policy_doc = await _get_policy_by(iam_client, collaborator_id)
        await _detach_and_delete_policy(iam_client, policy_arn)
        new_bucket_set = set(bucket_nm for bucket_nm in _get_buckets_from(policy_doc) if bucket_nm != bucket_name)
        if new_bucket_set:
            policy_doc = _new_policy_doc(new_bucket_set)
            logger.debug('Creating policy with policy document %s', policy_doc)
            policy = (await loop.run_in_executor(None, partial(iam_client.create_policy,
                                                            PolicyName=policy_name,
                                                            Path=_collab_policy_path, PolicyDocument=orjson.dumps(policy_doc).decode('utf-8'))))['Policy']
            await loop.run_in_executor(None, partial(iam_client.attach_role_policy, RoleName=role_name, PolicyArn=policy['Arn']))
    except ValueError:
        pass



def _to_aws_tags(hea_tags: list[Tag]) -> list[dict[str, str | None]]:
    """
    :param hea_tags: HEA tags to converted to aws tags compatible with boto3 api
    :return: aws tags
    """
    aws_tag_dicts = []
    for hea_tag in hea_tags:
        aws_tag_dict = {}
        aws_tag_dict['Key'] = hea_tag.key
        aws_tag_dict['Value'] = hea_tag.value
        aws_tag_dicts.append(aws_tag_dict)
    return aws_tag_dicts


_role_template = 'aws-Collaborator.Role_{user_id}'
_collaborator_policy_name_prefix = 'aws-Collaborator.Policy_'
_collaborator_policy_name_template = _collaborator_policy_name_prefix + '{user_id}'
_role_arn_template = 'arn:aws:iam::{account_id}:role/aws-Collaborator.Role_{user_id}'
_collab_policy_path = '/heainternal/collaborators/'
_policy_arn_template = 'arn:aws:iam::{account_id}:policy' + _collab_policy_path + _collaborator_policy_name_template
_arn_pattern = re.compile("[:/]")

def _new_policy_doc(bucket_names: Collection[str]) -> PolicyDocumentDictTypeDef:
    resources = list(chain.from_iterable((f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*") for bucket_name in bucket_names))
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "HEA0",
                "Effect": "Allow",
                "Action": [
                    "s3:GetBucketTagging",
                    "s3:GetObjectRetention",
                    "s3:ListBucketVersions",
                    "s3:RestoreObject",
                    "s3:ListBucket",
                    "s3:GetBucketVersioning",
                    "s3:GetBucketPolicy",
                    "s3:GetBucketObjectLockConfiguration",
                    "s3:GetObject",
                    "s3:GetEncryptionConfiguration",
                    "s3:GetObjectTagging",
                    "s3:GetBucketLocation",
                    "s3:GetObjectVersion"
                ],
                "Resource": resources
            },
            {
                "Sid": "HEA1",
                "Effect": "Allow",
                "Action": "s3:ListAllMyBuckets",
                "Resource": "*"
            }
        ]
    }

def _get_buckets_from(policy_doc: PolicyDocumentTypeDef | PolicyDocumentDictTypeDef) -> list[str]:
    assert not isinstance(policy_doc, str), 'Unexpected str'
    stmt = policy_doc['Statement']
    assert not isinstance(stmt, str), 'Unexpected str'
    resource = stmt[0]['Resource']
    if isinstance(resource, str):
        return [_arn_pattern.split(resource)[5]]
    else:
        return [_arn_pattern.split(arn)[5] for arn in resource]
