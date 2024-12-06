<!-- Copyright 2022 Karlsruhe Institute of Technology
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
    <div v-for="message in messages" :key="message.id">
      <flash-message class="mb-4" :message="message.message" :type="message.type" :timeout="message.timeout">
      </flash-message>
    </div>
  </div>
</template>

<script>
import FlashMessage from 'scripts/components/lib/base/FlashMessage.vue';

export default {
  components: {
    FlashMessage,
  },
  data() {
    return {
      messages: [],
    };
  },
  methods: {
    addMessage(type, message, options) {
      let _message = message;
      const settings = {
        request: null,
        timeout: 5_000,
        scrollTo: true,
        ...options,
      };

      if (settings.request !== null) {
        // Do nothing if the error originates from a canceled request.
        if (settings.request.status === 0) {
          return;
        }

        _message = `${message} (${settings.request.status})`;
      }

      this.messages.push({
        id: kadi.utils.randomAlnum(),
        message: _message,
        type,
        timeout: settings.timeout,
      });

      if (settings.scrollTo) {
        kadi.utils.scrollIntoView(this.$el, 'bottom');
      }
    },
    flashDanger(message, options) {
      this.addMessage('danger', message, options);
    },
    flashInfo(message, options) {
      this.addMessage('info', message, options);
    },
    flashSuccess(message, options) {
      this.addMessage('success', message, options);
    },
    flashWarning(message, options) {
      this.addMessage('warning', message, options);
    },
  },
};
</script>
