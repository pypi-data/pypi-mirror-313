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

import 'bootstrap';
import 'select2/dist/js/select2.full.js';
import Vue from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';
import i18next from 'i18next';
import jQuery from 'jquery';

// Additional imports for Day.js
import 'dayjs/locale/de.js';
import LocalizedFormat from 'dayjs/plugin/localizedFormat.js';
import RelativeTime from 'dayjs/plugin/relativeTime.js';

import 'styles/main.scss';
import translations from 'translations/translations.js';
import utils from 'scripts/lib/utils.js';

// Namespace for globally accessible objects.
window.kadi = kadi;
// Namespace for global utility functions.
window.kadi.utils = utils;

window.$t = i18next.t;
window.$ = window.jQuery = jQuery;
window.axios = axios;
window.dayjs = dayjs;
window.i18next = i18next;
window.Vue = Vue;

// Global axios settings.
axios.defaults.headers.common['X-CSRF-TOKEN'] = kadi.globals.csrfToken;
axios.defaults.params = {_internal: true};
axios.defaults.paramsSerializer = {indexes: null};

// Global Day.js settings.
dayjs.locale(kadi.globals.locale);
dayjs.extend(LocalizedFormat);
dayjs.extend(RelativeTime);

// Global i18next settings.
i18next.init({
  fallbackLng: false,
  keySeparator: false,
  lng: kadi.globals.locale,
  nsSeparator: false,
  resources: translations,
  returnEmptyString: false,
  supportedLngs: Object.keys(translations),
});

// Global jQuery settings.
$.ajaxSetup({
  headers: {'X-CSRF-TOKEN': kadi.globals.csrfToken},
  traditional: true,
});

// Global Vue settings.
Vue.options.delimiters = ['{$', '$}']; // For using Vue and Jinja in the same template.

Vue.prototype.kadi = kadi;
Vue.prototype.$t = i18next.t;
Vue.prototype.$ = Vue.prototype.jQuery = jQuery;

// Global Vue directives.
function trimEmptyTextNodes(el) {
  for (const node of el.childNodes) {
    if (node.nodeType === window.Node.TEXT_NODE && node.data.trim() === '') {
      node.remove();
    }
  }
}

Vue.directive('trim-ws', {
  inserted: trimEmptyTextNodes,
  componentUpdated: trimEmptyTextNodes,
});

// Global Vue components. All components inside 'components/global' are registered.
const componentsContext = import.meta.webpackContext('./components/global', {recursive: true, regExp: /\.vue$/});

componentsContext.keys().forEach((fileName) => {
  const componentName = fileName.split('/').pop().replace(/\.\w+$/, '');
  const componentConfig = componentsContext(fileName);
  Vue.component(componentName, componentConfig.default);
});

// Global Bootstrap settings.
const whiteList = $.fn.popover.Constructor.Default.whiteList;

for (const elem of ['button', 'dd', 'dl', 'dt', 'table', 'tbody', 'td', 'th', 'thead', 'tr']) {
  whiteList[elem] = [];
}

// Global Select2 settings.
$.fn.select2.defaults.set('theme', 'bootstrap4');
