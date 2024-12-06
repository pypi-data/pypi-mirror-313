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
  <div ref="container">
    <div ref="toolbar" class="card toolbar">
      <div class="card-body px-1 py-0">
        <div class="form-row align-items-center">
          <div class="col-md-6">
            <button type="button"
                    :title="$t('Toggle forces')"
                    :class="toolbarBtnClasses + (forceDisabled ? ' border-active' : '')"
                    :disabled="!initialized"
                    @click="forceDisabled = !forceDisabled">
              <i class="fa-solid fa-thumbtack"></i>
            </button>
            <button type="button"
                    :title="$t('Toggle legend')"
                    :class="toolbarBtnClasses + (legendHidden ? ' border-active' : '')"
                    :disabled="!initialized"
                    @click="toggleLegend">
              <i class="fa-solid fa-tags"></i>
            </button>
            <button type="button"
                    :title="$t('Toggle labels')"
                    :class="toolbarBtnClasses + (labelsHidden ? ' border-active' : '')"
                    :disabled="!initialized"
                    @click="toggleLabels">
              <i class="fa-solid fa-font"></i>
            </button>
            <button type="button"
                    :title="$t('Download graph')"
                    :class="toolbarBtnClasses"
                    :disabled="!initialized"
                    @click="downloadGraph">
              <i class="fa-solid fa-download"></i>
            </button>
            <button type="button"
                    :title="$t('Reset view')"
                    :class="toolbarBtnClasses"
                    :disabled="!initialized"
                    @click="resetView">
              <i class="fa-solid fa-eye"></i>
            </button>
            <button type="button"
                    :title="$t('Toggle fullscreen')"
                    :class="toolbarBtnClasses"
                    :disabled="!initialized"
                    @click="toggleFullscreen">
              <i class="fa-solid fa-expand"></i>
            </button>
            <i v-if="loading" class="fa-solid fa-circle-notch fa-spin text-muted ml-2"></i>
          </div>
          <div class="col-md-6 mb-2 mb-md-0">
            <div class="input-group input-group-sm">
              <input :id="`filter-${suffix}`"
                     v-model="filter"
                     class="form-control"
                     :placeholder="$t('Filter by identifier or link name')">
              <clear-button :input="filter" :input-id="`filter-${suffix}`" @clear-input="filter = ''"></clear-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div ref="graphContainer" class="card graph"></div>
  </div>
</template>

<style scoped>
.border-active {
  border: 1px solid #ced4da;
}

.graph {
  border: 1px solid #ced4da;
  border-radius: 0;
}

.toolbar {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  border-color: #ced4da;
  margin-bottom: -1px;
}
</style>

<script>
import * as d3 from 'd3';

import graphMixin from 'scripts/components/mixins/graph-mixin';

