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
  <input ref="input" class="form-control time-picker-input">
</template>

<!-- Not scoped on purpose, as the new elements are attached to the body. -->
<style lang="scss">
@import '~flatpickr/dist/flatpickr.css';

.flatpickr-day {
  &.selected, &.selected:hover {
    background: #2c3e50 !important;
    border-color: #2c3e50 !important;
  }
}

.flatpickr-input {
  background-color: white !important;
}

.flatpickr-months {
  margin-top: 7px;
  font-size: 10pt;

  .flatpickr-prev-month:hover svg, .flatpickr-next-month:hover svg {
    fill: #2c3e50;
  }

  .flatpickr-current-month .numInputWrapper {
    padding-left: 5px;

    .arrowUp, .arrowDown {
      display: none;
    }
  }
}

.flatpickr-time .numInputWrapper {
  .arrowUp, .arrowDown {
    width: 20px;
    padding-left: 5px;
  }
}
</style>

<script>
import flatpickr from 'flatpickr';

import 'flatpickr/dist/l10n/de.js';

export default {
  props: {
    initialValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      altInput: '',
      initialValueSet: false,
      picker: null,
    };
  },
  mounted() {
    this.$el.addEventListener('change', (e) => {
      if (!e._propagate) {
        e.stopPropagation();
      }
    });

    this.picker = flatpickr(this.$refs.input, {
      animate: false,
      closeOnSelect: true,
      defaultHour: 0,
      disableMobile: true,
      enableSeconds: true,
      enableTime: true,
      locale: kadi.globals.locale,
      minuteIncrement: 1,
      monthSelectorType: 'static',
      secondIncrement: 1,
      formatDate: this.formatDate,
      onChange: (dates) => {
        if (dates.length > 0) {
          this.altInput = dates[0].toISOString();
        } else {
          this.altInput = '';
        }

        // Ignore the change event triggered by a potential initial value.
        if (this.initialValueSet) {
          this.$emit('input', this.altInput);

          // Dispatch a native 'change' event from the element as well.
          const event = new Event('change', {bubbles: true});
          // Only let our own event through.
          event._propagate = true;

          this.$el.dispatchEvent(event);
        } else {
          this.initialValueSet = true;
        }
      },
    });

    const date = dayjs(this.initialValue);

    if (date.isValid()) {
      this.altInput = date.toISOString();
      this.picker.setDate(date.toDate(), true);
    } else {
      this.initialValueSet = true;
    }
  },
  beforeDestroy() {
    this.picker.destroy();
  },
  methods: {
    formatDate(date) {
      return dayjs(date).format('LL LTS');
    },
  },
};
</script>
