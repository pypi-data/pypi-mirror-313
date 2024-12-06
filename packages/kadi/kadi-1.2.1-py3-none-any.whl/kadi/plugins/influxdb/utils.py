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
from marshmallow import ValidationError
from marshmallow import fields

from kadi.lib.forms import JSONField
from kadi.lib.plugins.core import PluginConfigForm
from kadi.lib.schemas import BaseSchema

from . import PLUGIN_NAME


class _InfluxDBSchema(BaseSchema):
    name = fields.String(required=True)

    token = fields.String(required=True)

    title = fields.String(required=True)


class InfluxDBField(JSONField):
    """Custom field to process and validate InfluxDB instances."""

    def __init__(self, *args, **kwargs):
        kwargs["default"] = []
        super().__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)

        if valuelist:
            try:
                schema = _InfluxDBSchema(many=True)
                self.data = schema.load(self.data)

            except ValidationError as e:
                self.data = self.default
                raise ValueError("Invalid data structure.") from e


class InfluxDBConfigForm(PluginConfigForm):
    """Form for configuring InfluxDB instances."""

    influxdbs = InfluxDBField()

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, plugin_name=PLUGIN_NAME, encrypted_fields={"influxdbs"}, **kwargs
        )
