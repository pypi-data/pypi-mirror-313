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

<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="form-group" tabindex="-1">
    <div class="form-row mr-0" :class="{'drag': extra.isDragging}">
      <!-- Type selection. -->
      <div class="custom-col-2 custom-mb" :class="{'custom-mr': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend">
            <span class="input-group-text">{{ $t('Type') }}</span>
          </div>
          <select v-model="extra.type.value"
                  class="custom-select"
                  :class="[typeInputClass, {'has-error': extra.type.errors.length > 0 && !extra.isDragging}]"
                  :disabled="!editingMode || (hasOptions && !extra.editValidation)"
                  @change="changeType">
            <option value="str">String</option>
            <option value="int">Integer</option>
            <option value="float">Float</option>
            <option value="bool">Boolean</option>
            <option value="date">Date</option>
            <option value="dict">Dictionary</option>
            <option value="list">List</option>
          </select>
        </div>
        <div v-show="!extra.isDragging">
          <div v-for="error in extra.type.errors" :key="error" class="invalid-feedback">{{ error }}</div>
        </div>
      </div>
      <!-- Key input and additional settings toggle. -->
      <div class="custom-col-4 custom-mb" :class="{'custom-mr': nestedType}">
        <div class="input-group input-group-sm">
          <tooltip-item v-if="extra.description.value" class="input-group-prepend" :title="extra.description.value">
            <span class="input-group-text">
              <i class="fa-solid fa-circle-info text-default"></i>
            </span>
          </tooltip-item>
          <tooltip-item v-if="extra.term.value"
                        class="input-group-prepend stretched-link-container"
                        :title="extra.term.value">
            <span class="input-group-text">
              <a v-if="kadi.utils.isHttpUrl(extra.term.value)"
                 target="_blank"
                 rel="noopener noreferrer"
                 class="stretched-link"
                 tabindex="-1"
                 :href="extra.term.value">
                <i class="fa-solid fa-link text-default"></i>
              </a>
              <i v-else class="fa-solid fa-link text-default"></i>
            </span>
          </tooltip-item>
          <div class="input-group-prepend">
            <span class="input-group-text">{{ $t('Key') }}</span>
          </div>
          <input class="form-control"
                 :value="keyModel"
                 :class="[keyInputClass, {'has-error': extra.key.errors.length > 0 && !extra.isDragging,
                                          'font-weight-bold': isNestedType}]"
                 :readonly="!editingMode || isInList"
                 :tabindex="(!editingMode || isInList) ? -1 : 0"
                 @change="changeString('key', $event.target.value)">
          <!-- Additional settings toggle. -->
          <div v-if="editingMode" class="input-group-append">
            <button type="button"
                    class="input-group-text btn btn-light"
                    tabindex="-1"
                    :class="{'toggle-active': extra.editDetails}"
                    :title="$t('Additional settings')"
                    @click="editDetails">
              <i v-if="extra.editDetails" class="fa-solid fa-angle-up"></i>
              <i v-else class="fa-solid fa-angle-down"></i>
            </button>
          </div>
        </div>
        <div v-show="!extra.isDragging">
          <div v-for="error in extra.key.errors" :key="error" class="invalid-feedback">{{ error }}</div>
        </div>
      </div>
      <!-- Value inputs for all different types and validation toggle. -->
      <div class="custom-mb" :class="valueContainerClasses">
        <div class="input-group input-group-sm">
          <tooltip-item v-if="valueTooltip" class="input-group-prepend" :title="valueTooltip">
            <span class="input-group-text">
              <i class="fa-solid fa-circle-info text-default"></i>
            </span>
          </tooltip-item>
          <div class="input-group-prepend">
            <span class="input-group-text">
              {{ $t('Value') }} <strong v-if="isRequired" class="text-danger">*</strong>
            </span>
          </div>
          <!-- Regular input for strings and numeric values. Also shown for nested types in readonly state if no
               template endpoint is supplied. -->
          <input v-if="!hasOptions && !hasTemplateSelection && !['bool', 'date'].includes(extra.type.value)"
                 class="form-control"
                 :value="valueModel"
                 :class="[valueInputClass, {'has-error': extra.value.errors.length > 0 && !extra.isDragging}]"
                 :readonly="isNestedType"
                 :tabindex="isNestedType ? -1 : 0"
                 @change="changeValue($event.target.value)">
          <!-- Boolean input. -->
          <select v-if="!hasOptions && extra.type.value === 'bool'"
                  class="custom-select"
                  :value="valueModel"
                  :class="[valueInputClass, {'has-error': extra.value.errors.length > 0 && !extra.isDragging}]"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option value="true">true</option>
            <option value="false">false</option>
          </select>
          <!-- Date input. -->
          <input v-if="extra.type.value === 'date'" type="hidden" :value="extra.value.value">
          <date-time-picker v-if="extra.type.value === 'date'"
                            :class="[valueInputClass,
                                     {'has-error': extra.value.errors.length > 0 && !extra.isDragging}]"
                            :initial-value="extra.value.value"
                            @input="changeValue">
          </date-time-picker>
          <!-- Selection to be used if validation options have been specified. -->
          <select v-if="hasOptions"
                  class="custom-select"
                  :value="valueModel"
                  :class="[valueInputClass, {'has-error': extra.value.errors.length > 0 && !extra.isDragging}]"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option v-for="option in extra.validation.value.options" :key="option" :value="getOptionValue(option)">
              {{ getOptionValue(option) }}
            </option>
          </select>
          <!-- Template input for nested types, if an endpoint is supplied. -->
          <dynamic-selection v-if="hasTemplateSelection"
                             container-classes="select2-single-sm"
                             :class="valueInputClass"
                             :placeholder="$t('Select a template')"
                             :endpoint="templateEndpoint"
                             :reset-on-select="true"
                             @select="selectTemplate">
          </dynamic-selection>
          <!-- Validation toggle. -->
          <div v-if="editingMode && !isNestedType" class="input-group-append">
            <button type="button"
                    class="input-group-text btn btn-light"
                    tabindex="-1"
                    :class="{'toggle-active': extra.editValidation}"
                    :title="$t('Validation')"
                    @click="editValidation">
              <i v-if="extra.editValidation" class="fa-solid fa-angle-up"></i>
              <i v-else class="fa-solid fa-angle-down"></i>
            </button>
          </div>
        </div>
        <div v-show="!extra.isDragging">
          <div v-for="error in extra.value.errors" :key="error" class="invalid-feedback">{{ error }}</div>
        </div>
      </div>
      <!-- Unit input for numeric values. -->
      <div v-show="isNumericType" class="custom-col-2 custom-mb" :class="{'custom-mr': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend">
            <span class="input-group-text">{{ $t('Unit') }}</span>
          </div>
          <input class="form-control"
                 :value="extra.unit.value"
                 :class="{'has-error': extra.unit.errors.length > 0 && !extra.isDragging}"
                 @change="changeString('unit', $event.target.value)">
        </div>
        <div v-show="!extra.isDragging">
          <div v-for="error in extra.unit.errors" :key="error" class="invalid-feedback">{{ error }}</div>
        </div>
      </div>
      <!-- Buttons for adding, removing or duplicating extras and sort handle. -->
      <div v-if="editingMode || isInList" class="custom-col-2" :class="{'custom-mr': nestedType}">
        <div class="btn-group btn-group-sm w-100">
          <button type="button"
                  class="btn btn-light"
                  tabindex="-1"
                  :title="`${$t('Add metadatum')} (${$t('Ctrl')}+I)`"
                  @click="$emit('add-extra')">
            <i class="fa-solid fa-plus"></i>
          </button>
          <button type="button"
                  class="btn btn-light"
                  tabindex="-1"
                  :title="$t('Remove metadatum')"
                  @click="$emit('remove-extra')">
            <i class="fa-solid fa-xmark"></i>
          </button>
          <button v-if="editingMode"
                  type="button"
                  class="btn btn-light"
                  tabindex="-1"
                  :title="$t('Duplicate metadatum')"
                  @click="$emit('duplicate-extra')">
            <i class="fa-solid fa-copy"></i>
          </button>
          <span class="btn btn-light disabled sort-handle" tabindex="-1" :title="$t('Move metadatum')">
            <i class="fa-solid fa-bars"></i>
          </span>
        </div>
      </div>
    </div>
    <!-- Additional settings inputs. -->
    <div v-show="editingMode && extra.editDetails && !extra.isDragging" class="mt-1 mr-1">
      <div class="card">
        <div class="mx-2">
          <div class="form-row align-items-center my-2">
            <div class="col-md-2 text-muted">
              <small>{{ $t('Description') }}</small>
            </div>
            <div class="col-md-10">
              <textarea class="form-control form-control-sm description"
                        spellcheck="false"
                        rows="3"
                        :value="extra.description.value"
                        :class="{'has-error': extra.description.errors.length > 0}"
                        @change="changeString('description', $event.target.value)">
              </textarea>
              <div v-for="error in extra.description.errors" :key="error" class="invalid-feedback">{{ error }}</div>
            </div>
          </div>
          <div class="form-row align-items-center my-2">
            <div class="col-md-2 text-muted">
              <small>{{ $t('Term IRI') }}</small>
            </div>
            <div class="col-md-10">
              <div class="input-group input-group-sm">
                <input class="form-control"
                       :value="extra.term.value"
                       :class="{'has-error': extra.term.errors.length > 0}"
                       @change="changeString('term', $event.target.value)">
                <div v-if="enableTermSearch" class="input-group-append">
                  <button type="button" class="btn btn-light" @click="$emit('show-term-search', extra)">
                    <i class="fa-solid fa-search"></i> {{ $t('Find term') }}
                  </button>
                </div>
              </div>
              <div v-for="error in extra.term.errors" :key="error" class="invalid-feedback">{{ error }}</div>
              <small v-if="extra.term.errors.length === 0" class="form-text text-muted">
                {{ $t('An IRI specifying an existing term that the metadatum should represent.') }}
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Validation instructions for non-nested values. -->
    <div v-show="editingMode && extra.editValidation && !isNestedType && !extra.isDragging" class="mt-1 mr-1">
      <extras-editor-item-validation :class="{'has-error': extra.validation.errors.length > 0}"
                                     :type="extra.type.value"
                                     :convert-value="convertValue"
                                     :initial-validation="extra.validation.value"
                                     @validate="validate">
      </extras-editor-item-validation>
      <div v-for="error in extra.validation.errors" :key="error" class="invalid-feedback">{{ error }}</div>
    </div>
    <!-- Nested values. -->
    <div v-show="!extra.isDragging"
         v-if="isNestedType"
         class="card mt-1 pl-3 py-2 extras"
         :class="{'even': depth % 2 == 0, 'nested': depth > 0}">
      <extras-editor-items :extras="extra.value.value"
                           :template-endpoint="templateEndpoint"
                           :enable-term-search="enableTermSearch"
                           :editing-mode="editingMode"
                           :nested-type="extra.type.value"
                           :depth="depth + 1"
                           @show-term-search="$emit('show-term-search', $event)"
                           @save-checkpoint="$emit('save-checkpoint')">
      </extras-editor-items>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@mixin custom-breakpoint {
  @media (min-width: 1500px) or ((min-width: 992px) and (max-width: 1200px)) {
    @content;
  }
}