export default {
  mixins: [graphMixin],
  data() {
    return {
      data: null,
      coordinateStrength: 0.1,
    };
  },
  watch: {
    isRendered() {
      this.resizeView(this.$refs.container, this.$refs.toolbar);
    },
  },
  mounted() {
    this.createContainers(this.$refs.graphContainer);
    this.createSimulation();

    // Force the position of records to their collection coordinates.
    const foorceCoordinate = (d, coordinate) => {
      let result = 0;

      if (d._type === this.types.record) {
        const node = this.nodes.find((node) => node.id === d.collection);
        result = node[`f${coordinate}`];
      }

      return result || 0;
    };

    const forceX = d3
      .forceX()
      .strength(this.coordinateStrength)
      .x((d) => foorceCoordinate(d, this.forces.x));

    const forceY = d3
      .forceY()
      .strength(this.coordinateStrength)
      .y((d) => foorceCoordinate(d, this.forces.y));

    this.simulation.force(this.forces.x, forceX).force(this.forces.y, forceY);

    this.resizeCallback();
    this.updateData(this.endpoint);

    window.addEventListener('resize', this.resizeCallback);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeCallback);
  },
  methods: {
    getStartNode() {
      return this.nodes.find((node) => node.id === this.data.id) || null;
    },
    disableForces() {
      this.simulation.force(this.forces.x).strength(0);
      this.simulation.force(this.forces.y).strength(0);
    },
    enableForces() {
      this.simulation.force(this.forces.x).strength(this.coordinateStrength);
      this.simulation.force(this.forces.y).strength(this.coordinateStrength);
    },
    toggleFullscreen() {
      kadi.utils.toggleFullscreen(this.$refs.container);
    },
    resizeCallback() {
      this.resizeView(this.$refs.container, this.$refs.toolbar);
      this.resetView();
    },
    findCollection(id, _collection = null) {
      let collection = _collection;

      if (collection === null) {
        collection = this.data;
      }
      if (collection.id === id) {
        return collection;
      }
      if (collection.children === null) {
        return null;
      }

      for (const child of collection.children) {
        const result = this.findCollection(id, child);

        if (result !== null) {
          return result;
        }
      }

      return null;
    },
    iterateChildCollections(collection, callback) {
      if (collection.children === null) {
        return;
      }

      for (const child of collection.children) {
        callback(child);
        this.iterateChildCollections(child, callback);
      }
    },
    updateRecordNodes(collection) {
      for (const record of collection.records) {
        this.nodes.push({...record, collection: collection.id, _type: this.types.record});
      }
      for (const recordLink of collection.record_links) {
        this.links.push({...recordLink});
      }
    },
    updateGraph() {
      // Determine a (new) tree layout for the collection hierarchy.
      const root = d3.hierarchy(this.data);

      const treeLayout = d3
        .tree()
        .nodeSize([750, 500])
        .separation(() => 1);

      treeLayout(root);

      for (const node of this.nodes) {
        // If the node was never moved, use the coordinates of the tree layout.
        if (node._type === this.types.collection && !node._moved) {
          const treeNode = root.find((d) => d.data.id === node.id);

          node.fx = treeNode.x;
          node.fy = treeNode.y;
        }
      }

      const recordsCallback = (d) => {
        const collection = this.findCollection(d.id);

        // Only update the data if the records are still uninitialized.
        if (collection.records === null) {
          this.updateData(collection.records_endpoint);
          return;
        }

        for (const node of this.nodes) {
          if (node._type === this.types.record && node.collection === collection.id) {
            if (!this.excludedRecords.includes(node.id)) {
              this.excludedRecords.push(node.id);
            } else {
              kadi.utils.removeFromArray(this.excludedRecords, node.id);
            }
          }
        }

        this.filterNodes();
      };

      const childrenCallback = (d) => {
        const collection = this.findCollection(d.id);

        // Only update the data if the children are still uninitialized.
        if (collection.children === null) {
          this.updateData(collection.children_endpoint);
          return;
        }

        // Toggle the children.
        collection._collapsed = !collection._collapsed;

        const hasCollapsedParent = (child) => {
          let parent = child.parent;

          while (parent) {
            if (parent._collapsed) {
              return true;
            }

            parent = parent.parent;
          }

          return false;
        };

        this.iterateChildCollections(collection, (child) => {
          if (collection._collapsed) {
            if (!this.excludedCollections.includes(child.id)) {
              this.excludedCollections.push(child.id);
            }
          // Do not remove the child if it has another parent that is collapsed.
          } else if (!hasCollapsedParent(child)) {
            kadi.utils.removeFromArray(this.excludedCollections, child.id);
          }
        });

        this.filterNodes();
      };

      this.simulation.nodes(this.nodes);
      this.simulation.force(this.forces.link).links(this.links);

      this.drawNodes(true, recordsCallback, childrenCallback);
      this.drawLinks();
      this.drawLegend();

      this.filterNodes();

      this.simulation.alpha(1).restart();
    },
    async updateData(endpoint) {
      this.loading = true;

      try {
        const response = await axios.get(endpoint);
        const data = response.data;

        if (!this.initialized) {
          this.data = data;
          this.nodes.push({...data, _type: this.types.collection});
          this.updateRecordNodes(data);
        } else {
          const collection = this.findCollection(data.id);

          // Initialize the records of the collection, if applicable.
          if (data.records !== null) {
            collection.records = data.records;
            collection.record_links = data.record_links;

            this.updateRecordNodes(collection);
          }

          // Initialize the children of the collection, if applicable.
          if (data.children !== null) {
            collection.children = data.children;

            for (const child of collection.children) {
              child.parent = collection;

              this.nodes.push({...child, _type: this.types.collection});
              this.links.push({
                id: `${collection.id}-${child.id}`,
                source: collection.id,
                target: child.id,
              });
            }
          }
        }

        this.updateGraph();
      } catch (error) {
        kadi.base.flashDanger($t('Error loading collection links.'), {request: error.request});
      } finally {
        this.initialized = true;
        this.loading = false;
        this.forceDisabled = false;
      }
    },
  },
};
</script>
