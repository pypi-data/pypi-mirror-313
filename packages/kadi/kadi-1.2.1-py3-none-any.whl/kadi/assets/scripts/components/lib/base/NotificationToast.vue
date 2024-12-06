<!-- Copyright 2020 Karlsruhe Institute of Technology
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
  <div ref="toast" class="toast mw-100" data-animation="false" data-autohide="false" data-delay="0">
    <div class="toast-header bg-primary">
      <span class="mr-auto">{{ title }}</span>
      <button type="button" class="close text-white ml-2" @click="dismiss">
        <i class="fa-solid fa-xmark fa-xs"></i>
      </button>
    </div>
    <div class="toast-body py-2">
      <div class="notification-body" v-html="body"></div>
      <div class="mt-1">
        <small class="text-muted">
          <from-now :timestamp="timestamp"></from-now>
        </small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notification-body {
  overflow-wrap: break-word;
}

.toast {
  box-shadow: none;
}
</style>

<script>
export default {
  props: {
    title: String,
    body: String,
    timestamp: String,
    dismissEndpoint: String,
  },
  mounted() {
    $(this.$refs.toast).toast('show');
  },
  beforeDestroy() {
    $(this.$refs.toast).toast('dispose');
  },
  methods: {
    async dismiss() {
      try {
        await axios.delete(this.dismissEndpoint);

        $(this.$refs.toast).toast('dispose');
        kadi.base.getNotifications();
      } catch (error) {
        kadi.base.flashDanger($t('Error dismissing notification.'), {request: error.request});
      }
    },
  },
};
</script>
