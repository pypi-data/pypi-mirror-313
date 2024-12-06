# Copyright 2022 Karlsruhe Institute of Technology
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
from flask_babel import lazy_gettext as _l

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.forms import BaseForm
from kadi.lib.forms import JSONField
from kadi.modules.records.export import RecordROCrate
from kadi.modules.records.extras import ExtrasField


class ExportFilterField(JSONField):
    """Custom field to process and validate export filter data.

    Only performs some basic validation to make sure the overall structure of the filter
    is valid.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = {}
        super().__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)

        if valuelist:
            if not isinstance(self.data, dict):
                self.data = self.default
                raise ValueError("Invalid data structure.")


class ZenodoForm(BaseForm):
    """Base form class for use in publishing resources via Zenodo."""

    class Meta:
        """Container to store meta class attributes."""

        csrf = False

    export_filter = ExportFilterField(_l("Customize export data"))

    extras = ExtrasField(_l("Customize import metadata"))


class UploadCanceledException(Exception):
    """For exceptions related to canceled uploads."""


class UploadStream:
    """Helper class to handle uploading resource data as RO-Crate."""

    def __init__(self, record_or_records, resource, export_filter, user, task=None):
        self.ro_crate = RecordROCrate(
            record_or_records,
            resource.identifier,
            resource.title,
            genre=resource.__tablename__,
            export_filter=export_filter,
            user=user,
        )
        self.task = task

        # Total size of the data that was streamed so far.
        self._total_size = 0
        # Current size of the data that was streamed since the last time the task status
        # was checked, if applicable.
        self._current_size = 0

    def __iter__(self):
        for chunk in self.ro_crate:
            self._total_size += len(chunk)

            if self.task is not None:
                self._current_size += len(chunk)

                if self._current_size >= 10 * const.ONE_MB:
                    self._current_size = 0

                    if self.task.is_revoked:
                        raise UploadCanceledException

                    self.task.update_progress(self._total_size / len(self) * 100)
                    db.session.commit()

            yield chunk

    def __len__(self):
        return len(self.ro_crate)
