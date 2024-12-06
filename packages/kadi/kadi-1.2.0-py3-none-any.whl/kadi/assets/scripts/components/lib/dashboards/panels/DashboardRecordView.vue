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
    <div v-if="template" class="mt-1 mb-2">
      <a target="_blank"
         rel="noopener noreferrer"
         class="btn btn-sm btn-primary"
         :href="newRecordEndpoint">
        {{ $t('New record') }}
      </a>
    </div>

    <div class="w-100">
      <resource-view :title="$t('Records')"
                     :placeholder="$t('No records.')"
                     :endpoint="recordsEndpoint"
                     :per-page="perPage"
                     :show-description="false"
                     :enable-filter="false">
      </resource-view>
    </div>
  </div>
</template>

<script>
import dashboardPanelMixin from 'scripts/components/mixins/dashboard-panel-mixin';

export default {
  mixins: [dashboardPanelMixin],
  data() {
    return {
      perPageParam: 'per_page',
      perPage: 6,
    };
  },
  computed: {
    template() {
      return this.settings.template;
    },
    queryString() {
      return this.settings.queryString;
    },
    newRecordEndpoint() {
      if (!this.template) {
        return null;
      }

      const url = kadi.utils.setSearchParam('template', this.template.id, true, this.endpoints.newRecord);
      return url.toString();
    },
    recordsEndpoint() {
      let url = this.endpoints.records;
      const params = new URLSearchParams(this.queryString);

      for (const [key, value] of params) {
        if ([this.perPageParam, 'page'].includes(key)) {
          continue;
        }

        url = kadi.utils.setSearchParam(key, value, false, url);
      }

      return url.toString();
    },
  },
  watch: {
    queryString() {
      this.updatePerPage();
    },
  },
  created() {
    this.updatePerPage();
  },
  methods: {
    updatePerPage() {
      const params = new URLSearchParams(this.queryString);
      const perPage = Number.parseInt(params.get(this.perPageParam), 10);

      if (perPage) {
        this.perPage = Math.max(1, perPage);
      }
    },
  },
};
</script>
