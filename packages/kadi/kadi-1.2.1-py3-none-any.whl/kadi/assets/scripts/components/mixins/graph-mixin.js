/* Copyright 2023 Karlsruhe Institute of Technology
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
import * as d3 from 'd3';

/** Mixin to add common functionality to graph visualization components. */
export default {
  props: {
    endpoint: String,
    isRendered: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      suffix: kadi.utils.randomAlnum(),
      svg: null,
      legendContainer: null,
      graphContainer: null,
      linksContainer: null,
      nodesContainer: null,
      simulation: null,
      zoom: null,
      width: 0,
      height: 0,
      manyBodyStrength: -2_000,
      linkStrength: 0.25,
      forceDisabled: false,
      legendHidden: false,
      labelsHidden: false,
      initialized: false,
      loading: true,
      nodes: [],
      links: [],
      excludedTypes: [],
      excludedRecords: [],
      excludedCollections: [],
      filter: '',
      fontFamily: 'Arial, sans-serif',
      types: {
        record: 'record',
        collection: 'collection',
      },
      forces: {
        charge: 'charge',
        link: 'link',
        x: 'x',
        y: 'y',
      },
      displays: {
        inline: 'inline',
        none: 'none',
      },
      colors: {
        link: '#c9c9c9',
        linkFocus: '#8a8a8a',
        text: 'black',
        textFocus: '#2c3e50',
      },
      prefixes: {
        graph: 'graph',
        node: 'node',
        nodeLabel: 'node-label',
        controls: 'controls',
        link: 'link',
        linkLabel: 'link-label',
        linkPath: 'link-path',
        arrowHead: 'arrow-head',
        arrowHeadFocus: 'arrow-head-focus',
        iconGraph: 'icon-graph',
        iconDown: 'icon-down',
        iconUp: 'icon-up',
      },
      icons: {
        graph: `M10.609,4.004c0.896-0.21,1.563-1.015,1.563-1.976C12.173,0.908,11.266,0,10.145,0C9.043,0,8.149,0.875,
                8.115,1.965 L3.454,3.832C3.086,3.469,2.583,3.246,2.029,3.246C0.908,3.246,0,4.154,0,5.275c0,1.122,0.908,
                2.029,2.029,2.029 c0.31,0,0.604-0.068,0.865-0.192l3.692,3.231c-0.061,0.192-0.093,0.398-0.093,0.614c0,
                1.119,0.908,2.027,2.03,2.027 c1.119,0,2.027-0.908,2.027-2.027c0-0.704-0.354-1.324-0.897-1.686L10.609,
                4.004L10.609,4.004z M3.964,5.889 C4.02,5.713,4.052,5.528,4.058,5.338l4.661-1.864c0.092,0.088,0.188,0.17,
                0.295,0.241l-0.96,5.263 c-0.138,0.034-0.274,0.08-0.399,0.141L3.964,5.889z`,
        down: `M5.724,5.75c0.422-0.42,1.106-0.42,1.529,0l5.403,5.403c0.423,0.424,0.423,1.109,0,1.53c-0.422,0.425-1.107,
               0.425-1.53,0 L6.487,8.044L1.846,12.68c-0.422,0.422-1.107,0.422-1.529,0c-0.422-0.422-0.422-1.105,
               0-1.529l5.404-5.403L5.724,5.75z`,
        up: `M5.723,7.654c0.422,0.421,1.107,0.421,1.529,0l5.404-5.404c0.421-0.422,0.421-1.107,0-1.529
             c-0.424-0.422-1.106-0.422-1.53,0L6.486,5.36l-4.64-4.636c-0.422-0.422-1.107-0.422-1.529,0c-0.422,
             0.422-0.422,1.107,0,1.53 L5.72,7.657L5.723,7.654z`,
      },
    };
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-primary my-1';
    },
  },
  watch: {
    filter() {
      this.filterNodes();
    },
    forceDisabled() {
      if (this.forceDisabled) {
        this.simulation.force(this.forces.charge).strength(0);
        this.simulation.force(this.forces.link).strength(0);

        this.disableForces();
      } else {
        this.simulation.force(this.forces.charge).strength(this.manyBodyStrength);
        this.simulation.force(this.forces.link).strength(this.linkStrength);

        this.enableForces();

        this.simulation.alpha(0.5).restart();
      }
    },
  },
  methods: {
    getStartNode() {
      return null;
    },

    disableForces() {
      // Can be implemented to disable additional forces when toggling them.
    },

    enableForces() {
      // Can be implemented to enable additional forces when toggling them.
    },

    b64EncodeUnicode(str) {
      // See also: https://developer.mozilla.org/en-US/docs/Glossary/Base64
      return window.btoa(window.encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (match, p1) => {
        return String.fromCharCode(`0x${p1}`);
      }));
    },

    downloadGraph() {
      const svg = this.svg.node().cloneNode(true);
      const graph = svg.getElementById(`${this.prefixes.graph}-${this.suffix}`);

      // Use the existing containers for this, as the element needs to be part of the DOM to determine the bounding box.
      const graphBBox = this.graphContainer.node().getBBox();
      const legendBBox = this.legendContainer.node().getBBox();

      // Additional margin used on all sides of the graph.
      const margin = 30;

      // Specify the size of the SVG.
      svg.setAttribute('width', graphBBox.width + (margin * 2) + legendBBox.width);
      svg.setAttribute('height', Math.max(graphBBox.height + (margin * 2), legendBBox.height));

      // Translate the graph so it is completely visible inside the SVG.
      const translateX = -graphBBox.x + margin + legendBBox.width;
      const translateY = -graphBBox.y + margin;
      graph.setAttribute('transform', `translate(${translateX},${translateY}) scale(1)`);

      // Convert and download the SVG.
      const xmlString = `<?xml version="1.0" encoding="utf-8"?>${new XMLSerializer().serializeToString(svg)}`;
      const svgData = `data:image/svg+xml;base64,${this.b64EncodeUnicode(xmlString)}`;
      const startNode = this.getStartNode();
      const filename = `${startNode ? startNode.identifier_full : 'graph'}.svg`;

      const hyperlinkElem = document.createElement('a');

      hyperlinkElem.href = svgData;
      hyperlinkElem.download = filename;

      document.body.appendChild(hyperlinkElem);
      hyperlinkElem.click();
      document.body.removeChild(hyperlinkElem);
    },

    resizeView(containerElem, toolbarElem) {
      if (!this.isRendered) {
        return;
      }

      this.width = Math.round(containerElem.getBoundingClientRect().width) - 2;

      if (kadi.utils.isFullscreen()) {
        const containerHeight = Math.round(containerElem.getBoundingClientRect().height);
        const toolbarHeight = Math.round(toolbarElem.getBoundingClientRect().height);

        this.height = Math.max(containerHeight - toolbarHeight - 1, 1);
        toolbarElem.style.borderTopLeftRadius = toolbarElem.style.borderTopRightRadius = '0';
      } else {
        this.height = Math.round(window.innerHeight / window.innerWidth * this.width);
        toolbarElem.style.borderTopLeftRadius = toolbarElem.style.borderTopRightRadius = '0.25rem';
      }

      this.svg.attr('width', this.width).attr('height', this.height);
    },

    resetView() {
      const node = this.getStartNode();
      const x = node === null ? 0 : node.fx || 0;
      const y = node === null ? 0 : node.fy || 0;

      this.zoom.translateTo(this.svg, x, y, [this.width * 0.5, this.height * 0.5]);
      this.zoom.scaleTo(this.svg, 1);
    },

    toggleLegend() {
      this.legendHidden = !this.legendHidden;
      this.legendContainer.attr('display', this.legendHidden ? this.displays.none : this.displays.inline);
    },

    toggleLabels() {
      this.labelsHidden = !this.labelsHidden;

      this.graphContainer
        .selectAll(`.${this.prefixes.nodeLabel}-${this.suffix},.${this.prefixes.linkLabel}-${this.suffix}`)
        .each((d, i, nodes) => {
          d3.select(nodes[i]).attr('display', this.labelsHidden ? this.displays.none : this.displays.inline);
        });
    },

    getBezierPoints(node) {
      const dx = node.target.x - node.source.x;
      const dy = node.target.y - node.source.y;

      return {
        x1: node.source.x,
        y1: node.source.y,
        x2: node.source.x + (dx / 2) + (dy / 5 * node.link_index),
        y2: node.source.y + (dy / 2) - (dx / 5 * node.link_index),
        x3: node.target.x,
        y3: node.target.y,
      };
    },

    quadraticBezierCurve(node) {
      const points = this.getBezierPoints(node);
      return `M ${points.x1},${points.y1} Q ${points.x2} ${points.y2} ${points.x3} ${points.y3}`;
    },

    linkLabelTransformation(node) {
      const points = this.getBezierPoints(node);

      // Calculate a good position for the text along the link path.
      const t = 0.5;
      const posX = points.x2 + (((1 - t) ** 2) * (points.x1 - points.x2)) + ((t ** 2) * (points.x3 - points.x2));
      const posY = points.y2 + (((1 - t) ** 2) * (points.y1 - points.y2)) + ((t ** 2) * (points.y3 - points.y2));

      // Calculate the angle of the path at this position to rotate the text properly.
      const slopeX = (2 * (1 - t) * (points.x2 - points.x1)) + (2 * t * (points.x3 - points.x2));
      const slopeY = (2 * (1 - t) * (points.y2 - points.y1)) + (2 * t * (points.y3 - points.y2));

      let rotation = Math.atan2(slopeY, slopeX) * (180 / Math.PI);
      rotation = points.x1 > points.x3 ? rotation - 180 : rotation;

      // Calculate an additional margin between the path and the text based on the rotation.
      const margin = points.x1 > points.x3 ? -15 : 5;
      const marginX = Math.sin((rotation / 180) * Math.PI) * margin;
      const marginY = Math.cos((rotation / 180) * Math.PI) * margin;

      return `translate(${posX + marginX} ${posY - marginY}) rotate(${rotation})`;
    },

    getNodeById(id) {
      return this.nodesContainer.select(`#${this.prefixes.node}-${id}-${this.suffix}`);
    },

    filterNodes() {
      // First, filter all nodes based on the filter, excluded types and excluded collections.
      this.nodesContainer.selectAll(`.${this.prefixes.node}-${this.suffix}`).each((d, i, nodes) => {
        const node = d3.select(nodes[i]);

        if (d.identifier_full.includes(this.filter.trim())) {
          node.attr('display', this.displays.inline);

          if (d._type === this.types.collection) {
            if (this.excludedCollections.includes(d.id)) {
              node.attr('display', this.displays.none);
            }
          } else {
            if (this.excludedTypes.includes(d.type_full) || this.excludedRecords.includes(d.id)) {
              node.attr('display', this.displays.none);
            } else if (d.collection && this.excludedCollections.includes(d.collection)) {
              node.attr('display', this.displays.none);
            }
          }
        } else {
          node.attr('display', this.displays.none);
        }
      });

      // Next, filter all links depending on the filter and the corresponding nodes.
      this.linksContainer.selectAll(`.${this.prefixes.link}-${this.suffix}`).each((d, i, nodes) => {
        const link = d3.select(nodes[i]);

        if (d.source._type === this.types.record && d.name_full.includes(this.filter.trim())) {
          for (const node of [d.source, d.target]) {
            // Only consider linked records that have not been excluded via their type or collection.
            if (!this.excludedTypes.includes(node.type_full) && !this.excludedRecords.includes(node.id)) {
              this.getNodeById(node.id).attr('display', this.displays.inline);
            }
          }
        }

        if (this.getNodeById(d.source.id).attr('display') === this.displays.inline
            && this.getNodeById(d.target.id).attr('display') === this.displays.inline) {
          link.attr('display', this.displays.inline);
        } else {
          link.attr('display', this.displays.none);
        }
      });
    },

    createContainers(containerElem) {
      this.zoom = d3.zoom().on('zoom', (e) => this.graphContainer.attr('transform', e.transform));
      this.svg = d3.select(containerElem)
        .append('svg')
        .call(this.zoom)
        .on('dblclick.zoom', null);

      this.graphContainer = this.svg.append('g').attr('id', `${this.prefixes.graph}-${this.suffix}`);
      this.linksContainer = this.graphContainer.append('g');
      this.nodesContainer = this.graphContainer.append('g');
      this.legendContainer = this.svg.append('g');

      // Add common definitions.
      const defs = this.svg.append('defs');

      const _appendMarker = (id, color) => {
        defs.append('marker')
          .attr('id', id)
          .attr('viewBox', '0 0 10 10')
          .attr('refX', 22)
          .attr('refY', 4.5)
          .attr('orient', 'auto')
          .attr('markerWidth', 5)
          .attr('markerHeight', 5)
          .append('path')
          .attr('d', 'M 0 0 L 10 5 L 0 10 z')
          .attr('fill', color);
      };

      _appendMarker(`${this.prefixes.arrowHead}-${this.suffix}`, this.colors.link);
      _appendMarker(`${this.prefixes.arrowHeadFocus}-${this.suffix}`, this.colors.linkFocus);

      const _appendIcon = (id, path) => {
        defs.append('path')
          .attr('id', id)
          .attr('d', path)
          .attr('fill', 'white');
      };

      _appendIcon(`${this.prefixes.iconGraph}-${this.suffix}`, this.icons.graph);
      _appendIcon(`${this.prefixes.iconDown}-${this.suffix}`, this.icons.up);
      _appendIcon(`${this.prefixes.iconUp}-${this.suffix}`, this.icons.down);
    },

    createSimulation() {
      const forceManyBody = d3
        .forceManyBody()
        .strength(this.manyBodyStrength);

      const forceLink = d3
        .forceLink()
        .strength(this.linkStrength)
        .id((d) => d.id)
        .distance((d) => {
          const minDistance = 200;

          if (d.source._type === this.types.record) {
            return (d.link_length * 10) + minDistance;
          }

          return minDistance;
        });

      this.simulation = d3
        .forceSimulation()
        .velocityDecay(0.15)
        .force(this.forces.charge, forceManyBody)
        .force(this.forces.link, forceLink)
        .on('tick', () => {
          this.nodesContainer
            .selectAll(`.${this.prefixes.node}-${this.suffix}`)
            .attr('transform', (d) => `translate(${d.x} ${d.y})`);

          this.linksContainer
            .selectAll(`.${this.prefixes.linkLabel}-${this.suffix}`)
            .attr('transform', (d) => this.linkLabelTransformation(d));

          this.linksContainer
            .selectAll(`.${this.prefixes.linkPath}-${this.suffix}`)
            .attr('d', (d) => {
              if (d.source._type === this.types.collection) {
                const line = d3
                  .line()
                  .curve(d3.curveBumpY);

                return line([[d.source.x, d.source.y], [d.target.x, d.target.y - 18]]);
              }

              return this.quadraticBezierCurve(d);
            });
        });
    },

    getCollectionColor(scale, id, darker = false) {
      const color = scale(id);
      return darker ? d3.color(color).darker(0.5) : color;
    },

    getTypeColor(scale, type, darker = false) {
      const color = type === null ? 'grey' : scale(type);
      return darker ? d3.color(color).darker(0.5) : color;
    },

    drawNodes(highlightCollections = false, recordsCallback = null, childrenCallback = null) {
      const collections = this.nodes.filter((d) => d._type === this.types.collection).map((d) => d.id);
      const collectionColors = d3.scaleOrdinal(d3.schemePaired).domain(collections);

      const types = this.nodes.filter((d) => d._type === this.types.record).map((d) => d.type_full);
      const typeColors = d3.scaleOrdinal(d3.schemePaired).domain(types);

      const startNode = this.getStartNode();

      const drag = d3
        .drag()
        .on('start', (e, d) => {
          if (!e.active) {
            this.simulation.alphaTarget(0.5).restart();
          }

          // Save the starting position so we can determine whether the node was moved.
          d.fx = d._fx = d.x;
          d.fy = d._fy = d.y;
        })
        .on('drag', (e, d) => {
          d.fx = e.x;
          d.fy = e.y;

          // When dragging a collection node, we also need to reinitialize the coordinate forces.
          if (d._type === this.types.collection) {
            this.simulation.force(this.forces.x).initialize(this.nodes);
            this.simulation.force(this.forces.y).initialize(this.nodes);
          }
        })
        .on('end', (e, d) => {
          if (!e.active) {
            this.simulation.alphaTarget(0);
          }

          // Only mark the node as moved if it has been moved a certain distance.
          const distance = Math.sqrt(((d.fx - d._fx) ** 2) + ((d.fy - d._fy) ** 2));

          if (distance > 3) {
            d._moved = true;
          }

          if (d._type === this.types.record && (!startNode || d.id !== startNode.id)) {
            d.fx = null;
            d.fy = null;
          }
        });

      const nodesSelection = this.nodesContainer.selectAll(`.${this.prefixes.node}-${this.suffix}`);
      const nodesGroup = nodesSelection
        .data(this.nodes, (d) => d.id)
        .enter()
        .append('g')
        .attr('id', (d) => `${this.prefixes.node}-${d.id}-${this.suffix}`)
        .attr('class', `${this.prefixes.node}-${this.suffix}`)
        .call(drag);

      // Draw the collection nodes.
      const collectionGroup = nodesGroup.filter((d) => d._type === this.types.collection);

      const hoverCollection = (e, d, hover) => {
        const display = hover ? this.displays.inline : this.displays.none;
        const stroke = hover ? this.colors.linkFocus : this.colors.link;

        d3.select(e.currentTarget)
          .select(`.${this.prefixes.controls}-${this.suffix}`)
          .attr('display', display);

        this.linksContainer
          .selectAll(`.${this.prefixes.linkPath}-${this.suffix}`)
          .each((dLink, i, nodes) => {
            if (dLink.source.id === d.id || dLink.target.id === d.id) {
              d3.select(nodes[i]).attr('stroke', stroke);
            }
          });
      };

      collectionGroup
        .on('mouseover', (e, d) => hoverCollection(e, d, true))
        .on('mouseout', (e, d) => hoverCollection(e, d, false))
        .append('polygon')
        .attr('points', '-10,17 -20,0 -10,-17 10,-17 20,0 10,17')
        .attr('fill', (d) => this.getCollectionColor(collectionColors, d.id))
        .attr('stroke', (d) => this.getCollectionColor(collectionColors, d.id, true))
        .attr('stroke-width', (d) => (startNode && d.id === startNode.id ? 5 : 3))
        .attr('cursor', 'pointer');

      // Draw the controls of the collection nodes.
      const controlsGroup = collectionGroup
        .append('g')
        .attr('class', `${this.prefixes.controls}-${this.suffix}`)
        .attr('display', this.displays.none);

      const buttonDisabledOpacity = 0.4;

      const recordsButton = controlsGroup
        .append('g')
        .attr('cursor', 'pointer')
        .on('click', (e, d) => {
          if (recordsCallback !== null) {
            recordsCallback(d);
          }

          const use = d3.select(e.currentTarget).select('use');

          if (use.attr('opacity') === String(buttonDisabledOpacity)) {
            use.attr('opacity', 1);
          } else {
            use.attr('opacity', buttonDisabledOpacity);
          }
        });

      recordsButton
        .append('circle')
        .attr('r', 11)
        .attr('cx', -23)
        .attr('fill', (d) => this.getCollectionColor(collectionColors, d.id, true));

      recordsButton
        .append('use')
        .attr('href', `#${this.prefixes.iconGraph}-${this.suffix}`)
        .attr('transform', 'translate(-30 -6)')
        .filter((d) => d.id === startNode.id)
        .attr('opacity', buttonDisabledOpacity);

      const iconDownHref = `#${this.prefixes.iconDown}-${this.suffix}`;
      const iconDownTranslate = 'translate(16.5 -3)';

      const childrenButton = controlsGroup
        .append('g')
        .attr('cursor', 'pointer')
        .on('click', (e, d) => {
          if (childrenCallback !== null) {
            childrenCallback(d);
          }

          const use = d3.select(e.currentTarget).select('use');

          if (use.attr('href') === iconDownHref) {
            use.attr('href', `#${this.prefixes.iconUp}-${this.suffix}`).attr('transform', 'translate(16.5 -9)');
          } else {
            use.attr('href', iconDownHref).attr('transform', iconDownTranslate);
          }
        });

      childrenButton
        .append('circle')
        .attr('r', 11)
        .attr('cx', 23)
        .attr('fill', (d) => this.getCollectionColor(collectionColors, d.id, true));

      childrenButton
        .append('use')
        .attr('href', iconDownHref)
        .attr('transform', iconDownTranslate);

      // Draw the record nodes.
      const recordGroup = nodesGroup.filter((d) => d._type === this.types.record);

      const hoverRecord = (e, d, hover) => {
        const stroke = hover ? this.colors.linkFocus : this.colors.link;
        const marker = hover ? this.prefixes.arrowHeadFocus : this.prefixes.arrowHead;

        this.linksContainer
          .selectAll(`.${this.prefixes.linkPath}-${this.suffix}`)
          .each((dLink, i, nodes) => {
            if (dLink.source._type === this.types.record && (dLink.source.id === d.id || dLink.target.id === d.id)) {
              d3.select(nodes[i])
                .attr('stroke', stroke)
                .attr('marker-end', `url(#${marker}-${this.suffix})`);
            }
          });
      };

      recordGroup
        .on('mouseover', (e, d) => hoverRecord(e, d, true))
        .on('mouseout', (e, d) => hoverRecord(e, d, false))
        .append('circle')
        .attr('r', 20)
        .attr('cursor', 'pointer')
        .attr('stroke-width', (d) => (startNode && d.id === startNode.id ? 5 : 3))
        .attr('fill', (d) => {
          if (highlightCollections) {
            return 'white';
          }
          return this.getTypeColor(typeColors, d.type_full);
        })
        .attr('stroke', (d) => {
          if (highlightCollections && d.collection) {
            return this.getCollectionColor(collectionColors, d.collection);
          }
          return this.getTypeColor(typeColors, d.type_full, true);
        });

      if (highlightCollections) {
        recordGroup
          .append('circle')
          .attr('r', 15)
          .attr('cursor', 'pointer')
          .attr('fill', (d) => this.getTypeColor(typeColors, d.type_full));
      }

      // Draw the node labels.
      const nodeLabel = nodesGroup
        .append('g')
        .attr('class', `${this.prefixes.nodeLabel}-${this.suffix}`)
        .attr('display', this.labelsHidden ? this.displays.none : this.displays.inline);

      const identifierFontSize = 16;

      nodeLabel
        .append('a')
        .attr('href', (d) => d.url)
        .append('text')
        .text((d) => `@${d.identifier}`)
        .attr('dy', 38)
        .attr('font-family', this.fontFamily)
        .attr('font-size', `${identifierFontSize}px`)
        .attr('font-weight', 'bold')
        .attr('text-anchor', 'middle')
        .on('mouseover', (e) => {
          d3.select(e.target)
            .attr('fill', this.colors.textFocus)
            .attr('font-size', `${identifierFontSize + 2}px`);
        })
        .on('mouseout', (e) => {
          d3.select(e.target)
            .attr('fill', this.colors.text)
            .attr('font-size', `${identifierFontSize}px`);
        })
        .append('title')
        .text((d) => d.identifier_full);

      nodeLabel
        .filter((d) => d.type)
        .append('text')
        .text((d) => d.type)
        .attr('dy', 50)
        .attr('font-family', this.fontFamily)
        .attr('font-size', '12px')
        .attr('text-anchor', 'middle')
        .attr('cursor', 'default')
        .append('title')
        .text((d) => d.type_full);

      // Order collection nodes above record nodes.
      nodesSelection
        .filter((d) => d._type === this.types.collection)
        .raise();
    },

    drawLinks() {
      const hoverLink = (e, d, hover) => {
        const stroke = hover ? this.colors.linkFocus : this.colors.link;
        const marker = hover ? this.prefixes.arrowHeadFocus : this.prefixes.arrowHead;
        const path = d3.select(e.currentTarget).select('path');

        path.attr('stroke', stroke);

        if (d.source._type === this.types.record) {
          path.attr('marker-end', `url(#${marker}-${this.suffix})`);
        }
      };

      const linksSelection = this.linksContainer.selectAll(`.${this.prefixes.link}-${this.suffix}`);
      const linksGroup = linksSelection
        .data(this.links, (d) => d.id)
        .enter()
        .append('g')
        .attr('class', `${this.prefixes.link}-${this.suffix}`)
        .on('mouseover', (e, d) => hoverLink(e, d, true))
        .on('mouseout', (e, d) => hoverLink(e, d, false));

      linksGroup
        .append('path')
        .attr('class', `${this.prefixes.linkPath}-${this.suffix}`)
        .attr('stroke', this.colors.link)
        .attr('stroke-width', 3)
        .attr('fill', 'none')
        .filter((d) => d.source._type === this.types.record)
        .attr('marker-end', `url(#${this.prefixes.arrowHead}-${this.suffix})`);

      const linkNameFontSize = 14;

      linksGroup
        .filter((d) => d.source._type === this.types.record)
        .append('a')
        .attr('href', (d) => d.url)
        .append('text')
        .text((d) => d.name)
        .attr('class', `${this.prefixes.linkLabel}-${this.suffix}`)
        .attr('display', this.labelsHidden ? this.displays.none : this.displays.hidden)
        .attr('font-family', this.fontFamily)
        .attr('font-size', `${linkNameFontSize}px`)
        .attr('text-anchor', 'middle')
        .on('mouseover', (e) => {
          d3.select(e.target)
            .attr('fill', this.colors.textFocus)
            .attr('font-size', `${linkNameFontSize + 2}px`);
        })
        .on('mouseout', (e) => {
          d3.select(e.target)
            .attr('fill', this.colors.text)
            .attr('font-size', `${linkNameFontSize}px`);
        })
        .append('title')
        .text((d) => d.name_full);

      // Order record links above collection links.
      linksSelection
        .filter((d) => d.source._type === this.types.record)
        .raise();
    },

    drawLegend() {
      // For simplicity, we redraw the legend each time.
      this.legendContainer.selectAll('*').remove();

      const typesMap = new Map();

      for (const node of this.nodes) {
        if (node._type === this.types.record) {
          const type = node.type_full;
          const typeMeta = {count: typesMap.has(type) ? typesMap.get(type).count + 1 : 1};

          typesMap.set(type, typeMeta);
        }
      }

      // The order of this array should be consistent, as maps keep their insertion order
      const typesArray = Array.from(typesMap.keys());
      const typeColors = d3.scaleOrdinal(d3.schemePaired).domain(typesArray);

      // This sorts the types while putting null values at the end.
      const sortedTypesArray = [...typesArray].sort((a, b) => (a === null) - (b === null) || Number(a > b) || -(a < b));

      const legendGroup = this.legendContainer
        .selectAll()
        .data(sortedTypesArray)
        .enter()
        .append('g');

      const radius = 9;
      const padding = 8;
      const typeExcludedOpacity = 0.3;

      legendGroup
        .append('circle')
        .attr('r', radius)
        .attr('cx', radius + padding)
        .attr('cy', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .attr('fill', (d) => this.getTypeColor(typeColors, d))
        .attr('stroke', (d) => this.getTypeColor(typeColors, d, true))
        .attr('stroke-width', 2)
        .attr('cursor', 'pointer')
        .on('click', (e, d) => {
          const node = d3.select(e.target);
          const type = d;
          let opacity = 1;

          if (this.excludedTypes.includes(type)) {
            kadi.utils.removeFromArray(this.excludedTypes, type);
          } else {
            this.excludedTypes.push(type);
            opacity = typeExcludedOpacity;
          }

          node.attr('opacity', opacity);
          this.filterNodes();
        })
        .filter((d) => this.excludedTypes.includes(d))
        .attr('opacity', typeExcludedOpacity);

      legendGroup
        .append('text')
        .text((d) => `${d || 'No type'} (${typesMap.get(d).count})`)
        .attr('x', (radius * 3) + padding)
        .attr('y', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .attr('dy', 5)
        .attr('font-family', this.fontFamily)
        .attr('font-size', '15px')
        .attr('font-style', (d) => (d === null ? 'italic' : 'normal'))
        .attr('fill', (d) => this.getTypeColor(typeColors, d, true))
        .attr('cursor', 'default');
    },
  },
};
