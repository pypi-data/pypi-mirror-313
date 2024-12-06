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
  <base-field ref="base" :field="field">
    <template #default="props">
      <div class="input-group">
        <input :id="field.id"
               ref="input"
               v-model="identifier"
               :name="field.name"
               :required="field.validation.required"
               :class="[{'has-error': props.hasError}, classes]"
               :readonly="!editIdentifier">
        <div v-if="input !== null" class="input-group-append">
          <button type="button"
                  class="input-group-text btn btn-light"
                  :title="editIdentifier ? $t('Revert to default') : $t('Edit identifier')"
                  @click="toggleEdit">
            <i v-if="!editIdentifier" class="fa-solid fa-pencil"></i>
            <i v-if="editIdentifier" class="fa-solid fa-rotate"></i>
          </button>
        </div>
      </div>
    </template>
  </base-field>
</template>

<script>
export default {
  props: {
    field: Object,
    input: {
      type: String,
      default: null,
    },
    classes: {
      type: String,
      default: 'form-control form-control-sm',
    },
    checkIdentifierEndpoint: {
      type: String,
      default: null,
    },
    exclude: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      identifier: this.field.data,
      editIdentifier: false,
      checkIdentifierHandle: null,
    };
  },
  watch: {
    input() {
      if (!this.editIdentifier) {
        this.identifier = this.generateIdentifier(this.input);
      }
    },
    identifier() {
      const identifier = this.generateIdentifier(this.identifier);
      const selectionStart = this.$refs.input.selectionStart;

      if (this.identifier !== identifier) {
        // Prevent the cursor from jumping to the end of the input.
        this.$nextTick(() => this.$refs.input.selectionEnd = selectionStart);
      }

      this.identifier = identifier;
      this.$refs.base.validate(this.identifier);

      if (this.checkIdentifierEndpoint) {
        window.clearTimeout(this.checkIdentifierHandle);
        this.checkIdentifierHandle = window.setTimeout(this.checkIdentifier, 500);
      }
    },
  },
  mounted() {
    // Listen to the custom event of the submission form component.
    window.addEventListener('submitted', this.onSubmitted);

    const hasIdentifier = this.identifier !== '';

    if (hasIdentifier || this.input === null) {
      this.editIdentifier = true;
    }
    if (hasIdentifier && this.checkIdentifierEndpoint) {
      this.checkIdentifier();
    }
  },
  beforeDestroy() {
    window.removeEventListener('submitted', this.onSubmitted);
  },
  methods: {
    toggleEdit() {
      this.editIdentifier = !this.editIdentifier;

      if (!this.editIdentifier) {
        this.identifier = this.generateIdentifier(this.input);
      }
    },
    generateIdentifier(value) {
      let identifier = value;

      // Lowercase and normalize all characters, remove invalid ones and replace spaces with hyphens.
      identifier = identifier
        .toLowerCase()
        .normalize('NFKD')
        .replace(/[^a-z0-9-_ ]+/g, '')
        .replace(/[ ]+/g, '-');

      // When not editing, also collapse multiple hyphens/underscores and remove trailing hyphens/underscores.
      if (!this.editIdentifier) {
        identifier = identifier
          .replace(/[-]+/g, '-')
          .replace(/[_]+/g, '_')
          .replace(/^[-_]+/g, '')
          .replace(/[-_]+$/g, '');
      }

      if (!this.editIdentifier && this.field.validation.max) {
        identifier = identifier.substring(0, this.field.validation.max);
      }

      return identifier;
    },
    async checkIdentifier() {
      // Note that this requires the message set via server-side validation to be the same.
      const errorMsg = $t('Identifier is already in use.');

      try {
        const params = {identifier: this.identifier, exclude: this.exclude};
        const response = await axios.get(this.checkIdentifierEndpoint, {params});

        if (response.data.duplicate) {
          this.$refs.base.addError(errorMsg);
        } else {
          this.$refs.base.removeError(errorMsg);
        }
      } catch (error) {
        kadi.base.flashDanger($t('Error checking identifier.'), {request: error.request});
      }
    },
    onSubmitted() {
      // Clear the timeout, as the resource might have been created already once the request is actually sent.
      window.clearTimeout(this.checkIdentifierHandle);
    },
  },
};
</script>
