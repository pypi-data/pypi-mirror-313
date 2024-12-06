<!-- Copyright 2023 Karlsruhe Institute of Technology
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
  <div class="form-group">
    <label class="form-control-label">{{ field.label }}</label>
    <div class="card">
      <div class="card-body px-3 pt-3 pb-2">
        <div class="d-lg-flex justify-content-between">
          <div v-for="(actions, object, index) in scopes" :key="object" :class="{'mt-4 mt-lg-0': index > 0}">
            <input :id="object"
                   type="checkbox"
                   :checked="objectScopesChecked(object)"
                   @click="checkObjectScopes(object, $event)">
            <label :for="object">
              <strong>{{ kadi.utils.capitalize(object) }}</strong>
            </label>
            <div v-for="action in actions" :key="getScopeValue(object, action)">
              <input :id="getScopeValue(object, action)" v-model="scopesModel[object][action].checked" type="checkbox">
              <label :for="getScopeValue(object, action)">{{ action }}</label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <small class="form-text text-muted">{{ field.description }}</small>
    <input type="hidden" :name="field.name" :value="serializedScopes">
  </div>
</template>

<script>
export default {
  props: {
    field: Object,
    scopes: Object,
  },
  data() {
    return {
      scopesModel: null,
    };
  },
  computed: {
    serializedScopes() {
      const checkedScopes = [];

      for (const object in this.scopesModel) {
        for (const action in this.scopesModel[object]) {
          if (this.scopesModel[object][action].checked) {
            checkedScopes.push(this.getScopeValue(object, action));
          }
        }
      }

      return checkedScopes.join(' ');
    },
  },
  created() {
    const initialScopes = this.field.data.split(' ');
    const scopesModel = {};

    for (const object in this.scopes) {
      scopesModel[object] = {};

      this.scopes[object].forEach((action) => {
        let checked = false;

        if (initialScopes.includes(this.getScopeValue(object, action))) {
          checked = true;
        }

        scopesModel[object][action] = {checked};
      });
    }

    this.scopesModel = scopesModel;
  },
  methods: {
    getScopeValue(object, action) {
      return `${object}.${action}`;
    },
    objectScopesChecked(object) {
      for (const actionModel of Object.values(this.scopesModel[object])) {
        if (!actionModel.checked) {
          return false;
        }
      }
      return true;
    },
    checkObjectScopes(object, e) {
      for (const actionModel of Object.values(this.scopesModel[object])) {
        actionModel.checked = e.target.checked;
      }
    },
  },
};
</script>
