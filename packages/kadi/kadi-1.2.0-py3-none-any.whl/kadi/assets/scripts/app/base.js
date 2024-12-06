/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import {continueTour, hasProgress, initializeTour, startTour, tourActive} from 'scripts/lib/tour/core.js';
import BroadcastMessage from 'scripts/components/lib/base/BroadcastMessage.vue';
import FlashMessage from 'scripts/components/lib/base/FlashMessage.vue';
import FlashMessages from 'scripts/components/lib/base/FlashMessages.vue';
import HelpItem from 'scripts/components/lib/base/HelpItem.vue';
import LocaleChooser from 'scripts/components/lib/base/LocaleChooser.vue';
import NotificationManager from 'scripts/components/lib/base/NotificationManager.vue';
import QuickSearch from 'scripts/components/lib/base/QuickSearch.vue';
import RecentlyVisited from 'scripts/components/lib/base/RecentlyVisited.vue';

// Stop the logo animation once this script is loaded and the current animation iteration is finished.
document.querySelectorAll('.kadi-logo').forEach((el) => {
  el.addEventListener('animationiteration', () => el.style.animation = 'none');
  el.addEventListener('webkitAnimationIteration', () => el.style.animation = 'none');
});

// Scroll required inputs to a more sensible location, also taking different page layouts into account.
document.addEventListener('invalid', (e) => kadi.utils.scrollIntoView(e.target), true);

// Namespace for global base functionality and utility methods of base Vue components.
kadi.base = {
  newVue(options) {
    return new Vue({el: '#base-content', ...options});
  },
};

// Vue instance for the locale chooser in the navigation footer.
new Vue({el: '#base-locale-chooser', components: {LocaleChooser}});

// Vue instance for handling flash messages.
const flashMessages = new Vue({el: '#base-flash-messages', components: {FlashMessage, FlashMessages}});
const fmComponent = flashMessages.$refs.component;

Object.assign(kadi.base, {
  flashDanger: fmComponent.flashDanger,
  flashInfo: fmComponent.flashInfo,
  flashSuccess: fmComponent.flashSuccess,
  flashWarning: fmComponent.flashWarning,
});

// Vue instance for handling recently visited resources. Instantiated here so non-active users' items can be cleared.
const recentlyVisited = new Vue({el: '#base-recently-visited', components: {RecentlyVisited}});
const rvComponent = recentlyVisited.$refs.component;

kadi.base.visitItem = rvComponent.addItem;

// Initialization that should only be performed when the global broadcast message is shown.
if (kadi.globals.showBroadcast) {
  new Vue({el: '#base-broadcast-message', components: {BroadcastMessage}});
}

// Initializations that should only be performed for active users.
if (kadi.globals.userActive) {
  // Register global keyboard shortcuts.
  const keyMap = {
    'H': '',
    'R': 'records',
    'C': 'collections',
    'T': 'templates',
    'U': 'users',
    'G': 'groups',
  };

  // Do nothing if the user is either within an input field or if a tour is currently active.
  document.addEventListener('keydown', (e) => {
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)
        || e.target.contentEditable === 'true'
        || tourActive()) {
      return;
    }

    if (e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
      for (const [key, endpoint] of Object.entries(keyMap)) {
        if (e.key === key) {
          e.preventDefault();
          window.location.href = `/${endpoint}`;
          return;
        }
      }
    }
  });

  // Namespace for global tour functionality.
  kadi.base.tour = {
    continue: continueTour,
    hasProgress,
    initialize: initializeTour,
    start: startTour,
  };

  // Vue instance for the quick search in the navigation bar.
  new Vue({el: '#base-quick-search', components: {QuickSearch}});
  // Vue instance for the help item in the navigation bar.
  new Vue({el: '#base-help-item', components: {HelpItem}});

  // Vue instance for handling notifications.
  const notificationManager = new Vue({el: '#base-notification-manager', components: {NotificationManager}});
  const nmComponent = notificationManager.$refs.component;

  kadi.base.getNotifications = nmComponent.getNotifications;
}

// Initializations that should only be performed in production environments.
if (kadi.globals.environment === 'production') {
  console.info('If you found a bug, please report it at https://gitlab.com/iam-cms/kadi');
}
