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
  <div v-if="showLangPrompt" class="card bg-light">
    <div class="card-body py-3">
      <div class="row align-items-center">
        <div class="col-lg-9">
          Based on your browser settings, you seem to prefer a different language. Do you want to change the current
          language?
        </div>
        <div class="col-lg-3 mt-2 mt-lg-0 d-lg-flex justify-content-end">
          <div>
            <button type="button" class="btn btn-sm btn-primary" @click="acceptPrompt">Yes</button>
            <button type="button" class="btn btn-sm btn-light" @click="dismissPrompt">No</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import localeCookieMixin from 'scripts/components/mixins/locale-cookie-mixin';

export default {
  mixins: [localeCookieMixin],
  props: {
    preferredLocale: String,
  },
  data() {
    return {
      storageKey: 'hide_lang_prompt',
      showLangPrompt: false,
    };
  },
  mounted() {
    const hasLocaleCookie = Boolean(Cookies.get(this.cookieName));
    const promptDismissed = Boolean(window.localStorage.getItem(this.storageKey));

    if (!hasLocaleCookie && !promptDismissed && this.preferredLocale !== kadi.globals.locale) {
      this.showLangPrompt = true;
    }
  },
  methods: {
    acceptPrompt() {
      this.dismissPrompt();
      this.switchLocale(this.preferredLocale);
    },
    dismissPrompt() {
      this.showLangPrompt = false;
      window.localStorage.setItem(this.storageKey, 'true');
    },
  },
};
</script>
