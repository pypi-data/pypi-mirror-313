<!-- Copyright 2024 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div :id="`select-file-${id}`">
      <dynamic-selection container-classes="select2-single-sm"
                         :placeholder="$t('Select a JSON file')"
                         :endpoint="endpoints.selectJson"
                         :reset-on-select="true"
                         :dropdown-parent="`#select-file-${id}`"
                         @select="selectFile">
      </dynamic-selection>
    </div>

    <div v-for="(file, index) in settings_.files" :key="file.id" class="input-group input-group-sm mt-2">
      <input class="form-control" :value="file.name" disabled>

      <div class="input-group-append">
        <button type="button"
                class="input-group-text btn btn-sm btn-light"
                :title="$t('Remove file')"
                @click="removeFile(index)">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import dashboardSettingsMixin from 'scripts/components/mixins/dashboard-settings-mixin';

export default {
  mixins: [dashboardSettingsMixin],
  methods: {
    selectFile(file) {
      if (this.settings_.files.find((f) => f.id === file.id)) {
        return;
      }

      this.settings_.files.push({
        id: file.id,
        name: file.text,
        downloadEndpoint: new URL(file.download_endpoint).pathname,
      });
    },
    removeFile(index) {
      this.settings_.files.splice(index, 1);
    },
  },
};
</script>
