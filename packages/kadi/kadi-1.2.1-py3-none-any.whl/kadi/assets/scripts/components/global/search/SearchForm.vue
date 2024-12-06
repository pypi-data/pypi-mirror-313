<!-- Copyright 2021 Karlsruhe Institute of Technology
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
    <div v-if="extrasSearch" :id="extrasId" class="mb-4">
      <search-extras :query-string="extras" @change="extras = $event" @search="search"></search-extras>
    </div>
    <div class="form-row">
      <div class="mb-2 mb-xl-0" :class="{'col-xl-6': extrasSearch, 'col-xl-8': !extrasSearch}">
        <div class="input-group">
          <input :id="queryId"
                 v-model="query"
                 class="form-control"
                 :placeholder="$t('Search title, identifier and description')"
                 @keydown.enter="search">
          <clear-button :input="query" :input-id="queryId" @clear-input="query = ''"></clear-button>
          <div class="input-group-append">
            <button type="button"
                    class="btn btn-light"
                    :disabled="!query"
                    :title="$t('Toggle whole word match')"
                    @click="toggleQuotation">
              <i class="fa-solid fa-quote-left"></i>
            </button>
            <button type="button" class="btn btn-light" :title="$t('Execute search')" @click="search">
              <i class="fa-solid fa-magnifying-glass"></i> {{ $t('Search') }}
            </button>
          </div>
        </div>
      </div>
      <div class="col-xl-4 mb-2 mb-xl-0">
        <div class="input-group">
          <div class="input-group-prepend">
            <label class="input-group-text" :for="sortId">{{ $t('Sort by') }}</label>
          </div>
          <select :id="sortId" v-model="sort" class="custom-select">
            <option v-for="option in sortOptions" :key="option[0]" :value="option[0]">{{ option[1] }}</option>
          </select>
        </div>
      </div>
      <div v-if="extrasSearch" class="col-xl-2">
        <collapse-item :id="extrasId"
                       class="btn btn-block btn-light"
                       :is-collapsed="!extrasSearchActive"
                       :title="$t('Search extra metadata')"
                       @collapse="extrasSearchActive = !$event">
          {{ $t('Extras') }}
        </collapse-item>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    extrasSearch: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      query: '',
      prevQuery: '',
      queryParam: 'query',
      queryId: kadi.utils.randomAlnum(),
      sort: '_score',
      sortParam: 'sort',
      sortId: kadi.utils.randomAlnum(),
      sortOptions: [
        ['_score', $t('Relevance')],
        ['-last_modified', $t('Last modified (newest first)')],
        ['last_modified', $t('Last modified (oldest first)')],
        ['-created_at', $t('Created at (newest first)')],
        ['created_at', $t('Created at (oldest first)')],
        ['title', $t('Title (ascending)')],
        ['-title', $t('Title (descending)')],
        ['identifier', $t('Identifier (ascending)')],
        ['-identifier', $t('Identifier (descending)')],
      ],
      extras: '[]',
      prevExtras: '[]',
      extrasParam: 'extras',
      extrasId: kadi.utils.randomAlnum(),
      extrasSearchActive: false,
      prevExtrasSearchActive: false,
      initialized: false,
    };
  },
  watch: {
    sort() {
      if (this.initialized) {
        this.setSearchParam(this.sort !== this.sortOptions[0][0], this.sortParam, this.sort);
        this.$emit('search');
      }
    },
  },
  async beforeMount() {
    if (kadi.utils.hasSearchParam(this.queryParam)) {
      this.query = kadi.utils.getSearchParam(this.queryParam);
      this.prevQuery = this.query;

      this.setSearchParam(this.query, this.queryParam, this.query);
    }

    if (kadi.utils.hasSearchParam(this.extrasParam)) {
      this.extras = kadi.utils.getSearchParam(this.extrasParam);
      this.prevExtras = this.extras;
      this.prevExtrasSearchActive = this.extrasSearchActive = true;

      this.setSearchParam(this.extrasSearchActive, this.extrasParam, this.extras);
    }

    if (kadi.utils.hasSearchParam(this.sortParam)) {
      const sort = kadi.utils.getSearchParam(this.sortParam);

      for (const option of this.sortOptions) {
        if (option[0] === sort) {
          this.sort = sort;
          break;
        }
      }

      this.setSearchParam(this.sort !== this.sortOptions[0][0], this.sortParam, this.sort);
    }

    // Skip first potential change.
    await this.$nextTick();
    this.initialized = true;
  },
  methods: {
    toggleQuotation() {
      if (kadi.utils.isQuoted(this.query)) {
        this.query = this.query.slice(1, this.query.length - 1);
      } else {
        this.query = `"${this.query}"`;
      }
    },
    setSearchParam(condition, param, value) {
      let url = null;

      if (condition) {
        url = kadi.utils.setSearchParam(param, value);
      } else {
        url = kadi.utils.removeSearchParam(param);
      }

      kadi.utils.replaceState(url);
    },
    search() {
      // Do not search if nothing changed.
      if (this.query === this.prevQuery
          && this.extras === this.prevExtras
          && this.extrasSearchActive === this.prevExtrasSearchActive) {
        return;
      }

      this.setSearchParam(this.query, this.queryParam, this.query);
      this.setSearchParam(this.extrasSearchActive, this.extrasParam, this.extras);

      this.$emit('search');

      this.prevQuery = this.query;
      this.prevExtras = this.extras;
      this.prevExtrasSearchActive = this.extrasSearchActive;
    },
  },
};
</script>
