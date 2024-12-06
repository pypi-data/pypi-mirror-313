<!-- Copyright 2023 Karlsruhe Institute of Technology
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
    <em v-if="scope === null">{{ $t('Full access') }}</em>
    <div v-else @pointerover="showAllScopes = true" @pointerleave="showAllScopes = false">
      <div v-if="showAllScopes">
        <pre class="ws-pre-wrap mb-0">{{ allScopes }}</pre>
      </div>
      <div v-else>
        <pre class="ws-pre-wrap mb-0">{{ firstShownScopes }}</pre>
        <em>{{ scopesHoverText }}</em>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    scope: String,
    numScopesShown: {
      type: Number,
      default: 2,
    },
  },
  data() {
    return {
      scopesList: [],
      showAllScopes: false,
    };
  },
  computed: {
    allScopes() {
      return this.scopesList.join('\n');
    },
    firstShownScopes() {
      if (this.scopesList.length <= this.numScopesShown) {
        return this.allScopes;
      }

      return this.scopesList.slice(0, this.numScopesShown).join('\n');
    },
    scopesHoverText() {
      if (this.scopesList.length <= this.numScopesShown) {
        return '';
      }

      const numMoreScopes = this.scopesList.length - this.numScopesShown;
      return $t('...and {{count}} more', {count: numMoreScopes});
    },
  },
  mounted() {
    if (this.scope !== null) {
      this.scopesList = this.scope.split(' ');
    }
  },
};
</script>
