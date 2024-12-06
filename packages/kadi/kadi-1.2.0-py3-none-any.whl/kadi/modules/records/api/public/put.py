# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import current_app
from flask import request
from flask_babel import gettext as _
from flask_login import current_user
from werkzeug.datastructures import MultiDict

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import reqheaders
from kadi.lib.api.utils import reqschema
from kadi.lib.api.utils import status
from kadi.lib.exceptions import KadiStorageError
from kadi.lib.format import filesize
from kadi.lib.permissions.utils import permission_required
from kadi.modules.records.forms import UploadChunkForm
from kadi.modules.records.forms import UploadDataForm
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import Upload
from kadi.modules.records.models import UploadState
from kadi.modules.records.models import UploadType
from kadi.modules.records.schemas import FileSchema
from kadi.modules.records.schemas import UploadSchema
from kadi.modules.records.uploads import delete_upload
from kadi.modules.records.uploads import save_chunk_data
from kadi.modules.records.uploads import save_upload_data
from kadi.modules.records.utils import get_user_quota


@bp.put("/records/<int:record_id>/files/<uuid:file_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@reqschema(
    UploadSchema(exclude=["name"]), description="The metadata of the new upload."
)
@status(201, "Return the new upload.")
@status(413, "The user's upload quota was exceeded.")
def edit_file_data(record_id, file_id, schema):
    """Update the data of a file of a record.

    This endpoint will initiate a new upload with the given metadata in the record
    specified by the given *record_id*, replacing the data of the file specified by the
    given *file_id* once the upload is finished. The corresponding file data has to be
    uploaded separately in the same way as for new uploads, see the following
    :http:post:`endpoint </api/records/(int:id)/uploads>`.
    """
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()
    data = schema.load_or_400()

    upload = Upload.create(
        creator=current_user, record=record, file=file, name=file.name, **data
    )
    db.session.commit()

    max_quota = current_app.config["UPLOAD_USER_QUOTA"]

    if max_quota is not None and get_user_quota() > max_quota:
        delete_upload(upload)
        db.session.commit()

        return json_error_response(
            413,
            description=_(
                "Maximum upload quota exceeded (%(filesize)s).",
                filesize=filesize(max_quota),
            ),
        )

    return json_response(201, UploadSchema().dump(upload))


CHECKSUM_HEADER = "Kadi-MD5-Checksum"
CHUNK_INDEX_HEADER = "Kadi-Chunk-Index"
CHUNK_SIZE_HEADER = "Kadi-Chunk-Size"


@bp.put("/records/<int:record_id>/uploads/<uuid:upload_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@reqheaders(
    {
        CHECKSUM_HEADER: {
            "description": "An MD5 hash of the content of the uploaded data. If given,"
            " it will be used to verify the integrity of the data once uploaded.",
        },
        CHUNK_INDEX_HEADER: {
            "required": True,
            "description": "The index of an uploaded chunk starting at ``0``. Only"
            " relevant for chunked uploads.",
        },
        CHUNK_SIZE_HEADER: {
            "required": True,
            "description": "The size of an uploaded chunk in bytes. Only relevant for"
            " chunked uploads.",
        },
    }
)
@status(200, "Return the updated upload. Only relevant for chunked uploads")
@status(201, "Return the new file. Only relevant for direct uploads.")
@status(
    409,
    "A conflict occured while completing the upload. Only relevant for direct uploads.",
)
def upload_data(record_id, upload_id):
    """Upload the data of an upload.

    This endpoint is used to upload file data to the upload specified by the given
    *upload_id* of the record specified by the given *record_id*. Only uploads owned by
    the current user can be uploaded to.

    The actual data has to be uploaded as a binary stream of a file's content using the
    generic ``application/octet-stream`` content type. Which contents to actually upload
    depends on the upload type (see also the following
    :http:post:`endpoint </api/records/(int:id)/uploads>`):

    * For **direct** uploads, the whole file content is uploaded. Once the data is
      uploaded successfully, the upload process is finished.
    * For **chunked** uploads, the file content is uploaded in multiple chunks. Once all
      chunks have been uploaded successfully, the upload has to be finished using the
      following :http:post:`endpoint
      </api/records/(int:record_id)/uploads/(uuid:upload_id)>`, which is also returned
      as the ``_actions.finish`` property of the returned upload.
    """
    record = Record.query.get_active_or_404(record_id)
    upload = record.uploads.filter(
        Upload.id == upload_id,
        Upload.user_id == current_user.id,
        Upload.state == UploadState.ACTIVE,
    ).first_or_404()

    if upload.upload_type == UploadType.DIRECT:
        form = UploadDataForm(
            formdata=MultiDict({"checksum": request.headers.get(CHECKSUM_HEADER, "")})
        )
    else:
        form = UploadChunkForm(
            upload.chunk_count,
            formdata=MultiDict(
                {
                    "index": request.headers.get(CHUNK_INDEX_HEADER, ""),
                    "size": request.headers.get(CHUNK_SIZE_HEADER, ""),
                    "checksum": request.headers.get(CHECKSUM_HEADER, ""),
                }
            ),
        )

    if not form.validate():
        return json_error_response(400, errors=form.errors)

    if upload.upload_type == UploadType.DIRECT:
        upload.state = UploadState.PROCESSING
        db.session.commit()

        try:
            file = save_upload_data(upload, request.stream, checksum=form.checksum.data)
        except KadiStorageError as e:
            return json_error_response(400, description=str(e))

        if file is None:
            return json_response(409, "Error creating or updating file.")

        return json_response(201, FileSchema().dump(file))

    try:
        save_chunk_data(
            upload,
            request.stream,
            index=form.index.data,
            size=form.size.data,
            checksum=form.checksum.data,
        )
    except KadiStorageError as e:
        return json_error_response(400, description=str(e))

    return json_response(200, UploadSchema().dump(upload))
