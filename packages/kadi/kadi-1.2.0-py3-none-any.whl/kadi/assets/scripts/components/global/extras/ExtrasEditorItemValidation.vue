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
  <div class="card">
    <div class="mx-2">
      <div class="form-row align-items-center my-2">
        <div class="col-md-2 text-muted">
          <small>{{ $t('Required') }}</small>
        </div>
        <div class="col-md-10">
          <input v-model="required" type="checkbox" class="align-middle">
        </div>
      </div>
      <div v-if="isNumericType" class="form-row align-items-center my-2">
        <div class="col-md-2 text-muted">
          <small>{{ $t('Range') }}</small>
        </div>
        <div class="col-md-10">
          <div class="d-flex justify-content-between">
            <div class="input-group input-group-sm mr-1">
              <div class="input-group-prepend">
                <span class="input-group-text">&ge;</span>
              </div>
              <input class="form-control"
                     :value="kadi.utils.toExponentional(range.min)"
                     @change="changeRange('min', $event.target.value)">
            </div>
            <div class="input-group input-group-sm ml-1">
              <div class="input-group-prepend">
                <span class="input-group-text">&le;</span>
              </div>
              <input class="form-control"
                     :value="kadi.utils.toExponentional(range.max)"
                     @change="changeRange('max', $event.target.value)">
            </div>
          </div>
        </div>
      </div>
      <div v-if="['str', 'int', 'float'].includes(type)" class="form-row align-items-center my-2">
        <div class="col-md-2 text-muted">
          <small>{{ $t('Options') }}</small>
        </div>
        <div class="col-md-10">
          <vue-draggable handle=".sort-handle" :list="options" :force-fallback="true" @end="endDrag">
            <div v-for="(option, index) in options"
                 :key="option.id"
                 class="form-row"
                 :class="{'mb-md-1 mb-3': index < options.length - 1}">
              <div class="col-md-10 mb-1 mb-md-0">
                <input class="form-control form-control-sm"
                       :value="getOptionValue(option)"
                       @change="changeOption(option, $event.target.value)">
              </div>
              <div class="col-md-2">
                <div class="btn-group btn-group-sm w-100">
                  <button type="button" class="btn btn-light" tabindex="-1" @click="addOption(null, index)">
                    <i class="fa-solid fa-plus"></i>
                  </button>
                  <button v-if="options.length > 1"
                          type="button"
                          class="btn btn-light"
                          tabindex="-1"
                          @click="removeOption(index)">
                    <i class="fa-solid fa-xmark"></i>
                  </button>
                  <span class="btn btn-light disabled sort-handle" tabindex="-1">
                    <i class="fa-solid fa-bars"></i>
                  </span>
                </div>
              </div>
            </div>
          </vue-draggable>
          <small class="form-text text-muted">{{ $t('Possible values of this metadatum.') }}</small>
        </div>
      </div>
      <div v-if="type === 'str'" class="form-row align-items-center my-2">
        <div class="col-md-2 text-muted">
          <small>IRI</small>
        </div>
        <div class="col-md-10">
          <input v-model="iri" type="checkbox" class="align-middle">
          <small class="form-text text-muted">{{ $t('Whether the value of this metadatum represents an IRI.') }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueDraggable from 'vuedraggable';

export default {
  components: {
    VueDraggable,
  },
  props: {
    type: String,
    convertValue: Function,
    initialValidation: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      initialized: false,
      required: false,
      iri: false,
      range: {
        min: null,
        max: null,
      },
      options: [],
    };
  },
  computed: {
    isNumericType() {
      return ['int', 'float'].includes(this.type);
    },
  },
  watch: {
    type() {
      for (const option of this.options) {
        this.changeOption(option, option.value, false);
      }
      for (const prop of ['min', 'max']) {
        this.changeRange(prop, this.range[prop], false);
      }

      this.updateValidation();
    },
    required() {
      this.updateValidation();
    },
    iri() {
      this.updateValidation();
    },
  },
  async mounted() {
    this.addOption();

    // This initialization is enough, since the whole component is re-rendered anyways when e.g. using the undo/redo
    // functionality.
    if (this.initialValidation) {
      this.required = this.initialValidation.required || false;
      this.iri = this.initialValidation.iri || false;

      const range = this.initialValidation.range;

      if (range) {
        for (const prop of ['min', 'max']) {
          this.range[prop] = range[prop];
        }
      }

      const options = this.initialValidation.options;

      if (options && options.length > 0) {
        this.removeOption(0);

        for (const option of this.initialValidation.options) {
          this.addOption(option);
        }
      }
    }

    // Skip first potential change.
    await this.$nextTick();
    this.initialized = true;
  },
  methods: {
    updateValidation() {
      if (!this.initialized) {
        return;
      }

      if (kadi.utils.isNestedType(this.type)) {
        this.$emit('validate', null);
        return;
      }

      const validation = {
        required: this.required,
      };

      if (this.isNumericType) {
        validation.range = {min: this.range.min, max: this.range.max};
      }

      if (['str', 'int', 'float'].includes(this.type)) {
        validation.options = [];

        for (const option of this.options) {
          if (option.value !== null) {
            validation.options.push(option.value);
          }
        }
      }

      if (this.type === 'str') {
        validation.iri = this.iri;
      }

      this.$emit('validate', validation);
    },
    changeRange(prop, value, updateValidation = true) {
      const prevValue = this.range[prop];
      // See comment in 'changeOption'.
      this.range[prop] = value;

      const newValue = this.convertValue(value);
      this.range[prop] = newValue;

      if (updateValidation && prevValue !== newValue) {
        this.updateValidation();
      }
    },
    getOptionValue(option) {
      if (this.isNumericType) {
        return kadi.utils.toExponentional(option.value);
      }

      return option.value;
    },
    addOption(option = null, index = null) {
      const newOption = {
        id: kadi.utils.randomAlnum(),
        value: this.convertValue(option),
      };

      kadi.utils.addToArray(this.options, newOption, index);
    },
    removeOption(index) {
      const option = this.options.splice(index, 1)[0];

      if (option.value !== null) {
        this.updateValidation();
      }
    },
    changeOption(option, value, updateValidation = true) {
      const prevValue = option.value;
      // Set the value to the given value as is first, as otherwise the view is not updated correctly if the converted
      // value ('newValue') is the same as before.
      option.value = value;

      let newValue = this.convertValue(value);

      // Check if this option already exists and reset the new value if so.
      const index = this.options.findIndex((o) => o.value === newValue && o.id !== option.id);

      if (index !== -1) {
        newValue = null;
      }

      option.value = newValue;

      if (updateValidation && prevValue !== newValue) {
        this.updateValidation();
      }
    },
    endDrag(e) {
      if (e.oldIndex !== e.newIndex) {
        this.updateValidation();
      }
    },
  },
};
</script>