@each $col in (2, 4, 6) {
  .custom-col-#{$col} {
    position: relative;
    width: 100%;

    @include custom-breakpoint {
      flex: 0 0 calc(100% / 12 * #{$col});
      max-width: calc(100% / 12 * #{$col});
    }
  }
}

.custom-mb {
  margin-bottom: 0.25rem;

  @include custom-breakpoint {
    margin-bottom: 0 !important;
  }
}

.custom-mr {
  margin-right: 0.75rem;

  @include custom-breakpoint {
    margin-right: 0 !important;
  }
}

.description {
  min-height: 50px;
}

.drag {
  background-color: #dee6ed;
  border-radius: 0.5rem;
  padding: 10px 5px 10px 5px;
  margin: 0 5px 0 0 !important;
}

.extras {
  border-color: #d4d4d4;
  margin-right: -1px;
  min-width: 250px;

  &.even {
    background-color: #f2f2f2;
  }

  &.nested {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
  }
}
</style>

<!-- eslint-disable vue/no-mutating-props -->
<script>
export default {
  props: {
    extra: Object,
    index: Number,
    templateEndpoint: String,
    enableTermSearch: Boolean,
    editingMode: Boolean,
    nestedType: String,
    depth: Number,
  },
  data() {
    return {
      prevType: null,
    };
  },
  computed: {
    typeInputClass() {
      return `type-input-${this.extra.id}`;
    },
    keyInputClass() {
      return `key-input-${this.extra.id}`;
    },
    valueInputClass() {
      return `value-input-${this.extra.id}`;
    },
    keyModel: {
      get() {
        return this.isInList ? `(${this.index + 1})` : this.extra.key.value;
      },
      set(value) {
        this.extra.key.value = value;
      },
    },
    valueModel() {
      if (this.isNestedType) {
        return '';
      }

      if (this.isNumericType) {
        return kadi.utils.toExponentional(this.extra.value.value);
      }

      return this.extra.value.value;
    },
    valueTooltip() {
      const validation = this.extra.validation.value;

      if (!validation) {
        return '';
      }

      if (validation.iri) {
        return $t('Must be a valid IRI.');
      }

      if (this.hasRange) {
        const ranges = [];

        if (validation.range.min !== null) {
          ranges.push(`\u2265 ${kadi.utils.toExponentional(validation.range.min)}`);
        }
        if (validation.range.max !== null) {
          ranges.push(`\u2264 ${kadi.utils.toExponentional(validation.range.max)}`);
        }

        return ranges.join(', ');
      }

      return '';
    },
    valueContainerClasses() {
      let cols = this.isNumericType ? 2 : 4;

      if (!this.editingMode && this.nestedType !== 'list') {
        cols += 2;
      }

      let classes = `custom-col-${cols}`;

      if (this.nestedType) {
        classes += ' custom-mr';
      }

      return classes;
    },
    isNumericType() {
      return ['int', 'float'].includes(this.extra.type.value);
    },
    isNestedType() {
      return kadi.utils.isNestedType(this.extra.type.value);
    },
    isInList() {
      return this.nestedType === 'list';
    },
    isRequired() {
      const validation = this.extra.validation.value;
      return validation && validation.required;
    },
    hasRange() {
      const validation = this.extra.validation.value;
      return validation && validation.range && (validation.range.min !== null || validation.range.max !== null);
    },
    hasOptions() {
      const validation = this.extra.validation.value;
      return validation && validation.options && validation.options.length > 0;
    },
    hasTemplateSelection() {
      return this.templateEndpoint && this.isNestedType;
    },
  },
  mounted() {
    this.prevType = this.extra.type.value;

    if (this.extra.description.errors.length > 0 || this.extra.term.errors.length > 0) {
      this.extra.editDetails = true;
    }
    if (this.extra.validation.errors.length > 0) {
      this.extra.editValidation = true;
    }

    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  methods: {
    clampRangeValue(value) {
      if (!this.hasRange) {
        return value;
      }

      const range = this.extra.validation.value.range;

      if (range.min !== null && this.extra.value.value < range.min) {
        return range.min;
      }
      if (range.max !== null && this.extra.value.value > range.max) {
        return range.max;
      }

      return value;
    },
    convertValue(value, applyValidation = false) {
      if (value === null) {
        return value;
      }

      let newValue = value;

      if (typeof newValue === 'string') {
        newValue = newValue.trim();
      }

      if (this.extra.type.value === 'str') {
        newValue = String(newValue);
      } else if (this.isNumericType) {
        if (newValue) {
          newValue = Number.parseFloat(newValue, 10);

          if (this.extra.type.value === 'int') {
            newValue = Math.trunc(newValue);
          }

          if (window.isNaN(newValue)) {
            newValue = 0;
          }

          if (this.extra.type.value === 'int') {
            if (newValue > Number.MAX_SAFE_INTEGER) {
              newValue = Number.MAX_SAFE_INTEGER;
            } else if (newValue < -Number.MAX_SAFE_INTEGER) {
              newValue = -Number.MAX_SAFE_INTEGER;
            }
          } else if (!window.isFinite(newValue)) {
            newValue = Number.MAX_VALUE;
          }

          if (applyValidation) {
            newValue = this.clampRangeValue(newValue);
          }
        }
      } else if (this.extra.type.value === 'bool') {
        if (newValue === 'true') {
          newValue = true;
        } else if (newValue === 'false') {
          newValue = false;
        }
      }

      if (newValue === '') {
        newValue = null;
      }

      return newValue;
    },
    changeType() {
      this.extra.value.value = this.convertValue(this.extra.value.value, true);

      const specialInputTypes = ['bool', 'date'];
      if ((!this.isNestedType && kadi.utils.isNestedType(this.prevType))
          || specialInputTypes.includes(this.extra.type.value)
          || specialInputTypes.includes(this.prevType)) {
        this.extra.value.value = null;
      }

      if (this.isNestedType && !kadi.utils.isNestedType(this.prevType)) {
        this.$emit('init-nested-value');
      }

      this.prevType = this.extra.type.value;

      // No need to create a checkpoint here, since changing a type also triggers the "validate" function, which will
      // create the checkpoint only after possible changes in the validation based on the type have occured as well.
    },
    changeString(prop, value) {
      const oldValue = this.extra[prop].value;
      // Set the value to the given value as is first, as otherwise the view is not updated correctly if the converted
      // value ('newValue') is the same as before.
      this.extra[prop].value = value;

      let newValue = value.trim();
      if (newValue === '') {
        newValue = null;
      }

      this.extra[prop].value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    changeValue(value) {
      const oldValue = this.extra.value.value;
      // See comment in 'changeString'.
      this.extra.value.value = value;

      const newValue = this.convertValue(value, true);
      this.extra.value.value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    getOptionValue(value) {
      if (this.isNumericType) {
        return kadi.utils.toExponentional(value);
      }

      return value;
    },
    validate(validation) {
      this.extra.validation.value = validation;

      // Apply the validation to the current value, if applicable.
      if (this.extra.value.value) {
        if (this.hasOptions) {
          const options = this.extra.validation.value.options;

          if (!options.includes(this.extra.value.value)) {
            this.extra.value.value = null;
          }
        }

        this.extra.value.value = this.clampRangeValue(this.extra.value.value);
      }

      this.$emit('save-checkpoint');
    },
    selectTemplate(template) {
      this.$emit('init-nested-value', template.endpoint);
    },
    editDetails() {
      this.extra.editValidation = false;
      this.extra.editDetails = !this.extra.editDetails;
    },
    editValidation() {
      this.extra.editDetails = false;
      this.extra.editValidation = !this.extra.editValidation;
    },
    keydownHandler(e) {
      if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        e.stopPropagation();

        if (this.editingMode || this.isInList) {
          this.$emit('add-extra');
        }
      }
    },
  },
};
</script>
