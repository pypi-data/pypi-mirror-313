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
    <div v-for="notification in notifications" :key="notification.id">
      <notification-toast class="mb-4"
                          :title="notification.data.title"
                          :body="notification.data.body"
                          :timestamp="notification.created_at"
                          :dismiss-endpoint="notification._actions.dismiss">
      </notification-toast>
    </div>
  </div>
</template>

<script>
import NotificationToast from 'scripts/components/lib/base/NotificationToast.vue';

export default {
  components: {
    NotificationToast,
  },
  props: {
    endpoint: String,
  },
  data() {
    return {
      notifications: [],
      title: null,
      lastNotificationDate: null,
      currentTimeout: null,
      minTimeout: 5_000,
      maxTimeout: 30_000,
      pollTimeoutHandle: null,
    };
  },
  mounted() {
    this.title = document.title;
    this.currentTimeout = this.minTimeout;

    if (document.hasFocus()) {
      this.pollNotifications();
    }

    window.addEventListener('blur', this.onBlur);
    window.addEventListener('focus', this.onFocus);
    window.addEventListener('beforeunload', this.onBeforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('blur', this.onBlur);
    window.removeEventListener('focus', this.onFocus);
    window.removeEventListener('beforeunload', this.onBeforeUnload);
  },
  methods: {
    disablePolling() {
      window.clearTimeout(this.pollTimeoutHandle);
      this.pollTimeoutHandle = null;
    },
    pollNotifications() {
      // Clear any previous timeout, just in case.
      this.disablePolling();
      this.pollTimeoutHandle = window.setTimeout(this.pollNotifications, this.currentTimeout);

      // Make sure we don't retrieve notifications if the current timeout has not elapsed yet.
      if (this.lastNotificationDate === null || new Date() - this.lastNotificationDate >= this.currentTimeout) {
        this.getNotifications(false, false);
      }

      // Slowly increase the polling timeout up to the maximum.
      if (this.currentTimeout < this.maxTimeout) {
        this.currentTimeout += 1_000;
      }
    },
    async getNotifications(scrollTo = false, resetTimeout = true) {
      if (resetTimeout) {
        this.currentTimeout = this.minTimeout;
      }

      this.lastNotificationDate = new Date();

      try {
        const response = await axios.get(this.endpoint);

        this.notifications = response.data;
        const numNotifications = this.notifications.length;

        if (numNotifications > 0) {
          document.title = `(${numNotifications}) ${this.title}`;

          if (scrollTo) {
            this.$nextTick(() => kadi.utils.scrollIntoView(this.$el, 'bottom'));
          }

          // Start polling again if currently not the case.
          if (!this.pollTimeoutHandle) {
            this.pollNotifications();
          }
        } else {
          document.title = this.title;
          // If no notifications were retrieved, stop polling for the time being.
          this.disablePolling();
        }
      } catch {
        this.disablePolling();
      }
    },
    onBlur() {
      // Stop polling if the window is not in focus.
      this.disablePolling();
    },
    onFocus() {
      this.currentTimeout = this.minTimeout;
      // Start polling again if the window is back in focus.
      this.pollNotifications();
    },
    onBeforeUnload() {
      this.disablePolling();
    },
  },
};
</script>
