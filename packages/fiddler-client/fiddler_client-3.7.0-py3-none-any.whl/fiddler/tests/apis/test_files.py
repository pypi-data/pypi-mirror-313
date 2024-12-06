import os
from pathlib import Path
from uuid import UUID

import responses
from responses.matchers import multipart_matcher

from fiddler.entities.file import File
from fiddler.tests.constants import URL, USER_EMAIL, USER_ID, USER_NAME


FILE_NAME = 'model.yaml'
FILE_ID = 'f34ff7db-9653-49b5-b3d8-02c9670513a3'

SINGLE_UPLOAD_200_RESPONSE = {
    'api_version': '3.0',
    'data': {
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
        'filename': FILE_NAME,
        'id': FILE_ID,
        'status': 'SUCCESSFUL',
        'type': 'CSV',
        'created_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
        'updated_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
    },
    'kind': 'NORMAL',
}

MULTIPART_INIT_200_RESPONSE = {
    'api_version': '3.0',
    'data': {
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
        'filename': FILE_NAME,
        'id': FILE_ID,
        'status': 'SUCCESSFUL',
        'type': 'CSV',
        'created_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
        'updated_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
    },
    'kind': 'NORMAL',
}

MULTIPART_UPLOAD_200_RESPONSE = {
    'data': {'part_id': 'e887e82d-1f49-4de4-aca6-5dcdefa5f36c'},
    'api_version': '3.0',
    'kind': 'NORMAL',
}
MULTIPART_COMPLETE_200_RESPONSE = {
    'api_version': '3.0',
    'data': {
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
        'filename': FILE_NAME,
        'id': FILE_ID,
        'status': 'SUCCESSFUL',
        'type': 'CSV',
        'created_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
        'updated_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
    },
    'kind': 'NORMAL',
}

BASE_TEST_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_TEST_DIR / 'artifact_test_dir' / 'model.yaml'


@responses.activate
def test_single_upload_success() -> None:
    # Note(JP): this is to configure multipart matcher to inspect the
    # actual file upload.
    _data = open(FILE_PATH, 'rb').read()
    file = File(path=FILE_PATH, name=FILE_NAME)
    req_files = {'file': (file.name, _data)}

    responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
        match=[multipart_matcher(req_files)],
    )

    file.single_upload()
    assert isinstance(file, File)
    assert file.id == UUID(FILE_ID)

    file = File(
        path=str(FILE_PATH),
    ).single_upload()
    assert isinstance(file, File)
    assert file.id == UUID(FILE_ID)


@responses.activate
def test_multipart_upload_success() -> None:
    responses.post(
        url=f'{URL}/v3/files/multipart-init',
        json=MULTIPART_INIT_200_RESPONSE,
    )
    responses.post(
        url=f'{URL}/v3/files/multipart-upload',
        json=MULTIPART_UPLOAD_200_RESPONSE,
    )
    responses.post(
        url=f'{URL}/v3/files/multipart-complete',
        json=MULTIPART_COMPLETE_200_RESPONSE,
    )

    file = File(path=FILE_PATH, name=FILE_NAME).multipart_upload()
    assert isinstance(file, File)
    assert file.id == UUID(FILE_ID)


@responses.activate
def test_file_upload() -> None:
    multipart_init_resp = responses.post(
        url=f'{URL}/v3/files/multipart-init',
        json=MULTIPART_INIT_200_RESPONSE,
    )
    multipart_upload_resp = responses.post(
        url=f'{URL}/v3/files/multipart-upload',
        json=MULTIPART_UPLOAD_200_RESPONSE,
    )
    multipart_complete_resp = responses.post(
        url=f'{URL}/v3/files/multipart-complete',
        json=MULTIPART_COMPLETE_200_RESPONSE,
    )
    single_upload_resp = responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
    )
    chunk_size = os.path.getsize(FILE_PATH) // 2 + 1

    file_multi = File(path=FILE_PATH, name=FILE_NAME).upload(
        chunk_size=chunk_size,
    )

    assert isinstance(file_multi, File)
    assert multipart_init_resp.call_count == 1
    assert multipart_upload_resp.call_count == 2
    assert multipart_complete_resp.call_count == 1
    assert single_upload_resp.call_count == 0

    chunk_size = os.path.getsize(FILE_PATH) + 1
    file_single = File(path=FILE_PATH, name=FILE_NAME).upload(
        chunk_size=chunk_size,
    )

    assert isinstance(file_single, File)
    assert single_upload_resp.call_count == 1
