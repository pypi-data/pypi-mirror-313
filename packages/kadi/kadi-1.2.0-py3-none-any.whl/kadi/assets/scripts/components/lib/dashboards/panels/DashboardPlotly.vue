<!-- Copyright 2024 Karlsruhe Institute of Technology
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
  <div ref="plot"></div>
</template>

<script>
import Plotly from 'plotly.js-dist-min';
import dashboardPanelMixin from 'scripts/components/mixins/dashboard-panel-mixin';
import locale from 'plotly.js-locales/de';

export default {
  mixins: [dashboardPanelMixin],
  watch: {
    settings: {
      async handler() {
        await this.createPlot();
      },
      deep: true,
    },
  },
  async mounted() {
    Plotly.register(locale);
    Plotly.setPlotConfig({
      displaylogo: false,
      locale: kadi.globals.locale,
      showTips: false,
    });

    await this.createPlot();
  },
  methods: {
    async createPlot() {
      let data = [];
      const layout = {};
      const config = {};

      const tasks = [];

      for (const file of this.settings.files) {
        tasks.push(this.loadFile(file));
      }

      const plots = (await Promise.all(tasks)).filter((value) => value !== null);

      for (const plot of plots) {
        data = data.concat(plot.data);
        Object.assign(layout, plot.layout);
        Object.assign(config, plot.config);
      }

      config.responsive = true;

      Plotly.newPlot(this.$refs.plot, data, layout, config);
    },
    async loadFile(file) {
      try {
        const response = await axios.get(file.downloadEndpoint);
        const fileContent = response.data;

        const data = this.searchForKey(fileContent, 'data');
        if (!data) {
          return null;
        }

        return {
          data,
          layout: this.searchForKey(fileContent, 'layout'),
          config: this.searchForKey(fileContent, 'config'),
        };
      } catch (error) {
        kadi.base.flashDanger($t('Error loading file.'), {request: error.request || null});
      }

      return null;
    },
    searchForKey(object, searchedKey, depth = 0) {
      if (depth >= 4) {
        return null;
      }

      for (const key of Object.keys(object)) {
        if (key === searchedKey) {
          return object[key];
        } else if (kadi.utils.isObject(object[key])) {
          const result = this.searchForKey(object[key], searchedKey, depth + 1);
          if (result) {
            return result;
          }
        }
      }

      return null;
    },
  },
};
</script>
